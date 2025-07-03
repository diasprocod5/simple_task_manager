# cli.py
from typing import Optional
import typer
from contextlib import contextmanager
import api
from api import Task


def format_str():
    formatstr = "{: >4} {: >20} {: >6} {: <40} {}"
    print(formatstr.format("ID", "title", "done", " description", " tags"))
    print(formatstr.format("--", "-----", "----", " -----------", " ----"))
    return formatstr

app = typer.Typer()

@app.command()
def add(
        title: str = typer.Option(None, "--title","-t", help="Название задачи"),
        descr: str = typer.Option(None, "--descr", '-d',help="Описание задачи"),
        tags: str = typer.Option(None, "--tags","-g", help="Метки")
):
    with _db_session():
        task_id = api.add(Task(title=title, descr=descr, tags=tags))

@app.command()
def get(task_id: int = typer.Argument(..., help="ID задачи")):
    with _db_session():
        task = api.get(task_id)
    form_str = format_str()
    typer.echo(form_str.format(task.task_id, task.title or "", "✔  " if task.done else "❌  ",task.descr or "",
                               ",".join(task.tags) if task.tags else ""))


@app.command()
def update(
        task_id: int = typer.Argument(..., help="ID задачи"),
        title: Optional[str] = typer.Option(None, "--title", "-t", help="Изменить заголовок"),
        descr: Optional[str] = typer.Option(None, "--descr", "-d", help="Изменить описание"),
        tags: Optional[str] = typer.Option(None, "--tags", "-g", help="Изменить метки"),
        done: Optional[bool] = typer.Option(None,"--done/--no-done", "-x/-f",
            help="Статус задачи (--done / -x = Выполнена, --no-done / -f = В процессе)")
):
    update_data = {}

    if title is not None:
        update_data["title"] = title
    if descr is not None:
        update_data["descr"] = descr
    if tags is not None:
        update_data["tags"] = tags
    if done is not None:
        update_data["done"] = done


    if not update_data:
        typer.echo("⚠️  Нет данных для обновления.")
        raise typer.Exit()
    else:
        with _db_session():
            api.update(task_id, update_data)

@app.command()
def get_list(tags: str = typer.Argument(None, help='Поиск по тегам ')):
    with _db_session():
        tasks_list = api.get_list(tags)
    if not tasks_list:
        typer.echo("⚠️  Нет задач.")
        raise typer.Exit()
    form_str = format_str()
    for t in tasks_list:
        typer.echo(form_str.format(
            t.task_id,
            t.title or "",
            "✔️  " if t.done else "❌  ",
            t.descr or "",
            ",".join(t.tags) if t.tags else ""
        ))

@app.command()
def delete(task_id: int = typer.Argument(..., help='ID задачи')):
    with _db_session():
        api.delete(task_id)
@app.command()
def delete_all(tags: str = typer.Argument(None, help='Удаление по тегам')):
    with _db_session():
        api.delete_all(tags)





@contextmanager
def _db_session():
    api.start_tiny_db()
    try:
        yield
    finally:
        api.stop_tiny_db()


if __name__=='__main__':
    app()