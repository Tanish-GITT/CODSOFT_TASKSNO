class QuestionValidator:
    VALID_QUESTION_TYPES = ['multiple_choice', 'true_false']

    @staticmethod
    def validate_create(data):
        errors = []

        # Validate quiz_id
        if not data.get('quiz_id'):
            errors.append('Quiz ID is required')

        # Validate question_text
        if not data.get('question_text'):
            errors.append('Question text is required')
        elif len(data['question_text']) > 1000:
            errors.append('Question text must not exceed 1000 characters')

        # Validate question_type
        if data.get('question_type') and data['question_type'] not in QuestionValidator.VALID_QUESTION_TYPES:
            errors.append(f'Question type must be one of: {", ".join(QuestionValidator.VALID_QUESTION_TYPES)}')

        # Validate marks
        if data.get('marks'):
            if not isinstance(data['marks'], (int, float)) or data['marks'] <= 0:
                errors.append('Marks must be a positive number')

        # Validate options
        if 'options' in data:
            if not isinstance(data['options'], list):
                errors.append('Options must be a list')
            elif len(data['options']) < 2:
                errors.append('At least 2 options are required')
            else:
                correct_count = sum(1 for opt in data['options'] if opt.get('is_correct'))
                if correct_count == 0:
                    errors.append('At least one option must be marked as correct')
                elif correct_count > 1 and data.get('question_type') != 'multiple_choice':
                    errors.append('Only one option can be correct for true/false questions')

                for i, opt in enumerate(data['options']):
                    if not opt.get('option_text'):
                        errors.append(f'Option {i+1} text is required')

        return errors

    @staticmethod
    def validate_update(data):
        errors = []

        if data.get('question_text') and len(data['question_text']) > 1000:
            errors.append('Question text must not exceed 1000 characters')

        if data.get('question_type') and data['question_type'] not in QuestionValidator.VALID_QUESTION_TYPES:
            errors.append(f'Question type must be one of: {", ".join(QuestionValidator.VALID_QUESTION_TYPES)}')

        if data.get('marks'):
            if not isinstance(data['marks'], (int, float)) or data['marks'] <= 0:
                errors.append('Marks must be a positive number')

        return errors
