def read_file(input_path):
    lines = []
    with open(input_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            vector = line.split()  # Split line into a list of elements
            lines.append(vector)  # Add the vector to the list
    return lines

# case 0x22: printf("SHLD   $%02x%02x", code[2], code[1]); opbytes=3; break;

def generate_code(output_path, vectors):
    output = 'int Disassemble8080Op(unsigned char *codebuffer, int pc)\n'   
    output += '{\n'    
    output += 'unsigned char *code = &codebuffer[pc];\n'   
    output += 'int opbytes = 1;\n'    
    output += 'printf ("%04x ", pc);\n'  
    output += 'switch (*code)\n'
    output += '{\n' 
    for vector in vectors:
        switchCase = f'case {vector[0]}: printf('
        instr = vector[1]
        if instr == '-':
            output += '//unclear\n'
            continue
        switchCase += f'"{instr}'
        if vector[2] != '*':
            if vector[3] == '1':
                switchCase += f'     {vector[2]}"); break;'
            elif vector[3] == '3' or vector[3] == '2':
                count = int(vector[3])
                if vector[2] == 'adr':
                    switchCase += '     $'
                    for i in range(count - 1, 0, -1):
                        switchCase += '%02x'
                    switchCase += '", '
                    switchCase = ",".join([f'code[{i}]' for i in range(count - 1, 0, -1)])
                    switchCase += f'); opbytes={count}; break;\n'
                elif vector[2][:2] == 'SP':
                    switchCase += '     SP,#$'
                    for i in range(count - 1, 0, -1):
                        switchCase += '%'
                        switchCase += '02x'
                    switchCase += '", '
                    switchCase = ",".join([f'code[{i}]' for i in range(count - 1, 0, -1)])
                    switchCase += f'); opbytes={count}; break;\n'
                else:
                    str = vector[2]
                    switchCase += f'     {str[0]},#$'
                    for i in range(count - 1, 0, -1):
                        switchCase += '%02x'
                    switchCase += '", '
                    switchCase = ",".join([f'code[{i}]' for i in range(count - 1, 0, -1)])
                    switchCase += f'); opbytes={count}; break;\n'
        else:
            switchCase += '"); break;'
        output += switchCase + '\n'
    output += '}\n'
    output += 'printf("\\n");\n'
    output += 'return opbytes;'
    output += '}'
        
    
    with open(output_path, 'w') as file:
        file.write(output)
    return

input_path = 'C:/users/clewa/OneDrive/Documents/PersonalProjects/emulator/opcodes.txt'
output_path = 'C:/users/clewa/OneDrive/Documents/PersonalProjects/emulator/disassemblerInvaders.c'
vectors = read_file(input_path)
generate_code(output_path, vectors)


