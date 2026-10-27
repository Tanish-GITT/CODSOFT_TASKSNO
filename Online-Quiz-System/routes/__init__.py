from .auth import auth_bp
from .quizzes import quiz_bp
from .attempts import attempt_bp

__all__ = ['auth_bp', 'quiz_bp', 'attempt_bp']
