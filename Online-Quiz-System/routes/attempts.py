from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.quizzes import Quiz
from models.questions import Question
from models.options import Option
from models.quiz_attempts import QuizAttempt
from models.answers import Answer
from models.users import User
from validators.answers import AnswerValidator
from datetime import datetime, timedelta
from sqlalchemy import func, desc

attempt_bp = Blueprint('attempts', __name__, url_prefix='/api/attempts')


@attempt_bp.route('/start', methods=['POST'])
@jwt_required()
def start_quiz():
    """Start a new quiz attempt"""
    user_id = get_jwt_identity()
    data = request.get_json()

    quiz_id = data.get('quiz_id')
    if not quiz_id:
        return jsonify({'error': 'Quiz ID is required'}), 400

    quiz = Quiz.query.get(quiz_id)
    if not quiz or not quiz.is_active:
        return jsonify({'error': 'Quiz not found'}), 404

    if len(quiz.questions) == 0:
        return jsonify({'error': 'Quiz has no questions'}), 400

    # Create new attempt
    attempt = QuizAttempt(
        user_id=user_id,
        quiz_id=quiz_id,
        start_time=datetime.utcnow(),
        status='in_progress'
    )

    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        'message': 'Quiz started successfully',
        'attempt': attempt.to_dict(),
        'quiz': quiz.to_dict(include_questions=True),
        'end_time': (attempt.start_time + timedelta(minutes=quiz.duration_minutes)).isoformat()
    }), 201


@attempt_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_answers():
    """Submit answers and calculate score"""
    user_id = get_jwt_identity()
    data = request.get_json()

    errors = AnswerValidator.validate_submit_answers(data)
    if errors:
        return jsonify({'errors': errors}), 400

    attempt = QuizAttempt.query.filter_by(
        id=data['attempt_id'],
        user_id=user_id
    ).first()

    if not attempt:
        return jsonify({'error': 'Attempt not found'}), 404

    if attempt.status == 'completed':
        return jsonify({'error': 'Quiz already submitted'}), 400

    quiz = Quiz.query.get(attempt.quiz_id)

    # Calculate score
    total_score = 0
    total_marks = sum(q.marks for q in quiz.questions)
    correct_answers = 0
    wrong_answers = 0

    for answer_data in data['answers']:
        question = Question.query.get(answer_data['question_id'])
        if not question or question.quiz_id != quiz.id:
            continue

        selected_option = Option.query.get(answer_data['selected_option_id'])
        if not selected_option or selected_option.question_id != question.id:
            continue

        # Check if answer is correct
        is_correct = selected_option.is_correct
        marks_obtained = 0

        if is_correct:
            marks_obtained = question.marks
            correct_answers += 1
        else:
            wrong_answers += 1
            if quiz.has_negative_marking:
                marks_obtained = -quiz.negative_marks

        total_score += marks_obtained

        # Save answer
        answer = Answer(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_option_id=selected_option.id,
            is_correct=is_correct,
            marks_obtained=marks_obtained
        )
        db.session.add(answer)

    # Update attempt
    attempt.end_time = datetime.utcnow()
    attempt.status = 'completed'
    attempt.score = max(0, total_score)  # Score cannot be negative
    attempt.total_marks = total_marks
    attempt.percentage = (attempt.score / total_marks * 100) if total_marks > 0 else 0
    attempt.passed = attempt.percentage >= quiz.pass_percentage
    attempt.certificate_eligible = attempt.passed
    attempt.time_taken_minutes = int((attempt.end_time - attempt.start_time).total_seconds() / 60)

    db.session.commit()

    return jsonify({
        'message': 'Quiz submitted successfully',
        'result': {
            'attempt_id': attempt.id,
            'score': attempt.score,
            'total_marks': total_marks,
            'percentage': round(attempt.percentage, 2),
            'passed': attempt.passed,
            'certificate_eligible': attempt.certificate_eligible,
            'correct_answers': correct_answers,
            'wrong_answers': wrong_answers,
            'total_questions': len(quiz.questions),
            'time_taken_minutes': attempt.time_taken_minutes
        }
    }), 200


