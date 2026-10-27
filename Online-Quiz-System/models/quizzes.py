from extensions import db
from datetime import datetime


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    duration_minutes = db.Column(db.Integer, default=30)  # Quiz timer
    pass_percentage = db.Column(db.Integer, default=60)  # For certificate eligibility
    has_negative_marking = db.Column(db.Boolean, default=False)
    negative_marks = db.Column(db.Float, default=0.25)  # Marks to deduct for wrong answer
    randomize_questions = db.Column(db.Boolean, default=False)  # Random question order
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_questions=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'duration_minutes': self.duration_minutes,
            'pass_percentage': self.pass_percentage,
            'has_negative_marking': self.has_negative_marking,
            'negative_marks': self.negative_marks if self.has_negative_marking else 0,
            'randomize_questions': self.randomize_questions,
            'is_active': self.is_active,
            'total_questions': len(self.questions),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by
        }

        if include_questions:
            data['questions'] = [q.to_dict(include_options=True) for q in self.questions]

        return data
