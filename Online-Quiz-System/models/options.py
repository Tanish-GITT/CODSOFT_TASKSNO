from extensions import db


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)  # Option order (A, B, C, D)

    def to_dict(self, include_correct=False):
        data = {
            'id': self.id,
            'question_id': self.question_id,
            'option_text': self.option_text,
            'order': self.order
        }

        if include_correct:
            data['is_correct'] = self.is_correct

        return data
