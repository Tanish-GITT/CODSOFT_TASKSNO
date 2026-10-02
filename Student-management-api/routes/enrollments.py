from flask import Blueprint, request

from extensions import db
from models import Enrollment, Student, Course
from validators import validate_enrollment_data


enrollment_bp = Blueprint('enrollments', __name__)

@enrollment_bp.post('/api/enrollments')
def create_enrollment():
    data = request.get_json()

    errors = validate_enrollment_data(data)

    if errors:
        return {
            'error': 'Validation failed',
            'details': errors
        }, 400

    student = Student.query.get(data['student_id'])

    if student is None:
        return {
            'error': 'Student not found'
        }, 404

    course = Course.query.get(data['course_id'])

    if course is None:
        return {
            'error': 'Course not found'
        }, 404

    existing_enrollment = Enrollment.query.filter_by(
        student_id=data['student_id'],
        course_id=data['course_id']
    ).first()

    if existing_enrollment:
        return {
            'error': 'Student is already enrolled in this course'
        }, 409

    enrollment = Enrollment(
        student_id=data['student_id'],
        course_id=data['course_id']
    )

    db.session.add(enrollment)
    db.session.commit()

    return {
        'id': enrollment.id,
        'student_id': enrollment.student_id,
        'course_id': enrollment.course_id
    }, 201

@enrollment_bp.get('/api/enrollments')
def get_enrollments():
    student_id = request.args.get('student_id', type=int)
    course_id = request.args.get('course_id', type=int)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Enrollment.query

    if student_id:
     query = query.filter_by(student_id=student_id)

    if course_id:
     query = query.filter_by(course_id=course_id)

    pagination = query.paginate(
    page=page,
    per_page=per_page,
    error_out=False
)

    enrollments = pagination.items

    result = []
    for enrollment in enrollments:
        result.append({
    'id': enrollment.id,
    'student': {
        'id': enrollment.student.id,
        'name': enrollment.student.name,
        'email': enrollment.student.email
    },
    'course': {
        'id': enrollment.course.id,
        'name': enrollment.course.name,
        'code': enrollment.course.code
    }
})
    return {
        'enrollments': result
    }, 200

@enrollment_bp.get('/api/enrollments/<int:enrollment_id>')
def get_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)

    if enrollment is None:
        return {
            'error': 'Enrollment not found'
        }, 404

    return {
        'id': enrollment.id,
        'student': {
            'id': enrollment.student.id,
            'name': enrollment.student.name,
            'email': enrollment.student.email
        },
        'course': {
            'id': enrollment.course.id,
            'name': enrollment.course.name,
            'code': enrollment.course.code
        }
    }, 200

@enrollment_bp.delete('/api/enrollments/<int:enrollment_id>')
def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)

    if enrollment is None:
        return {
            'error': 'Enrollment not found'
        }, 404

    db.session.delete(enrollment)
    db.session.commit()

    return {
        'message': 'Enrollment deleted successfully'
    }, 200