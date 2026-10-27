from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.quizzes import Quiz
from models.questions import Question
from models.options import Option
from models.users import User
from validators.quizzes import QuizValidator
from validators.questions import QuestionValidator
from middleware.auth import admin_required
import random

quiz_bp = Blueprint('quizzes', __name__, url_prefix='/api/quizzes')


# Admin Routes

@quiz_bp.route('', methods=['POST'])
@admin_required
def create_quiz():
    """Admin: Create a new quiz"""
    user_id = get_jwt_identity()
    data = request.get_json()

    errors = QuizValidator.validate_create(data)
    if errors:
        return jsonify({'errors': errors}), 400

    quiz = Quiz(
        title=data['title'],
        description=data.get('description'),
        category=data.get('category'),
        difficulty=data.get('difficulty', 'medium'),
        duration_minutes=data.get('duration_minutes', 30),
        pass_percentage=data.get('pass_percentage', 60),
        has_negative_marking=data.get('has_negative_marking', False),
        negative_marks=data.get('negative_marks', 0.25),
        randomize_questions=data.get('randomize_questions', False),
        created_by=user_id
    )

    db.session.add(quiz)
    db.session.commit()

    return jsonify({
        'message': 'Quiz created successfully',
        'quiz': quiz.to_dict()
    }), 201


@quiz_bp.route('/<int:quiz_id>', methods=['PUT'])
@admin_required
def update_quiz(quiz_id):
    """Admin: Update quiz details"""
    data = request.get_json()

    errors = QuizValidator.validate_update(data)
    if errors:
        return jsonify({'errors': errors}), 400

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    if 'title' in data:
        quiz.title = data['title']
    if 'description' in data:
        quiz.description = data['description']
    if 'category' in data:
        quiz.category = data['category']
    if 'difficulty' in data:
        quiz.difficulty = data['difficulty']
    if 'duration_minutes' in data:
        quiz.duration_minutes = data['duration_minutes']
    if 'pass_percentage' in data:
        quiz.pass_percentage = data['pass_percentage']
    if 'has_negative_marking' in data:
        quiz.has_negative_marking = data['has_negative_marking']
    if 'negative_marks' in data:
        quiz.negative_marks = data['negative_marks']
    if 'randomize_questions' in data:
        quiz.randomize_questions = data['randomize_questions']
    if 'is_active' in data:
        quiz.is_active = data['is_active']

    db.session.commit()

    return jsonify({
        'message': 'Quiz updated successfully',
        'quiz': quiz.to_dict()
    }), 200


@quiz_bp.route('/<int:quiz_id>', methods=['DELETE'])
@admin_required
def delete_quiz(quiz_id):
    """Admin: Delete a quiz"""
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    db.session.delete(quiz)
    db.session.commit()

    return jsonify({'message': 'Quiz deleted successfully'}), 200


@quiz_bp.route('/<int:quiz_id>/questions', methods=['POST'])
@admin_required
def add_question(quiz_id):
    """Admin: Add question to quiz"""
    data = request.get_json()
    data['quiz_id'] = quiz_id

    errors = QuestionValidator.validate_create(data)
    if errors:
        return jsonify({'errors': errors}), 400

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    question = Question(
        quiz_id=quiz_id,
        question_text=data['question_text'],
        question_type=data.get('question_type', 'multiple_choice'),
        marks=data.get('marks', 1.0),
        order=data.get('order', len(quiz.questions) + 1)
    )

    db.session.add(question)
    db.session.flush()

    # Add options
    if 'options' in data:
        for i, opt_data in enumerate(data['options']):
            option = Option(
                question_id=question.id,
                option_text=opt_data['option_text'],
                is_correct=opt_data.get('is_correct', False),
                order=i + 1
            )
            db.session.add(option)

    db.session.commit()

    return jsonify({
        'message': 'Question added successfully',
        'question': question.to_dict(include_options=True, include_correct_answer=True)
    }), 201


@quiz_bp.route('/<int:quiz_id>/questions/<int:question_id>', methods=['PUT'])
@admin_required
def update_question(quiz_id, question_id):
    """Admin: Update question"""
    data = request.get_json()

    errors = QuestionValidator.validate_update(data)
    if errors:
        return jsonify({'errors': errors}), 400

    question = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    if 'question_text' in data:
        question.question_text = data['question_text']
    if 'question_type' in data:
        question.question_type = data['question_type']
    if 'marks' in data:
        question.marks = data['marks']
    if 'order' in data:
        question.order = data['order']

    db.session.commit()

    return jsonify({
        'message': 'Question updated successfully',
        'question': question.to_dict(include_options=True, include_correct_answer=True)
    }), 200


@quiz_bp.route('/<int:quiz_id>/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(quiz_id, question_id):
    """Admin: Delete question"""
    question = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({'message': 'Question deleted successfully'}), 200


# Public Routes (for all authenticated users)

@quiz_bp.route('', methods=['GET'])
@jwt_required()
def get_all_quizzes():
    """Get all active quizzes"""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Quiz.query.filter_by(is_active=True)

    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    query = query.order_by(Quiz.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'quizzes': [quiz.to_dict() for quiz in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }), 200


@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz(quiz_id):
    """Get quiz details (without answers)"""
    quiz = Quiz.query.get(quiz_id)
    if not quiz or not quiz.is_active:
        return jsonify({'error': 'Quiz not found'}), 404

    # Return questions in random order if randomize is enabled
    quiz_data = quiz.to_dict(include_questions=True)

    if quiz.randomize_questions and 'questions' in quiz_data:
        random.shuffle(quiz_data['questions'])

    return jsonify({'quiz': quiz_data}), 200


@quiz_bp.route('/admin/all', methods=['GET'])
@admin_required
def get_all_quizzes_admin():
    """Admin: Get all quizzes (including inactive)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = Quiz.query.order_by(Quiz.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'quizzes': [quiz.to_dict(include_questions=True) for quiz in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }), 200
