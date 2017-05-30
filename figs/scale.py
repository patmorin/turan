from __future__ import division




print("""<?xml version="1.0"?>
    <!DOCTYPE ipestyle SYSTEM "ipe.dtd">
    <ipestyle name="scale">""")

colours=[(166,206,227),(31,120,180),(178,223,138),(51,160,44),(251,154,153),
         (227,26,28),(253,191,111),(255,127,0),(202,178,214),(106,61,154),
         (255,255,153),(177,89,40)]

for i in range(len(colours)):
    (r,g,b) = [c/255 for c in colours[i]]
    print('   <color name="scale{}" value="{} {} {}"/>'.format(i, r, g, b))

print("""</ipestyle>""")
