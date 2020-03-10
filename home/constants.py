FOOTBALL_DATA_DOT_ORG_API_ID_KEY = "football-data.org"
FANTASY_EPL_API_ID_KEY = "fantasy_epl"

api_identifiers_dict = {
    FOOTBALL_DATA_DOT_ORG_API_ID_KEY: 0,
    FANTASY_EPL_API_ID_KEY: 1,
}


def get_football_data_dot_org_api_id():
    return api_identifiers_dict[FOOTBALL_DATA_DOT_ORG_API_ID_KEY]


def get_fantasy_epl_api_id():
    return api_identifiers_dict[FANTASY_EPL_API_ID_KEY]
