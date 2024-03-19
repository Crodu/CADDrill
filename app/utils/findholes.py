import ezdxf
import Motor
import Drill
import time

class DXFProcessor:
  def __init__(self, file_name):
    self.doc = ezdxf.readfile(file_name)
    self.modelspace = self.doc.modelspace()
    self.rectangles = [entity for entity in self.modelspace.query('LWPOLYLINE') if len(entity) == 4]

  def process_rectangles(self):
    for rectangle in self.rectangles:
      points = rectangle.get_points()
      width = abs(points[0][0] - points[1][0])
      height = abs(points[0][1] - points[3][1])
      return width, height

  def process_points(self):
    return ([point.dxf.location[0], point.dxf.location[1]] for point in self.modelspace.query('POINT'))