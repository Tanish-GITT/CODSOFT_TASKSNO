from extensions import db
from datetime import datetime


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice')  # multiple_choice, true_false
    marks = db.Column(db.Float, default=1.0)
    order = db.Column(db.Integer)  # Question order in quiz
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_options=False, include_correct_answer=False):
        data = {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'marks': self.marks,
            'order': self.order,
            'created_at': self.created_at.isoformat()
        }

        if include_options:
            if include_correct_answer:
                # For admin view - include correct answers
                data['options'] = [o.to_dict(include_correct=True) for o in self.options]
            else:
                # For user view - hide correct answers
                data['options'] = [o.to_dict(include_correct=False) for o in self.options]

        return data
