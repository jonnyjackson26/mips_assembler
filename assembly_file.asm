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
spaceKey: 32

.text
j main

main:
    lw R1, screenStart    # Screen start address
    lw R2, screenEnd      # Screen end address
    lw R3, colorRed       # Initial color (red)

checkKeyInput:
    lw R4, keyboardMem    # Load keyboard memory value
    lw R4, 0(R4)
    lw R5, rightArrow  
    beq R4, R5, rightArrowPressed
    lw R5, leftArrow  
    beq R4, R5, leftArrowPressed
    lw R5, spaceKey  
    beq R4, R5, spacePressed
    j checkKeyInput



leftArrowPressed:
    lw R3, colorRed  
    sw R3, 0(R1)    
    lw R7, screenStart    #this and the next 2 lines make sure u dont go off the screen 
    slt R2, R1, R7
    bne R2, R0, checkKeyInput
    addi R1, R1, -1
    display
    j checkKeyInput


rightArrowPressed:
    lw R3, colorGreen 
    sw R3, 0(R1)
    lw R7, screenEnd    #this and the next 2 lines make sure u dont go off the screen 
    slt R2, R1, R7
    beq R2, R0, checkKeyInput
    addi R1, R1, 1
    display
    j checkKeyInput

#R1 holds the value for where the cursor is. screenStart: 16384, screenEnd: 24576 
#13,904 total pixels in this screen. 
#the goal is to getclosest to 6954, but well say 
# 7400> X > 6600 is a succses of cutting the screen in half.
#if R1 is greater than 6600 and less than 7400,
        #set R6 to 1
spacePressed:
    addi R7, R0, 100      
    slt R2, R7, R1    
    beq R2, R0, endSpaceCheck 

    addi R7, R0, 1000       
    slt R2, R1, R7    
    beq R2, R0, endSpaceCheck  

    addi R6, R0, 1    

endSpaceCheck:
    j checkKeyInput   