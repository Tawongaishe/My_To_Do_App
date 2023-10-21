from flask import Blueprint, render_template
from .models import Task, List  # Import your Task model
from .api_requests import get_lists, get_tasks  


web = Blueprint('web', __name__)

# Define a route for the home page
@web.route('/')
@web.route('/home')
def home():
    # Query the database to get a list of tasks
    lists = List.query.all()
    lists = get_lists()
    # Render an HTML template and pass the tasks as a context variable
    return render_template('home.html', lists=lists)

@web.route('/list/<int:list_id>')
def list_tasks(list_id):
    list = List.query.get(list_id)
    # Fetch tasks associated with the specified list ID
    tasks = get_tasks(list_id)  # Implement this function to fetch tasks for the given list
    return render_template('list_tasks.html', tasks=tasks, list = list )
