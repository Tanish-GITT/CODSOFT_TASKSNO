from extensions import db
from datetime import datetime


class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, abandoned
    score = db.Column(db.Float)
    total_marks = db.Column(db.Float)
    percentage = db.Column(db.Float)
    passed = db.Column(db.Boolean)
    certificate_eligible = db.Column(db.Boolean, default=False)
    time_taken_minutes = db.Column(db.Integer)

    # Relationships
    answers = db.relationship('Answer', backref='attempt', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_answers=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'quiz_id': self.quiz_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'score': self.score,
            'total_marks': self.total_marks,
            'percentage': self.percentage,
            'passed': self.passed,
            'certificate_eligible': self.certificate_eligible,
            'time_taken_minutes': self.time_taken_minutes
        }

        if include_answers:
            data['answers'] = [a.to_dict() for a in self.answers]

        return data
