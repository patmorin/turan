#!/usr/bin/python

from __future__ import division


if __name__ == "__main__":
    head="""<?xml version="1.0"?>
    <!DOCTYPE ipestyle SYSTEM "ipe.dtd">
    <ipestyle name="colors">
    <color name="aliceblue" value="0.941 0.973 1"/>
    """

    colorbrewer="#8dd3c7 #ffffb3 #bebada #fb8072 #80b1d3 #fdb462 #b3de69 #fccde5"
    colors = colorbrewer.split()
    colors = [(c[1:3],c[3:5],c[5:7]) for c in colors]
    colors = [ [int(x, 16)/255 for x in c] for c in colors]
    
    tail="""</ipestyle>\n"""

    of=open("figs/brew.isy", "w")

    of.write(head)
    for i in range(len(colors)):
        of.write('<color name="brew{}" value="{} {} {}"/>\n'.format(i+1,
                   colors[i][0], colors[i][1], colors[i][2]))
    of.write(tail)
    of.close()
