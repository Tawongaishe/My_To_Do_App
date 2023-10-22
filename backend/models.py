from . import db
from sqlalchemy.orm import collections
from flask import flash

class List(db.Model):
    """
    Represents a to-do list.

    Attributes:
    - id (int): The unique identifier for the list.
    - title (str): The title of the list.
    - tasks (list): A list of tasks associated with the list.

    Methods:
    - __init__(self, title): Initializes a new instance of the List class.
    - delete(self): Deletes the list and all associated tasks.
    - edit(self, new_title): Edits the title of the list.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    tasks = db.relationship('Task', backref='task_list', remote_side=[id], uselist=True, cascade="all, delete-orphan", single_parent=True)

    def __init__(self, title):
        self.title = title

    def delete(self):
        # Delete all tasks associated with this list
        for task in self.tasks:
            task.delete()
        db.session.delete(self)
        db.session.commit()

    def edit(self, new_title):
        self.title = new_title
        db.session.commit()

    def make_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'tasks': [task.make_dict() for task in self.tasks]
        }

class Task(db.Model):
    """
    Represents a task in a to-do list.

    Attributes:
        id (int): The unique identifier for the task.
        title (str): The title of the task.
        done (bool): Whether the task has been completed or not.
        list_id (int): The ID of the list that the task belongs to.
        task_depth (int): The depth level of the task in the task hierarchy.
        parent_id (int): The ID of the parent task, if this task is a subtask.
        parent_task (Task): The parent task object, if this task is a subtask.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=True)
    task_depth = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('task.id'), default=None)  # Allow null for root tasks
    subtasks = db.relationship('Task', backref=db.backref('parent_task', remote_side=[id]))


    def __init__(self, title, list_id, parent_id=None):
        # if parent_id is not None:
        #     parent_task = Task.query.get(parent_id)
        #     if parent_task and parent_task.task_depth >= 2:
        #         raise ValueError("Cannot create a task at this depth level.")
        #     self.task_depth = parent_task.task_depth + 1 if parent_task else 0

        # else:
        self.parent_id=parent_id
        self.title = title
        self.list_id = list_id
        self.parent_id = parent_id
        self.task_depth = 0
        

    def calculate_depth(self):
        if self.parent_id:
            parent_task = Task.query.get(self.parent_id)
            if parent_task:
                parent_depth = parent_task.task_depth
                if parent_depth < 2:
                    self.task_depth = parent_depth + 1
                    db.session.commit()
                    return True
                else:
                    return False
        return {"message": "Task created successfully"}

    def add_subtask(self, title):
        subtask = Task(title=title, list_id=self.list_id, parent_id=self.id)
        db.session.add(subtask)
        db.session.commit()

    def delete_task_and_subtasks(self):
        def recursive_delete(task):
            if task.subtasks:
                flash('subtasks exist')
                for subtask in task.subtasks:
                    recursive_delete(subtask)
            db.session.delete(task)

        recursive_delete(self)
        db.session.commit()
            


    def edit(self, new_title):
        self.title = new_title
        db.session.commit()

    def mark_as_done(self):
        self.done = True
        db.session.commit()

    def make_dict(self):
        task_dict = {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'parent_id': self.parent_id,
            'task_depth': self.task_depth,
            'list_id': self.list_id,
        }

        
        if self.subtasks:
            if isinstance(self.subtasks, (list, collections.InstrumentedList)):
                task_dict['subtasks'] = [subtask.id for subtask in self.subtasks]
            else:
                # Handle the case when self.subtasks is not a list
                task_dict['subtasks'] = ['nothing here']
        else:
            task_dict['subtasks'] = []

        return task_dict
