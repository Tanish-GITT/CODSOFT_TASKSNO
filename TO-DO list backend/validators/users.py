import re
from email_validator import validate_email, EmailNotValidError


class UserValidator:
    @staticmethod
    def validate_registration(data):
        errors = []

        # Validate username
        if not data.get('username'):
            errors.append('Username is required')
        elif len(data['username']) < 3:
            errors.append('Username must be at least 3 characters long')
        elif len(data['username']) > 80:
            errors.append('Username must not exceed 80 characters')

        # Validate email
        if not data.get('email'):
            errors.append('Email is required')
        else:
            try:
                validate_email(data['email'])
            except EmailNotValidError:
                errors.append('Invalid email format')

        # Validate password
        if not data.get('password'):
            errors.append('Password is required')
        elif len(data['password']) < 6:
            errors.append('Password must be at least 6 characters long')

        return errors

    @staticmethod
    def validate_login(data):
        errors = []

        if not data.get('username') and not data.get('email'):
            errors.append('Username or email is required')

        if not data.get('password'):
            errors.append('Password is required')

        return errors
