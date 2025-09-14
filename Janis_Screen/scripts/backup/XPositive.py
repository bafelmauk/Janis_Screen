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

# Axis to probe
#Axis numbers X=0 Y=1 Z=2 A=3 B=4 C=5
AxisNumber = 0
Axis=Axis.X

AxisDirectionNegative = False

# probe index
ProbeIndex = int(d.getMachineParam( 10 ))

print (ProbeIndex)

# probe diameter
ProbeDiameter = d.getMachineParam( 13 )

# Max probe distance (absolute)
MaxProbeDistance = d.getMachineParam( 15 )

# approach velocity (units/min)
Vel = 15000

# probing speed (units/min)
FastProbeSpeed = d.getMachineParam( 11 )
SlowProbeSpeed = d.getMachineParam( 12 )

# lift up dist before fine probing
RetractDistance = d.getMachineParam( 16 )

# delay (seconds) before fine probing
fineProbingDelay = 0.2

#############################################
###### END SETTINGS
#############################################



#############################################
# Macro START
#############################################
d.setSpindleState(SpindleState.OFF)
# if axis direction is negative

if(AxisDirectionNegative == False):

  # get current absolute position
	pos = d.getPosition(CoordMode.Machine)

  # start fast probing
	pos[AxisNumber] = (pos[AxisNumber]+MaxProbeDistance);
	print (pos)
	probeResult = d.executeProbing(CoordMode.Machine, pos, ProbeIndex, FastProbeSpeed)
	if(probeResult == False):
		sys.exit("fast probing failed!")

  # Retract Axis
	RetractFrom = d.getPosition(CoordMode.Machine)
	RetractFrom[AxisNumber] = (RetractFrom[AxisNumber]-RetractDistance)
	d.moveToPosition( CoordMode.Machine, RetractFrom, Vel )

  # start fine probing
	probeResult = d.executeProbing(CoordMode.Machine, pos, ProbeIndex, SlowProbeSpeed)
	if(probeResult == False):
		sys.exit("slow probing failed!")
  # get fine probe contact position
	probeFinishPos = d.getProbingPosition(CoordMode.Machine)
	print (probeFinishPos)

  # Retract Axis
	RetractFrom[AxisNumber] = (probeFinishPos[AxisNumber]-RetractDistance)
	d.moveToPosition( CoordMode.Machine, RetractFrom, Vel )

  # Set program cordinate Z to zero
	d.setAxisProgPosition( Axis,((RetractDistance+(ProbeDiameter/2))*-1))
	print (((RetractDistance+(ProbeDiameter/2))*-1))

else:
	pos = d.getPosition(CoordMode.Machine)

  # start fast probing
	pos[AxisNumber] = (pos[AxisNumber]-MaxProbeDistance);
	print (pos)
	probeResult = d.executeProbing(CoordMode.Machine, pos, ProbeIndex, FastProbeSpeed)
	if(probeResult == False):
		sys.exit("fast probing failed!")

  # Retract Axis
	RetractFrom = d.getPosition(CoordMode.Machine)
	RetractFrom[AxisNumber] = (RetractFrom[AxisNumber]+RetractDistance)
	d.moveToPosition( CoordMode.Machine, RetractFrom, Vel )

  # start fine probing
	probeResult = d.executeProbing(CoordMode.Machine, pos, ProbeIndex, SlowProbeSpeed)
	if(probeResult == False):
		sys.exit("slow probing failed!")
  # get fine probe contact position
	probeFinishPos = d.getProbingPosition(CoordMode.Machine)
	print (probeFinishPos)

  # Retract Axis
	RetractFrom[AxisNumber] = (probeFinishPos[AxisNumber]+RetractDistance)
	d.moveToPosition( CoordMode.Machine, RetractFrom, Vel )

  # Set program cordinate Z to zero
	d.setAxisProgPosition( Axis,(RetractDistance+(ProbeDiameter/2)))
	print ((RetractDistance+(ProbeDiameter/2)))