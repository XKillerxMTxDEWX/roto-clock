#!/usr/bin/env python3

from math import atan, sin, cos

line_template =  "(fp_line (start {startxy}) (end {endxy}) (layer {layer}) (width {width}) (tstamp {tstamp}))\n"

arc_template = "(fp_arc (start {sx} {sy}) (mid {mx} {my}) (end {ex} {ey}) (layer {layer}) (width {width}) (tstamp {tstamp}))\n"

HEADER_STR = ( '(footprint "PCB_coil_{value:g}" (version 20210824) (generator pcbnew) (layer "F.Cu")\n'
        '   (tedit 6272C06B)\n'
        '   (fp_text reference "REF**" (at 0 -0.5 unlocked) (layer "F.SilkS")\n'
        '       (effects (font (size 1 1) (thickness 0.15)))\n'
        '       (tstamp 60abf682-d68e-4d1b-b25d-cfe53e7aec56)\n'
        '   )\n'
        '   (fp_text value "approx {value:g} nH" (at 0 1 unlocked) (layer "F.Fab")\n'
        '       (effects (font (size 1 1) (thickness 0.15)))\n'
        '       (tstamp 11d83a30-e9b2-4faf-8187-1e21fe33a419)\n'
        '   )\n'
)

layers = { "front" : "F.Cu",
           "back" : "B.Cu",
    }

def draw_segments():
    pass

def draw_arcs(coil_parameters):
    for key in ["center", "radius", "track_width", "track_distance", "end_gap"]:
        if key == "center":
            coil_parameters[key][0] = round((coil_parameters[key][0] / 39.37), 5)
            coil_parameters[key][1] = round((coil_parameters[key][1] / 39.37), 5)
        else:
            coil_parameters[key] = round((coil_parameters[key] / 39.37), 5)
            
    string_out = ""
    for i in range(10):
        sector_angle = 90 - 2 * atan(coil_parameters["end_gap"] / (4 * (coil_parameters["radius"] + (i * coil_parameters["track_distance"]))))
        end_x = round(coil_parameters["radius"] * -sin(sector_angle), 5)
        end_y = round(coil_parameters["radius"] * cos(sector_angle), 5)
        string_out += arc_template.format(sx = 0, sy = -i * coil_parameters["track_distance"], \
                                            ex = end_x, ey = end_y, mx = 1.28, my = coil_parameters["radius"], \
                                            width = coil_parameters["track_width"], layer = coil_parameters["layer"], \
                                            tstamp = i)
    
    print(string_out)
        
"""
x      y    r
a^2 + b^2 = c^2

x = sqrt(c^2 - b^2)
y = sqrt(c^2 - a^2)

chord = end_gap


sector angle = 2 arctan( chord / (2d))

90 - 9.4 deg = 80.6 deg

x = r * sin(80.6)
y = r * cos(80.6)

"""

def main():
    coil_parameters = {
        "center" : [0,0],         # x/y coordinates of the centre of the coil in mils
        "radius" : 100,             # start radius in mil
        "end_gap": 20,             # gap distance between start and end of one arc in mils
        "start_angle" : 0.0,      # start rotation of coil in degrees
        "track_width" : 10,        # width of track in mil
        "track_distance" : 10,   # distance between tracks edges in mils
        "turns" :  100,           # number of turns in the coil
        "spin" : -1,              # ccw = +1, cw = -1
        "layer" : "F.Cu",          # layer to draw the coil on
        }
    
    arc_string = draw_arcs(coil_parameters)


if __name__ == "__main__":
    main()
