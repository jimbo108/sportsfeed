"""

"""

from datetime import datetime
import json
from unittest.mock import patch
from django.test import TestCase
from .models import (
                    TeamMapping, Team, Api, RequestType, RequestLimitType,
                    RequestAudit, Fixture, FixtureMapping
                    )
from .enums import ExternalIdentifierType
#from .constants import get_fantasy_epl_api_id
from .services import FDDOApiClient, UrlGenerationError


class HomeTest(TestCase):

    def test_home_renders_correct_template(self):
        response = self.client.get('/home/')
        self.assertTemplateUsed(response, 'home.html')

    #def test_get_team_from_external_id__numeric_id_present__returns_team(self):
    #    external_identifier = 99999
    #    team_id = 1

    #    team = Team(id=team_id, name="test_team")
    #    api = Api(id=get_fantasy_epl_api_id(), name="test_api")

    #    numeric_team_mapping = TeamMapping(team=team, api=api,
    #                                       numeric_external_identifier=external_identifier)
    #    numeric_team_mapping.save()

    #    team_found = TeamMapping.get_team_from_external_id(ExternalIdentifierType.NUMERIC,
    #                                                       external_identifier,
    #                                                       get_fantasy_epl_api_id())

    #    self.assertEqual(team_found.id, team_id)

    #def test_get_team_from_external_id__numeric_id_not_present__returns_None(self):
    #    existing_external_identifier = 99999
    #    team_id = 1
    #    nonexistant_external_identifier = 88888

    #    team = Team(id=team_id, name="test_team")
    #    api = Api(id=get_fantasy_epl_api_id(), name="test_api")

    #    numeric_team_mapping = TeamMapping(team=team, api=api,
    #                                       numeric_external_identifier=existing_external_identifier)
    #    numeric_team_mapping.save()

    #    team_found = TeamMapping.get_team_from_external_id(ExternalIdentifierType.NUMERIC,
    #                                                       nonexistant_external_identifier,
    #                                                       get_fantasy_epl_api_id())

    #    self.assertIsNone(team_found) 

    #def test_get_team_from_external_id__string_id_present__returns_team(self):
    #    external_identifier = "ASDF"
    #    team_id = 1

    #    team = Team(id=team_id, name="test_team")
    #    api = Api(id=get_fantasy_epl_api_id(), name="test_api")

    #    numeric_team_mapping = TeamMapping(team=team, api=api,
    #                                       string_external_identifier=external_identifier)
    #    numeric_team_mapping.save()

    #    team_found = TeamMapping.get_team_from_external_id(ExternalIdentifierType.STRING,
    #                                                       external_identifier,
    #                                                       get_fantasy_epl_api_id())

    #    self.assertEqual(team_found.id, team_id)

    #def test_get_team_from_external_id__string_id_not_present__returns_None(self):
    #    existing_external_identifier = "ASDF"
    #    team_id = 1
    #    nonexistant_external_identifier = "SDFG"

    #    team = Team(id=team_id, name="test_team")
    #    api = Api(id=get_fantasy_epl_api_id(), name="test_api")

    #    numeric_team_mapping = TeamMapping(team=team, api=api,
    #                                       string_external_identifier=existing_external_identifier)
    #    numeric_team_mapping.save()

    #    team_found = TeamMapping.get_team_from_external_id(ExternalIdentifierType.STRING,
    #                                                       nonexistant_external_identifier,
    #                                                       get_fantasy_epl_api_id())

    #    self.assertIsNone(team_found)


