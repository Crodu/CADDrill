import ezdxf
import Motor
import Drill
import time

# Load the DXF document.
doc = ezdxf.readfile("holes.dxf")

# Get the modelspace which contains all entities of the DXF document.
modelspace = doc.modelspace()

# Find all rectangles (LWPOLYLINE entities with 4 points) in the modelspace.
rectangles = [entity for entity in modelspace.query('LWPOLYLINE') if len(entity) == 4]

# Iterate over all rectangles.
for rectangle in rectangles:
  # Get the points of the rectangle.
  points = rectangle.get_points()

  # Calculate the width and height of the rectangle.
  width = abs(points[0][0] - points[1][0])
  height = abs(points[0][1] - points[3][1])

  print(f"Rectangle width: {width}, height: {height}")

# Iterate over all points in the modelspace.
for point in modelspace.query('POINT'):
  print(point.dxf.location)
  # Declare two motors
  motor_x = Motor.Motor(0,2000)
  motor_y = Motor.Motor(0,2000)
  drill = Drill.Drill()

  # Move the motors to the x and y positions
  motor_x.move_to_position(point.dxf.location[0])
  motor_y.move_to_position(point.dxf.location[1])
  drill.drill()
  time.sleep(2)
  drill.stop()