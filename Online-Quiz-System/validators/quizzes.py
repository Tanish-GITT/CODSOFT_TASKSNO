class QuizValidator:
    VALID_DIFFICULTIES = ['easy', 'medium', 'hard']

    @staticmethod
    def validate_create(data):
        errors = []

        # Validate title
        if not data.get('title'):
            errors.append('Title is required')
        elif len(data['title']) > 200:
            errors.append('Title must not exceed 200 characters')

        # Validate description
        if data.get('description') and len(data['description']) > 2000:
            errors.append('Description must not exceed 2000 characters')

        # Validate category
        if data.get('category') and len(data['category']) > 50:
            errors.append('Category must not exceed 50 characters')

        # Validate difficulty
        if data.get('difficulty') and data['difficulty'] not in QuizValidator.VALID_DIFFICULTIES:
            errors.append(f'Difficulty must be one of: {", ".join(QuizValidator.VALID_DIFFICULTIES)}')

        # Validate duration
        if data.get('duration_minutes'):
            if not isinstance(data['duration_minutes'], int) or data['duration_minutes'] < 1:
                errors.append('Duration must be a positive integer')
            elif data['duration_minutes'] > 300:
                errors.append('Duration must not exceed 300 minutes')

        # Validate pass percentage
        if data.get('pass_percentage'):
            if not isinstance(data['pass_percentage'], int) or data['pass_percentage'] < 0 or data['pass_percentage'] > 100:
                errors.append('Pass percentage must be between 0 and 100')

        # Validate negative marking
        if data.get('has_negative_marking') and data.get('negative_marks'):
            if not isinstance(data['negative_marks'], (int, float)) or data['negative_marks'] < 0:
                errors.append('Negative marks must be a positive number')

        return errors

    @staticmethod
    def validate_update(data):
        return QuizValidator.validate_create(data)
