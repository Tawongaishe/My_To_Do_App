from Backend import db, app

# Import your models
from Backend.models import Task #TodoList, Task, Subtask, SubSubtask

# Create a Flask application context
with app.app_context():
    # Create tables
    db.create_all()

print("Database tables created successfully.")