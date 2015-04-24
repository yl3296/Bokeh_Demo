＃Demo 1_ scatter plotting
# Set up plotting environment, import data and plotting functions
from bokeh.sampledata.iris import flowers
from bokeh.plotting import *
#Set colors
colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
flowers['color'] = flowers['species'].map(lambda x: colormap[x])

# Name the title, labels and define the output format
output_file("iris.html", title="iris.py example")

p = figure(title = "Iris Morphology")
p.xaxis.axis_label = 'Petal Length'
p.yaxis.axis_label = 'Petal Width'

p.circle(flowers["petal_length"], flowers["petal_width"],
        color=flowers["color"], fill_alpha=0.2, size=10, )

show(p)

# Demo 2_ Animated line 

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

# Demo 3_ Animated graph
# time is needed for all animated graph
import time

from numpy import pi, cos, sin, linspace, roll, zeros_like
from bokeh.plotting import *
from bokeh.models import GlyphRenderer

# Define a function
N = 50 + 1
r_base = 8
theta = linspace(0, 2*pi, N)
r_x = linspace(0, 6*pi, N-1)
rmin = r_base - cos(r_x) - 1
rmax = r_base + sin(r_x) + 1

colors = ["FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#2C7FB8", "#253494", "#2C7FB8", "#41B6C4", "#7FCDBB", "#C7E9B4"] * 5

cx = cy = zeros_like(rmin)

output_server("animated")
# Create a static figure
p = figure(x_range=[-11, 11], y_range=[-11, 11])

p.annular_wedge(
    cx, cy, rmin, rmax, theta[:-1], theta[1:],
    inner_radius_units="data",
    outer_radius_units="data",
    fill_color = colors,
    line_color="black",
)

show(p)
# make the figure animated.
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

Demo 4 _ Time Series 
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show, VBox

AAPL = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=AAPL&a=0&b=1&c=2000&d=0&e=1&f=2014",
    parse_dates=['Date'])
MSFT = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=MSFT&a=0&b=1&c=2000&d=0&e=1&f=2014",
    parse_dates=['Date'])
IBM = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=IBM&a=0&b=1&c=2000&d=0&e=1&f=2014",
    parse_dates=['Date'])

output_file("Stocks1.html", title="stocks.py example")

p1 = figure(title="Stocks",x_axis_type="datetime")

p1.line(AAPL['Date'], AAPL['Adj Close'],color='#A6CEE3',legend='AAPL',size=12)
p1.line(IBM['Date'], IBM['Adj Close'], color='#33A02C', legend='IBM',size=12)
p1.line(MSFT['Date'], MSFT['Adj Close'], color='#FB9A99', legend='MSFT',size=12)

p1.title = "Stock Closing Prices"
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'

##—Add moving average here:

p2 = figure(title="AAPL average",x_axis_type="datetime")
aapl = AAPL['Adj Close']
aapl_dates = AAPL['Date']

window_size = 30
window = np.ones(window_size)/float(window_size)
aapl_avg = np.convolve(aapl, window, 'same')

p2.scatter(aapl_dates, aapl, size=4,color='#C3D7D7', alpha=0.2,legend='daily close price')
p2.line(aapl_dates, aapl_avg,x_axis_type="datetime", color='blue',legend='moving avg price')

p2.title = "AAPL One-Month Average"
p2.grid.grid_line_alpha=0.3
p2.xaxis.axis_label = 'Date'
p2.yaxis.axis_label = 'Price'

show(VBox(p1, p2))

# Demo 5_Period Table
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.sampledata import periodic_table

elements = periodic_table.elements[periodic_table.elements['group'] != "-"]

group_range = [str(x) for x in range(1,19)]
period_range = [str(x) for x in reversed(sorted(set(elements['period'])))]

output_file("periodic1.html")

colormap = {
    'alkali metal'         : "#a6cee3",
    'alkaline earth metal' : "#1f78b4",
    'halogen'              : "#fdbf6f",
    'metal'                : "#b2df8a",
    'metalloid'            : "#33a02c",
    'noble gas'            : "#bbbb88",
    'nonmetal'             : "#baa2a6",
    'transition metal'     : "#e08e79",
}

source = ColumnDataSource(
    data=dict(
        group=[str(x) for x in elements['group']],
        period=[str(y) for y in elements['period']],
        symx=[str(x)+":0.1" for x in elements['group']],
        numbery=[str(x)+":0.8" for x in elements['period']],
        massy=[str(x)+":0.15" for x in elements['period']],
        namey=[str(x)+":0.3" for x in elements['period']],
        sym=elements['symbol'],
        name=elements['name'],
        cpk=elements['CPK'],
        atomic_number=elements['atomic number'],
        electronic=elements['electronic configuration'],
        mass=elements['atomic mass'],
        type=elements['metal'],
        type_color=[colormap[x] for x in elements['metal']],
    )
)

p = figure(title="Periodic Table", tools="resize,hover",
           x_range=group_range, y_range=period_range,
           plot_width=1200)

p.rect("group", "period", 0.9, 0.9, source=source,
       fill_alpha=0.6, color="type_color")


##-add text displaying more info in HoverTool

text_props = {
    "source": source,
    "angle": 0,
    "color": "black",
    "text_align": "left",
    "text_baseline": "middle"}

p.text(x=dict(field="symx", units="data"),
       y=dict(field="period", units="data"),
       text=dict(field="sym", units="data"),
       text_font_style="bold", text_font_size="15pt", **text_props)
p.text(x=dict(field="symx", units="data"),
       y=dict(field="numbery", units="data"),
       text=dict(field="atomic_number", units="data"),
       text_font_size="9pt", **text_props)
p.text(x=dict(field="symx", units="data"),
       y=dict(field="namey", units="data"),
       text=dict(field="name", units="data"),
       text_font_size="6pt", **text_props)
p.text(x=dict(field="symx", units="data"),
       y=dict(field="massy", units="data"),
       text=dict(field="mass", units="data"),
       text_font_size="5pt", **text_props)

p.grid.grid_line_color = None
hover = p.select(dict(type=HoverTool))
hover.tooltips = [
    ("name", "@name"),
    ("atomic number", "@atomic_number"),
    ("type", "@type"),
    ("atomic mass", "@mass"),
    ("electronic configuration", "@electronic"),
]

p.xaxis.axis_label = 'Group'
p.yaxis.axis_label = 'Period'
show(p)
