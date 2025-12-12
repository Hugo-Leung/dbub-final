#!/usr/bin/python
import sys, os, tempfile, shutil
import argparse
import subprocess
from pathlib import Path
from pylatexenc import latexwalker
import tarfile

def list_of_strings(arg):
    return arg.split(',')

def main():
    args = argparse.ArgumentParser(prog="make_tarball.py", 
                                   description="try to make a tarball for journal submission")
    args.add_argument("filename", help="Name of the main tex file")
    args.add_argument("-B", "--buildDir", help="/path/to/build/dir")
    args.add_argument("--bbl", action='store_true', default=False, help="To include the bbl file")
    args.add_argument("-F","--FileList", type=list_of_strings, help="Extra files to be included")
    args.add_argument("-O", "--outName", help="output name")
    parse_args= args.parse_args()
    #print(parse_args)
    # open file in readOnly and test for errors
    if (not os.path.isfile(parse_args.filename)):
        print(parse_args.filename," not found")
        sys.exit(1)
    if (not os.access(parse_args.filename, os.R_OK)):
        print(parse_args.filename," not readable")
        sys.exit(1)
    if (not parse_args.filename.endswith(".tex")):
        print(parse_args.filename," is not a tex file")
        sys.exit(1)
    try:
        file = open(parse_args.filename, "r")
    except:
        print("unable to open ",parse_args.filename)
        sys.exit(1)
    # parse the tex file
    tex = latexwalker.LatexWalker(file.read())
    file.close()
    if tex is None:
        print("Could not open the main tex file")
        sys.exit(1)
    graphics = []
    graphics_path = []
    bib_list=[]
    nodelist = tex.get_latex_nodes()[0]
    for n in nodelist:
        if n.isNodeType(latexwalker.LatexEnvironmentNode):
            if n.envname=="document":
                print ("Found document environment")
                for nn in n.nodelist:
                    if nn.isNodeType(latexwalker.LatexEnvironmentNode):
                        if nn.envname=="figure" or nn.envname=="figure*":
                            print("Found figure environment")
                            graphics.extend(getGraphicsNodes(nn.nodelist))
                    elif nn.isNodeType(latexwalker.LatexMacroNode):
                        if nn.macroname=="bibliography":
                            print("Found bibliography")
                            bib_list.extend(getBibList(nn.nodeargs))
        elif n.isNodeType(latexwalker.LatexMacroNode):
            if n.macroname=="graphicspath":
                print("Found graphicspath")
                n_next = nodelist[nodelist.index(n)+1]
                graphics_path.extend(getGraphicsPath(n_next.nodelist))
                
    
    tmpDir_obj = tempfile.TemporaryDirectory()
    if tmpDir_obj is None:
        print("Cannot make tempdir")
        sys.exit(1)
    # use latexpand to combine all latex files
    path_obj = Path(parse_args.filename)
    pathToFile = str(path_obj.parent)
    baseName=path_obj.stem
    outName = baseName
    if parse_args.outName != None:
        outName = parse_args.outName
    graphics_path=checkPathList(graphics_path,pathToFile)
    #print(graphics_path)
    full_list = getFullPath(graphics_path,graphics)
    #print(full_list)
    for f in full_list:
        full_tmpPath=os.path.join(tmpDir_obj.name,os.path.basename(f))
        if (os.path.isfile(full_tmpPath)):
            print("Duplicate files named ",os.path.basename(f))
            print("This behavior has not been implemented")
            sys.exit(1)
        shutil.copy(f,full_tmpPath)

    if parse_args.FileList != None:
        extra_files=parse_args.FileList
        for ef in extra_files:
            full_ef=os.path.join(pathToFile,ef)
            if os.path.isfile(full_ef):
                full_tmpPath=os.path.join(tmpDir_obj.name,os.path.basename(ef))
                if (os.path.isfile(full_tmpPath)):
                    print("Duplicate files named ",os.path.basename(ef))
                    print("This behavior has not been implemented")
                    sys.exit(1)
                shutil.copy(full_ef,full_tmpPath)
            else:
                print("Extra file ",ef," not found")
                sys.exit(1)

    cmd =["latexpand"]
    if parse_args.bbl:
        search_path = [pathToFile]
        if parse_args.buildDir != None:
            search_path.append (parse_args.buildDir)
        for s in search_path:
            tmpPath=os.path.join(s,(baseName+".bbl"))
            if os.path.isfile(tmpPath):
                cmd.extend(["--expand-bbl",tmpPath])
                break
    else:
        bib_list=getBibFile(bib_list,pathToFile)
        for b in bib_list:
            full_tmpPath=os.path.join(tmpDir_obj.name, os.path.basename(b))
            if (os.path.isfile(full_tmpPath)):
                print("Duplicate files named ",os.path.basename(b))
                print("This behavior has not been implemented" )
                sys.exit(1)
            shutil.copy(b,full_tmpPath)


    cmd.extend(["--output",os.path.join(tmpDir_obj.name,(outName+".tex"))])
    cmd.append(parse_args.filename)
    print(" ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running latexpand")
        tmpDir_obj.cleanup()
        sys.exit(1)
    # make tarball
    tar = tarfile.open(os.path.join(os.getcwd(),(outName+".tar.gz")), "w:gz")
    for filename in os.listdir(tmpDir_obj.name):
        if not filename.startswith('.'):
            tar.add(os.path.join(tmpDir_obj.name, filename), arcname=filename)
    tar.close()
    tmpDir_obj.cleanup()
    
    pass

