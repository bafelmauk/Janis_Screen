X = 0
Y = 1
Z = 2

PosX = d.getMachineParam( 36 )
PosY = d.getMachineParam( 37 )
PosZ = d.getMachineParam( 38 )

pos = d.getPosition(CoordMode.Machine)

pos[Z] = PosZ
d.moveToPosition( CoordMode.Machine, pos, 15000 )

pos[X] = PosX
pos[Y] = PosY
d.moveToPosition( CoordMode.Machine, pos, 15000 )