class ApiClientTest(TestCase):

    @patch('home.services.RequestType.objects')
    @patch('home.models.RequestType', autospec=True)
    @patch('home.models.Api', autospec=True)
    def test_request__api_in_cooldown__returns_true(self, api_mock, req_type_mock, req_type_objects_mock):
        self.set_up_mocked_models(api_mock, req_type_mock, req_type_objects_mock, True)
        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertTrue(ret_val)

    @patch('home.services.RequestType.objects')
    @patch('home.models.RequestType', autospec=True)
    @patch('home.models.Api', autospec=True)
    def test_request__url_generation_failed__raises_error(self, api_mock, req_type_mock, req_type_objects_mock):
        self.set_up_mocked_models(api_mock, req_type_mock, req_type_objects_mock, False, None)
        api_client = FDDOApiClient()
        self.assertRaises(UrlGenerationError, api_client.request)

    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    @patch('home.models.RequestType', autospec=True)
    @patch('home.models.Api', autospec=True)
    def test_request__request_none__returns_false(self, api_mock, req_type_mock, req_type_objects_mock, get_mock):
        self.set_up_mocked_models(api_mock, req_type_mock, req_type_objects_mock)
        get_mock.return_value = None
        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)

    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    @patch('home.models.RequestType', autospec=True)
    @patch('home.models.Api', autospec=True)
    def test_request__request_not_ok__returns_false(self, api_mock, req_type_mock, req_type_objects_mock, get_mock):
        self.set_up_mocked_models(api_mock, req_type_mock, req_type_objects_mock)
        get_mock.return_value.ok = False
        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)

    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    @patch('home.models.RequestType', autospec=True)
    @patch('home.models.Api', autospec=True)
    def test_request__request_returns_blank__returns_false(self, api_mock, req_type_mock, req_type_objects_mock, get_mock):
        self.set_up_mocked_models(api_mock, req_type_mock, req_type_objects_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.content = ''
        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)

    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__request_valid_unsuccessful__returns_false_and_unsuccessful_request_audit(self, req_type_objects_mock, get_mock, is_in_cooldown_mock, get_url_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.content = 'Not blank'
        get_mock.return_value.status_code = 200
        req_audit_result = None
        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)
        try:
            req_audit_result = RequestAudit.objects.get(url=api_client.url)
        except RequestAudit.DoesNotExist:
            self.fail()

        self.assertEqual(req_audit_result.api.id, self.api.id)
        self.assertEqual(req_audit_result.url, api_client.url)
        self.assertEqual(req_audit_result.request_type.id, self.request_type.id)
        self.assertEqual(req_audit_result.request_time.replace(tzinfo=None), api_client.request_time)
        self.assertEqual(req_audit_result.hashed_response, api_client.hashed_response)
        self.assertEqual(req_audit_result.response_code, api_client.response.status_code)
        self.assertFalse(req_audit_result.successful)

    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__no_competition_key__returns_false(self, req_type_objects_mock, get_mock, is_in_cooldown_mock, get_url_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.content = 'Not blank'
        get_mock.return_value.status_code = 200
        
        json = self.get_json_dict()
        del json['competition']

        get_mock.return_value.json.return_value = json

        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)

    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__no_competition_id_key__returns_false(self, req_type_objects_mock, get_mock, is_in_cooldown_mock, get_url_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.content = 'Not blank'
        get_mock.return_value.status_code = 200

        json = self.get_json_dict()
        del json['competition']['id']

        get_mock.return_value.json.return_value = json

        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)

    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__incorrect_competition_id_key__returns_false(self, req_type_objects_mock, get_mock, is_in_cooldown_mock, get_url_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.content = 'Not blank'
        get_mock.return_value.status_code = 200

        json = self.get_json_dict()
        json['competition']['id'] = 22

        get_mock.return_value.json.return_value = json

        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)

    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__no_matches_key__returns_false(self, req_type_objects_mock, get_mock, is_in_cooldown_mock, get_url_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.content = 'Not blank'
        get_mock.return_value.status_code = 200

        json = self.get_json_dict()
        del json['matches']

        get_mock.return_value.json.return_value = json

        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)

    # Test no 'id' in match_json
    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__no_matches_id_key__returns_false(self, req_type_objects_mock, get_mock, is_in_cooldown_mock, get_url_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.content = 'Not blank'
        get_mock.return_value.status_code = 200

        json = self.get_json_dict()
        del json['matches'][1]
        get_mock.return_value.json.return_value = json

        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertFalse(ret_val)

    # Test existing fixture completed
    @patch('home.services.FDDOApiClient._create_fixture')
    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__existing_fixture_completed__returns_true_and_no_new_fixture(self, req_type_objects_mock, get_mock, is_in_cooldown_mock, get_url_mock, create_fixture_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.status_code = 200
        get_mock.return_value.content = self.get_json_string()

        json = self.get_json_dict()

        del json['matches'][1]
        self.create_teams()
        self.create_existing_fixture(json['matches'][0]['id'])

        get_mock.return_value.json.return_value = json

        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertTrue(ret_val)
        self.assertLess(Fixture.objects.count(), 2)
        create_fixture_mock.assert_not_called()

    # Test existing fixutre not completed
    @patch('home.models.TeamMapping.get_model_from_external_id')
    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__existing_fixture_not_completed__returns_true_and_updates(self, req_type_objects_mock, get_mock,
                                                                               is_in_cooldown_mock, get_url_mock,
                                                                               get_model_from_external_id_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.status_code = 200
        get_mock.return_value.content = self.get_json_string()
        json = self.get_json_dict()

        del json['matches'][1]
        self.create_teams()
        self.create_existing_fixture(json['matches'][0]['id'], True)
        get_model_from_external_id_mock.side_effect = [self.home_team, self.away_team]

        get_mock.return_value.json.return_value = json

        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertTrue(ret_val)
        self.assertLess(Fixture.objects.count(), 2)

        result_fixture = Fixture.objects.all()[0]
        self.assertEqual(result_fixture.home_score, 4)
        self.assertEqual(result_fixture.away_score, 1)

        expected_dt = datetime.strptime(json['matches'][0]['utcDate'], "%Y-%m-%dT%H:%M:%SZ")

        self.assertEqual(result_fixture.kickoff_time_utc.replace(tzinfo=None), expected_dt)
        self.assertFalse(result_fixture.is_ongoing)

    # Test no existing fixture (and full fixture data)
    @patch('home.models.TeamMapping.get_model_from_external_id')
    @patch('home.models.RequestType.get_url')
    @patch('home.models.Api.is_in_cooldown')
    @patch('home.services.get')
    @patch('home.services.RequestType.objects')
    def test_request__no_existing_fixture__returns_true_and_creates(self, req_type_objects_mock, get_mock,
                                                                    is_in_cooldown_mock, get_url_mock,
                                                                    get_model_from_external_id_mock):
        self.set_up_real_models(req_type_objects_mock, is_in_cooldown_mock, get_url_mock)
        get_mock.return_value.ok = True
        get_mock.return_value.status_code = 200
        get_mock.return_value.content = self.get_json_string()
        json = self.get_json_dict()

        del json['matches'][1]
        self.create_teams()
        get_model_from_external_id_mock.side_effect = [self.home_team, self.away_team]

        get_mock.return_value.json.return_value = json

        api_client = FDDOApiClient()
        ret_val = api_client.request()
        self.assertTrue(ret_val)
        self.assertLess(Fixture.objects.count(), 2)

        result_fixture = Fixture.objects.all()[0]
        self.assertEqual(result_fixture.home_score, 4)
        self.assertEqual(result_fixture.away_score, 1)

        expected_dt = datetime.strptime(json['matches'][0]['utcDate'], "%Y-%m-%dT%H:%M:%SZ")

        self.assertEqual(result_fixture.kickoff_time_utc.replace(tzinfo=None), expected_dt)
        self.assertFalse(result_fixture.is_ongoing)

    @classmethod
    def create_teams(cls):
        cls.home_team = Team(name='test_home', is_active=True)
        cls.home_team.save()
        cls.away_team = Team(name='test_away', is_active=True)
        cls.away_team.save()

    @classmethod
    def create_existing_fixture(cls, id, is_ongoing=False):
        fixture = Fixture(home_team=cls.home_team, away_team=cls.away_team, home_score=1, away_score=2,
                          kickoff_time_utc=datetime.utcnow(), is_ongoing=is_ongoing)
        fixture.save()

        FixtureMapping(value_id=fixture.id, api_id=cls.api.id,
                       numeric_external_identifier=id).save()

    @classmethod
    def set_up_real_models(cls, req_type_objects_mock, is_in_cooldown_mock, get_url_mock):
        cls.req_limit_type = RequestLimitType(description='staggered')
        cls.req_limit_type.save()
        cls.api = Api(name='test_api', request_limit_type=cls.req_limit_type, request_interval_ms=10000)
        cls.api.save()
        cls.request_type = RequestType(api=cls.api, base_url='testurl.com', description='test_req_type',
                                       current_version_iter=0)
        cls.request_type.save()
        req_type_objects_mock.get.return_value = cls.request_type
        is_in_cooldown_mock.return_value = False
        get_url_mock.return_value = cls.request_type.base_url

    @classmethod
    def set_up_mocked_models(cls, api_mock, req_type_mock, req_type_objects_mock, cooldown=False, url='testurl.com'):
        api_mock.return_value.is_in_cooldown.return_value = cooldown
        req_type_mock.return_value.api = api_mock.return_value
        req_type_objects_mock.get.return_value = req_type_mock.return_value
        req_type_mock.return_value.get_url.return_value = url

    @classmethod
    def get_json_dict(cls):
        return json.loads(cls.get_json_string())
    
    @classmethod
    def get_json_string(cls):
        return """
{
    "count": 380,
    "filters": {},
    "competition": {
        "id": 2021,
        "area": {
            "id": 2072,
            "name": "England"
        },
        "name": "Premier League",
        "code": "PL",
        "plan": "TIER_ONE",
        "lastUpdated": "2020-03-15T00:00:51Z"
    },
    "matches": [
        {
            "id": 264341,
            "season": {
                "id": 468,
                "startDate": "2019-08-09",
                "endDate": "2020-05-17",
                "currentMatchday": 30
            },
            "utcDate": "2019-08-09T19:00:00Z",
            "status": "FINISHED",
            "matchday": 1,
            "stage": "REGULAR_SEASON",
            "group": "Regular Season",
            "lastUpdated": "2019-09-26T15:34:45Z",
            "odds": {
                "msg": "Activate Odds-Package in User-Panel to retrieve odds."
            },
            "score": {
                "winner": "HOME_TEAM",
                "duration": "REGULAR",
                "fullTime": {
                    "homeTeam": 4,
                    "awayTeam": 1
                },
                "halfTime": {
                    "homeTeam": 4,
                    "awayTeam": 0
                },
                "extraTime": {
                    "homeTeam": null,
                    "awayTeam": null
                },
                "penalties": {
                    "homeTeam": null,
                    "awayTeam": null
                }
            },
            "homeTeam": {
                "id": 64,
                "name": "Liverpool FC"
            },
            "awayTeam": {
                "id": 68,
                "name": "Norwich City FC"
            },
            "referees": [
                {
                    "id": 11605,
                    "name": "Michael Oliver",
                    "nationality": null
                },
                {
                    "id": 11564,
                    "name": "Stuart Burt",
                    "nationality": null
                },
                {
                    "id": 11488,
                    "name": "Simon Bennett",
                    "nationality": null
                },
                {
                    "id": 11503,
                    "name": "Graham Scott",
                    "nationality": null
                },
                {
                    "id": 11610,
                    "name": "Andre Marriner",
                    "nationality": null
                }
            ]
        },
        {
            "id": 264342,
            "season": {
                "id": 468,
                "startDate": "2019-08-09",
                "endDate": "2020-05-17",
                "currentMatchday": 30
            },
            "utcDate": "2019-08-10T11:30:00Z",
            "status": "FINISHED",
            "matchday": 1,
            "stage": "REGULAR_SEASON",
            "group": "Regular Season",
            "lastUpdated": "2019-09-26T15:34:45Z",
            "odds": {
                "msg": "Activate Odds-Package in User-Panel to retrieve odds."
            },
            "score": {
                "winner": "AWAY_TEAM",
                "duration": "REGULAR",
                "fullTime": {
                    "homeTeam": 0,
                    "awayTeam": 5
                },
                "halfTime": {
                    "homeTeam": 0,
                    "awayTeam": 1
                },
                "extraTime": {
                    "homeTeam": null,
                    "awayTeam": null
                },
                "penalties": {
                    "homeTeam": null,
                    "awayTeam": null
                }
            },
            "homeTeam": {
                "id": 563,
                "name": "West Ham United FC"
            },
            "awayTeam": {
                "id": 65,
                "name": "Manchester City FC"
            },
            "referees": [
                {
                    "id": 11575,
                    "name": "Mike Dean",
                    "nationality": null
                },
                {
                    "id": 11576,
                    "name": "Darren Cann",
                    "nationality": null
                },
                {
                    "id": 11431,
                    "name": "Daniel Robathan",
                    "nationality": null
                },
                {
                    "id": 9382,
                    "name": "Gavin Ward",
                    "nationality": null
                },
                {
                    "id": 11556,
                    "name": "David Coote",
                    "nationality": null
                }
                ]
            }
    ]
}
"""
