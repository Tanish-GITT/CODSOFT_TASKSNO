import re


def validate_student_data(data):
    errors = {}

    if not data:
        errors['body'] = 'Request body is required'
        return errors

    name = data.get('name')
    email = data.get('email')

    if not name:
        errors['name'] = 'Name is required'
    elif not isinstance(name, str):
        errors['name'] = 'Name must be a string'
    elif len(name.strip()) < 2:
        errors['name'] = 'Name must be at least 2 characters'

    if not email:
        errors['email'] = 'Email is required'
    elif not isinstance(email, str):
        errors['email'] = 'Email must be a string'
    elif not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        errors['email'] = 'Invalid email format'

    return errors