from flask import Blueprint, request

from extensions import db
from models import Course
from validators import validate_course_data


course_bp = Blueprint('courses', __name__)

@course_bp.post('/api/courses')
def create_course():
    data = request.get_json()

    errors = validate_course_data(data)

    if errors:
        return {
            'error': 'Validation failed',
            'details': errors
        }, 400

    existing_course = Course.query.filter_by(
        code=data['code']
    ).first()

    if existing_course:
        return {
            'error': 'A course with this code already exists'
        }, 409

    course = Course(
        name=data['name'],
        code=data['code'],
        description=data.get('description'),
        credits=data['credits']
    )

    db.session.add(course)
    db.session.commit()
    
    return {
            'id': course.id,
            'name': course.name,
            'code': course.code,
            'description': course.description,
            'credits': course.credits
        }, 201

@course_bp.get('/api/courses')
def get_courses():
    credits = request.args.get('credits', type=int)
    sort = request.args.get('sort')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Course.query

    if credits:
        query = query.filter_by(credits=credits)

    if sort == 'credits':
        query = query.order_by(Course.credits.asc())
    elif sort == '-credits':
        query = query.order_by(Course.credits.desc())
    elif sort == 'name':
        query = query.order_by(Course.name.asc())
    elif sort == '-name':
        query = query.order_by(Course.name.desc())    

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    courses = pagination.items

    return {
    'courses': [{
        'id': course.id,
        'name': course.name,
        'code': course.code,
        'description': course.description,
        'credits': course.credits
    } for course in courses],
    'pagination': {
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages
    }
}, 200

@course_bp.get('/api/courses/<int:course_id>')
def get_course(course_id):
    course = Course.query.get(course_id)

    if course is None:
        return {
            'error': 'Course not found'
        }, 404

    return {
        'id': course.id,
        'name': course.name,
        'code': course.code,
        'description': course.description,
        'credits': course.credits
    }, 200

@course_bp.put('/api/courses/<int:course_id>')
def update_course(course_id):
    course = Course.query.get(course_id)

    if course is None:
        return {
            'error': 'Course not found'
        }, 404

    data = request.get_json()

    errors = validate_course_data(data)

    if errors:
        return {
            'error': 'Validation failed',
            'details': errors
        }, 400
    
    existing_course = Course.query.filter_by(
        code=data['code']
    ).first()

    if existing_course and existing_course.id != course.id:
        return {
            'error': 'A course with this code already exists'
        }, 409

    course.name = data['name']
    course.code = data['code']
    course.description = data.get('description')
    course.credits = data['credits']

    db.session.commit()

    return {
        'id': course.id,
        'name': course.name,
        'code': course.code,
        'description': course.description,
        'credits': course.credits
    }, 200

@course_bp.delete('/api/courses/<int:course_id>')
def delete_course(course_id):
    course = Course.query.get(course_id)

    if course is None:
        return {
            'error': 'Course not found'
        }, 404

    db.session.delete(course)
    db.session.commit()

    return {
        'message': 'Course deleted successfully'
    }, 200    