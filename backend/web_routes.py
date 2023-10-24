from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Task, List, db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

web = Blueprint('web', __name__)


# Define a route for the home page
@web.route('/home')
@login_required
def home():
    """
    This function is responsible for rendering the home page of the web application. 
    It queries the database to get all the lists and renders an HTML template with the lists as a context variable.
    
    :return: The rendered HTML template with the lists as a context variable.
    """
    # Query the database to get a list of tasks
    lists = List.query.filter_by(user_id=current_user.id).all()
    #if there are no lists prompt a user with a button to add a list 
    if len(lists) == 0:
        return render_template('home.html', lists=lists, no_lists = True)
    # Render an HTML template and pass the tasks as a context variable
    return render_template('home.html', lists=lists)

@web.route('/lists', methods=['POST'])
@login_required
def create_list():
    if request.method == 'POST':
        title = request.form['title']
        print(title, current_user)
        if title:
            new_list = List(title=title, user_id=current_user.id)
            db.session.add(new_list)
            db.session.commit()
    return redirect(url_for('web.home'))


@web.route('/list/<int:list_id>', methods = ['GET', 'POST'])
@login_required
def list_tasks(list_id, parent_id=None):
    """
    This function is responsible for rendering the tasks associated with a specific list ID. 
    It queries the database to get the list object and the tasks associated with the list ID. 
    It then renders an HTML template with the tasks and list object as context variables.

    :param list_id: The ID of the list to fetch tasks for.
    :type list_id: int
    :return: The rendered HTML template with the tasks and list object as context variables.
    """

    if request.method == 'POST':
        # Get the task title from the form
        title = request.form.get('title')
        if not title:
            flash('Task title is required', 'error')
        else:
            lst = List.query.get(list_id)
            if not lst:
                flash('List not found', 'error')
            else:
                # Create a new task and associate it with the list
                task = Task(title=title, list_id=list_id, user_id=current_user.id)
                db.session.add(task)
                db.session.commit()
                return redirect(url_for('web.list_tasks', list_id=list_id))

    # Fetch tasks associated with the specified list ID
    list = List.query.get(list_id)
    tasks = Task.query.filter_by(list_id=list_id, user_id = current_user.id).all()

    # Organize tasks into a list of dictionaries
    task_list = []
    for task in tasks:
        if task.parent_id is None:
            # This is a root task
            task_dict = {
                'task': task,
                'subtasks': []
            }
            task_list.append(task_dict)
        else:
            # This is a subtask
            for root_task_dict in task_list:
                if task.parent_id == root_task_dict['task'].id:
                    # Add subtask to the corresponding root task
                    root_task_dict['subtasks'].append(task)

    return render_template('list_tasks.html', task_list=task_list, list=list)

@web.route('/list/<int:list_id>/<int:task_id>', methods=['POST'])
@login_required
def create_subtask(list_id, task_id):
    if request.method == 'POST':
        # Get the task title from the form
        title = request.form.get('title')
        if not title:
            flash('Task title is required', 'error')
        else:
            lst = List.query.get(list_id)
            if not lst:
                flash('List not found', 'error')
            else:
                # Create a new task and associate it with the list
                task = Task(title=title, list_id=list_id, parent_id=task_id, user_id=current_user.id)
                depth = task.calculate_depth()
                if depth == False:
                    db.session.rollback()
                    flash('Cannot create a subtask at this depth level', 'error')
                    return redirect(url_for('web.list_tasks', list_id=list_id))
                db.session.add(task)
                db.session.commit()
                return redirect(url_for('web.list_tasks', list_id=list_id))

    if not title:
        flash('Subtask title is required', 'error')
        return redirect(url_for('web.list_tasks', list_id=list_id))
    else:
        # Verify that the list and parent task exist
        lst = List.query.get(list_id)
        parent_task = Task.query.get(task_id)

        if not lst:
            flash('List not found', 'error')
            return redirect(url_for('web.list_tasks', list_id=list_id))
        elif not parent_task:
            flash('Parent task not found', 'error')
            return redirect(url_for('web.list_tasks', list_id=list_id))
        elif parent_task.task_depth > 1:
            flash('Cannot create a subtask at this depth level', 'error')
            return redirect(url_for('web.list_tasks', list_id=list_id))
        else:
            # Create a new subtask and associate it with the list and parent task
            subtask = Task(title=title, list_id=list_id, parent_id=task_id)
            db.session.add(subtask)
            db.session.commit()

    # Fetch tasks associated with the specified list ID and parent task



@web.route('/list/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """
    This function is responsible for deleting a task from the database. 
    It queries the database to get the task object and then deletes it. 
    It then returns a JSON response with a success message.

    :param task_id: The ID of the task to delete.
    :type task_id: int
    :return: A JSON response with a success message.
    """
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            task.delete_task_and_subtasks()
            return redirect(url_for('web.list_tasks', list_id=task.list_id))
        else:
            flash('You do not have permission to delete this task', 'error')
            return redirect(url_for('web.list_tasks', list_id=task.list))


#click into a task and get all the subtasks and subsubtasks for that task 
@web.route('/task/<int:task_id>')
@login_required
def task_details(task_id):
    """
    generate detailed docstring for me here

    """
    task = Task.query.get(task_id)
    return render_template('task_details.html', task = task)
