import os
from pygments.styles import STYLE_MAP


def generate(s):
    # command = f'pygmentize -f html -a .highlight -S {s} > {s}.css'
    command = f'pygmentize -f html -a .codehilite -S {s} > {s}.css'
    os.system(command)


for key in STYLE_MAP.keys():
    print(key)
    generate(key)

