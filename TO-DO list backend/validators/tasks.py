from datetime import datetime


class TaskValidator:
    VALID_STATUSES = ['pending', 'completed']
    VALID_PRIORITIES = ['low', 'medium', 'high']

    @staticmethod
    def validate_create(data):
        errors = []

        # Validate title
        if not data.get('title'):
            errors.append('Title is required')
        elif len(data['title']) > 200:
            errors.append('Title must not exceed 200 characters')

        # Validate description (optional)
        if data.get('description') and len(data['description']) > 1000:
            errors.append('Description must not exceed 1000 characters')

        # Validate status
        if data.get('status') and data['status'] not in TaskValidator.VALID_STATUSES:
            errors.append(f'Status must be one of: {", ".join(TaskValidator.VALID_STATUSES)}')

        # Validate priority
        if data.get('priority') and data['priority'] not in TaskValidator.VALID_PRIORITIES:
            errors.append(f'Priority must be one of: {", ".join(TaskValidator.VALID_PRIORITIES)}')

        # Validate category (optional)
        if data.get('category') and len(data['category']) > 50:
            errors.append('Category must not exceed 50 characters')

        # Validate due_date (optional)
        if data.get('due_date'):
            try:
                datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                errors.append('Invalid due_date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)')

        return errors

    @staticmethod
    def validate_update(data):
        errors = []

        # Validate title (optional for update)
        if data.get('title') is not None and len(data['title']) == 0:
            errors.append('Title cannot be empty')
        elif data.get('title') and len(data['title']) > 200:
            errors.append('Title must not exceed 200 characters')

        # Validate description (optional)
        if data.get('description') and len(data['description']) > 1000:
            errors.append('Description must not exceed 1000 characters')

        # Validate status
        if data.get('status') and data['status'] not in TaskValidator.VALID_STATUSES:
            errors.append(f'Status must be one of: {", ".join(TaskValidator.VALID_STATUSES)}')

        # Validate priority
        if data.get('priority') and data['priority'] not in TaskValidator.VALID_PRIORITIES:
            errors.append(f'Priority must be one of: {", ".join(TaskValidator.VALID_PRIORITIES)}')

        # Validate category (optional)
        if data.get('category') and len(data['category']) > 50:
            errors.append('Category must not exceed 50 characters')

        # Validate due_date (optional)
        if data.get('due_date'):
            try:
                datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                errors.append('Invalid due_date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)')

        return errors
