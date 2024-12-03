.data
# Screen info
screenStart: 16384    # 0x4000
screenEnd: 24576      # 0x6000
colorRed: 63488 
colorGreen: 2016
colorBlue: 31

# Keyboard info
keyboardMem: 24576
upArrow: 38
downArrow: 40
wKey: 87
sKey: 83
spaceKey: 32

.text
j main

main:
    lw R1, screenStart    # Screen start address
    lw R2, screenEnd      # Screen end address
    lw R3, colorRed       # Initial color (red)

makeScreenRed:
    # Draw pixel to current address
    sw R3, 0(R1)
    addi R1, R1, 1        # Move to next address
    display
    
    # Check if we've reached the end of the screen
    beq R1, R2, drawEnd

    j makeScreenRed

drawEnd:
    lw R4, keyboardMem    # Load keyboard memory value
    lw R4, 0(R4)
    lw R5, sKey           # Load "S" key value
    bne R4, R5, drawEnd               # Restart the main loop
    


setBlue:
    lw R1, screenStart
    lw R3, colorBlue      # Change current color to blue
    sw R3, 0(R1)
    display
     