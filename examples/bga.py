#!/usr/bin/python
import footgen

# 1 mm BGAs
bga_names = ["F169", "FT256", "FBG484", "FBG676"]
bga_columns = [13, 16, 22, 26]
for i in range(len(bga_names)):
    f = footgen.Footgen(bga_names[i])
    f.bga(rows = bga_columns[i], pitch = 1.0, diameter = 0.45)
    f.silkbox(w=bga_columns[i]+1.0, notch=0.75)
    f.finish()

# 1 mm BGA with some balls omitted
f = footgen.Footgen("FF665")
f.bga(rows = 26, pitch = 1.0, diameter = 0.45,
      omit = "A1,B1,G1,H1,N1,P1,W1,Y1,AE1,AF1,J9")
f.silkbox(w=27, notch=0.75)
f.finish()

# 0.8 mm BGAs
bga_names = ["TFBGA100", "CLG225", "CLG400"]
bga_columns = [10, 15, 20]
bga_sizes = [9,13,17]
for i in range(len(bga_names)):
    f = footgen.Footgen(bga_names[i])
    f.bga(rows = bga_columns[i], pitch = 0.8, diameter = 0.4)
    f.silkbox(w=bga_sizes[i], notch=0.75)
    f.finish()

# DDR3 RAM
f = footgen.Footgen("FBGA96")
f.bga(rows = 16, columns = 9, pitch = 0.8, diameter = 0.4, omit = "A4:T6")
f.silkbox(w=9, h=13, notch=0.5)
f.finish()

# 0.4 mm
f = footgen.Footgen('CM36')
f.bga(rows = 6, pitch = 0.4, diameter = 0.2)
f.silkbox(w=2.8, notch=0.25)
f.finish()
