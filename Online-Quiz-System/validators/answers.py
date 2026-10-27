class AnswerValidator:
    @staticmethod
    def validate_submit_answers(data):
        errors = []

        # Validate attempt_id
        if not data.get('attempt_id'):
            errors.append('Attempt ID is required')

        # Validate answers
        if not data.get('answers'):
            errors.append('Answers are required')
        elif not isinstance(data['answers'], list):
            errors.append('Answers must be a list')
        elif len(data['answers']) == 0:
            errors.append('At least one answer is required')
        else:
            for i, answer in enumerate(data['answers']):
                if not answer.get('question_id'):
                    errors.append(f'Question ID is required for answer {i+1}')
                if not answer.get('selected_option_id'):
                    errors.append(f'Selected option ID is required for answer {i+1}')

        return errors
