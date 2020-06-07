import re
from datetime import datetime, timedelta
from django.db import models
from django.db.models import Max, Count
from .enums import ExternalIdentifierType
from typing import Union
from . import constants


class Team(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_active_teams(cls):
        return Team.objects.filter(is_active=True)


class RequestLimitType(models.Model):
    description = models.CharField(max_length=200)


class Api(models.Model):
    name = models.CharField(max_length=100)
    request_limit_type = models.ForeignKey(to=RequestLimitType, on_delete=models.SET_NULL, null=True)
    requests_per_minute = models.IntegerField(null=True)
    request_interval_ms = models.IntegerField(null=True)

    def is_in_cooldown(self) -> bool:
        if self.request_limit_type.id == constants.REQUEST_LIMIT_TYPE_STAGGERED:
            last_request_time_dict = RequestAudit.objects.filter(api=self).aggregate(Max('request_time'))
            last_request_time = last_request_time_dict['request_time__max']
            if last_request_time is None:
                return False
            elif (datetime.utcnow() - last_request_time.replace(tzinfo=None)) < timedelta(
                    seconds=self.request_interval_seconds):
                return True
            else:
                return False
        elif self.request_limit_type.id == constants.REQUEST_LIMIT_TYPE_PER_MINUTE:
            one_minute_ago = datetime.now() - timedelta(minutes=1)
            requests_last_minute_dict = RequestAudit.objects.filter(request_time__gte=one_minute_ago).aggregate(
                Count('id'))
            requests_last_minute = requests_last_minute_dict['id__count']
            if requests_last_minute >= self.requests_per_minute:
                return True
            else:
                return False

    @property
    def request_interval_seconds(self) -> float:
        return self.request_interval_ms / 1000


class FixtureStatus(models.Model):
    description = models.CharField(max_length=30)


class Fixture(models.Model):
    home_team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="fixture_home_team")
    away_team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="fixture_away_team")
    home_score = models.IntegerField(null=True, default=None)
    away_score = models.IntegerField(null=True, default=None)
    kickoff_time_utc = models.DateTimeField()
    status = models.ForeignKey(to=FixtureStatus, on_delete=models.CASCADE)


class RequestType(models.Model):
    api = models.ForeignKey(to=Api, on_delete=models.CASCADE)
    base_url = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    current_version_iter = models.IntegerField()

    def get_url(self, *args) -> Union[str, None]:
        url = self.base_url
        if url is None:
            return None
        for arg in args:
            url = re.sub('[\[].*?[\]]', arg, url, 1)
        return url


class RequestAudit(models.Model):
    api = models.ForeignKey(to=Api, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    request_type = models.ForeignKey(to=RequestType, on_delete=models.CASCADE)
    request_time = models.DateTimeField()
    hashed_response = models.CharField(max_length=100, null=True)
    response_code = models.IntegerField()
    successful = models.BooleanField()


class MappingModel(models.Model):
    value = None
    api = models.ForeignKey(Api, on_delete=models.deletion.CASCADE)
    numeric_external_identifier = models.IntegerField(default=None, null=True)
    string_external_identifier = models.CharField(max_length=100, default=None,
                                                  null=True)

    class Meta:
        abstract = True

    @classmethod
    def get_model_from_external_id(cls, external_identifier_type: ExternalIdentifierType,
                                   external_identifier: Union[int, str],
                                   api_id: int) -> Union[models.ForeignKey, None]:
        try:
            api = Api.objects.get(id=api_id)
        except Api.DoesNotExist:
            return None
        try:
            if external_identifier_type == ExternalIdentifierType.NUMERIC:
                mapping = cls.objects.get(api=api,
                                          numeric_external_identifier=external_identifier)
            elif external_identifier_type == ExternalIdentifierType.STRING:
                mapping = cls.objects.get(api=api,
                                          string_external_identifier=external_identifier)
            else:
                raise ValueError("Invalid ExternalIdentifierType enum")
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned as e:
            raise e
        if not mapping:
            return None

        return mapping.value


class FixtureStatusMapping(MappingModel):
    value = models.ForeignKey(FixtureStatus, on_delete=models.deletion.CASCADE)


class TeamMapping(MappingModel):
    value = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)


class FixtureMapping(MappingModel):
    value = models.ForeignKey(Fixture, on_delete=models.deletion.CASCADE)
