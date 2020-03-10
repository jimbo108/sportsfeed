from django.test import TestCase
from .models import TeamMapping, Team, Api
from .enums import ExternalIdentifierType
from .constants import get_fantasy_epl_api_id


class HomeTest(TestCase):

    def test_home_renders_correct_template(self):
        response = self.client.get('/home/')
        self.assertTemplateUsed(response, 'home.html')

    def test_get_team_from_external_id__numeric_id_present__returns_team(self):
        external_identifier = 99999
        team_id = 1

        team = Team(id=team_id, name="test_team")
        api = Api(id=get_fantasy_epl_api_id(), name="test_api")

        numeric_team_mapping = TeamMapping(team=team, api=api,
                                           numeric_external_identifier=external_identifier)
        numeric_team_mapping.save()

        team_found = TeamMapping.get_team_from_external_id(ExternalIdentifierType.NUMERIC,
                                                           external_identifier,
                                                           get_fantasy_epl_api_id())

        self.assertEqual(team_found.id, team_id)

    def test_get_team_from_external_id__numeric_id_not_present__returns_None(self):
        existing_external_identifier = 99999
        team_id = 1
        nonexistant_external_identifier = 88888

        team = Team(id=team_id, name="test_team")
        api = Api(id=get_fantasy_epl_api_id(), name="test_api")

        numeric_team_mapping = TeamMapping(team=team, api=api,
                                           numeric_external_identifier=existing_external_identifier)
        numeric_team_mapping.save()

        team_found = TeamMapping.get_team_from_external_id(ExternalIdentifierType.NUMERIC,
                                                           nonexistant_external_identifier,
                                                           get_fantasy_epl_api_id())

        self.assertIsNone(team_found) 

    def test_get_team_from_external_id__string_id_present__returns_team(self):
        external_identifier = "ASDF"
        team_id = 1

        team = Team(id=team_id, name="test_team")
        api = Api(id=get_fantasy_epl_api_id(), name="test_api")

        numeric_team_mapping = TeamMapping(team=team, api=api,
                                           string_external_identifier=external_identifier)
        numeric_team_mapping.save()

        team_found = TeamMapping.get_team_from_external_id(ExternalIdentifierType.STRING,
                                                           external_identifier,
                                                           get_fantasy_epl_api_id())

        self.assertEqual(team_found.id, team_id)

    def test_get_team_from_external_id__string_id_not_present__returns_None(self):
        existing_external_identifier = "ASDF"
        team_id = 1
        nonexistant_external_identifier = "SDFG"

        team = Team(id=team_id, name="test_team")
        api = Api(id=get_fantasy_epl_api_id(), name="test_api")

        numeric_team_mapping = TeamMapping(team=team, api=api,
                                           string_external_identifier=existing_external_identifier)
        numeric_team_mapping.save()

        team_found = TeamMapping.get_team_from_external_id(ExternalIdentifierType.STRING,
                                                           nonexistant_external_identifier,
                                                           get_fantasy_epl_api_id())

        self.assertIsNone(team_found)
