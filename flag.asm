.data
# Screen info
screenStart: 16384    # 0x4000
screenEnd: 24576      # 0x6000
rowShift: 128 #how many pixels in a width of the screen

#colors
colorRed: 63488 
colorGreen: 2016
colorBlue: 31
colorWhite: 65535 
colorBlack: 0
colorYellow: 65504   

# Keyboard info
keyboardMem: 24576
upArrow: 38
downArrow: 40
leftArrow: 37
rightArrow: 39
#spaceKey: 32

.text
j main

main:
    lw R1, screenStart    # Screen start address
    lw R2, screenEnd      # Screen end address
    lw R3, colorRed       # Initial color (red)

checkKeyInput:
    lw R4, keyboardMem    # Load keyboard memory value
    lw R4, 0(R4)
    lw R5, upArrow  
    beq R4, R5, upArrowPressed
    lw R5, downArrow  
    beq R4, R5, downArrowPressed
    lw R5, rightArrow  
    beq R4, R5, rightArrowPressed
    lw R5, leftArrow  
    beq R4, R5, leftArrowPressed
    j checkKeyInput



leftArrowPressed:
    lw R3, colorRed  
    sw R3, 0(R1)    
    addi R1, R1, -1
    display
    j checkKeyInput


rightArrowPressed:
    lw R3, colorGreen 
    sw R3, 0(R1)
    addi R1, R1, 1
    display
    j checkKeyInput

downArrowPressed:
    lw R3, colorBlack  
    sw R3, 0(R1)
    addi R1, R1, 128 #(the row shift)
    display
    j checkKeyInput

upArrowPressed:
    lw R3, colorYellow     
    sw R3, 0(R1)
    addi R1, R1, -128
    display
    j checkKeyInput