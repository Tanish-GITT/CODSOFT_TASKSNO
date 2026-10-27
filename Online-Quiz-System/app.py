from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, jwt
from config.settings import Config
from routes.auth import auth_bp
from routes.quizzes import quiz_bp
from routes.attempts import attempt_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(attempt_bp)


@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'ok', 'message': 'Online Quiz System API is running'}, 200


@app.errorhandler(404)
def not_found(error):
    return {'error': 'Endpoint not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)
