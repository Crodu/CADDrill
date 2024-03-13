class Drill:
  def __init__(self):
    self.drilling = False

  def drill(self):
    self.drilling = True
    print("Drilling...")

  def stop(self):
    self.drilling = False