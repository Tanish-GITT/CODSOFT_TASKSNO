from flask import Blueprint, request

from extensions import db
from models import Student
from validators import validate_student_data

student_bp = Blueprint('students', __name__)

@student_bp.get('/api/students')
def get_students():
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Student.query

    if search:
        query = query.filter(
        db.or_(
            Student.name.ilike(f'%{search}%'),
            Student.email.ilike(f'%{search}%')
        )
    )

    pagination = query.paginate(
    page=page,
    per_page=per_page,
    error_out=False
)

    students = pagination.items

    result = []

    for student in students:
        result.append({
            'id': student.id,
            'name': student.name,
            'email': student.email
        })

    return {
    'students': result,
    'pagination': {
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages
    }
    }, 200

@student_bp.get('/api/students/<int:student_id>')
def get_student(student_id):
    student = Student.query.get(student_id)

    if student is None:
        return {
            'error': 'Student not found'
        }, 404

    return {
        'id': student.id,
        'name': student.name,
        'email': student.email
    }, 200

@student_bp.put('/api/students/<int:student_id>')
def update_student(student_id):
    student = Student.query.get(student_id)

    if student is None:
        return {
            'error': 'Student not found'
        }, 404

    data = request.get_json()

    errors = validate_student_data(data)

    if errors:
        return {
            'error': 'Validation failed',
            'details': errors
        }, 400

    existing_student = Student.query.filter_by(
        email=data['email']
    ).first()

    if existing_student and existing_student.id != student.id:
        return {
            'error': 'A student with this email already exists'
        }, 409

    student.name = data['name']
    student.email = data['email']

    db.session.commit()

    return {
        'id': student.id,
        'name': student.name,
        'email': student.email
    }, 200

@student_bp.delete('/api/students/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get(student_id)

    if student is None:
        return {
            'error': 'Student not found'
        }, 404

    db.session.delete(student)
    db.session.commit()

    return {
        'message': 'Student deleted successfully'
    }, 200

@student_bp.post('/api/students')
def create_student():
    data = request.get_json()

    errors = validate_student_data(data)

    if errors:
        return {
            'error': 'Validation failed',
            'details': errors
        }, 400

    existing_student = Student.query.filter_by(
        email=data['email']
    ).first()

    if existing_student:
        return {
            'error': 'A student with this email already exists'
        }, 409

    student = Student(
        name=data['name'],
        email=data['email']
    )

    db.session.add(student)
    db.session.commit()

    return {
        'id': student.id,
        'name': student.name,
        'email': student.email
    }, 201

