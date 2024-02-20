#/usr/bin/python3
import sys
import subprocess

if __name__== "__main__":
    current_tag = ""

    if len(sys.argv)>1:
        ref = sys.argv[1]
        if ref.startswith("refs/tags/"):
            current_tag=ref.replace("refs/tags/","")
    result = subprocess.run(['git', 'tag' ,'-l', '--sort=taggerdate', "v*"], stdout=subprocess.PIPE) 
    tags_list = result.stdout.decode("utf-8").split('\n')[:-1]
    previous_tag=""
    for i in reversed(tags_list):
        if current_tag!=i:
            previous_tag=i
            break
    print(previous_tag)
