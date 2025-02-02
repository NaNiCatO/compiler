LD R0 #23
LD R1 #8
ADD.i R2 23 8
ST @print R2

LD R3 #2.5
LD R4 #0
MUL.i R5 2.5 0
ST @print R5

ERROR

LD R6 #5
ST @x 5

LD R7 #10
LD R8 #@x
MUL.i R9 10 x
ST @print R9

ERROR

LD R10 #2
LD R11 #5
ADD.i R12 2 5
ST @print R12

LD R0 #0 // load 0, list x[2] we should set x[0] and x[1] to 0
LD R1 @x // load base address of x
LD R2 #0 // load offset 0
LD R3 #4 // size = 4 bytes
MUL.i R4 R2 R3 // offset * size
ADD.i R5 R1 R4 // x[0] address
ST R5 R0 // x[0] = 0
LD R2 #1
LD R3 #4
MUL.i R4 R2 R3
ADD.i R5 R1 R4 // x[1] address
ST R5 R0 // x[1] = 0

LD R0 @x
LD R1 #0
LD R2 #4
MUL.i R3 R1 R2
ADD.i R4 R0 R3
ST $print R4 // print x[0]

LD R0 @x
LD R1 #1
LD R2 #4
MUL.i R3 R1 R2
ADD.i R4 R0 R3
ST $print R4 // print x[1]

ADD.i R13 ((x[(0)])) ((x[(1)]))
ST @print R13

LD R14 #30
LD R15 #30
ST @print R15

LD R16 #45
LD R17 #45
ST @print R17

LD R18 #60
LD R19 #60
ST @print R19

LD R20 #30
LD R21 #30
ST @print R21

ST @x (sin(30))
LD R22 #45
LD R23 #45
ST @print R23

ST @y (cos(45))
LD R24 #60
LD R25 #60
ST @print R25

ST @z (tan(60))
LD R26 #@x
LD R27 #@y
LD R28 #@z
SUB.i R29 y z
ST @print R29

ADD.i R30 x (y-z)
ST @print R30

ST @result (x+(y-z))
LD R0 #0 // load 0, list w[3] we should set w[0] and w[1] to 0
LD R1 @w // load base address of w
LD R2 #0 // load offset 0
LD R3 #4 // size = 4 bytes
MUL.i R4 R2 R3 // offset * size
ADD.i R5 R1 R4 // w[0] address
ST R5 R0 // w[0] = 0
LD R2 #1
LD R3 #4
MUL.i R4 R2 R3
ADD.i R5 R1 R4 // w[1] address
ST R5 R0 // w[1] = 0

ERROR

ERROR

ERROR

LD R0 @w
LD R1 #0
LD R2 #4
MUL.i R3 R1 R2
ADD.i R4 R0 R3
ST $print R4 // print w[0]

LD R0 @w
LD R1 #1
LD R2 #4
MUL.i R3 R1 R2
ADD.i R4 R0 R3
ST $print R4 // print w[1]

LD R0 @w
LD R1 #2
LD R2 #4
MUL.i R3 R1 R2
ADD.i R4 R0 R3
ST $print R4 // print w[2]

ADD.i R31 ((w[(1)])) ((w[(2)]))
ST @print R31

ADD.i R32 ((w[(0)])) (((w[(1)]))+((w[(2)])))
ST @print R32

ERROR

