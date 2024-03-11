DEBUG = True
def printdbg(str, end='\n'):
    if DEBUG==True:
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
        if token=='input' or token=='output' or token=='wire':
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
            if(name in portnames):
                continue
            portnames.append(name)
            direction.append('clock')
            widths.append(get_width(line))
        elif 'input' in line:
            name = get_name(line)
            if(name in portnames):
                continue
            printdbg('returned name is ' + name)
            portnames.append(name)
            direction.append('input')
            widths.append(get_width(line))
        elif 'output' in line:
            name = get_name(line)
            if(name in portnames):
                continue
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
        # print(port)
        complete_string += (line_begin + '<' + port[1] + ' name="' + port[0] + '" num_pins="' + port[2] + '"/>\n')
    return complete_string

def generate_interconnect_string(ports_info, top: str, bot: str, line_begin = '\t'): #assuming ports are the same top and bottom
    constr = line_begin + '<interconnect>\n'
    newlb = line_begin + '\t'
    for port in ports_info:
        if port[1] == 'output':
            constr += newlb
            constr += '<direct name="' + port[0] + '2' + port[0] + '" '
            constr += 'input="' + bot + '.' + port[0] + '" '
            constr += 'output="' + top + '.' + port[0] + '"/>\n'
            continue
        else: #input and clock should be treated about the same
            constr += newlb
            constr += '<direct name="' + port[0] + '2' + port[0] + '" '
            constr += 'input="' + top + '.' + port[0] + '" '
            constr += 'output="' + bot + '.' + port[0] + '"/>\n'
            continue
    constr += line_begin + '</interconnect>\n'
    return constr

def generate_picaso_pb():
    fin = open("synth_picasso.reference", "r")
    fout = open("picaso_pb_type.xml", "w+")
    fout.write('<pb_type name="picaso_block">\n')
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
    fout.write(current_indent + '<pb_type name="picaso_slice" blif_model=".subckt picaso" num_pb="1">\n')
    
    current_indent = '\t\t\t\t'
    slice_ports_str = generate_ports_string(ports, current_indent)
    fout.write(slice_ports_str)
    current_indent = '\t\t\t'
    fout.write(current_indent + '</pb_type>\n')

    interconnect_str = generate_interconnect_string(ports, 'picaso_block', 'picaso_slice', line_begin=current_indent)
    fout.write(interconnect_str)
    

    current_indent = '\t\t'
    fout.write(current_indent + '</mode>\n')

def gen_equivalent_sites(line_start='\t\t'):
    s = line_start
    s += '<equivalent_sites>\n'
    s += line_start + '\t<site pb_type="picaso_block" pin_mapping="direct"/>\n'
    s += line_start + '</equivalent_sites>\n'
    return s

def generate_picaso_tile():
    fin = open("synth_picasso.reference", "r")
    fout = open("picaso_tile.xml", "w+")
    fout.write('<tile name="picaso">\n\t<sub_tile name="picaso" capacity="1">\n')
    fout.write(gen_equivalent_sites())

    lines = fin.readlines()
    ports_info = extract_ports(lines)
    ports_string = generate_ports_string(ports_info, line_begin='\t\t')
    fout.write(ports_string)
    # write_physical_mode(fout, ports_info)

    fout.write('\t\t<fc in_type="frac" in_val="0.2" out_type="frac" out_val="0.10"/>\n')
    fout.write('\t\t<pinlocations pattern="perimeter"/>\n')

    fout.write('\t</sub_tile>\n</tile>')
    fout.close()
    fin.close()

def generate_circtui_model_ports_string(ports, linebegin='\t'):
    s=''
    for port in ports:
        s += linebegin + '<port type="' + port[1] + '" prefix="' + port[0] + '" size="' + port[2] + '"/>\n'
    return s

def generate_picaso_openfpga_circuit():
    fin = open("synth_picasso.reference", "r")
    fout = open("picaso_circuit_model.xml", "w+")
    fout.write('<circuit_model type="hard_logic" name="picaso" prefix="picaso" is_default="true" verilog_netlist="$\{OPENFPGA_PATH\}/temp_mve/MV_Engine_For_SPAR/BitSerial-v1/MV-Engine/lib/work/yosys/picaso_synth.v">\n')
    fout.write('\t<design_technology type="cmos"/>\n')
    fout.write('\t<input_buffer exist="true" circuit_model_name="INVTX1"/>\n')
    fout.write('\t<output_buffer exist="true" circuit_model_name="INVTX1"/>\n')
    #define the ports of the circuit
    lines = fin.readlines()
    ports_info = extract_ports(lines)
    fout.write(generate_circtui_model_ports_string(ports_info))

    fout.write('</circuit_model>\n')

DEBUG=False
generate_picaso_model()
DEBUG=False
generate_picaso_pb()
generate_picaso_tile()
DEBUG=True
generate_picaso_openfpga_circuit()