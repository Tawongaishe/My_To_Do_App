from . import db

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
    tasks = db.relationship('Task', backref='task_list')

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


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    task_depth = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('task.id'), default=None) 
    subtasks = db.relationship('Task', backref='parent_task', remote_side=[id], uselist=True, cascade="all, delete-orphan", single_parent=True)

    def delete_task_and_subtasks(self):
        # Recursively delete subtasks
        for subtask in self.subtasks:
            subtask.delete_task_and_subtasks()

        # Delete the current task
        db.session.delete(self)
        db.session.commit()


    def edit(self, new_title):
        self.title = new_title
        db.session.commit()

    def mark_as_done(self):
        self.done = True
        db.session.commit()

    def make_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'parent_id': self.parent_id,
            'task_depth': self.task_depth,
            'subtasks': [subtask.make_dict() for subtask in self.subtasks]
        }
