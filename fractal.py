#Jesse Lam, Samuel Isakov
#2024

#You need to install colour not color module!
#This is calculation-intensive. Order 16 might take up to 10 seconds to load.
import turtle
from math import atan2, sin, cos
from colour import Color

tu = turtle.Turtle()
turtle.tracer(0)
tu.ht()
tu.up()

def gradient(t, initial, end, ilist):
    maxy = max(ilist, key=lambda coord: coord[1])
    miny = min(ilist, key=lambda coord: coord[1])[1]
    maxx = max(ilist, key=lambda coord: coord[0])[0]
    minx = min(ilist, key=lambda coord: coord[0])[0]
    w = round(maxx - minx) + 2
    h = round(maxy[1] - miny) + 2
    colors = list(Color(initial).range_to(Color(end), w))
    t.up()
    t.goto(minx + xshift - 1, miny + yshift - 1)
    t.lt(90)
    t.down()
    for i in [x.hex_l for x in colors]:
        t.color(i)
        t.fd(h)
        t.up()
        t.goto(t.xcor() + 1, miny + yshift - 1)
        t.down()
    t.up()

def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** .5

def towards(start, end):
    return atan2(end[1] - start[1], end[0] - start[0])
    
def rotranslate(pt, deg, origin):
    return pt[0] * cos(deg) - pt[1] * sin(deg) + origin[0], pt[0] * sin(deg) + pt[1] * cos(deg) + origin[1]

def coordinates(ilist, px, py, nth, instruction):
    for _ in range(nth):
        elist = [ilist[0]]
        for i in range(len(ilist) - 1):
            prev = ilist[i]
            nex = ilist[i + 1]
            length = dist(prev, nex)
            if instruction[i % len(instruction)]:
                nh = (1 - px) * length
                nk = -1 * py * length
                elist += [rotranslate((nh, nk), towards(prev, nex), prev)] + [nex]
            else:
                h = px * length
                k = py * length
                elist += [rotranslate((h, k), towards(prev, nex), prev)] + [nex]
        ilist = tuple(elist)
    return ilist

def outline(t, ilist):
    maxy = max(ilist, key=lambda coord: coord[1])
    miny = min(ilist, key=lambda coord: coord[1])[1]
    maxx = max(ilist, key=lambda coord: coord[0])[0]
    minx = min(ilist, key=lambda coord: coord[0])[0]
    t.goto(maxy[0] + xshift, maxy[1] + yshift)
    t.fillcolor("black")
    t.begin_fill()
    for xy in ilist:
        t.goto(xy[0] + xshift, xy[1] + yshift)
        if xy == maxy:
            t.goto(maxy[0] + xshift, maxy[1] + yshift)
            t.sety(maxy[1] + margin[0] + yshift)
            t.setx(maxx + margin[1] + xshift)
            t.sety(miny - margin[2] + yshift)
            t.setx(minx - margin[3] + xshift)
            t.sety(maxy[1] + margin[0] + yshift)
            t.setx(maxy[0] + xshift)
            t.goto(maxy[0] + xshift, maxy[1] + yshift)
    t.end_fill()

p = (1 + 5 ** 0.5) / 2
r = (p - 1) ** (p - 1)
cosine = (1 + r ** 2 - r ** 4) / (2 * r)
sine = (1 - cosine ** 2) ** .5
x = cosine * r
y = sine * r

initial_shape =  ((-300, 0), (74.19915379779962, 242.02302109782485), (300, 0), (-300, 0))
percentx = x
percenty = y
order = 16
turning_scheme = (0, 0, 1) #(0, 1) is default
margin = (300, 500, 300, 500) #starts from top then clockwise
xshift = 50
yshift = -330
scale = 2
initial_shape = tuple((x * scale, y * scale) for x, y in initial_shape)

initial_color = "red"
final_color = "gold"

coordinate_list = coordinates(initial_shape, percentx, percenty, order, turning_scheme)
gradient(tu, initial_color, final_color, coordinate_list)
outline(tu, coordinate_list)
turtle.update()
turtle.done()
