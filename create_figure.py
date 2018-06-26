import pandas as pd
import geopandas as gpd
import os
import fiona
import datetime
import shapely

import bokeh
from bokeh.plotting import Figure, show
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import Slider, DateSlider
from bokeh.layouts import column
from bokeh.io import show, output_file
from bokeh.models import HoverTool, ColumnDataSource, LinearColorMapper, LogColorMapper, ColorBar, LogTicker, BasicTicker
from bokeh.embed import components
from bokeh.resources import CDN

bv = bokeh.__version__

PGH_review = pd.read_csv('data/dataforheroku/Yelp_ReviewCount_withPredict.csv', sep = '\t',parse_dates=['Month'], index_col='Month')
#neighborhoods = gpd.read_file(os.path.join(r"/Users/chenchen/Documents/DataScience/DataIncubator/dataset/PA_neighborhood/","ZillowNeighborhoods-PA.shp"))
neighborhoods = gpd.read_file("data/dataforheroku/PAneighbor/ZillowNeighborhoods-PA.shp")
Pittsburgh_neighborhood = neighborhoods[neighborhoods['City'] == 'Pittsburgh']
#PGH_neighbor = PGH_review['2006':].T.copy().reset_index()
#PGH_neighbor.rename(columns = {'index':'Name'},inplace=True)
#Merged_result = pd.merge(Pittsburgh_neighborhood, PGH_neighbor, on='Name')
PGH_neighbor = PGH_review['2006':].T.copy().reset_index()
PGH_neighbor.rename(columns = {'index':'Name'},inplace=True)
Merged_result = pd.merge(PGH_neighbor, Pittsburgh_neighborhood, on='Name', how='outer')

for col in Merged_result.columns:
    if isinstance(col, datetime.date):
        new_name = col.strftime('%Y-%m')
        Merged_result.rename(columns = {col:new_name},inplace=True)

bokeh_df = Merged_result.drop(['State','County','City','RegionID'],axis = 1)
#bokeh_df_uncategorized = bokeh_df.iloc[65,:]
#bokeh_df = bokeh_df.drop(bokeh_df.index[[1,65]])


def getPolyCoords(row, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""

    # Parse the exterior of the coordinate
    if isinstance(row[geom], shapely.geometry.multipolygon.MultiPolygon):
        exterior = row[geom][1].exterior

    else:
        exterior = row[geom].exterior

    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list( exterior.coords.xy[0] )
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list( exterior.coords.xy[1] )

bokeh_df['x'] = bokeh_df.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
bokeh_df['y'] = bokeh_df.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)
bokeh_df.drop(['geometry'],axis = 1,inplace=True)

bokeh_df_percent = bokeh_df.copy()
for i in bokeh_df.columns[1:157]:
    bokeh_df_percent[i] = 100 * bokeh_df[i]/bokeh_df[i].sum()


bokeh_df_percent['used'] = bokeh_df_percent['2012-01']

source = ColumnDataSource(bokeh_df_percent)
TOOLS = "pan,wheel_zoom,reset,hover,save"
custom_colors = ['#ffede6','#ffb699','#ffa07a','#ff7f4d','#ff4800']
color_mapper = LinearColorMapper(palette=custom_colors, low = 0.0, high = 15)

#output_file("yelp_count.html")

p = Figure(title="", tools = TOOLS, x_axis_location=None, y_axis_location=None, toolbar_location="below")
p.width=250
p.height = 200
p.grid.grid_line_color = None

color_bar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(),
                     label_standoff=16, border_line_color=None, location=(0,0),
                     major_label_text_color = 'black',major_label_text_font_size = "14pt",
                     title='fraction of reviews (%)', title_standoff=12, title_text_font_size='14pt')


p.add_layout(color_bar, 'left')

renderer = p.patches('x', 'y', source=source,
          fill_color={'field': 'used', 'transform': color_mapper},
          fill_alpha = 0.7, line_color='black', line_width=0.6)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@Name"),
    ("Percentage of Monthly Reviews", "@used"),
    ("(Lat, Long)", "($y, $x)"),
]


callback = CustomJS(args=dict(source=source, plot=p, color_mapper = color_mapper,renderer = renderer),code="""
    var data = source.data;
    date = new Date(slider.value)
    var year = date.getFullYear().toString();
    var month = date.getMonth().toString();
    console.log(month)
    var month_str = month.length == 1 ? '0'+ month : month;

    var time = year+'-'+month_str;
    used = data['used']
    should_be = data[time]
    for (i = 0; i < should_be.length; i++) {
         used[i] = should_be[i];
    }

    source.change.emit()
    """)

time_slider = DateSlider(title="Year-Month", start=datetime.date(2006, 1, 1), end=datetime.date(2018, 12, 1),value=datetime.date(2014, 4, 1), step=1, format = "%Y-%m", callback=callback)
callback.args['slider'] = time_slider

layout = column(time_slider, p, sizing_mode='scale_width')

script, div = components(layout)
#script, div = components(p)

cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files[0]
bv = bv
#show(layout)
