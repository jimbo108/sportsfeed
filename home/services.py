"""Defines classes for external API clients needed by the home module

ApiGetClient is an abstract base class that GET client implementations can inherit from.
    
"""
import hashlib
import abc
from datetime import datetime
from typing import Dict
import requests
from django.db.models import Q
from home import enums, models, constants
try:
    from sportsfeed.local_settings import FOOTBALL_DATA_DOT_ORG_API_KEY
except ImportError as error:
    # No local_settings, can't access external API
    raise error


class UrlGenerationError(Exception):
    """Error class to be raised when a URL can't be generated from models.RequestType.base_url and arguments."""

class ApiGetClient(abc.ABC): # pylint: disable=too-few-public-methods
    """Base class for HTTP GET clients

    Attributes:
        request_type::RequestType
            The models.RequestType associated with this GET client
        url::str
            The to send the request to
        response::requests.Response
            The response object for the HTTP response
        hashed_response::str
            A str representation of a hash of the response
        request_time::datetime
            The time that approximates when the request was sent

    """
    def __init__(self, request_type: models.RequestType, url: str = None):
        """Inits ApiGetClient with request_type and an optional url"""
        self.request_type = request_type
        self.url = url
        self.response = None
        self.hashed_response = None
        self.request_time = None

    def request(self) -> bool:
        """Sends a GET request to url and processes the response

        Sends a GET request to url, inserting headers via the _get_headers hook, and generating the url from
        the RequestType.base_url and args, or optionally an explicitly passed in URL on instantiation.  The response
        is then hashed, validated, processed and audited.  Automatically detects identical requests via hash and does
        not reprocess.

        The result of the method running will be:
            (1) A RequestAudit being created and marked as successful or unsuccessful
            (2) Whatever is saved as a result of a child classe's overridden _validate method

        Returns:
            True if successful, otherwise False

        Raises:
            MultipleObjectsReturned: Multiple Django models returned by an ...objects.get call to the DB
            UrlGenerationError: The URL could not be generated from the RequestType.base_url and args
        """
        if self.request_type.api.is_in_cooldown():
            return True
        self.request_time = datetime.utcnow()
        headers = self._get_headers()
        if self.url is None:
            url = self.request_type.get_url(str(constants.FDDO_PREMIER_LEAGUE_ID))
            if url in("", None):
                # TODO: Logging
                print("Failed to generate URL")
                raise UrlGenerationError()
            self.url = url
        self.response = requests.get(url, headers=headers)
        if self.response is None:
            return False
        return self._handle_response()

    def _handle_response(self) -> bool:
        """Wrapper for handle response content that handles identical requests and auditing

        Returns:
            True if successful, False otherwise
        """
        if not self.response.ok or len(self.response.content) == 0:
            return False
        self.hashed_response = hashlib.md5(str(self.response.content).encode('utf-8')).hexdigest()
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
        """Determines if another RequestAudit of the RequestType self.request_type with the same hash as this
        exists.

        Returns:
            True if an identical request is found, False otherwise.
        """
        identical_requests = models.RequestAudit.objects.filter(Q(request_type_id=self.request_type.id),
                                                                Q(hashed_response=self.hashed_response),
                                                                ~Q(id=request_audit_id),
                                                                Q(successful=True))
        return len(identical_requests) > 0

    def _audit_request(self) -> int:
        """Creates a RequestAudit and returns the ID"""
        if self.response is None or self.response.status_code is None:
            return None

        request_audit = None

        # only setting 'successful' to False for now, until we're finished processing fixtures
        request_audit = models.RequestAudit(api_id=self.request_type.api.id,
                                            url=self.url,
                                            request_type_id=self.request_type.id,
                                            request_time=self.request_time, hashed_response=self.hashed_response,
                                            response_code=self.response.status_code,
                                            successful=False)

        request_audit.save()
        return request_audit.id

    @staticmethod
    def _set_req_audit_successful(request_audit_id: int) -> None:
        """Sets a RequestAudit as successful

        Args:
            request_audit_id::int
                The primary key of a RequestAudit object
        """
        request_audit = None
        try:
            request_audit = models.RequestAudit.objects.get(id=request_audit_id)
        except models.RequestAudit.DoesNotExist:
            # More logging here
            pass
        except models.RequestAudit.MultipleObjectsReturned as error: # pylint: disable=no-member
            raise error

        if request_audit is not None:
            request_audit.successful = True
            request_audit.save()

    @abc.abstractmethod
    def _handle_response_content(self, response_content: Dict) -> bool:
        """Method to be implemented by subclasses to save response_content to the database, and/or have some
        side effect.

        Args:
            response_content::Dict
                A dictionary containing the content of the response to the GET request.

        Returns:
            True if successful, False otherwise.
        """

    @abc.abstractmethod
    def _get_headers(self, **kwargs: Dict) -> Dict:
        """Method to be implemented by subclasses to get headers to populate the request.

        Args:
            **kwargs::Dict
                Key-word arguments dictionary to maintain flexible for the implementing class

        Returns:
            A dictionary of the following format:
                {
                    "header_key_one": header_val_one,
                    "header_key_two": header_val_two,
                    ...
                }
            that will populate the headers in the GET request
        """

    @abc.abstractmethod
    def _validate(self, json: Dict) -> bool:
        """Method to be implemented by subclasses to get headers to populate the request.

        This method should be used for some basic response checks.  More granular validation can occur
        in _handle_response_content if necessary.

        Args:
            json::Dict
                A dictionary containing the full response

        Returns:
            True if successful, False otherwise.
        """


