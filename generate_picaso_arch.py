
def shouldISkip(line) -> bool:
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
            print('valid name is ' + valid)
            break
    filtered_string = ''.join(c for c in valid if (c.isalnum() and c!=';' and c!='\n'))
    print('filtered valid name is ' + filtered_string)
    return filtered_string

def write_picasso_model():
    fin = open("synth_picasso.reference", "r")
    fout = open("picasso_model.xml", "w+")
    fout.write('<model name="picasso">\n')
    lines = fin.readlines()
    fout.write('\t<input_ports>\n')
    for line in lines:
        if "input" in line and (not shouldISkip(line)):
            words = line.split(' ')
            words_filtered = []
            for word in words:
                if word!='' and word!=' ':
                    words_filtered.append(word)
            print(words)
            print(words_filtered)
            name = (get_name(words_filtered))
            fout.write('\t\t<port name="')
            fout.write(name)
            fout.write('\"/>\n')
            print(name)
    fout.write('\t</input_ports>\n')
    fout.write('\t<output_ports>\n')
    for line in lines:
        if "output" in line and (not shouldISkip(line)):
            words = line.split(' ')
            words_filtered = []
            for word in words:
                if word!='' and word!=' ':
                    words_filtered.append(word)
            print(words)
            print(words_filtered)
            name = (get_name(words_filtered))
            fout.write('\t\t<port name="')
            fout.write(name)
            fout.write('" />\n')
            print(name)
    fout.write('\t</output_ports>\n')
    fout.write('</model>')
    fin.close()
    fout.close()

write_picasso_model()