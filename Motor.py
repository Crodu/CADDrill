class Motor:
  def __init__(self, min_position, max_position):
    self.position = min_position
    self.min_position = min_position
    self.max_position = max_position

  def move_to_position(self, pos):
    if pos < self.min_position:
      print(f"Input {pos} is less than minimum position {self.min_position}. Moving to minimum position.")
      self.position = self.min_position
    elif pos > self.max_position:
      print(f"Input {pos} is greater than maximum position {self.max_position}. Moving to maximum position.")
      self.position = self.max_position
    else:
      print(f"Moving to position {pos}.")
      self.position = pos

    print(f"Current position: {self.position}")


# Create a motor with min position 0 and max position 100
motor = Motor(0, 100)

# Move motor based on x parameter
x = 50
motor.move_to_position(x)