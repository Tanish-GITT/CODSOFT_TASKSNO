from extensions import db


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('course.id'),
        nullable=False
    )
    student = db.relationship('Student')
    course = db.relationship('Course')

    __table_args__ = (
    db.UniqueConstraint(
        'student_id',
        'course_id',
        name='unique_student_course'
    ),
)