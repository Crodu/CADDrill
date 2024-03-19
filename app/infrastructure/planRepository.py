from ..domain.models import Plan
from sqlalchemy.orm import Session


class PlanRepository:
    def __init__(self, db_session: Session = None):
        self.db = db_session or SessionLocal()

    def save(self, plan_data: dict) -> Plan:
        db_plan = Plan(**plan_data)
        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan
    
    def get(self, plan_id: int, q: str) -> Plan:
        plan = self.db.query(Plan).filter(Plan.id == plan_id).first()
        return plan
    
    def get_all(self, q: str) -> Plan:
        plans = self.db.query(Plan).all()
        return plans
    
    # def update(self, user_data: dict, user_id: int) -> User:
    #     user = self.db.query(User).filter(User.id == user_id).first()
    #     if user:
    #         for var, value in user_data.items():
    #             setattr(user, var, value)
    #         self.db.commit()
    #         self.db.refresh(user)
    #         return user
    #     return None # type: ignore
        
