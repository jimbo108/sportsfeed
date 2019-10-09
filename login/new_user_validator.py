from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from enum import Enum 
from .models import User

class NewUserSubmissionErrors(Enum):
    MISSING_NAME = "missing_name"
    INVALID_NAME = "invalid_name"
    MISSING_EMAIL = "missing_email"
    INVALID_EMAIL = "invalid_email"
    OVERSHORT_PASSWORD = "overshort_password"
    MISSING_PASSWORD = "missing_password"
    DUPLICATE_EMAIL = "duplicate_email"


class NewUserValidator():

    MIN_PASSWORD_LENGTH = 8

    def __init__(self, name, email, password):
        self.missing_name = (name is None) or (name == "")
        self.missing_email = (email is None) or (email == "")
        self.missing_password = (password is None) or (password == "")

        self.missing_fields = self.missing_name or self.missing_email or self.missing_password
        if self.missing_fields:
            self.invalid_name = False
            self.invalid_email = False
            self.overshort_password = False
            return

        self.invalid_name = self.name_is_invalid(name)
        self.invalid_email = False
        try:
            validate_email(email)
        except ValidationError:
            self.invalid_email=True
        
        self.duplicate_email = self.email_already_exists(email)

        self.overshort_password = self.password_is_overshort(password)

    def name_is_invalid(self, name):
        if not all(x.isalpha() or x == " " for x in name):
            return True
        else:
            return False
        
    def password_is_overshort(self, password):
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return True
        else:
            return False
        
    def email_already_exists(self, email):
        user_already_exists = True

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            user_already_exists = False
        
        return user_already_exists