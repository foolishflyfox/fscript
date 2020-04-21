#!env python
import os
import argparse
import sys
import subprocess
import re

# 获取 plantuml.jar 的位置
def getPlantuml():
    # 安装了 plantuml 创建后，plantuml.jar 将出现在文件夹
    # ~/.vscode/extensions/jebbs.plantuml-x.x.x 中
    extensions_path = os.path.expanduser("~/.vscode/extensions")
    if not os.path.isdir(extensions_path):
        return ""
    plantuml_dir = ""
    for extension in os.listdir(extensions_path):
        if extension.startswith("jebbs.plantuml"):
            plantuml_dir = extension
    if plantuml_dir=="":
        return ""
    plantuml_path = extensions_path+"/"+plantuml_dir+"/"+"plantuml.jar"
    if os.path.isfile(plantuml_path):
        return plantuml_path
    else:
        return ""
    
def dealWithError(msg):
    print("\033[31;1mERROR: "+msg+"\033[0m", file=sys.stderr)
    exit(1)

def dealWithWarning(msg):
    print("\033[33;1mWarning: "+msg+"\033[0m")
    

if __name__ == "__main__":
    plantuml = getPlantuml()
    if plantuml=="":
        dealWithError("Can't find plantuml.jar, please install vscode and " +
            "plnatuml plugin")
    # parser = argparse.ArgumentParser("Export plantuml fragments in markdown as images:\n")
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help="markdown file path")
    export_types = set(["svg","png","eps","latex","latex:nopreamble","vdx",
                        "xmi","scxml","html","txt","utxt"])
    parser.add_argument('-t', '--type', help=f"export type, can be {'/'.join(export_types)}")
    parser.add_argument('-o', '--output', help="export director, dafulat is current directory")
    args = parser.parse_args()

    input_path = ""
    output_type = "svg"
    output_dir = "."
    puml_paths = set()
    
    if not os.path.isfile(args.input_path):
        dealWithError(f"Can't open file {args.input_path}")
    input_path = args.input_path
    if args.type:
        output_type = args.type
    if args.output:
        output_dir = args.output
    if not os.path.isdir(output_dir):
        dealWithError(output_dir + " is not a directory")
    cmd = f"java -jar {plantuml} "
    if output_type in export_types:
        cmd += "-t" + output_type + " "
    else:
        dealWithError(f"Type {output_type} is unsupported")
    # 获取 plantuml 片段
    with open(input_path) as f_input:
        enter_plantuml = False
        start_flag_reg = re.compile(r"```plantuml\s+")
        export_name_reg = re.compile(r"@[a-zA-Z]+[\s]+([\S]+)")
        end_flag_reg = re.compile(r"```\s+")

        puml_path = ""
        export_name = ""
        puml_file = None
        for sline in f_input:
            if start_flag_reg.match(sline):
                enter_plantuml = True
            elif enter_plantuml:
                match_result = export_name_reg.search(sline)
                if match_result:
                    export_name = match_result[1]
                    puml_path = output_dir+"/"+export_name+".puml"
                    # 显示plantuml名称冲突
                    if puml_path in puml_paths:
                        dealWithWarning('Name conflict of '+export_name)
                    else:
                        puml_paths.add(puml_path)
                        if os.path.exists(puml_path):
                            print(puml_path, "has existed!")
                        else:
                            print("Writing to file :", puml_path, "...")
                            puml_file = open(puml_path, "w")
                            print(sline, file=puml_file, end='')
                else:
                    if end_flag_reg.match(sline):
                        enter_plantuml = False
                        if puml_file:
                            print("Finish", puml_path)
                            puml_file.close()
                            puml_file = None
                            print("Creating", output_type, "file :", export_name, "...")
                            t_cmd = cmd + " -I " + puml_path
                            subprocess.call(t_cmd, shell=True)
                            print("Finish", output_type, "file :", export_name)
                    else:
                        if puml_file:
                            print(sline, file=puml_file, end='')
    print("Finished!")

                    
# java -jar ~/.vscode/extensions/jebbs.plantuml-2.13.6/plantuml.jar -tsvg -I sys_sequence.puml -o .