class FDDOApiClient(ApiGetClient): # pylint: disable=too-few-public-methods
    """HTTP GET client inheriting from / implementing ApiGetClient.

    This class implements ApiGetClient, specifically _handle_response_content and _validate.
    It gets the RequestType from the database and passes it into ApiGetClient's __init__.

    Attributes:
        (class) request_type::RequestType
            The RequestType for FootballData.org GET client.
    """
    request_type = None
    try:
        request_type = models.RequestType.objects.get(id=constants.FOOTBALL_DATA_DOT_ORG_GET_MATCHES_REQ_TYPE)
    except models.RequestType.DoesNotExist as error:
        # TODO: logging
        raise error


    def __init__(self):
        """Initialize the FDDOApi"""
        super().__init__(FDDOApiClient.request_type)

    def _handle_response_content(self, response_content: Dict) -> bool:
        success = True

        for match in response_content['matches']:
            success = success and self._handle_match(match)

        return success

    def _handle_match(self, match_json: Dict) -> bool:
        """Check for an existing Fixture and then create it

        Args:
            match_json::Dict
                A dictionary containing the response for a single match

        Returns:
            True on success, otherwise False
        """
        # TODO: log validation errors
        if 'id' not in match_json:
            return False

        existing_fixture = models.FixtureMapping.get_model_from_external_id(
            models.ExternalIdentifierType.NUMERIC,
            match_json['id'],
            self.request_type.api.id
        )

        if existing_fixture is not None and not self._fixture_status_is_final(existing_fixture.status_id):
            return True
        return self._create_fixture(match_json, existing_fixture)

    @staticmethod
    def _fixture_status_is_final(status_id: int) -> bool:
        """Determines if the fixture is final (meaning it should no longer change)

        Args:
            status_id::int
                The fixture status ID from the FDDO response

        Returns:
            True if the ID represents a final status, otherwise False
        """
        return status_id in (enums.FixtureStatusIds.FINISHED,
                             enums.FixtureStatusIds.AWARDED,
                             enums.FixtureStatusIds.CANCELED)

    def _create_fixture(self, match_json: dict, existing_fixture: models.Fixture = None) -> models.Fixture: # pylint: disable=too-many-branches
        """Creates a Fixture from the response

        Args:
            match_json::dict
                The JSON representing a single match.
            existing_fixture::models.Fixture
                If a Fixture row already exists for the fixture being processed, a reference to that object.

        Returns:
            A Fixture object referencing the modified or created Fixture.
        """

        status = None
        utc_date = None
        home_team_ext_id = None
        away_team_ext_id = None
        home_score = None
        away_score = None

        status = match_json.get('status')
        utc_date = match_json.get('utcDate')

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

        home_team_internal = models.TeamMapping.get_model_from_external_id(
            models.ExternalIdentifierType.NUMERIC, home_team_ext_id,
            self.request_type.api.id
        )

        away_team_internal = models.TeamMapping.get_model_from_external_id(
            models.ExternalIdentifierType.NUMERIC, away_team_ext_id,
            self.request_type.api.id
        )

        if home_team_internal is None or away_team_internal is None:
            return False

        fixture_dt = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%SZ")
        if fixture_dt is None:
            return False

        internal_status = self._get_status(status)
        if internal_status is None:
            return False

        if existing_fixture is not None:
            existing_fixture.home_team = home_team_internal
            existing_fixture.away_team = away_team_internal
            existing_fixture.home_score = home_score
            existing_fixture.away_score = away_score
            existing_fixture.kickoff_time_utc = fixture_dt
            existing_fixture.status = internal_status
            existing_fixture.save()
        else:
            fixture = models.Fixture(
                home_team=home_team_internal,
                away_team=away_team_internal,
                home_score=home_score,
                away_score=away_score,
                kickoff_time_utc=fixture_dt,
                status=internal_status
            )
            fixture.save()
            fixture_mapping = models.FixtureMapping(
                value_id=fixture.id,
                api_id=self.request_type.api.id,
                numeric_external_identifier=match_json['id']
            )
            fixture_mapping.save()
        return True

    def _get_status(self, status: str) -> models.FixtureStatus:
        """Get a FixtureStatus model from the status

        Args:
            status::str
                The status code as a string.

        Returns:
            An existing FixtureStatus model that is mapped to by the status
        """
        fixture_status = models.FixtureStatusMapping.get_model_from_external_id(
            models.ExternalIdentifierType.STRING,
            status,
            self.request_type.api.id
        )
        return fixture_status

    @staticmethod
    def _status_is_ongoing(status: str) -> bool:
        """Implementation of _status_is_ongoing, overrides ApiGetClient._status_is_ongoing abstract method."""
        return not status == "FINISHED"

    def _get_headers(self, **kwargs: Dict) -> Dict:
        """Implementation of _get_headers, overrides ApiGetClient._get_headers abstract method."""
        return {'X-Auth-Token': FOOTBALL_DATA_DOT_ORG_API_KEY}

    def _validate(self, json: dict) -> bool:
        """Implementation of _validate, overrides ApiGetClient._validate abstract method."""
        if 'competition' not in json:
            return False
        if 'id' not in json['competition']:
            return False
        if not json['competition']['id'] == constants.FDDO_PREMIER_LEAGUE_ID:
            return False

        if 'matches' not in json:
            return False

        return True
