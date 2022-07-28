#!/usr/bin/python3
import sys, os
import shutil
import math
import itertools

# syntax Reference
# (fp_line (start 0.709776 5.845528) (end 0.000000 5.900000) (width 0.4) (layer F.Cu) (tstamp 303))

DICT_lyr = { "dwg" : "Dwgs.User",
             "cmt" : "Cmts.User",
             "cut" : "Edge.Cuts",
             "fcu" : "F.Cu",
             "bcu" : "B.Cu",
             "allcu" : "*.Cu",
             "allmask" : "*.Mask"
             }
line_template =  "(fp_line (start {startxy}) (end {endxy}) (width {width}) (layer {layer}) (tstamp {tstamp}))\n"


def FNC_spiral (cntr, # (x,y)
                radius,
                segs,
                startangle,
                track_width, # track width
                track_distance, # track distance
                turns,
                spin, # cw or ccw, +1 or -1
                layer
                ):

    STR_data = ""
    baseX = cntr[0]
    baseY = cntr[1]
    tstamp = 0
    track_distance = track_distance + track_width

    for j in range(turns):
        
        
        segs += 0.0
        segangle = 360.0 / segs
        segradius = track_distance / segs


        for i in range(int(segs)):
            # central rings for HV and SNS
            startX = baseX + (radius + segradius * i + track_distance * (j+1)) * math.sin(math.radians(segangle*spin*i + startangle))
            startY = baseY + (radius + segradius * i + track_distance * (j+1)) * math.cos(math.radians(segangle*spin*i + startangle))
            endX = baseX + (radius + segradius * (i + 1.0) + track_distance * (j+1)) * math.sin(math.radians(segangle*spin*(i + 1.0) + startangle))
            endY = baseY + (radius + segradius * (i + 1.0) + track_distance * (j+1)) * math.cos(math.radians(segangle*spin*(i + 1.0) + startangle))

            STR_data += line_template.format(startxy = "{:.6f}".format(startX) + " " + "{:.6f}".format(startY), \
                                            endxy = "{:.6f}".format(endX) + " " + "{:.6f}".format(endY), \
                                            width = track_width, \
                                            layer = DICT_lyr[layer], \
                                            tstamp = tstamp)                                                   
            tstamp += 1
            
    return STR_data

def Generate_footprint_file(Center,
                            Radius,
                            Sides,
                            StartAngle,
                            TrackWidth,
                            TrackDistance,
                            Turns,
                            Spin,
                            Layer,
                            ):
    
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
    # Add all of the spiral segments
    HEADER_STR += FNC_spiral (Center,
                      Radius,
                      Sides,
                      StartAngle,
                      TrackWidth,
                      TrackDistance,
                      Turns,
                      Spin,
                      Layer,
                      )
    # Add the final closing bracket
    HEADER_STR += '    )'
    HEADER_STR = HEADER_STR.format(value = estimate_inductance(Radius, TrackWidth, TrackDistance, Turns))
    
    print(HEADER_STR)
  
  
def estimate_inductance(inner_radius, track_width, track_distance, turns):
    # formula is ( ( (4.921)*N(sqr)(d1+d2)(sqr) ) / (15d1-7d2) )
    
    # d2 is inner diamter
    d2 = (inner_radius + track_distance) * 2
    
    # d1 is outer diameter
    d1 = inner_radius + (track_distance * turns + 1) + inner_radius + (track_distance * turns)
    
    # calculate inductance in nanoHenries nH
    L = round(((4.921 * pow(turns,2) * pow((d1 + d2),2)) / ((15 * d1) - (7 * d2))), 0)
    
    # Return string 
    #return "Inner diameter = {d2} mm, Outer diameter = {d1} mm, Turns = {turns}, Estimated L = {L} nH".format(d1 = d1, d2 = d2, turns = turns, L = L)
    
    return L
    
    

def main():
    
    Center = [0,0]          # x/y coordinates of the centre of the pcb sheet
    Radius = 0            # start radius in mm
    Sides = 50            # smoothness of segments
    StartAngle = 0.0        # degrees
    TrackWidth = 0.25       # width of track
    TrackDistance = 0.3       # distance between tracks edges
    Turns =  15             # number of turns in the spiral
    Spin = -1               # ccw = +1, cw = -1
    Layer = "fcu"           # layer to draw the spiral on
    
    Generate_footprint_file(Center,
                            Radius,
                            Sides,
                            StartAngle,
                            TrackWidth,
                            TrackDistance,
                            Turns,
                            Spin,
                            Layer,
                            )

if __name__ == '__main__':
    main()
