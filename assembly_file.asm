#USERS MANUAL:
#CONTROL WITH UP DOWN LEFT AND RIGHT ARROW KEYS
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

checkKeyInput:
    lw R4, keyboardMem    # Load keyboard memory value
    lw R4, 0(R4)
    lw R5, rightArrow  
    beq R4, R5, rightArrowPressed
    lw R5, leftArrow  
    beq R4, R5, leftArrowPressed
    lw R5, upArrow  
    beq R4, R5, upArrowPressed
    lw R5, downArrow  
    beq R4, R5, downArrowPressed
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

checkKeyInputIntermediate:
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


upArrowPressed:
    lw R3, colorBlue       
    sw R3, 0(R1)           
    lw R7, screenStart     
    slt R2, R7, R1         
    beq R2, R0, checkKeyInputIntermediate  # stay within bounds
    lw R5, rowShift        
    sub R1, R1, R5         
    display
    j checkKeyInput


downArrowPressed:          
    lw R5, rowShift         
    lw R7, screenEnd       
    slt R4, R1, R7         
    beq R4, R0, checkKeyInputIntermediate 
    lw R3, colorYellow     
    sw R3, 0(R1) 
    add R1, R1, R5         
    display
    j checkKeyInput