# api.py
from dataclasses import dataclass, field
from typing import Optional, Union
import  tasks_tiny_db

def normalize_tags(value: Union[str, list[str], None]) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [v.strip() for v in value.split(',') if v.strip()]
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return value
    raise TypeError('tags must be a string, list of strings or None')


@dataclass
class Task:
    title: Optional[str] = None
    descr: Optional[str] = None
    tags: Union[str ,list[str]] = field(default_factory=list, repr=False)
    done: bool = False
    task_id: Optional[int] = None

    def __post_init__(self):
        self.tags = normalize_tags(self.tags)


    def as_dict(self):
        dict_tasks ={
            'title': self.title,
            'descr': self.descr,
            'tags': self.tags,
            'done': self.done,
            'task_id': self.task_id
        }
        return dict_tasks

class TaskException(Exception):
    """Task error has occurred"""
class UninitializedDatabase(TaskException):
    """Call connect_tiny_db before other functions"""

def add(task: Task)-> int:
    if not isinstance(task, Task):
        raise TypeError('task must be Task object')
    if not isinstance(task.title, str):
        raise ValueError('title must be string')
    if not ((task.descr is None) or isinstance(task.descr, str)):
        raise ValueError('description must be string or None')
    if not (task.tags is None or (isinstance(task.tags, list) and all(isinstance(tag, str) for tag in task.tags))):
        raise ValueError('tags must be None or a list of strings')
    if not isinstance(task.done, bool):
        raise ValueError('done must be True or False')
    if task.task_id is not None:
        raise ValueError('id must be None')
    if _tasks_db is None:
        raise UninitializedDatabase()
    task_id = _tasks_db.add(task.as_dict())
    return task_id

def update(task_id: int, updates: dict):
    if not isinstance(task_id, int):
        raise TypeError('task_id must be integer')
    if not isinstance(updates, dict):
        raise TypeError('updates must be dictionary')
    if _tasks_db is None:
        raise UninitializedDatabase()
    _tasks_db.update(task_id, updates)

def get(task_id: int)-> Task:
    if not isinstance(task_id, int):
        raise TypeError('task_id must be integer')
    if _tasks_db is None:
        raise UninitializedDatabase()
    task_dict = _tasks_db.get(task_id)
    return Task(**task_dict)


def get_list(tags=None)-> list[Task]:
    if tags and not  isinstance(tags, Union[str, list]):
        raise TypeError('tags must be string or list of strings')
    if _tasks_db is None:
        raise UninitializedDatabase()
    return [Task(**t) for t in _tasks_db.get_list(tags)]

def delete(task_id: int):
    if not isinstance(task_id, int):
        raise TypeError('task_id must be integer')
    if _tasks_db is None:
        raise UninitializedDatabase
    _tasks_db.delete(task_id)

def delete_all(tags=None):
    if tags and not  isinstance(tags, Union[str, list]):
        raise TypeError('tags must be string or list of strings')
    if _tasks_db is None:
        UninitializedDatabase()
    _tasks_db.delete_all(tags)


_tasks_db: Optional[tasks_tiny_db.TasksTinyDB] = None

def start_tiny_db():
    global _tasks_db
    _tasks_db = tasks_tiny_db.start_tiny_db()

def stop_tiny_db():
    global _tasks_db
    _tasks_db.stop_tiny_db()

