from gpiozero import DigitalOutputDevice, Device, DigitalInputDevice
from time import sleep
from gpiozero.pins.mock import MockFactory
from ..config.config import set_config_value
import asyncio
import time

Device.pin_factory = MockFactory()

class MotorController:
  def __init__(self):
    self.drillCoil = None
    self.drillDir = None
    self.drillDepth = 10
    self.drillSleepTime = 0.01
    self.drillDelay = 0.5

    self.coil = []
    self.dir = []
    self.currMotorPosition = [0, 0]
    self.currDir = [0, 0]
    self.millsPerStep = [0.1, 0.1, 0.1]
    self.sleepTime = 0.01
    self.limits = [0, 0]
    self.limitSensors = []

  def setupConfig(self, config):
    self.drillDelay = config["motor"]["drillDelay"]
    self.sleepTime = config["motor"]["sleepTime"]
    self.drillDepth = config["motor"]["drillDepth"]
    self.limits[0] = config["motor"]["limits"]["x"]
    self.limits[1] = config["motor"]["limits"]["y"]
    self.millsPerStep[0] = config["motor"]["millsPerStep"]["x"]
    self.millsPerStep[1] = config["motor"]["millsPerStep"]["y"]
    self.millsPerStep[2] = config["motor"]["millsPerStep"]["z"]
    try:
      self.coil[0].close()
      self.coil[1].close()
      self.dir[0].close()
      self.dir[1].close()
      self.drillCoil.close()
      self.drillDir.close()
      self.limitSensors[0].close()
      self.limitSensors[1].close()
    except:
      pass
    self.coil = [DigitalOutputDevice(config["motor"]["coilPins"]["x"]), DigitalOutputDevice(config["motor"]["coilPins"]["y"])]
    self.dir = [DigitalOutputDevice(config["motor"]["directionPins"]["x"]), DigitalOutputDevice(config["motor"]["directionPins"]["y"])]
    self.drillCoil = DigitalOutputDevice(config["motor"]["coilPins"]["z"])
    self.drillDir = DigitalOutputDevice(config["motor"]["directionPins"]["z"])
    self.limitSensors = [DigitalInputDevice(config["motor"]["limitPins"]["x"]), DigitalInputDevice(config["motor"]["limitPins"]["y"])]
    self.motorInfo("Config loaded")

  def motorInfo(self, error_message):
    print(error_message)

  def step(self, pin):
    pin.on()
    sleep(self.sleepTime)
    pin.off()
    sleep(self.sleepTime)

  def testMotor(self, motorId):
    self.motorInfo("Testing motor")
    for i in range(10):
      self.step(self.coil[motorId])
      self.dir[motorId].on() if i % 2 == 0 else self.dir[motorId].off()

  def isPinBusy(self, pin):
    try:
      pin.on()
      pin.off()
      return False
    except:
      return True

  def isDrillBusy(self):
    return self.isPinBusy(self.drillCoil) or self.isPinBusy(self.drillDir)

  def isMotorBusy(self):
    return self.isPinBusy(self.coil[0]) or self.isPinBusy(self.coil[1])

  def resetMotor(self):
    if self.isMotorBusy():
      self.motorInfo("Motor is busy")
      return
    for c in self.coil:
      c.off()
    for d in self.dir:
      d.off()
    self.currMotorPosition = [0, 0]
    self.motorInfo("Motor reset")

  def moveToPosition(self, motorId, position):
    if self.isMotorBusy():
      self.motorInfo("Motor is busy")
      return
    if position < 0:
      self.motorInfo("Position is less than 0")
      return
    if self.currMotorPosition[motorId] >= (position - self.millsPerStep[motorId]) and self.currMotorPosition[motorId] <= (position + self.millsPerStep[motorId]):
      self.motorInfo("Already at position")
      return
    if self.currMotorPosition[motorId] < position:
      self.dir[motorId].on()
      while self.currMotorPosition[motorId] < position:
        self.step(self.coil[motorId])
        self.currMotorPosition[motorId] += self.millsPerStep[motorId]
    else:
      self.dir[motorId].off()
      while self.currMotorPosition[motorId] > position:
        self.step(self.coil[motorId])
        self.currMotorPosition[motorId] -= self.millsPerStep[motorId]
    self.motorInfo("Moved to position " + str(self.currMotorPosition[motorId]))

  def drillHole(self):
    if self.isDrillBusy():
      self.motorInfo("Drill is busy")
      return
    for i in range(self.drillDepth / self.millsPerStep[2]):
      self.step(self.drillCoil)
    sleep(self.drillDelay)
    self.drillDir.on()
    for i in range(self.drillDepth / self.millsPerStep[2]):
      self.step(self.drillCoil)
    self.motorInfo("Drilled hole")

  def executeRoutine(self, positions):
    for position in positions:
      self.moveToPosition(0, position[0])
      self.moveToPosition(1, position[1])
      self.drillHole()
    self.motorInfo("Routine executed")

  def getMotorInfo(self):
    return {
      "drillDelay": self.drillDelay,
      "millsPerStep": [self.millsPerStep[0], self.millsPerStep[1], self.millsPerStep[2]],
      "sleepTime": self.sleepTime,
      "coilPins": [c.pin.number for c in self.coil],
      "directionPins": [d.pin.number for d in self.dir],
    }

  def calibrateMotor(self):
    currTime = time.time()

    self.motorInfo("Calibrating motors")
    for i in range(2):
      currTime = time.time()
      stepCount = 0
      while not self.limitSensors[i]._active_state == 0 and time.time() - currTime < 10:
        self.step(self.coil[i])
        stepCount += 1

      self.currMotorPosition[i] = 0
      print(stepCount)
      self.millsPerStep[i] = self.limits[i] / stepCount
      self.motorInfo(f"Calibrated motor {['x', 'y'][i]}")

    newMillsPerStep = {
      "x": self.millsPerStep[0],
      "y": self.millsPerStep[1],
      "z": self.millsPerStep[2]
    }
    set_config_value("config.json", "motor.millsPerStep", newMillsPerStep, self)

    # Example usage:
    # asyncio.run(activate_limit_pin_after_time(motor_controller.limitSensors[0], 5))

# Example usage:
# config = {
#     "motor": {
#         "drillDelay": 0.5,
#         "millsPerStep": 0.1,
#         "sleepTime": 0.01,
#         "coilPins": {"0": 17, "1": 18, "2": 27},
#         "directionPins": {"0": 22, "1": 23, "2": 24}
#     }
# }
# motor_controller = MotorController()
# motor_controller.setupConfig(config)
# motor_controller.executeRoutine([(10, 20), (30, 40)])
