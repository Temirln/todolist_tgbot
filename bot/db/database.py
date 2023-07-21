from .base import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
from sqlalchemy import select, create_engine, update, delete
from .models import User, Tasks, BaseModel
from sqlalchemy.orm import Session

session = None


async def start_db():
    engine = create_engine(os.getenv("sqlite_url"), echo=True)
    with engine.connect() as conn:
        BaseModel.metadata.create_all(bind=engine)

    global session
    session = Session(bind=engine)


async def add_user(username: str, id: int):
    with session as ses:
        stmt = select(User).where(User.tg_user_id == id)
        user = ses.execute(stmt).all()
        print(user)
        if not user:
            ses.add(User(username=username, tg_user_id=id))
            ses.commit()


async def add_task(title: str, description: str, owner_id):
    with session as ses:
        ses.add(Tasks(title=title, description=description, owner_id=owner_id))
        ses.commit()


async def get_tasks(id):
    print(id)
    with session as ses:
        stmt = select(Tasks).where(Tasks.owner_id == id)
        tasks = ses.execute(stmt).scalars().all()
        if len(tasks) == 0:
            return "Ваш Список дел Пуст"
        text = ""
        counter = 1
        for task in tasks:
            status = "🔘"
            if task.status:
                status = "✅"
            task_desc = (
                f"{counter}) {task.title} - {task.description} ({task.id}) {status}\n"
            )
            text += task_desc
            print(task_desc)

        return text


async def change_task_status(task_id, owner_id):
    with session as ses:
        stmt = (
            update(Tasks)
            .where(Tasks.id == task_id)
            .where(Tasks.owner_id == owner_id)
            .values(status=True)
        )
        result = ses.execute(stmt)
        if result.rowcount == 0:
            return False
        ses.commit()
        return True


async def delete_task_from_db(task_id, owner_id):
    with session as ses:
        stmt = (
            delete(Tasks).where(Tasks.id == task_id).where(Tasks.owner_id == owner_id)
        )
        result = ses.execute(stmt)
        if result.rowcount == 0:
            return False
        ses.commit()
        return True
