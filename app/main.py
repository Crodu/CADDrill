import json
from .config.config import load_config, replace_config
from typing import Union
from fastapi import FastAPI, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from .infrastructure.database import get_db
from .application.planService import PlanService
from .infrastructure.planRepository import PlanRepository
from fastapi.middleware.cors import CORSMiddleware
from .utils.motorUtils import MotorController
import multiprocessing
from contextlib import asynccontextmanager

# app = FastAPI()

motor_controller = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    motor_controller = MotorController()
    app.state.motor_controller = motor_controller
    app.state.motor_controller.setupConfig(load_config())

    yield
    

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://192.168.0.105:3000",
    "http://192.168.0.105",
    "http://driller.local:3000",
    "http://driller.local",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/plans/add")
async def create_plan(name: str = Form(...), hole_diameter: float = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    # print(name)
    # print(hole_diameter)
    # print(file)
    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    plan_service = PlanService(PlanRepository(db))
    return plan_service.create_plan({"name": name, "hole_diameter": hole_diameter}, file)

@app.get("/plans/run/{plan_id}")
def run_plan(plan_id: int, q: Union[str, None] = None, db: Session = Depends(get_db)):
    plan_service = PlanService(PlanRepository(db))
    plan_info = plan_service.get_plan(plan_id, q)
    print(app.state.motor_controller.currMotorPosition)
    app.state.motor_controller.executeRoutine(json.loads(plan_info.hole_coords))
    return {"payload": plan_info, "item_id": plan_id, "q": q}

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

@app.get("/config")
def get_config():
    loaded_config = load_config()
    return {"payload": loaded_config}

@app.post("/config")
def update_config(new_config: dict):
    replace_config("config.json", new_config, app.state.motor_controller)
    return {"payload": new_config}

@app.get("/calibrateMotor")
def calibrate_motor():
    app.state.motor_controller.calibrateMotor()
    return {"payload": app.state.motor_controller.getMotorInfo()}

@app.get("/getMotorInfo")
def get_motor_info():
    return {"payload": app.state.motor_controller.getMotorInfo()}