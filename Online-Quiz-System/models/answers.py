from extensions import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('option.id'))
    is_correct = db.Column(db.Boolean)
    marks_obtained = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'attempt_id': self.attempt_id,
            'question_id': self.question_id,
            'selected_option_id': self.selected_option_id,
            'is_correct': self.is_correct,
            'marks_obtained': self.marks_obtained
        }
