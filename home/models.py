"""Defines models for the home feed

This module defines data models for the home feed, as well as mappings for the external APIs being interacted with.
"""
from typing import Union
import re
from datetime import datetime, timedelta
from django.db import models
from home import enums
from home import constants


class Team(models.Model):
    """Django Model representing a Team.

    Simple class defining a team name and an active status.  Mapped to by TeamMapping.

    Attributes:
        name::str
            The team name.
        is_active::bool
            The team's 'active' status.
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_active_teams(cls):
        """Get all active teams"""
        return Team.objects.filter(is_active=True)


class RequestLimitType(models.Model):
    """Model representing the type of request limit.

    This model is used for defining limit types to be used for rate limiting.

    Attributes:
        description::str
            A description of the type.
    """
    description = models.CharField(max_length=200)


class Api(models.Model):
    """Model representing one external API.

    Represents an API, including logic for determining whether it is in cooldown.

    Attributes:
        name::str
            A description of the API.
        request_limit_type::ForeignKey (RequestLimitType)
            The limit type of the API.
        requests_per_minute::IntegerField
            The number of requests allowed per minute from the API.  Only applies to RequestLimitType 'staggered'.
        request_interval_ms::IntegerField
            The number of ms cooldown between API calls.  Only applies to RequestLimitType 'per-minute'.

    Properties:
        request_interval_seconds::int
            request_interval_ms in seconds
    """
    name = models.CharField(max_length=100)
    request_limit_type = models.ForeignKey(to=RequestLimitType, on_delete=models.SET_NULL, null=True)
    requests_per_minute = models.IntegerField(null=True)
    request_interval_ms = models.IntegerField(null=True)

    def is_in_cooldown(self) -> bool:
        """Returns True if the Api is in cooldown and can't be called right now.

        Determines if there is a RequestAudit that took place within request_interval_ms for Apis with
        a RequestLimitType of 'staggered', or if there are N=requests_per_minute number of RequestAudits in the
        last minute for Apis with RequestType 'per-minute.'
        """
        if self.request_limit_type.id == constants.REQUEST_LIMIT_TYPE_STAGGERED:
            last_request_time_dict = RequestAudit.objects.filter(api=self).aggregate(models.Max('request_time'))
            last_request_time = last_request_time_dict['request_time__max']
            if last_request_time is None:
                return False
            if (datetime.utcnow() - last_request_time.replace(tzinfo=None)) < timedelta(
                    seconds=self.request_interval_seconds):
                return True
            return False
        if self.request_limit_type.id == constants.REQUEST_LIMIT_TYPE_PER_MINUTE:
            one_minute_ago = datetime.now() - timedelta(minutes=1)
            requests_last_minute_dict = RequestAudit.objects.filter(request_time__gte=one_minute_ago).aggregate(
                models.Count('id'))
            requests_last_minute = requests_last_minute_dict['id__count']
            if requests_last_minute >= self.requests_per_minute:
                return True
            return False
        raise ValueError("Api has invalid RequestLimitType.")

    @property
    def request_interval_seconds(self) -> float: # pylint: disable=missing-function-docstring
        return self.request_interval_ms / 1000


class FixtureStatus(models.Model):
    """Model representing a FixtureStatus category.

    Attributes:
        description::str
            A description of the status.
    """
    description = models.CharField(max_length=30)


class Fixture(models.Model):
    """Model representing a single Fixture.

    Attributes:
        home_team::ForeignKey (Team)
            The away team in the fixture.
        away_team::ForeignKey (Team)
            The away team in the fixture.
        home_score::IntegerField
            The score of the home team.
        away_score::IntegerField
            The score of the away team.
        kickoff_time_utc::DateTimeField
            The kickoff time as a UTC DateTimeField
        status::ForeignKey (FixtureStatus)
            The status of the fixture.
    """
    home_team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="fixture_home_team")
    away_team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="fixture_away_team")
    home_score = models.IntegerField(null=True, default=None)
    away_score = models.IntegerField(null=True, default=None)
    kickoff_time_utc = models.DateTimeField()
    status = models.ForeignKey(to=FixtureStatus, on_delete=models.CASCADE)


class RequestType(models.Model):
    """A model representing the RequestType category.

    Each RequestType model represents a single HTTP Method + base URL.  This model also includes
    logic for constructing URLs.

    Attributes:
        api::ForeignKey (Api)
            The API associated with this request type.
        base_url::CharField
            The base URL for this request type.  base_url is more of a template than a pure base_url.
            base_urls place argments in the full url as [argument_name].  _construct_url then builds the
            actual URL by replacing these bracketed argument descriptions with the actual arguments.
        description::CharField
            A string description
        current_version_iter::IntegerField
            The version of this API.  This is an internal version for handling backwards compatibility.
    """
    api = models.ForeignKey(to=Api, on_delete=models.CASCADE)
    base_url = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    current_version_iter = models.IntegerField()

    def get_url(self, *args) -> Union[str, None]:
        """Gets a URL for this request type given args.

        Inputs args into bracketed arg placeholders in the base URL.  See the base_url description for more information.
        """
        url = self.base_url
        for arg in args:
            url = re.sub(r'[\[].*?[\]]', arg, url, 1)
        return url


class RequestAudit(models.Model):
    """A model representing an audit of a sent request and it's associated response.

    Attributes:
        api::ForeignKey (Api)
            The API used for the audited request.
        url::CharField
            The URL used for the request.
        request_type::ForeignKey (RequestType)
            The request type associated with the audited request.
        request_time::DateTimeField
            The time of the audited request.
        hashed_response::CharField
            A hash of the response.  Can be used for determining whether a request needs to be reprocessed.
        response_code::IntegerField
            The HTTP response code of the response to the audited request.
        successful::BooleanField
            Whether or not the response was successful.  Will be False for any partial failure state.
    """
    api = models.ForeignKey(to=Api, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    request_type = models.ForeignKey(to=RequestType, on_delete=models.CASCADE)
    request_time = models.DateTimeField()
    hashed_response = models.CharField(max_length=100, null=True)
    response_code = models.IntegerField()
    successful = models.BooleanField()


class MappingModel(models.Model):
    """An abstract model representing a mapping from an external value to an internal model.

    Also contains the logic for doing the actual mapping.

    Attributes:
        value::Model
            The model being mapped to.
        api::Api
            The API associated with the mapping (the source of the external value).
        numeric_external_identifier::IntegerField
            If the external value is numeric, the numeric value associated with that external value.
        string_external_identifier::IntegerField
            If the external value is a string, the string value associated with that external value.
    """
    value = None
    api = models.ForeignKey(Api, on_delete=models.deletion.CASCADE)
    numeric_external_identifier = models.IntegerField(default=None, null=True)
    string_external_identifier = models.CharField(max_length=100, default=None,
                                                  null=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Needed for Django abstract model."""
        abstract = True

    @classmethod
    def get_model_from_external_id(cls, external_identifier_type: enums.ExternalIdentifierType,
                                   external_identifier: Union[int, str],
                                   api_id: int) -> Union[models.ForeignKey, None]:
        """Class method that does the work of mapping the external value to an internal model

        Args:
            external_identifier_type::enums.ExternalIdentifierType
                Numeric or string.
            external_identifier::int||str
                The external identifier being mapped from.
            api_id::int
                The identifier of the Api model.
        Returns:
            The model being mapped to, if found.  Otherwise, raises a DoesNotExist or MultipleObjectsReturned Error.

        Raises:
            DoesNotExist: If the mapped to value is not found.
            ValueError: If the external_identifier_type is not valid.
            MultipleObjectsReturned: Should not occur, is technically thrown by Model.objects.get.
        """
        try:
            api = Api.objects.get(id=api_id)
        except Api.DoesNotExist:
            return None
        try:
            if external_identifier_type == enums.ExternalIdentifierType.NUMERIC:
                mapping = cls.objects.get(api=api,
                                          numeric_external_identifier=external_identifier)
            elif external_identifier_type == enums.ExternalIdentifierType.STRING:
                mapping = cls.objects.get(api=api,
                                          string_external_identifier=external_identifier)
            else:
                raise ValueError("Invalid enums.ExternalIdentifierType enum")
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned as error: # pylint: disable=no-member
            raise error
        if not mapping:
            return None

        return mapping.value


class FixtureStatusMapping(MappingModel):
    """A model representing a mapping to a fixture.

    Attributes:
        value::ForeignKey (FixtureStatus)
            The value being mapped to.  Overrides the parent attribute.
    """
    value = models.ForeignKey(FixtureStatus, on_delete=models.deletion.CASCADE)


class TeamMapping(MappingModel):
    """A model representing a mapping to a Team.

    Attributes:
        value::ForeignKey (Team)
            The value being mapped to.  Overrides the parent attribute.
    """
    value = models.ForeignKey(Team, on_delete=models.deletion.CASCADE)


class FixtureMapping(MappingModel):
    """A model representing a mapping to a Fixture.

    Attributes:
        value::ForeignKey (Fixture)
            The value being mapped to.  Overrides the parent attribute.
    """
    value = models.ForeignKey(Fixture, on_delete=models.deletion.CASCADE)