@attempt_bp.route('/my-attempts', methods=['GET'])
@jwt_required()
def get_my_attempts():
    """Get current user's quiz attempts"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    quiz_id = request.args.get('quiz_id', type=int)

    query = QuizAttempt.query.filter_by(user_id=user_id)

    if quiz_id:
        query = query.filter_by(quiz_id=quiz_id)

    query = query.order_by(QuizAttempt.start_time.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    attempts_with_quiz = []
    for attempt in pagination.items:
        attempt_data = attempt.to_dict()
        quiz = Quiz.query.get(attempt.quiz_id)
        attempt_data['quiz_title'] = quiz.title if quiz else 'Unknown'
        attempts_with_quiz.append(attempt_data)

    return jsonify({
        'attempts': attempts_with_quiz,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }), 200


@attempt_bp.route('/<int:attempt_id>', methods=['GET'])
@jwt_required()
def get_attempt_details(attempt_id):
    """Get detailed result of a quiz attempt"""
    user_id = get_jwt_identity()

    attempt = QuizAttempt.query.filter_by(id=attempt_id, user_id=user_id).first()
    if not attempt:
        return jsonify({'error': 'Attempt not found'}), 404

    quiz = Quiz.query.get(attempt.quiz_id)
    result = attempt.to_dict(include_answers=True)
    result['quiz_title'] = quiz.title

    # Include question and option details
    detailed_answers = []
    for answer in attempt.answers:
        question = Question.query.get(answer.question_id)
        selected_option = Option.query.get(answer.selected_option_id)
        correct_option = Option.query.filter_by(
            question_id=question.id,
            is_correct=True
        ).first()

        detailed_answers.append({
            'question': question.to_dict(include_options=True, include_correct_answer=True),
            'selected_option': selected_option.to_dict(include_correct=True) if selected_option else None,
            'correct_option_id': correct_option.id if correct_option else None,
            'is_correct': answer.is_correct,
            'marks_obtained': answer.marks_obtained
        })

    result['detailed_answers'] = detailed_answers

    return jsonify({'result': result}), 200


@attempt_bp.route('/leaderboard/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_leaderboard(quiz_id):
    """Get leaderboard for a specific quiz"""
    limit = request.args.get('limit', 10, type=int)

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    # Get best attempt for each user
    subquery = db.session.query(
        QuizAttempt.user_id,
        func.max(QuizAttempt.score).label('best_score')
    ).filter_by(
        quiz_id=quiz_id,
        status='completed'
    ).group_by(QuizAttempt.user_id).subquery()

    leaderboard = db.session.query(
        QuizAttempt,
        User.username
    ).join(
        subquery,
        db.and_(
            QuizAttempt.user_id == subquery.c.user_id,
            QuizAttempt.score == subquery.c.best_score
        )
    ).join(
        User,
        QuizAttempt.user_id == User.id
    ).filter(
        QuizAttempt.quiz_id == quiz_id
    ).order_by(
        desc(QuizAttempt.score),
        QuizAttempt.time_taken_minutes.asc()
    ).limit(limit).all()

    leaderboard_data = []
    for rank, (attempt, username) in enumerate(leaderboard, start=1):
        leaderboard_data.append({
            'rank': rank,
            'username': username,
            'score': attempt.score,
            'percentage': round(attempt.percentage, 2),
            'time_taken_minutes': attempt.time_taken_minutes,
            'attempt_date': attempt.end_time.isoformat() if attempt.end_time else None
        })

    return jsonify({
        'quiz_title': quiz.title,
        'leaderboard': leaderboard_data
    }), 200


@attempt_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_user_statistics():
    """Get performance statistics for current user"""
    user_id = get_jwt_identity()

    total_attempts = QuizAttempt.query.filter_by(
        user_id=user_id,
        status='completed'
    ).count()

    passed_attempts = QuizAttempt.query.filter_by(
        user_id=user_id,
        status='completed',
        passed=True
    ).count()

    avg_score = db.session.query(
        func.avg(QuizAttempt.percentage)
    ).filter_by(
        user_id=user_id,
        status='completed'
    ).scalar() or 0

    certificates_earned = QuizAttempt.query.filter_by(
        user_id=user_id,
        status='completed',
        certificate_eligible=True
    ).count()

    # Get recent attempts
    recent_attempts = QuizAttempt.query.filter_by(
        user_id=user_id,
        status='completed'
    ).order_by(
        QuizAttempt.end_time.desc()
    ).limit(5).all()

    recent_data = []
    for attempt in recent_attempts:
        quiz = Quiz.query.get(attempt.quiz_id)
        recent_data.append({
            'quiz_title': quiz.title if quiz else 'Unknown',
            'score': attempt.score,
            'percentage': round(attempt.percentage, 2),
            'passed': attempt.passed,
            'date': attempt.end_time.isoformat() if attempt.end_time else None
        })

    return jsonify({
        'total_attempts': total_attempts,
        'passed_attempts': passed_attempts,
        'failed_attempts': total_attempts - passed_attempts,
        'average_score': round(avg_score, 2),
        'certificates_earned': certificates_earned,
        'recent_attempts': recent_data
    }), 200


@attempt_bp.route('/admin/all-attempts', methods=['GET'])
@jwt_required()
def get_all_attempts_admin():
    """Admin: Get all quiz attempts"""
    user = User.query.get(get_jwt_identity())
    if not user or user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = QuizAttempt.query.order_by(
        QuizAttempt.start_time.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    attempts_data = []
    for attempt in pagination.items:
        user = User.query.get(attempt.user_id)
        quiz = Quiz.query.get(attempt.quiz_id)
        attempt_data = attempt.to_dict()
        attempt_data['username'] = user.username if user else 'Unknown'
        attempt_data['quiz_title'] = quiz.title if quiz else 'Unknown'
        attempts_data.append(attempt_data)

    return jsonify({
        'attempts': attempts_data,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }), 200
