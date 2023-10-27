from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Task, List, db
from flask_login import login_required, current_user

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
    return render_template('home.html', lists=lists, current_user=current_user)

@web.route('/lists', methods=['POST'])
@login_required
def create_list():
    """
    Creates a new to-do list for the current user.

    If the request method is POST, this function retrieves the title of the new list from the request form data,
    creates a new List object with the given title and the current user's ID, adds the new list to the database,
    and redirects the user to the list_tasks view for the newly created list.

    Returns:
        A redirect response to the list_tasks view for the newly created list.
    """
    if request.method == 'POST':
        title = request.form['title']
        print(title, current_user)
        if title:
            new_list = List(title=title, user_id=current_user.id)
            db.session.add(new_list)
            db.session.commit()
    return redirect(url_for('web.list_tasks', list_id=new_list.id))


@web.route('/list/<int:list_id>', methods = ['GET', 'POST'])
@login_required
def list_tasks(list_id, parent_id=None):
    """
    This function is responsible for rendering the tasks associated with a specific list ID. 
    It queries the database to get the list object and the tasks associated with the list ID. 
    It then renders an HTML template with the tasks and list object as context variables.

    :param list_id: The ID of the list to fetch tasks for.
    :type list_id: int
    :param parent_id: The ID of the parent task, if any.
    :type parent_id: int, optional
    :return: The rendered HTML template with the tasks and list object as context variables.
    :rtype: str
    """

    if request.method == 'POST':
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
                lists = List.query.filter_by(user_id=current_user.id).all()
                return redirect(url_for('web.list_tasks', list_id=list_id, lists=lists))

    # Fetch tasks associated with the specified list ID
    list = List.query.get(list_id)
    lists = List.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(list_id=list_id, user_id = current_user.id).all()

    # Organize tasks into a list of dictionaries
    task_list = []
    for task in tasks:
        if task.parent_id is None:
            task_dict = {
                'task': task,
                'subtasks': []
            }
            task_list.append(task_dict)
        else:
            for root_task_dict in task_list:
                if task.parent_id == root_task_dict['task'].id:
                    root_task_dict['subtasks'].append(task)

    return render_template('list_tasks.html', task_list=task_list, list=list, lists=lists, current_user=current_user)

@web.route('/list/<int:list_id>/<int:task_id>', methods=['POST'])
@login_required
def create_subtask(list_id, task_id):
    """
    Creates a new subtask associated with the specified list and parent task.

    Args:
        list_id (int): The ID of the list to associate the subtask with.
        task_id (int): The ID of the parent task to associate the subtask with.

    Returns:
        Redirects to the list_tasks view for the specified list ID.

    Raises:
        None.
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


@web.route('/move_task/<int:task_id>/<int:new_list_id>', methods=['POST'])
@login_required
def move_task(task_id, new_list_id):
    """
    This function is responsible for moving a task and its children to another list. It takes the task ID
    and the new list ID as parameters, queries the database to find the task and the new list, and updates
    the task's list_id and parent_id to reflect the move. Subtasks and subsubtasks list_id is also updated
    to the new list.

    :param task_id: The ID of the task to move.
    :type task_id: int
    :param new_list_id: The ID of the new list to move the task to.
    :type new_list_id: int
    :return: A JSON response indicating the success of the move.
    """
    task = Task.query.get(task_id)
    new_list = List.query.get(new_list_id)

    if not task or not new_list:
        flash('Task or new list not found', 'error')
        return redirect(url_for('web.home'))

    # Check if the current user has permission to move the task
    if task.user_id != current_user.id:
        print(task.user_id, current_user.id)
        flash('You do not have permission to move this task', 'error')
        return redirect(url_for('web.home'))

    # Update the task's list_id to move it to the new list
    task.list_id = new_list_id

    # Update the parent_id and list_id of the task's children (subtasks) to maintain the hierarchy
    for subtask in task.subtasks:
        subtask.parent_id = task_id  # Set parent_id to the moved task's ID
        subtask.list_id = new_list_id  # Update the list_id for subtasks

        # Update the list_id of subsubtasks
        for subsubtask in subtask.subtasks:
            subsubtask.list_id = new_list_id

    db.session.commit()
    flash('Task and its children moved successfully', 'success')
    return redirect(url_for('web.list_tasks', list_id=new_list_id))


@web.route('/delete_list/<int:list_id>', methods=['POST'])
@login_required
def delete_list(list_id):
    """
    This route handles the deletion of a list and all tasks associated with it based on the list_id.
    It retrieves the list and all its tasks from the database, checks if they belong to the current user,
    and deletes them. After deletion, the user is redirected to the home page.

    :param list_id: The ID of the list to delete.
    :type list_id: int
    :return: Redirects the user to the home page after deletion.
    """
    list = List.query.get(list_id)

    # Check if the list exists and belongs to the current user
    if not list:
        flash('List not found', 'error')
    elif list.user_id != current_user.id:
        flash('You do not have permission to delete this list', 'error')
    else:
        # Retrieve all tasks associated with the list
        tasks = Task.query.filter_by(list_id=list_id).all()

        # Delete the tasks associated with the list
        for task in tasks:
            db.session.delete(task)

        # Delete the list itself
        db.session.delete(list)
        db.session.commit()

        remaining_lists = List.query.filter_by(user_id=current_user.id).count()
        
    
        if remaining_lists > 0:
            other_list = List.query.filter_by(user_id=current_user.id).first()
            return redirect(url_for('web.list_tasks', list_id=other_list.id))
        else:
            # If there are no remaining lists, redirect to the home page
            return redirect(url_for('web.home'))


