from flask import Flask

from extensions import db
from routes.students import student_bp
from routes.courses import course_bp
from routes.enrollments import enrollment_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db.init_app(app)

app.register_blueprint(student_bp)
app.register_blueprint(course_bp)
app.register_blueprint(enrollment_bp)

@app.get('/api/health')
def health_check():
    return {'status': 'ok'}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)