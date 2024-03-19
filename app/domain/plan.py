class Plan:
    def __init__(self, name: str, size_x: float, size_y: float, hole_diameter: int, hole_coords: str, id: int = None):
        self.id = id
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.hole_diameter = hole_diameter
        self.hole_coords = hole_coords
