from hashlib import md5
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict
from requests import get, Response
from django.db.models import Q
from .enums import FixtureStatusIds
from .models import (
    RequestType, RequestAudit, FixtureMapping,
    ExternalIdentifierType, Fixture, TeamMapping, 
    FixtureStatus,FixtureStatusMapping
                    )
from .constants import FDDO_PREMIER_LEAGUE_ID, FOOTBALL_DATA_DOT_ORG_GET_MATCHES_REQ_TYPE
try:
    from sportsfeed.local_settings import FOOTBALL_DATA_DOT_ORG_API_KEY
except ImportError as e:
    # No local_settings, can't access external API
    raise e


class UrlGenerationError(Exception):
    pass


class ApiGetClient(ABC):

    def __init__(self, request_type: RequestType, url: str = None):
        self.request_type = request_type
        self.url = url
        self.response = None
        self.hashed_response = None
        self.request_time = None

    def request(self) -> bool:
        if self.request_type.api.is_in_cooldown():
            return True
        self.request_time = datetime.utcnow()
        headers = self._get_headers()
        if self.url is None:
            url = self.request_type.get_url(str(FDDO_PREMIER_LEAGUE_ID))
            if url in("", None):
                # TODO: Logging
                print("Failed to generate URL")
                raise UrlGenerationError()
            else:
                self.url = url
        self.response = get(url, headers=headers)
        if self.response is None:
            return False
        return self._handle_response()

    def _handle_response(self) -> bool:
        if not self.response.ok or len(self.response.content) == 0:
            return False
        self.hashed_response = md5(str(self.response.content).encode('utf-8')).hexdigest()
        request_audit_id = self._audit_request()

        if self._identical_request_found(request_audit_id):
            return True

        json = self.response.json()

        if not self._validate(json):
            return False

        if not self._handle_response_content(json):
            return False

        self._set_req_audit_successful(request_audit_id)
        return True

    def _identical_request_found(self, request_audit_id: int) -> bool:
        identical_requests = RequestAudit.objects.filter(Q(request_type_id=self.request_type.id),
                                                         Q(hashed_response=self.hashed_response),
                                                         ~Q(id=request_audit_id),
                                                         Q(successful=True))
        if len(identical_requests) > 0:
            return True
        else:
            return False

    def _audit_request(self) -> None:
        if self.response is None or self.response.status_code is None:
            return

        request_audit = None

        # only setting 'successful' to False for now, until we're finished processing fixtures
        request_audit = RequestAudit(api_id=self.request_type.api.id,
                                     url=self.url,
                                     request_type_id=self.request_type.id,
                                     request_time=self.request_time, hashed_response=self.hashed_response,
                                     response_code=self.response.status_code,
                                     successful=False)

        request_audit.save()
        return request_audit.id

    def _set_req_audit_successful(self, request_audit_id: int) -> None:
        request_audit = None
        try:
            request_audit = RequestAudit.objects.get(id=request_audit_id)
        except RequestAudit.DoesNotExist:
            # More logging here
            pass
        except RequestAudit.MultipleObjectsReturned as e:
            raise e

        if request_audit is not None:
            request_audit.successful = True
            request_audit.save()

    @abstractmethod
    def _handle_response_content(self, response_content: Dict) -> bool:
        pass

    @abstractmethod
    def _get_headers(self, **kwargs: Dict) -> Dict:
        pass

    @abstractmethod
    def _validate(self, json: Dict) -> bool:
        pass


