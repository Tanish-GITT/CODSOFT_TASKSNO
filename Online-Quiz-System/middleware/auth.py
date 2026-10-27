from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.users import User


def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or missing token'}), 401
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user or user.role != 'admin':
                return jsonify({'error': 'Admin access required'}), 403

            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or missing token'}), 401
    return wrapper


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)
