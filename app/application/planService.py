from ..domain.plan import Plan
from ..infrastructure.planRepository import PlanRepository
from ..utils.findholes import DXFProcessor


class PlanService:
    def __init__(self, plan_repository: PlanRepository):
        self.plan_repository = plan_repository

    def create_plan(self, user_data: dict, file) -> Plan:
        dxfFile = DXFProcessor(file.filename)
        points = str(list(dxfFile.process_points()))
        print(dxfFile.process_rectangles())
        print(points)
        user_data["hole_coords"] = points
        user_data["size_x"] = dxfFile.process_rectangles()[0]
        user_data["size_y"] = dxfFile.process_rectangles()[1]
        return self.plan_repository.save(user_data)
    
    def get_plan(self, plan_id: int, q: str) -> Plan:
        return self.plan_repository.get(plan_id, q)
    
    def get_all_plans(self, q: str) -> Plan:
        return self.plan_repository.get_all(q)
    
    # def update_plan(self, user_data: dict, user_id:int) -> User:
    #     return self.plan_repository.update(user_data, user_id)

    # Additional methods for user management
