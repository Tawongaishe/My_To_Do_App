from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager  # Import Manager from Flask-Script


# Import your Flask app instance here
from backend import app, db


# Create a manager object
manager = Manager(app)

migrate = Migrate(app, db)

# Register the 'db' command for migrations
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
