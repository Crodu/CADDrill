from typing import Union
from fastapi import FastAPI, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from .infrastructure.database import get_db
from .application.planService import PlanService
from .infrastructure.planRepository import PlanRepository
# from .application.userService import UserService
# from .application.tweetService import TweetService
# from .infrastructure.userRepository import UserRepository
# from .infrastructure.tweetRepository import TweetRepository
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/plans/add")
def create_plan(name: str = Form(...), hole_diameter: float = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    # print(name)
    # print(hole_diameter)
    # print(file)
    plan_service = PlanService(PlanRepository(db))
    return plan_service.create_plan({"name": name, "hole_diameter": hole_diameter}, file)

# @app.post("/plans/add")
# def create_user(plan_data: dict, db: Session = Depends(get_db)):
#     print(plan_data)
#     user_service = PlanService(PlanRepository(db))
#     return user_service.create_user(plan_data)

@app.get("/plans/{plan_id}")
def get_plan(plan_id: int, q: Union[str, None] = None, db: Session = Depends(get_db)):
    plan_service = PlanService(PlanRepository(db))
    plan_info = plan_service.get_plan(plan_id, q)
    return {"payload": plan_info, "item_id": plan_id, "q": q}

@app.get("/plans")
def get_plans(q: Union[str, None] = None, db: Session = Depends(get_db)):
    plan_service = PlanService(PlanRepository(db))
    plan_info = plan_service.get_all_plans(q)
    return {"payload": plan_info, "q": q}