class FDDOApiClient(ApiGetClient):

    def __init__(self):
        request_type = None
        try:
            request_type = RequestType.objects.get(id=FOOTBALL_DATA_DOT_ORG_GET_MATCHES_REQ_TYPE)
        except RequestType.DoesNotExist as e:
            # TODO: logging
            raise e

        super().__init__(request_type)

    def _handle_response_content(self, response_content: Dict) -> bool:
        success = True

        for match in response_content['matches']:
            success = success and self._handle_match(match)

        return success

    def _handle_match(self, match_json: Dict) -> bool:
        # TODO: log validation errors
        if 'id' not in match_json:
            return False

        existing_fixture = FixtureMapping.get_model_from_external_id(ExternalIdentifierType.NUMERIC, match_json['id'],
                                                                     self.request_type.api.id)

        if existing_fixture is not None and not self._fixture_status_is_final(existing_fixture.status_id):
            return True
        return self._create_fixture(match_json, existing_fixture)

    def _fixture_status_is_final(self, status_id: int) -> bool:
        if status_id in (FixtureStatusIds.FINISHED, FixtureStatusIds.AWARDED,
                         FixtureStatusIds.CANCELED):
            return True
        else:
            return False

    def _create_fixture(self, match_json: dict, existing_fixture: Fixture = None) -> Fixture:
        status = None
        utc_date = None
        home_team_ext_id = None
        away_team_ext_id = None
        home_score = None
        away_score = None

        if 'status' in match_json:
            status = match_json['status']
        if 'utcDate' in match_json:
            utc_date = match_json['utcDate']
        if 'homeTeam' in match_json:
            if 'id' in match_json['homeTeam']:
                home_team_ext_id = match_json['homeTeam']['id']
        if 'awayTeam' in match_json:
            if 'id' in match_json['homeTeam']:
                away_team_ext_id = match_json['awayTeam']['id']
        if 'score' in match_json:
            if 'fullTime' in match_json['score']:
                if 'homeTeam' in match_json['score']['fullTime']:
                    home_score = match_json['score']['fullTime']['homeTeam']
                if 'awayTeam' in match_json['score']['fullTime']:
                    away_score = match_json['score']['fullTime']['awayTeam']
        
        if any(var is None for var in [status, utc_date, home_team_ext_id,
                                       away_team_ext_id]):
            return False

        home_team_internal = TeamMapping.get_model_from_external_id(ExternalIdentifierType.NUMERIC, home_team_ext_id,
                                                                    self.request_type.api.id)
        away_team_internal = TeamMapping.get_model_from_external_id(ExternalIdentifierType.NUMERIC, away_team_ext_id,
                                                                    self.request_type.api.id) 
        if home_team_internal is None or away_team_internal is None:
            breakpoint()
            return False

        fixture_dt = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%SZ")
        if fixture_dt is None:
            breakpoint()
            return False
       
        internal_status = self._get_status(status)
        if internal_status is None:
            breakpoint()
            return False 

        if existing_fixture is not None:
            existing_fixture.home_team = home_team_internal
            existing_fixture.away_team = away_team_internal
            existing_fixture.home_score = home_score
            existing_fixture.away_score = away_score
            existing_fixture.kickoff_time_utc = fixture_dt
            existing_fixture.is_ongoing = is_ongoing
            existing_fixture.save()
        else:
            fixture = Fixture(home_team=home_team_internal, away_team=away_team_internal, home_score=home_score,
                              away_score=away_score,
                              kickoff_time_utc=fixture_dt,
                              status=internal_status)
            fixture.save()
            fixture_mapping = FixtureMapping(value_id=fixture.id,
                                             api_id=self.request_type.api.id,
                                             numeric_external_identifier=match_json['id'])
            fixture_mapping.save()
        return True

    def _get_status(self, status: str) -> FixtureStatus:
        fixture_status = FixtureStatusMapping.get_model_from_external_id(ExternalIdentifierType.STRING,
                                                                         status,
                                                                         self.request_type.api.id)
        return fixture_status

    def _status_is_ongoing(self, status: str) -> bool:
        return not (status == "FINISHED")

    def _get_headers(self, **kwargs: Dict) -> Dict:
        return {'X-Auth-Token': FOOTBALL_DATA_DOT_ORG_API_KEY}

    def _validate(self, json: dict) -> bool:
        if 'competition' not in json:
            return False
        if 'id' not in json['competition']:
            return False
        if not json['competition']['id'] == FDDO_PREMIER_LEAGUE_ID:
            return False
    
        if 'matches' not in json:
            return False
    
        return True

