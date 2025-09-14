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
AxisNumber1 = 2
AxisNumber2 = 0
AxisNumber3 = 1

#Axis probe Direction 0=Negative 1=positive
Direction1 = 0
Direction2 = 0
Direction3 = 1

# probe index
ProbeIndex = int(d.getMachineParam( 10 ))

#print (ProbeIndex)

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

#############################################
###### END SETTINGS
#############################################

#paneb last tool offseti probe omaks kuna probe on otsas ja moodab materjali 0 kohta
d.setMachineParam( 29, d.getMachineParam( 28 ))


#############################################
# Macro START
#############################################
d.setSpindleState(SpindleState.OFF)
# if axis direction is negative

def Probing(AxisNumber, Direction):
	pos = d.getPosition(CoordMode.Machine)

  # start fast probing
	if(Direction == 0):
		pos[AxisNumber] = (pos[AxisNumber]-MaxProbeDistance)
	elif(Direction == 1):
		pos[AxisNumber] = (pos[AxisNumber]+MaxProbeDistance)
	print ("1")

	probeResult = d.executeProbing(CoordMode.Machine, pos, ProbeIndex, FastProbeSpeed)
	if(probeResult == False):
		sys.exit("fast probing failed!")
	print ("2")

  # Retract Axis
	RetractFrom = d.getPosition(CoordMode.Machine)
	if(Direction == 0):
		RetractFrom[AxisNumber] = (RetractFrom[AxisNumber]+RetractDistance)
	elif(Direction == 1):
		RetractFrom[AxisNumber] = (RetractFrom[AxisNumber]-RetractDistance)
	print ("3")

	d.moveToPosition( CoordMode.Machine, RetractFrom, Vel )
	print ("4")

  # start fine probing
	probeResult = d.executeProbing(CoordMode.Machine, pos, ProbeIndex, SlowProbeSpeed)
	if(probeResult == False):
		sys.exit("slow probing failed!")
  # get fine probe contact position
	probeFinishPos = d.getProbingPosition(CoordMode.Machine)
	print ("5")


  # Retract Axis
	if(Direction == 0):
		RetractFrom[AxisNumber] = (probeFinishPos[AxisNumber]+RetractDistance)
	elif(Direction == 1):
		RetractFrom[AxisNumber] = (probeFinishPos[AxisNumber]-RetractDistance)
	print ("6")
	
	d.moveToPosition( CoordMode.Machine, RetractFrom, Vel )
	print ("7")
	if(AxisNumber == 0):
		axis = Axis.X
	elif(AxisNumber == 1):
		axis = Axis.Y
	elif(AxisNumber == 2):
		axis = Axis.Z
	elif(AxisNumber == 3):
		axis = Axis.A
	elif(AxisNumber == 4):
		axis = Axis.B
	elif(AxisNumber == 5):
		axis = Axis.C
	print ("8")
	print (str(axis))

  # Set program cordinate Z to zero
	if(Direction == 0):
		if(AxisNumber == 2):
			d.setAxisProgPosition( axis,(RetractDistance))
		else:
			d.setAxisProgPosition( axis,(RetractDistance+(ProbeDiameter/2)))
	elif(Direction == 1):
		if(AxisNumber == 2):
			d.setAxisProgPosition( axis,((RetractDistance)*-1))
		else:
			d.setAxisProgPosition( axis,((RetractDistance+(ProbeDiameter/2))*-1))

#probe first axis
Probing(AxisNumber1, Direction1)

# get safe start position
SafeStart = d.getPosition(CoordMode.Machine)

#Movment to second axis probe start position'
#Move axis-X
if(Direction2 == 0):
	d.moveAxisIncremental( Axis.X, (MaxProbeDistance-RetractDistance), Vel )
elif(Direction2 == 1):
	d.moveAxisIncremental( Axis.X, ((MaxProbeDistance-RetractDistance)*-1), Vel )

#Move axis-Z Down
d.moveAxisIncremental( Axis.Z, ((ProbeDiameter*2+RetractDistance)*-1), Vel )

#probe second axis
Probing(AxisNumber2, Direction2)

#Move axis-Z Up
d.moveAxisIncremental( Axis.Z, (ProbeDiameter*2+RetractDistance), Vel )

#Movment to third axis probe start position'
d.moveToPosition( CoordMode.Machine, SafeStart, Vel )
#Move axis-X
if(Direction3 == 0):
	d.moveAxisIncremental( Axis.Y, (MaxProbeDistance-RetractDistance), Vel )
elif(Direction3 == 1):
	d.moveAxisIncremental( Axis.Y, ((MaxProbeDistance-RetractDistance)*-1), Vel )

#Move axis-Z Down
d.moveAxisIncremental( Axis.Z, ((ProbeDiameter*2+RetractDistance)*-1), Vel )

#probe third axis
Probing(AxisNumber3, Direction3)

#Move axis-Z Up
d.moveAxisIncremental( Axis.Z, (ProbeDiameter*2+RetractDistance), Vel )

#Move XY to 0
pos = d.getPosition(CoordMode.Program)
pos[0]=0
pos[1]=0
d.moveToPosition( CoordMode.Program, pos, Vel )
