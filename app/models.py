from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import collections
from flask import flash
from flask_login import UserMixin

db = SQLAlchemy()
class Users(UserMixin, db.Model):
    """
    A class representing a user of the To-Do app.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address associated with the user's account.
        password (str): The hashed password for the user's account.
        tasks (list): A list of Task objects associated with the user.
        lists (list): A list of List objects associated with the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)  # Add an email column
    password = db.Column(db.String(250), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    lists = db.relationship('List', backref='user', lazy=True)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

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
        subtasks (list): A list of subtasks for this task.
        user_id (int): The ID of the user who created the task.

    Methods:
        __init__(self, title, list_id, user_id, parent_id=None): Initializes a new Task object.
        calculate_depth(self): Calculates the depth level of the task in the task hierarchy.
        add_subtask(self, title): Adds a new subtask to this task.
        delete_task_and_subtasks(self): Deletes this task and all of its subtasks.
        edit(self, new_title): Edits the title of this task.
        mark_as_done(self): Marks this task as done.
        make_dict(self): Returns a dictionary representation of this task.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=True)
    task_depth = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('task.id'), default=None)  # Allow null for root tasks
    subtasks = db.relationship('Task', backref=db.backref('parent_task', remote_side=[id]))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def __init__(self, title, list_id, user_id, parent_id=None):
        """
        Initializes a new Task object.

        Args:
            title (str): The title of the task.
            list_id (int): The ID of the list that the task belongs to.
            user_id (int): The ID of the user who created the task.
            parent_id (int, optional): The ID of the parent task, if this task is a subtask. Defaults to None.
        """
        self.parent_id=parent_id
        self.title = title
        self.list_id = list_id
        self.parent_id = parent_id
        self.task_depth = 0
        self.user_id = user_id
        

    def calculate_depth(self):
        """
        Calculates the depth level of the task in the task hierarchy.

        Returns:
            bool or dict: Returns True if the task depth was successfully calculated, False if the task depth is too deep, or a dictionary with a message if the parent task does not exist.
        """
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
        """
        Adds a new subtask to this task.

        Args:
            title (str): The title of the subtask.
        """
        subtask = Task(title=title, list_id=self.list_id, parent_id=self.id)
        db.session.add(subtask)
        db.session.commit()

    def delete_task_and_subtasks(self):
        """
        Deletes this task and all of its subtasks.
        """
        def recursive_delete(task):
            if task.subtasks:
                flash('subtasks exist')
                for subtask in task.subtasks:
                    recursive_delete(subtask)
            db.session.delete(task)

        recursive_delete(self)
        db.session.commit()
            


    def edit(self, new_title):
        """
        Edits the title of this task.

        Args:
            new_title (str): The new title for the task.
        """
        self.title = new_title
        db.session.commit()

    def mark_as_done(self):
        """
        Marks this task as done.
        """
        self.done = True
        db.session.commit()

    def make_dict(self):
        """
        Returns a dictionary representation of this task.

        Returns:
            dict: A dictionary representation of this task.
        """
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
                task_dict['subtasks'] = ['nothing here']
        else:
            task_dict['subtasks'] = []

        return task_dict