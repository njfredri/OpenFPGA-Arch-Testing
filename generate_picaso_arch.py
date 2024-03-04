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
    valid = ''
    for token in line:
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

def generate_picaso_pb():
    fin = open("synth_picasso.reference", "r")
    fout = open("picaso_pb_type.xml", "w+")
    fout.write('<pb_type name="picaso">\n')
    lines = fin.readlines()
    ports = generate_pbtype_top_ports(lines)
    for port in ports:
        fout.write(port)
    write_physical_mode(fout, lines)
    fout.write('</pb_type>')
    fout.close()
    fin.close()

def write_physical_mode(fout, lines):
    current_indent = '\t\t'
    fout.write(current_indent + '<mode name="physical">\n')
    
    current_indent = '\t\t\t'
    fout.write(current_indent + '<pb_type name="picaso_slice" num_pb="1">\n')
    
    current_indent = '\t\t\t\t'
    slice_ports = generate_pbtype_top_ports(lines, line_begin='\t\t\t\t') #generate_slice_ports(lines)
    for port in slice_ports:
        fout.write(port)
    
    current_indent = '\t\t\t'
    fout.write(current_indent + '</pb_type>\n')
    current_indent = '\t\t'
    fout.write(current_indent + '</mode>\n')

generate_picaso_model()

printdbg(get_width(['thie', 'tga', '[5:2]', '', 'end;\n']))

generate_picaso_pb()