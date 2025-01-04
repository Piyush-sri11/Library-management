from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, Issue
from routes.user_routes import user_blueprint
from routes.book_routes import book_blueprint
from routes.issuance_routes import issuance_blueprint
from config import Config
from flask_apscheduler import APScheduler
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(book_blueprint, url_prefix='/books')
app.register_blueprint(issuance_blueprint, url_prefix='/issuances')

@app.route('/', methods=['GET'])
def home():
    return {
        "message": "Welcome to the Library Management System API"
    }

def update_overdue_issues():
    with app.app_context():
        overdue_issues = Issue.query.filter(Issue.return_date < datetime.utcnow(), Issue.status == 'issued').all()
        for issue in overdue_issues:
            issue.status = 'overdue'
        db.session.commit()

@app.cli.command('reset-db')
def reset_db():
    """Drops and recreates the database."""
    db.drop_all()
    db.create_all()
    print("Database has been reset.")

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    # Schedule the task to run every day at midnight
    scheduler.add_job(id='update_overdue_issues', func=update_overdue_issues, trigger='interval', hours=24)

    with app.app_context():
        db.create_all()

    print("Starting the app")
    app.run(debug=True)
