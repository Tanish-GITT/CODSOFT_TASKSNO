from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.tasks import Task
from validators.tasks import TaskValidator
from datetime import datetime

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


class TaskRoutes:
    @staticmethod
    @task_bp.route('', methods=['POST'])
    @jwt_required()
    def create_task():
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate request data
        errors = TaskValidator.validate_create(data)
        if errors:
            return jsonify({'errors': errors}), 400

        # Parse due_date if provided
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid due_date format'}), 400

        # Create new task
        task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            category=data.get('category'),
            due_date=due_date,
            user_id=user_id
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            'message': 'Task created successfully',
            'task': task.to_dict()
        }), 201

    @staticmethod
    @task_bp.route('', methods=['GET'])
    @jwt_required()
    def get_tasks():
        user_id = get_jwt_identity()

        # Get query parameters
        status = request.args.get('status')
        priority = request.args.get('priority')
        category = request.args.get('category')
        search = request.args.get('search')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Build query
        query = Task.query.filter_by(user_id=user_id)

        # Apply filters
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if category:
            query = query.filter_by(category=category)
        if search:
            query = query.filter(
                db.or_(
                    Task.title.ilike(f'%{search}%'),
                    Task.description.ilike(f'%{search}%')
                )
            )

        # Sort by due_date (ascending) and created_at (descending)
        query = query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc())

        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'tasks': [task.to_dict() for task in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }), 200

    @staticmethod
    @task_bp.route('/<int:task_id>', methods=['GET'])
    @jwt_required()
    def get_task(task_id):
        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({'task': task.to_dict()}), 200

    @staticmethod
    @task_bp.route('/<int:task_id>', methods=['PUT'])
    @jwt_required()
    def update_task(task_id):
        user_id = get_jwt_identity()
        data = request.get_json()

        # Validate request data
        errors = TaskValidator.validate_update(data)
        if errors:
            return jsonify({'errors': errors}), 400

        # Find task
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Update task fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'category' in data:
            task.category = data['category']
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({'error': 'Invalid due_date format'}), 400
            else:
                task.due_date = None

        db.session.commit()

        return jsonify({
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }), 200

    @staticmethod
    @task_bp.route('/<int:task_id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(task_id):
        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200

    @staticmethod
    @task_bp.route('/<int:task_id>/complete', methods=['PATCH'])
    @jwt_required()
    def mark_complete(task_id):
        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        task.status = 'completed'
        db.session.commit()

        return jsonify({
            'message': 'Task marked as completed',
            'task': task.to_dict()
        }), 200

    @staticmethod
    @task_bp.route('/<int:task_id>/pending', methods=['PATCH'])
    @jwt_required()
    def mark_pending(task_id):
        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        task.status = 'pending'
        db.session.commit()

        return jsonify({
            'message': 'Task marked as pending',
            'task': task.to_dict()
        }), 200

    @staticmethod
    @task_bp.route('/stats', methods=['GET'])
    @jwt_required()
    def get_stats():
        user_id = get_jwt_identity()

        total_tasks = Task.query.filter_by(user_id=user_id).count()
        completed_tasks = Task.query.filter_by(user_id=user_id, status='completed').count()
        pending_tasks = Task.query.filter_by(user_id=user_id, status='pending').count()

        # Tasks by priority
        high_priority = Task.query.filter_by(user_id=user_id, priority='high', status='pending').count()
        medium_priority = Task.query.filter_by(user_id=user_id, priority='medium', status='pending').count()
        low_priority = Task.query.filter_by(user_id=user_id, priority='low', status='pending').count()

        # Overdue tasks
        now = datetime.utcnow()
        overdue_tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.status == 'pending',
            Task.due_date < now
        ).count()

        return jsonify({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'by_priority': {
                'high': high_priority,
                'medium': medium_priority,
                'low': low_priority
            }
        }), 200
