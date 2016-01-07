#!/usr/bin/python
import footgen

f = footgen.Footgen("BMI-S-230-F")
for y in [18.95, -18.95]:
    for i in range(-3, 4):
        f.add_pad(name = "1", x = 6.0*i, y = y, xsize = 3.8, ysize = 1.0)
        f.add_pad(name = "1", x = 6.0*i, y = y, xsize = 1.0, ysize = 1.0, drill = 0.5)
    for i in [-1,1]:
        f.add_pad(name = "1", x = i*(6.0*4-0.05), y = y, xsize = 3.7, ysize = 1.0)
        f.add_pad(name = "1", x = i*(6.0*4-0.05), y = y, xsize = 1.0, ysize = 1.0, drill = 0.5)
    for i in range(8):
        f.add_pad(name = "1", x = -21.0 + i*6.0, y = y, xsize = 1.5, ysize = 1.5, drill = 1.0)

for x in [25.3, -25.3]:
    for i in range(-2, 3):
        f.add_pad(name = "1", x = x, y = 6.0*i, xsize = 1.0, ysize = 3.8)
        f.add_pad(name = "1", x = x, y = 6.0*i, xsize = 1.0, ysize = 1.0, drill = 0.5)
    for i in [-1,1]:
        f.add_pad(name = "1", x = x, y = i*(18.0-0.45/2), xsize = 1.0, ysize = 3.8-0.45)
        f.add_pad(name = "1", x = x, y = i*(18.0-0.45/2), xsize = 1.0, ysize = 1.0, drill = 0.5)
    for i in range(6):
        f.add_pad(name = "1", x = x, y = -15.0 + i*6.0, xsize = 1.5, ysize = 1.5, drill = 1.0)



output_file = open("BMI-S-230-F.kicad_mod", "w")
output_file.write(f.generator.finish())
output_file.close()
