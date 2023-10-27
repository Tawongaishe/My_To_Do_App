from flask import request, jsonify, Blueprint
from .models import Task, List, db


# Create a Blueprint for tasks
tasks = Blueprint('tasks', __name__)


@tasks.route('/lists', methods=['POST']) #base_url/api/lists
def create_list():
    data = request.get_json()
    title = data.get('title')
    lst = List(title=title)
    db.session.add(lst)
    db.session.commit()
    return jsonify(lst.make_dict()), 201

@tasks.route('/lists', methods=['GET']) #base_url/api/lists
def list_all_lists():
    #get all lists from the db
    lists = List.query.all()
    list_data = []
    for lst in lists:
        list_data.append(lst.make_dict())

    return jsonify(list_data), 200


@tasks.route('/lists/<int:list_id>', methods=['GET'])
def get_list(list_id):
    lst = List.query.get(list_id)
    if lst:
        # Fetch the tasks associated with the list
        tasks = Task.query.filter_by(list_id=list_id).all() #SQL 
        
        # Create a dictionary to represent the data
        data = {
            'list': lst.make_dict(),
            'tasks': [task.make_dict() for task in tasks]
        }
        
        # Return the data as a JSON response
        return jsonify(data), 200
    return jsonify({'message': 'List not found'}), 404


@tasks.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    list_id = data.get('list_id')  # Mandatory list ID

    # Verify that the list exists
    lst = List.query.get(list_id)
    if not lst:
        return jsonify({'message': 'List not found'}), 404
    else:
        task = Task( title=title, list_id=list_id)
        db.session.add(task)
        db.session.commit()
        return jsonify(task.make_dict()), 201

@tasks.route('/tasks', methods=['GET'])
def list_all_tasks():
    tasks = Task.query.all()
    task_data = []

    for task in tasks:
        task_data.append(task.make_dict())

    return jsonify(task_data), 200

@tasks.route('/add_subtask/<int:task_id>', methods=['POST'])
def add_subtask(task_id):
    """
    Add a subtask to a parent task.

    Args:
        task_id (int): The ID of the parent task.

    Returns:
        A JSON response containing the ID of the newly created subtask and a success message.
        If the parent task is not found, a 404 error is returned.
        If the subtask depth is greater than 3, a 400 error is returned.
    """
    data = request.get_json()
    parent_id = task_id
    title = data.get('title')
    parent_task = Task.query.get(parent_id)
    depth = parent_task.task_depth + 1

    if not parent_task:
        return jsonify({'message': 'Parent task not found'}), 404

    if depth > 2:
        return jsonify({'message': 'Subtask depth cannot be greater than 3'}), 400
    
    else:
        subtask = Task(title=title, parent_id=parent_id, task_depth=depth)
        db.session.add(subtask)
        db.session.commit()

    return jsonify({
        'id': subtask.id,
        'message': 'Added subtask successfully'
    }), 201

@tasks.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({
            'id': task.id,
            'title': task.title,
            'done': task.done,
            'subtasks': [subtask.id for subtask in task.subtasks]
        }), 200
    return jsonify({'message': 'Task not found'}), 404

@tasks.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    data = request.get_json()
    new_title = data.get('title')
    task.title = new_title
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200

@tasks.route('/tasks/<int:task_id>/mark_done', methods=['PUT'])
def mark_task_done(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task.done = True
    db.session.commit()

    return jsonify({'message': 'Task marked as done successfully'}), 200

@tasks.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.delete_task_and_subtasks()
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404
