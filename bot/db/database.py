from .base import BaseModel
from .engine import create_async_engine,get_session_maker,proceed_schemas
from dotenv import load_dotenv
import os
load_dotenv()
from sqlalchemy import select, create_engine, update
from .models import User,Tasks,BaseModel
from sqlalchemy.orm import Session

session = None

async def start_db():
    engine = create_engine(os.getenv("sqlite_url"),echo=True)
    with engine.connect() as conn:
        BaseModel.metadata.create_all(bind = engine)

    global session 
    session = Session(bind=engine)

async def add_user(username: str, id: int):
    with session as ses:
        stmt = select(User).where(User.tg_user_id == id)
        user = ses.execute(stmt).all()
        print(user)
        if not user:
            ses.add(User(username = username,tg_user_id = id))
            ses.commit()

async def add_task(title: str, description: str,owner_id):
    with session as ses:
        ses.add(Tasks(title = title,description = description,owner_id = owner_id))
        ses.commit()
    
async def get_tasks(id):
    print(id)
    with session as ses:
        stmt = select(Tasks).where(Tasks.owner_id == id)
        tasks = ses.execute(stmt).scalars().all()
        text = ""
        counter = 1
        for task in tasks:
            status = "🔘"
            if task.status:
                status = "✅"
            task_desc = f"{counter}) {task.title} - {task.description} ({task.id}) {status}\n"
            text += task_desc
            print(task_desc)

        return text
    
async def change_task_status(task_id):
    with session as ses:
        stmt = update(Tasks).where(Tasks.id == task_id).values(status = True)
        ses.execute(stmt)
        ses.commit()