from .models import Task
from . import db

def test_delete_task_and_subtasks():
    # Create a task with subtasks
    task = Task(title='Parent Task')
    subtask1 = Task(title='Subtask 1', parent_task=task)
    subtask2 = Task(title='Subtask 2', parent_task=task)
    subsubtask = Task(title='Sub-subtask', parent_task=subtask1)
    db.session.add_all([task, subtask1, subtask2, subsubtask])
    db.session.commit()

    # Delete the parent task and all subtasks
    task.delete_task_and_subtasks()

    # Check that all tasks have been deleted
    assert Task.query.filter_by(id=task.id).first() is None
    assert Task.query.filter_by(id=subtask1.id).first() is None
    assert Task.query.filter_by(id=subtask2.id).first() is None
    assert Task.query.filter_by(id=subsubtask.id).first() is None




    # Create a task with subtasks
    task = Task(title='Parent Task')
    subtask1 = Task(title='Subtask 1', parent_task=task)
    subtask2 = Task(title='Subtask 2', parent_task=task)
    subsubtask = Task(title='Sub-subtask', parent_task=subtask1)
    db.session.add_all([task, subtask1, subtask2, subsubtask])
    db.session.commit()

    # Delete the parent task and all subtasks
    task.delete_task_and_subtasks()

    # Check that all tasks have been deleted
    assert Task.query.filter_by(id=task.id).first() is None
    assert Task.query.filter_by(id=subtask1.id).first() is None
    assert Task.query.filter_by(id=subtask2.id).first() is None
    assert Task.query.filter_by(id=subsubtask.id).first() is None

def test_edit():
    # Create a task
    task = Task(title='Original Title')
    db.session.add(task)
    db.session.commit()

    # Edit the task's title
    task.edit('New Title')

    # Check that the title has been updated
    assert task.title == 'New Title'

def test_mark_as_done():
    # Create a task
    task = Task(title='Task')
    db.session.add(task)
    db.session.commit()

    # Mark the task as done
    task.mark_as_done()

    # Check that the task is marked as done
    assert task.done == True

def test_make_dict():
    # Create a task with subtasks
    task = Task(title='Parent Task')
    subtask1 = Task(title='Subtask 1', parent_task=task)
    subtask2 = Task(title='Subtask 2', parent_task=task)
    subsubtask = Task(title='Sub-subtask', parent_task=subtask1)
    db.session.add_all([task, subtask1, subtask2, subsubtask])
    db.session.commit()

    # Create a dictionary representation of the task
    task_dict = task.make_dict()

    # Check that the dictionary contains the correct information
    assert task_dict['id'] == task.id
    assert task_dict['title'] == task.title
    assert task_dict['done'] == task.done
    assert task_dict['parent_id'] == task.parent_id
    assert task_dict['task_depth'] == task.task_depth
    assert len(task_dict['subtasks']) == 2
    assert task_dict['subtasks'][0]['id'] == subtask1.id
    assert task_dict['subtasks'][0]['title'] == subtask1.title
    assert task_dict['subtasks'][0]['done'] == subtask1.done
    assert task_dict['subtasks'][0]['parent_id'] == subtask1.parent_id
    assert task_dict['subtasks'][0]['task_depth'] == subtask1.task_depth
    assert len(task_dict['subtasks'][0]['subtasks']) == 1
    assert task_dict['subtasks'][0]['subtasks'][0]['id'] == subsubtask.id
    assert task_dict['subtasks'][0]['subtasks'][0]['title'] == subsubtask.title
    assert task_dict['subtasks'][0]['subtasks'][0]['done'] == subsubtask.done
    assert task_dict['subtasks'][0]['subtasks'][0]['parent_id'] == subsubtask.parent_id
    assert task_dict['subtasks'][0]['subtasks'][0]['task_depth'] == subsubtask.task_depth
    assert task_dict['subtasks'][1]['id'] == subtask2.id
    assert task_dict['subtasks'][1]['title'] == subtask2.title
    assert task_dict['subtasks'][1]['done'] == subtask2.done
    assert task_dict['subtasks'][1]['parent_id'] == subtask2.parent_id
    assert task_dict['subtasks'][1]['task_depth'] == subtask2.task_depth
    assert len(task_dict['subtasks'][1]['subtasks']) == 0


#call the test functions one by one 
test_delete_task_and_subtasks()