def getGraphicsNodes(nodelist):
    graphics=[]
    for node in nodelist:
        if node.isNodeType(latexwalker.LatexMacroNode) and (node.macroname=="includegraphics" or node.macroname=="includegraphics*"):
            groupNodes=node.nodeargs
            for gn in groupNodes:
                for n in gn.nodelist:
                    print("Found ",n.chars)
                    if(os.path.dirname(n.chars)):
                        print("The latex source code contain figures: ",n.chars)
                        print("I haven't implement updating source code")
                        sys.exit(1)
                    graphics.append(n.chars)
        if node.isNodeType(latexwalker.LatexEnvironmentNode) and node.envname=="subfigure":
            graphics.extend(getGraphicsNodes(node.nodelist))
    return graphics

def getGraphicsPath(nodelist):
    paths=[]
    for node in nodelist:
        if node.isNodeType(latexwalker.LatexGroupNode):
            paths.extend(getGraphicsPath(node.nodelist))
        elif node.isNodeType(latexwalker.LatexCharsNode):
            paths.append(node.chars)
            print("Append path: ",node.chars)
    return paths

def getFullPath(path_list, graphics_list):
    full_list=[]
    subfix_list=["",".pdf", ".eps", ".png", ".jpeg", ".jpg"] # make assumption which file format we prefer
    for p in path_list:
        for g in graphics_list:
            for s in subfix_list:
                tmpPath = os.path.join(p,(g+s))
                if os.path.isfile(tmpPath):
                    full_list.append(tmpPath)
                    break
    return full_list

def checkPathList(path_list, pathToTex):
    checked_list=[]
    #check if every element in path_list is unique, and make sure pathToTex is in path_list
    cwd_obj=Path(pathToTex)
    found_cwd=False
    for p in path_list:
        p_obj=Path(os.path.join(pathToTex,p))
        if(p_obj==cwd_obj):
            found_cwd=True
        if (p_obj.is_dir() and (not str(p_obj) in checked_list)):
            checked_list.append(str(p_obj))
    if not found_cwd and cwd_obj.is_dir():
        checked_list.append(str(cwd_obj))
    return checked_list

def getBibList(nodelist):
    bib_list=[]
    for node in nodelist:
        if node.isNodeType(latexwalker.LatexGroupNode):
            bib_list.extend(getBibList(node.nodelist))
        elif node.isNodeType(latexwalker.LatexCharsNode):
            bib_list.append(node.chars)
    return bib_list

def getBibFile(bibList, pathToTex):
    check_list=[]
    for b in bibList:
        tmpPath=os.path.join(pathToTex,b)
        if not tmpPath.endswith(".bib"):
            tmpPath+=".bib"
        if os.path.isfile(tmpPath) and not (tmpPath in check_list):
            check_list.append(tmpPath)
    return check_list

if __name__ == "__main__":
    main()