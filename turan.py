from __future__ import division
from math import sin, cos, pi

# Notes: All our triangles have the first vertex from the bottom half (indices
# 0,...,n-1) and the next two vertices from the top half (indices n,...,2n-1)
# The vertices are listed counterclockwise, so t[0] < t[1] < t[2]


def vertex_b(ta, tb):
    """Return true iff triangles ta and tb form a vertex_b configuration"""
    if (ta[0] == tb[0]):
        if ta[1] < tb[1] and tb[2] < ta[2]: return True
        if tb[1] < ta[1] and ta[2] < tb[2]: return True
    return False

def edge_b(ta, tb):
    """Return true iff triangles ta and tb form an edge_b configuration"""
    if ta[1] == tb[1] and ta[2] == tb[2]: return True
    if ta[0] == tb[0]:
        if ta[1] == tb[1] return True
        if ta[2] == tb[2] return True
    return False

def gon(n):
    """Return a list of the vertices of a regular 2n-gon.

    The vertices are ordered clockwise starting with a vertex that forms
    an angle of -pi/2n with the x-axis.
    """
    theta = pi/(2*n)
    return [ (cos(-pi*i/n-theta), sin(-pi*i/n-theta)) for i in range(2*n)]

 
