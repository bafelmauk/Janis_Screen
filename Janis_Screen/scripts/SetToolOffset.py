#############################################
# CS-Lab s.c.
#
# simCNC sample automatic tool lenght probing macro
#############################################
import sys
import time

#############################################
# BEGIN WARNING BLOCK
# comment this block when you set/check settings below
#############################################
#msg.wrn("Setup probing macro configuration first.\n\nMenu 'Macro->Show Script Editor' and choose 'probing'", "Warning!")
#sys.exit("Error! Probing macro not configured!")
#############################################
# END WARNING BLOCK
#############################################


#############################################
###### BEGIN SETTINGS
#############################################
# probe index
probeIndex = 1
# probing start position [X, Y, Z]
probeStartAbsPos = [977.3, 50.3, 0]
# Axis probing end position (absolute)
EndPosition = -250
# approach velocity (units/min)
vel = 5000
# probing velocity (units/min)
fastProbeVel = 400
slowProbeVel = 50
# lift up dist before fine probing
goUpDist = 3
# delay (seconds) before fine probing
fineProbingDelay = 0.2
#############################################
###### END SETTINGS
#############################################



#############################################
# Macro START
#############################################
d.setSpindleState(SpindleState.OFF)

# get current absolute position
pos = d.getPosition(CoordMode.Machine)

# get current absolute position
pos = d.getPosition(CoordMode.Machine)
# lift up Z to absolute 0
pos[Axis.Z.value] = 0;
d.moveToPosition(CoordMode.Machine, pos, vel)
# go to XY start probe position
pos[Axis.X.value] = probeStartAbsPos[Axis.X.value]
pos[Axis.Y.value] = probeStartAbsPos[Axis.Y.value]
d.moveToPosition(CoordMode.Machine, pos, vel)

# start fast probing
pos[Axis.Z.value] = EndPosition;
probeResult = d.executeProbing(CoordMode.Machine, pos, probeIndex, fastProbeVel)
if(probeResult == False):
  sys.exit("fast probing failed!")
# get fast probe contact position
fastProbeFinishPos = d.getProbingPosition(CoordMode.Machine)

# lift-up Z
d.moveAxisIncremental(Axis.Z, goUpDist, vel)
# delay
time.sleep(fineProbingDelay)
# start fine probing
probeResult = d.executeProbing(CoordMode.Machine, pos, probeIndex, slowProbeVel)
if(probeResult == False):
  sys.exit("slow probing failed!")
# get fine probe contact position
probeFinishPos = d.getProbingPosition(CoordMode.Machine)

# Set program cordinate Z to zero
print ("programm parameeter mis getib: ", d.getProbingPosition(CoordMode.Program)[Axis.Z.value])
print ("masina parameeter mis getib: ", d.getProbingPosition(CoordMode.Machine)[Axis.Z.value])
print ("28parameeter: ", float(d.getMachineParam( 29 )))
offset = (float(d.getMachineParam( 29 ))-(d.getProbingPosition(CoordMode.Machine)[Axis.Z.value]))
d.setMachineParam(29, (d.getMachineParam( 29 ) - offset)) # lisatud et peale esimest mootmist oleks 0 koht ikka õige
print ("offset: ", offset)
UusZ = (d.getPosition(CoordMode.Program)[Axis.Z.value])+offset
#UusZ = 37.557499
print ("uusZ: ", UusZ)
d.setAxisProgPosition( Axis.Z, UusZ)
#gui.MeasureToolOffsetValue.setText( d.getProbingPosition(CoordMode.Program)[Axis.Z.value])
# lift-up Z
pos[Axis.Z.value] = 0;
d.moveToPosition(CoordMode.Machine, pos, vel)
# lift Z to abs 0
#pos[Axis.Z.value] = 0
#d.moveToPosition(CoordMode.Machine, pos, vel)

