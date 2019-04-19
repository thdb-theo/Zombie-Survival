"""
import sys
import os
sys.path.append(os.getcwd()+"/src/")
from math import *
from maths import color

def foo():
    with open("assets/Tools/ciede_data.txt") as file:
        lines = file.read().splitlines()
        for i in range(0, len(lines)-1, 2):
            line1 = lines[i].split()
            line2 = lines[i+1].split()
            c1 = color.from_lab(*tuple(map(float, line1[:3])))
            c2 = color.from_lab(*tuple(map(float, line2[:3])))
            print(line1[:3], c1, line2[:3], c2)
            r1 = float(line1[-1])
            my = c1.ciede2000(c2)
            close = isclose(r1, my, abs_tol=1e-4)
            assert close, (*c1, *c2, r1, my, abs(r1 - my))
            # print(str(c1) + "\n" + str(c2))
            # print(r1, my, abs(r1-my), isclose(r1, my, abs_tol=1e-3), "\n")

if __name__ == "__main__":
    print(color.from_lab(50, 0, -2).lab)
"""
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
c1 = sRGBColor(100, 20, 45)
c2 = sRGBColor(255, 0, 0)
lab1 = convert_color(c1, LabColor)
lab2 = convert_color(c2, LabColor)
print(delta_e_cie2000(lab1, lab2))
