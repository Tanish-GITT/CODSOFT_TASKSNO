def validate_enrollment_data(data):
    errors = {}

    if not data:
        errors['body'] = 'Request body is required'
        return errors

    if 'student_id' not in data:
        errors['student_id'] = 'Student ID is required'
    elif not isinstance(data['student_id'], int):
        errors['student_id'] = 'Student ID must be an integer'
    elif data['student_id'] <= 0:
        errors['student_id'] = 'Student ID must be greater than 0'

    if 'course_id' not in data:
        errors['course_id'] = 'Course ID is required'
    elif not isinstance(data['course_id'], int):
        errors['course_id'] = 'Course ID must be an integer'
    elif data['course_id'] <= 0:
        errors['course_id'] = 'Course ID must be greater than 0'

    return errors