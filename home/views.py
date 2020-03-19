from datetime import datetime
from hashlib import md5
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from requests import get, Response
from preferences.models import TeamPreference
from .models import Api, RequestAudit, FixtureMapping, ExternalIdentifierType, Fixture, Team, TeamMapping
from . import constants
# Create your views here.

@csrf_exempt
def home(request):
    fixtures = set()
    # Get user
    user = request.user

    # Pull preferences
    team_preferences = TeamPreference.get_user_team_preferences(user)

    # Check last successful request for matches
    api = Api.objects.get(id=constants.FOOTBALL_DATA_DOT_ORG_API_ID)

    if not api.is_in_cooldown():
        request_time = datetime.utcnow()
        response = get(constants.PREMIER_LEAGUE_MATCH_URL)
        handle_match_response(response, request_time)

    # TODO: Handle seasons
    for team in team_preferences:
        fixtures_for_team = Fixture.objects.filter(Q(home_team=team) | Q(away_team=team))
        fixtures = fixtures.union(set(fixtures_for_team))

    # DEBUG:
    for fixture in fixtures:
        print(fixtures.__dict__)

    return render(request, 'home.html')


def audit_matches_request(response: Response, request_time: datetime, hashed_resp: str=None) -> None:
    if response is None or response.status_code is None:
        return

    if response.status_code < 200 or response.status_code > 299:
        request_audit = RequestAudit(api__id=constants.FOOTBALL_DATA_DOT_ORG_API_ID, 
                                    url=constants.PREMIER_LEAGUE_MATCH_URL,
                                    request_type__id=constants.FOOTBALL_DATA_DOT_ORG_GET_MATCHES_REQ_TYPE, 
                                    request_time=request_time, hashed_response=None, response_code=response.status_code,
                                    successful=False)
    else:
        request_audit = RequestAudit(api__id=constants.FOOTBALL_DATA_DOT_ORG_API_ID, 
                                     url=constants.PREMIER_LEAGUE_MATCH_URL,
                                     request_type__id=constants.FOOTBALL_DATA_DOT_ORG_GET_MATCHES_REQ_TYPE, 
                                     request_time=request_time, hashed_response=hashed_resp, 
                                     response_code=response.status_code,
                                     successful=True)
    return


def validate_matches_response(json: dict) -> bool:
    if 'competition' not in json:
        return False
    if 'id' not in json['competition']:
        return False
    if not json['competition']['id'] == constants.FOOTBALL_DATA_DOT_ORG_PREMIER_LEAGUE_COMP_ID:
        return False
    
    if 'matches' not in json:
        return False


def identical_request_found(response_hash: str) -> bool:
    identical_requests = RequestAudit.objects.filter(
                            request_type__id=constants.FOOTBALL_DATA_DOT_ORG_GET_MATCHES_REQ_TYPE,
                            hashed_response=response_hash)
    if len(identical_requests) > 0:
        return True
    else:
        return False


def map_team_to_internal(ext_id: int) -> Team:
    team = TeamMapping.get_model_from_external_id(ExternalIdentifierType.NUMERIC, ext_id)
    return team


def status_is_ongoing(status: str) -> bool:
    if status == "FINISHED":
        return False
    else:
        return True


def create_fixture(match_json: dict, existing_fixture: Fixture=None) -> Fixture:
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

    if any(var is None for var in [status, utc_date, home_team_ext_id, away_team_ext_id, home_score, away_score]):
        return False

    home_team_internal = map_team_to_internal(home_team_ext_id)
    away_team_internal = map_team_to_internal(away_team_ext_id)
    if home_team_internal is None or away_team_internal is None:
        return False

    fixture_dt = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%SZ")
    if fixture_dt is None:
        return False

    is_ongoing = status_is_ongoing(status)     

    if existing_fixture is not None:
        existing_fixture.home_team = home_team_internal
        existing_fixture.away_team = away_team_internal
        existing_fixture.home_score = home_score
        existing_fixture.away_score = away_score
        existing_fixture.kickoff_time_utc = fixture_dt
        existing_fixture.is_ongoing = is_ongoing
    else:
        fixture = Fixture(home_team=home_team_internal, away_team=away_team_internal, home_score=home_score,
                          away_score=away_score, kickoff_time_utc=fixture_dt, is_ongoing=is_ongoing)
        fixture.save()

    return True


def handle_match(match_json: dict) -> bool:
    # TODO: log validation errors
    if 'id' not in match_json:
        return False

    existing_fixture = FixtureMapping.get_model_from_external_id(ExternalIdentifierType.NUMERIC, match_json['id'],
                                                                 constants.FOOTBALL_DATA_DOT_ORG_API_ID)

    if existing_fixture is None or not existing_fixture.is_ongoing:
        return True

    create_fixture(match_json)


def handle_match_response(response: Response, request_time: datetime) -> None:
    if response.status_code is None or response.status_code < 200 or response.status_code > 299:
        audit_matches_request(response, request_time, None)
        return False
    response_md5_hash = md5(str(response.content))
    audit_matches_request(response, request_time, response_md5_hash)

    if identical_request_found(response_md5_hash):
        return True
    
    json = response.json()

    if not validate_matches_response(json):
        return False

    for match in json['matches']:
        handle_match()        