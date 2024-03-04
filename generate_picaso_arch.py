DEBUG = True
def printdbg(str, end='\n'):
    if DEBUG:
        print(str, end=end)

def shouldISkip_bcuzClk(line) -> bool:
    if('clk' in line):
        return True
    if('clock' in line):
        return True
    return False

def get_name(line) -> str:
    temp_line = line
    valid = ''
    printdbg('input line is: ' + str(line))
    # tokens = line.split(' ')
    if isinstance(line, str):
        temp_line = line.split(' ')
    for token in temp_line:
        if token=='input' or token=='output':
            continue
        elif token=='':
            continue
        elif token==' ':
            continue
        elif '[' in token:
            continue
        else:
            valid=token
            printdbg('valid name is ' + valid)
            break
    filtered_string = ''.join(c for c in valid if (c.isalnum() and c!=';' and c!='\n'))
    printdbg('filtered valid name is ' + filtered_string)
    return filtered_string

def extract_ports(lines):
    portnames = []
    direction = []
    widths = []
    for line in lines:
        if 'clk' in line or 'clock' in line:
            name = get_name(line)
            portnames.append(name)
            direction.append('clock')
            widths.append(get_width(line))
        elif 'input' in line:
            name = get_name(line)
            print('returned name is ' + name)
            portnames.append(name)
            direction.append('input')
            widths.append(get_width(line))
        elif 'output' in line:
            name = get_name(line)
            portnames.append(name)
            direction.append('output')
            widths.append(get_width(line))
        
    return list(zip(portnames, direction, widths))

def get_width(line) -> str:
    for word in line:
        if '[' in word:
            printdbg(word)
            justval = ''.join(c for c in word if (c!='[' and c!=']'))
            printdbg(justval)
            split = justval.split(':')
            if(len(split) > 1):
                printdbg(split)
                num1 = int(split[0])
                num2 = int(split[1])
                dif = abs(num1-num2) + 1
                printdbg(dif)
                return(str(dif))
    return '1'

def generate_picaso_model():
    fin = open("synth_picasso.reference", "r")
    fout = open("picaso_model.xml", "w+")
    fout.write('<model name="picaso">\n')
    lines = fin.readlines()
    fout.write('\t<input_ports>\n')
    for line in lines:
        if "input" in line and (not shouldISkip_bcuzClk(line)):
            words = line.split(' ')
            words_filtered = []
            for word in words:
                if word!='' and word!=' ':
                    words_filtered.append(word)
            printdbg(words)
            printdbg(words_filtered)
            name = (get_name(words_filtered))
            fout.write('\t\t<port name="')
            fout.write(name)
            fout.write('\"/>\n')
            printdbg(name)
    fout.write('\t</input_ports>\n')
    fout.write('\t<output_ports>\n')
    for line in lines:
        if "output" in line and (not shouldISkip_bcuzClk(line)):
            words = line.split(' ')
            words_filtered = []
            for word in words:
                if word!='' and word!=' ':
                    words_filtered.append(word)
            printdbg(words)
            printdbg(words_filtered)
            name = (get_name(words_filtered))
            fout.write('\t\t<port name="')
            fout.write(name)
            fout.write('" />\n')
            printdbg(name)
    fout.write('\t</output_ports>\n')
    fout.write('</model>')
    fin.close()
    fout.close()

def generate_pbtype_top_ports(lines, line_begin='\t'):
    ports = []
    ports.append(line_begin + '<clock name="clk" num_pins="1"/>\n')
    for line in lines:
        if "input" in line and (not shouldISkip_bcuzClk(line)):
            port_string =''
            words = line.split(' ')
            words_filtered = []
            for word in words:
                if word!='' and word!=' ':
                    words_filtered.append(word)
            printdbg(words)
            printdbg(words_filtered)
            num_pins = get_width(words)
            name = (get_name(words_filtered))
            port_string += line_begin+'<input name="'
            port_string += name
            port_string += '" num_pins="'
            port_string += num_pins
            port_string += '\"/>\n'
            printdbg(name)
            printdbg(port_string)
            ports.append(port_string)
        elif "output" in line and (not shouldISkip_bcuzClk(line)):
            port_string =''
            words = line.split(' ')
            words_filtered = []
            for word in words:
                if word!='' and word!=' ':
                    words_filtered.append(word)
            printdbg(words)
            printdbg(words_filtered)
            name = (get_name(words_filtered))
            port_string += line_begin+'<output name="'
            port_string += name
            port_string += '" num_pins="'
            port_string += num_pins
            port_string += '\"/>\n'
            printdbg(name)
            printdbg(port_string)
            ports.append(port_string)
    return ports

def generate_slice_ports(lines, line_begin='\t\t\t\t'):
    ports = []
    ports.append('\t<clock name="clk" num_pins="1"/>\n')
    for line in lines:
        if "input" in line and (not shouldISkip_bcuzClk(line)):
            port_string =''
            words = line.split(' ')
            words_filtered = []
            for word in words:
                if word!='' and word!=' ':
                    words_filtered.append(word)
            printdbg(words)
            printdbg(words_filtered)
            num_pins = get_width(words)
            name = (get_name(words_filtered))
            port_string += line_begin+'<input name="'
            port_string += name+'_cfg'
            port_string += '" num_pins="'
            port_string += num_pins
            port_string += '\"/>\n'
            printdbg(name)
            printdbg(port_string)
            ports.append(port_string)
        elif "output" in line and (not shouldISkip_bcuzClk(line)):
            port_string =''
            words = line.split(' ')
            words_filtered = []
            for word in words:
                if word!='' and word!=' ':
                    words_filtered.append(word)
            printdbg(words)
            printdbg(words_filtered)
            name = (get_name(words_filtered))
            port_string += line_begin+'<output name="'
            port_string += name+'_cfg'
            port_string += '" num_pins="'
            port_string += num_pins
            port_string += '\"/>\n'
            printdbg(name)
            printdbg(port_string)
            ports.append(port_string)
    return ports

def generate_ports_string(ports_info, line_begin='\t'):
    complete_string = ''
    for port in ports_info:
        print(port)
        complete_string += (line_begin + '<' + port[1] + ' name="' + port[0] + '" num_pins="' + port[2] + '"/>\n')
    return complete_string

def generate_picaso_pb():
    fin = open("synth_picasso.reference", "r")
    fout = open("picaso_pb_type.xml", "w+")
    fout.write('<pb_type name="picaso">\n')
    lines = fin.readlines()
    ports_info = extract_ports(lines)
    ports_string = generate_ports_string(ports_info, line_begin='\t')
    fout.write(ports_string)
    write_physical_mode(fout, ports_info)

    fout.write('</pb_type>')
    fout.close()
    fin.close()

def write_physical_mode(fout, ports):
    current_indent = '\t\t'
    fout.write(current_indent + '<mode name="physical">\n')
    
    current_indent = '\t\t\t'
    fout.write(current_indent + '<pb_type name="picaso_slice" num_pb="1">\n')
    
    current_indent = '\t\t\t\t'
    slice_ports_str = generate_ports_string(ports, '\t\t\t')
    fout.write(slice_ports_str)
    
    current_indent = '\t\t\t'
    fout.write(current_indent + '</pb_type>\n')
    current_indent = '\t\t'
    fout.write(current_indent + '</mode>\n')

def write_base_pb_type(fout, lines):
    current_indent='\t\t\t\t'
    


generate_picaso_model()
generate_picaso_pb()