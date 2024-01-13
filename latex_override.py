import os
import re

pattern = r'(.*\.((txt|pdf|jpg|png)))'


SOURCE= "PAPER_FOLDER"
PROJECT = "PROJECT_NAME".lower()
PATH_PREFIX = "data/"+PROJECT+"/"

def process_tex(tex_file):
    print("Processing: ", tex_file)
    with open(tex_file, 'r', encoding="utf-8") as f:
        tex = f.readlines()
    if "main.tex" in tex_file:
        # Handle main.tex
        with open(os.path.join(SOURCE, "include.tex"), 'w') as f:
            for line in tex:
                content = line.strip()
                if content.startswith("\\input{"):
                    file = content[7:-1]
                    if file.endswith(".tex"):
                        file = file[:-4]
                    f.write("\\input{"+os.path.join(PATH_PREFIX, file)+"}\n")
    else:
        with open(tex_file, 'w', encoding="utf-8") as f:
            for line in tex:
                line = line.replace("\\ref{", "\\ref{"+PROJECT+":")
                line = line.replace("\\label{", "\\label{"+PROJECT+":")
                if "\\includegraphics" in line:
                    graphDIR = line.split("includegraphics")[1].split("{")[1].split("}")[0]
                    newDIR = os.path.join(PATH_PREFIX, graphDIR)
                    line = line.replace(graphDIR, newDIR)
                if "\\input{" in line:
                    print(line)
                    file = line.split("input")[1].split("{")[1].split("}")[0]
                    if file.endswith(".tex"):
                        file = file[:-4]
                    line = line.replace(file, os.path.join(PATH_PREFIX, file))
                if "{" in line and "}" in line:
                    sections = line.split("{")
                    for i in range(1, len(sections)):
                        if "}" in sections[i]:
                            sections[i] = sections[i].split("}")[0]
                            match = re.match(pattern, sections[i])
                            if match:
                                print("REG: ", match.group(1))
                                if "data/"+PROJECT not in sections[i]:
                                    print("NOT IN: ", sections[i])
                                    line = line.replace(match.group(1), os.path.join(PATH_PREFIX, match.group(1)))
                line = line.replace("/./", "/")
                f.write(line)



for root, dirs, files in os.walk(SOURCE):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith((".tex", ".htm")):
            process_tex(filepath)

        elif filepath.endswith(".txt"):
            with open(filepath, 'r', encoding="utf-8") as f:
                content = f.readlines()
            with open(filepath, 'w', encoding="utf-8") as f:
                for line in content:
                    line = line.replace("\\label{", "\\label{"+PROJECT+":")
                    f.write(line)

            