

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

def encode_instruction(line_num, instruction, label_table, data_table):
    """
    Encodes a single instruction into a binary string (16 bits)
    """
    pass

def encode_program(lines, label_table, data_table):
    """
    Encodes the entire program into a list of binary strings
    """
    encoded_program = []
    for i, line in enumerate(lines):
        encoded_program.append(encode_instruction(i, line, label_table, data_table))
    return encoded_program

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
    print(data_table)
    print(data_list)
    #print_lines(lines)

    # Step 3: Build a label table and strip out the labels from the code
    label_table, lines = create_label_table(lines)
    print(label_table)
    print(lines)

    # Step 4: Encode the program into a list of binary strings
    # encoded_program = encode_program(lines, label_table, data_table)

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