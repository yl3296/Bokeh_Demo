---
title: Bokeh_Demo 
author: Yang(Claire) Liu
date: Feb 19, 2015
layout: post
output: md
tags: Bokeh, interactive,graph
---

##Introduction
**Bokeh**

An interactive, browser–based visualization library, driven from Python

**Features**

* interactive visualization
* as first class interface target
* no need to write JavaScript
* vovel, animated graphics
 * *two types of graph: static plot & server plot*

**Set Up**

```
Conda install bokeh      # if using Anaconda
Pip install bokeh           # if using pip

To get up-to-date version:
conda install -c bokeh/channel/dev 
```
**Demo1**

* Classification-Iris Morphology
  * *Given:*
  Three kinds of flowers, four features
  * *Goal:* 
  Feature selection based on pairwise correlation

![iris](https://cloud.githubusercontent.com/assets/10662777/7507077/ec531bd8-f437-11e4-8951-c5cfd1527c4a.png)

![iris_2](https://cloud.githubusercontent.com/assets/10662777/7507083/00ea3086-f438-11e4-8e84-fd9e7f6dbc94.png)

```
from __future__ import print_function

from math import pi

from bokeh.browserlib import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.models.glyphs import Circle, Text
from bokeh.models import (
    BasicTicker, ColumnDataSource, Grid, GridPlot, LinearAxis,
    DataRange1d, PanTool, Plot, WheelZoomTool
)
from bokeh.resources import INLINE
from bokeh.sampledata.iris import flowers

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}

flowers['color'] = flowers['species'].map(lambda x: colormap[x])


source = ColumnDataSource(
    data=dict(
        petal_length=flowers['petal_length'],
        petal_width=flowers['petal_width'],
        sepal_length=flowers['sepal_length'],
        sepal_width=flowers['sepal_width'],
        color=flowers['color']
    )
)

text_source = ColumnDataSource(
    data=dict(xcenter=[125], ycenter=[135])
)

xdr = DataRange1d(sources=[source.columns("petal_length", "petal_width", "sepal_length", "sepal_width")])
ydr = DataRange1d(sources=[source.columns("petal_length", "petal_width", "sepal_length", "sepal_width")])

def make_plot(xname, yname, xax=False, yax=False, text=None):
    plot = Plot(
        x_range=xdr, y_range=ydr, background_fill="#efe8e2",
        border_fill='white', title="", min_border=2, h_symmetry=False, v_symmetry=False,
        plot_width=250, plot_height=250)

    circle = Circle(x=xname, y=yname, fill_color="color", fill_alpha=0.2, size=4, line_color="color")
    plot.add_glyph(source, circle)

    xticker = BasicTicker()
    if xax:
        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        xticker = xaxis.ticker
    plot.add_layout(Grid(dimension=0, ticker=xticker))

    yticker = BasicTicker()
    if yax:
        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'left')
        yticker = yaxis.ticker
    plot.add_layout(Grid(dimension=1, ticker=yticker))

    plot.add_tools(PanTool(), WheelZoomTool())

    if text:
        text = " ".join(text.split('_'))
        text = Text(
            x={'field':'xcenter', 'units':'screen'},
            y={'field':'ycenter', 'units':'screen'},
            text=[text], angle=pi/4, text_font_style="bold", text_baseline="top",
            text_color="#ffaaaa", text_alpha=0.7, text_align="center", text_font_size="28pt"
        )
        plot.add_glyph(text_source, text)

    return plot

xattrs = ["petal_length", "petal_width", "sepal_width", "sepal_length"]
yattrs = list(reversed(xattrs))
plots = []

for y in yattrs:
    row = []
    for x in xattrs:
        xax = (y == yattrs[-1])
        yax = (x == xattrs[0])
        text = x if (x==y) else None
        plot = make_plot(x, y, xax, yax, text)
        row.append(plot)
    plots.append(row)

grid = GridPlot(children=plots, title="iris_splom")

doc = Document()
doc.add(grid)

if __name__ == "__main__":
    filename = "iris_splom.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Iris Data SPLOM"))
    print("Wrote %s" % filename)
    view(filename)
    
 ```

**Demo2**

* updating data on the Bokeh server triggers the rendered Bokeh plot to update automatically

![animated1](https://cloud.githubusercontent.com/assets/10662777/7507088/0b6c97ba-f438-11e4-9d7a-19e985fc46af.png)

```
bokeh-server   ## run server
# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

# time is needed for animated graph
import time

import numpy as np

from bokeh.plotting import *
# Define the function
N = 80

x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)

# Name the animated graph in server
output_server("line_animate")

# Create the static graph
p = figure()

p.line(x, y, color="#3333ee", name="sin")
p.line([0,4*np.pi], [-1, 1], color="#ee3333")

show(p)
# make it animated
renderer = p.select(dict(name="sin"))
ds = renderer[0].data_source

while True:
    for i in np.hstack((np.linspace(1, -1, 100), np.linspace(-1, 1, 100))):
        ds.data["y"] = y * i
        cursession().store_objects(ds)
        time.sleep(0.05)

```

**Demo3**

* streaming data causing updates to the rendered plot.
![animated2](https://cloud.githubusercontent.com/assets/10662777/7507090/1a8dae50-f438-11e4-89c7-3ff8a0147499.png)

```
# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

# time is needed for all animated graph

# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

import time

from numpy import pi, cos, sin, linspace, roll, zeros_like

from bokeh.plotting import *
from bokeh.models import GlyphRenderer

N = 50 + 1
r_base = 8
theta = linspace(0, 2*pi, N)
r_x = linspace(0, 6*pi, N-1)
rmin = r_base - cos(r_x) - 1
rmax = r_base + sin(r_x) + 1

colors = ["FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#2C7FB8", "#253494", "#2C7FB8", "#41B6C4", "#7FCDBB", "#C7E9B4"] * 5

cx = cy = zeros_like(rmin)

output_server("animated")

p = figure(x_range=[-11, 11], y_range=[-11, 11])

p.annular_wedge(
    cx, cy, rmin, rmax, theta[:-1], theta[1:],
    inner_radius_units="data",
    outer_radius_units="data",
    fill_color = colors,
    line_color="black",
)

show(p)

renderer = p.select(dict(type=GlyphRenderer))
ds = renderer[0].data_source

while True:

    rmin = ds.data["inner_radius"]
    rmin = roll(rmin, 1)
    ds.data["inner_radius"] = rmin

    rmax = ds.data["outer_radius"]
    rmax = roll(rmax, -1)
    ds.data["outer_radius"] = rmax

    cursession().store_objects(ds)
    time.sleep(.10)
    
```

