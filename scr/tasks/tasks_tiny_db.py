# tasks_tyny_db.py
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

class TasksTinyDB:
    def __init__(self, use_memory: bool = False, storage_path: str = './tasks_tiny_db.json'):
        self._db_instance = TinyDB(storage=MemoryStorage() if use_memory else storage_path)
        self._db = self._db_instance.table('task')

    def add(self, task):
        task_id = self._db.insert(task)
        task['task_id'] = task_id
        self._db.update(task, doc_ids=[task_id])
        return task_id

    def update(self, task_id, updates):
        self._db.update(updates, doc_ids=[task_id])

    def get(self, task_id):
        return self._db.get(doc_id=task_id)

    def get_list(self, tags=None):
        if tags is None:
            return self._db.all()
        return self._db.search(Query().tags.any(tags))

    def delete(self, task_id):
        self._db.remove(doc_ids=[task_id])

    def delete_all(self, tags=None):
        if tags is None:
            self._db.truncate()
        else:
            self._db.remove(Query().tags.any(tags))

    def stop_tiny_db(self):
        self._db_instance.close()

def start_tiny_db():
    return TasksTinyDB()




