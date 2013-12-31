#!/usr/bin/python
import footgen

bga_names = ["F169", "FT256", "FBG484", "FBG676"]
bga_columns = [13, 16, 22, 26]
for i in range(len(bga_names)):
    f = footgen.Footgen(bga_names[i])
    f.pitch = 1.0
    f.diameter = 0.45
    f.bga(bga_columns[i])
    f.silkbox(w=bga_columns[i]+f.pitch, notch=0.75)
    f.finish()

f = footgen.Footgen("FF665")
f.pitch = 1.0
f.diameter = 0.45
f.bga(26, omit = "A1,B1,G1,H1,N1,P1,W1,Y1,AE1,AF1,J9")
f.silkbox(w=27, notch=0.75)
f.finish()
