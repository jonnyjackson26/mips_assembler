#TODO: if you have the instruction "j ..." thats not jal, j, or jr, the error thrown isnt useful

def preprocess_lines(lines):
    """
    remove comments and whitespace
    """
    newlines=[]
    for line in lines:
        if line.strip()=="": #removes empty lines
            pass
        else:
            if "#" in line.strip():
                line = line[:line.index("#")]
                if line.strip()!="":
                    newlines.append(line.strip()) #gets rid of inline comments
            else:
                newlines.append(line.strip())
    return newlines

def build_data_table(lines):
    data_table = {}
    data_list = []
    newlines = []
    inDataSection = False
    inc=0
    for line in lines:
        if line == ".data":
            inDataSection = True
        elif line == ".text":
            inDataSection = False

        if not inDataSection and not line==".text":
            newlines.append(line)
        else:
            if ":" in line:
                data_list_item=int(line[line.index(":")+1:])
                data_list.append(data_list_item)
                data_table[line[:line.index(":")]]=inc
                inc+=1
    return data_table, data_list, newlines  

def create_label_table(lines):
    label_table = {}
    newlines = []
    inc=0
    for line in lines:
        if ":" in line:
            label_table[line[:line.index(":")]] = inc
        else:
            newlines.append(line)
            inc+=1
    return label_table, newlines

def dec_to_bin(num, bit):
    """
    Converts an integer 'num' to a 'bit'-bit binary string.
    Handles negative numbers using two's complement representation.
    """
    if num < 0:
        # Compute two's complement and mask to 'bit' bits
        num = (1 << bit) + num
    return f"{num & ((1 << bit) - 1):0{bit}b}"


def register_to_binary(register):
    """
    converts a register name to a 3-bit binary string
    """
    return f"{int(register[1:]):03b}"

def encode_instruction(line_num, instruction, label_table, data_table):
    """
    Encodes a single instruction into a binary string (16 bits)
    """
    parts = instruction.replace(",", " ").split() # Remove leading/trailing spaces and split by spaces and commas
    if parts[0] == "j" or parts[0] == "jal" or parts[0] == "jr":
        target_address = "0" * 12  # Default to 12 zeros
        if parts[0] == "jr":
            op = "0111"
            target_address = register_to_binary(parts[1])+ " "+"000"+" "+"000"+" "+"000"
        elif parts[0] == "jal":
            op = "1000"
            target_address = dec_to_bin(label_table[parts[1]], 12)
        elif parts[0] == "j":
            op = "0100"
            target_address = dec_to_bin(label_table[parts[1]], 12)
        return op + " " + target_address


    elif parts[0] == "lw" or parts[0] == "sw":
        op = "0001" if parts[0] == "lw" else "0010"
        rt = parts[1]
        if "(" in parts[2]:
            offset, rs = parts[2].replace(")", "").split("(")
            imm = int(offset)
        else:
            rs = "R0"
            imm = data_table[parts[2]]
        return op + " " + register_to_binary(rs) + " " + register_to_binary(rt) + " " + dec_to_bin(imm, 6)

    # Handle bne/beq instructions
    elif parts[0] == "bne" or parts[0] == "beq":
        op="0110" if parts[0]=="bne" else "0011"
        rs=parts[2]
        rt=parts[1] #these are switched, idk why but it works
        target_address=label_table[parts[3]]-line_num-1
        return op + " " + register_to_binary(rs) + " " + register_to_binary(rt) + " " + dec_to_bin(target_address,6)


    # Handle addi instruction
    elif parts[0] == "addi":
        op = "0101"
        rs=parts[2]
        rt=parts[1] #these are switched, idk why but it works
        imm = parts[3]
        return op + " " + register_to_binary(rs) + " " + register_to_binary(rt) + " " + dec_to_bin(int(imm),6)

    # Handle add/sub instructions
    elif parts[0] == "add" or parts[0] == "sub":
        if parts[0] == "add":
            op = "0000"
            funct = "010"
        elif parts[0] == "sub":
            op = "0000"
            funct = "110"
        rd = parts[1]
        rs = parts[2]
        rt = parts[3]
        return op + " " + register_to_binary(rs) + " " + register_to_binary(rt) + " " + register_to_binary(rd) + " " + funct

    # Handle and/or instructions
    elif parts[0] == "and" or parts[0] == "or":
        op="0000"
        funct="000" if parts[0]=="and" else "001"
        rd = parts[1]
        rs = parts[2]
        rt = parts[3]
        return op + " " + register_to_binary(rs) + " " + register_to_binary(rt) + " " + register_to_binary(rd) + " " + funct
        

    # Handle slt instruction
    elif parts[0] == "slt":
        op="0000"
        funct="111"
        rd = parts[1]
        rs = parts[2]
        rt = parts[3]
        return op + " " + register_to_binary(rs) + " " + register_to_binary(rt) + " " + register_to_binary(rd) + " " + funct

    # Handle display instruction
    elif parts[0] == "display":
        return "1111" + "0" * 12

    # Handle unrecognized instructions
    else:
        raise ValueError(f"Unknown instruction: {instruction}")


        
def encode_program(lines, label_table, data_table):
    """
    Encodes the entire program into a list of binary strings
    """
    encoded_program = []
    for i, line in enumerate(lines):
        encoded_program.append(encode_instruction(i, line, label_table, data_table))
    return encoded_program

def print_encoded_program(encoded_program):
    for line in encoded_program:
        print(line)

def print_lines(lines):
    for line in lines:
        print(line)

def main():
    # Defining the assembly file to read from
    filename = "assembly_file.asm"

    # Read all lines from the assembly file, and store them in a list
    with open(filename, "r") as infile:
        lines = infile.readlines()

    # Step 1: Preprocess the lines to remove comments and whitespace
    lines = preprocess_lines(lines)
    #print_lines(lines)

    # Step 2: Use the preprocessed program to build data table
    data_table, data_list, lines = build_data_table(lines)
    #print(data_table)
    #print(data_list)
    #print_lines(lines)

    # Step 3: Build a label table and strip out the labels from the code
    label_table, lines = create_label_table(lines)
    print(label_table)
    print(lines)
   
    # Step 4: Encode the program into a list of binary strings
    encoded_program = encode_program(lines, label_table, data_table)
    print_encoded_program(encoded_program)

    # Step 5: Convert the strings to hexadecimal and write them to a file
    # hex_program = post_process(encoded_program)
    # with open("output.hex", "w") as outfile:
    #     outfile.write("v3.0 hex words addressed\n00: ")
    #     outfile.writelines(hex_program)

    # Step 6: Convert the data list to hexadecimal and write it to a file
    # with open("data.hex", "w") as outfile:
    #     outfile.write("v3.0 hex words addressed\n00: ")
    #     outfile.writelines([f"{d:04x} " for d in data_list])


if __name__ == "__main__":
    main()