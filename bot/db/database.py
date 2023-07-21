from sqlalchemy.orm import Session
from .models import User, Tasks, BaseModel
from sqlalchemy import select, create_engine, update, delete
from .base import BaseModel
from dotenv import load_dotenv
import os
from utils import log_action

load_dotenv()

session = None
engine = None


async def start_db():
    global engine
    engine = create_engine(os.getenv("sqlite_url"), echo=True)
    with engine.connect():
        BaseModel.metadata.create_all(bind=engine)

    global session
    session = Session(bind=engine)


async def shutdown_db():
    session.close()
    engine.dispose()


async def add_user(username: str, id: int):
    with session as ses:
        stmt = select(User).where(User.tg_user_id == id)
        user = ses.execute(stmt).all()
        if not user:
            ses.add(User(username=username, tg_user_id=id))
            ses.commit()
            log_action().info("User Added to Database")


async def add_task(title: str, description: str, owner_id):
    with session as ses:
        ses.add(Tasks(title=title, description=description, owner_id=owner_id))
        ses.commit()
        log_action().info("Task Added to Database")


async def get_tasks(id):
    with session as ses:
        stmt = select(Tasks).where(Tasks.owner_id == id)
        tasks = ses.execute(stmt).scalars().all()

        return tasks


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
        log_action().info("Task's Status changed to done")
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
        log_action().info("Task Was deleted from Database")
        return True
