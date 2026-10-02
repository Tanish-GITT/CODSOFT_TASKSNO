def validate_course_data(data):
    errors = {}

    if not data:
        errors['body'] = 'Request body is required'
        return errors

    if not data.get('name'):
        errors['name'] = 'Course name is required'

    if not data.get('code'):
        errors['code'] = 'Course code is required'

    if 'credits' not in data:
        errors['credits'] = 'Course credits are required'
    elif not isinstance(data['credits'], int):
        errors['credits'] = 'Credits must be an integer'
    elif data['credits'] <= 0:
        errors['credits'] = 'Credits must be greater than 0'

    return errors