from gpiozero import DigitalOutputDevice
from time import sleep

drillCoil = DigitalOutputDevice(18)
drillDir = DigitalOutputDevice(25)
drillDepth = 10
drillSleepTime = 0.01
drillDelay = 0.5

coil = [DigitalOutputDevice(14), DigitalOutputDevice(15)]
dir = [DigitalOutputDevice(23), DigitalOutputDevice(24)]
currMotorPosition = [0, 0]
currDir = [0, 0]
millsPerStep = 0.1
sleepTime = 0.01

def motorInfo(error_message):
  print(error_message)

def step(pin):
  pin.on()
  sleep(sleepTime)
  pin.off()
  sleep(sleepTime)


def testMotor(motorId):
  motorInfo("Testing motor")
  for i in range(10):
          step(coil[motorId])
          dir.on() if i % 2 == 0 else dir.off()

def isPinBusy(pin):
  try:
    pin.on()
    pin.off()
    return False
  except:
    return True
  
def isDrillBusy():
  return isPinBusy(drillCoil) or isPinBusy(drillDir)
  
def isMotorBusy():
  return isPinBusy(coil[0]) or isPinBusy(coil[1])

def resetMotor():
  if isMotorBusy():
    motorInfo("Motor is busy")
    return
  coil.off()
  dir.off()
  currMotorPosition = [0, 0]
  motorInfo("Motor reset")

def moveToPosition(motorId, position):
  #check if motor is busy
  if isMotorBusy():
    motorInfo("Motor is busy")
    return
  if position < 0:
    motorInfo("Position is less than 0")
    return
  if currMotorPosition[motorId] == position:
    motorInfo("Already at position")
    return
  if currMotorPosition[motorId] < position:
    dir[motorId].on()
    while currMotorPosition[motorId] < position:
      step(coil[motorId])
      currMotorPosition[motorId] += millsPerStep
  else:
    dir[motorId].off()
    while currMotorPosition[motorId] > position:
      step(coil[motorId])
      currMotorPosition[motorId] -= millsPerStep
  motorInfo("Moved to position" + str(currMotorPosition[motorId]))

def drillHole():
  if isDrillBusy():
    motorInfo("Drill is busy")
    return
  for i in range(drillDepth):
    step(drillCoil)
  sleep(drillDelay)
  drillDir.on()
  for i in range(drillDepth):
    step(drillCoil)
  
  motorInfo("Drilled hole")

def executeRoutine(positions):
  for position in positions:
    moveToPosition(0, position[0])
    moveToPosition(1, position[1])
    drillHole()
  motorInfo("Routine executed")

