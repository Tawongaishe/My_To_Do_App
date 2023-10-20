from flask import request, jsonify
from . import app, db
from .models import Task, List

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It works!'}), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    list_id = data.get('list_id')  # Mandatory list ID
    
    task_id = data.get('id')  # Optional task ID

    # Verify that the list exists
    lst = List.query.get(list_id)
    if not lst:
        return jsonify({'message': 'List not found'}), 404
    else:
        task = Task(id=task_id, title=title, list_id=list_id)
        db.session.add(task)
        db.session.commit()
        return jsonify(task.make_dict()), 201  # Return the task details as JSON1
    

@app.route('/tasks', methods=['GET'])
def list_all_tasks():
    tasks = Task.query.all()
    task_data = []

    for task in tasks:
        task_data.append({
            'id': task.id,
            'title': task.title,
            'done': task.done,
            'list_id': task.list_id,
            'subtasks': [subtask.id for subtask in task.subtasks]
        })

    return jsonify(task_data), 200
    

@app.route('/add_subtask/<int:task_id>', methods=['POST'])
def add_subtask(task_id):
    data = request.get_json()
    parent_id = task_id
    title = data.get('title')
    parent_task = Task.query.get(parent_id)
    depth = parent_task.task_depth + 1

    if not parent_task:
        return jsonify({'message': 'Parent task not found'}), 404
    
    if depth > 2:
        return jsonify({'message': 'Subtask depth cannot be greater than 3'}), 400

    subtask = Task(title=title, parent_id=parent_id, task_depth=depth)
    db.session.add(subtask)

    db.session.commit()

    return jsonify({
        'id': subtask.id,
        'message': 'Added subtask successfully'
    }), 201



@app.route('/tasks/<int:task_id>', methods=['GET'])
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

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    data = request.get_json()
    new_title = data.get('title')
    task.title = new_title
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200


@app.route('/tasks/<int:task_id>/mark_done', methods=['PUT'])
def mark_task_done(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task.done = True
    db.session.commit()

    return jsonify({'message': 'Task marked as done successfully'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.delete()
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404



@app.route('/lists', methods=['GET', 'POST'])
def manage_lists():
    if request.method == 'GET':
        # Retrieve all lists
        lists = List.query.all()
        if lists is not None:
            list_data = [{'id': lst.id, 'title': lst.title} for lst in lists]
        else:
            list_data = []
        return jsonify(list_data), 200

    elif request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        if not title:
            return jsonify({'message': 'Title is required for creating a list'}), 400
        new_list = List(title=title)
        db.session.add(new_list)
        db.session.commit()
        return jsonify({'id': new_list.id,
                        'message': 'List created successfully'}), 201
    else:
        return jsonify({'message': 'Invalid request method'}), 400
    

@app.route('/lists/<int:list_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_list(list_id):
    lst = List.query.get(list_id)
    if not lst:
        return jsonify({'message': 'List not found'}), 404

    if request.method == 'GET':
        # Retrieve a specific list and its tasks
        list_data = {
            'id': lst.id,
            'title': lst.title,
            'tasks': [{'id': task.id, 'title': task.title, 'done': task.done} for task in lst.tasks]
        }
        return jsonify(list_data), 200

    elif request.method == 'PUT':
        # Edit the title of the list
        data = request.get_json()
        new_title = data.get('title')
        lst.edit(new_title)
        return jsonify({'message': 'List updated successfully'}), 200

    elif request.method == 'DELETE':
        # Delete the list and its tasks
        lst.delete()
        return jsonify({'message': 'List and associated tasks deleted successfully'}), 200
