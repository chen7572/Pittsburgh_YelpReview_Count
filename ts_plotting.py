import pandas as pd
import numpy as np

from bokeh.layouts import gridplot, widgetbox, column, row
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_file, show
from bokeh.models import HoverTool,ColumnDataSource, Select, CustomJS
from bokeh.embed import components
from bokeh.models.widgets import Paragraph



forecast = pd.read_csv('data/dataforheroku/forecast_dataframe_50conf.csv', sep = '\t', index_col = 'Date')
PGH_review = pd.read_csv('data/dataforheroku/Yelp_ReviewCount.csv', sep = '\t')
PGH_review = PGH_review[PGH_review.Month != '2017-12-01']
PGH_review = PGH_review.drop(['Uncategorized'], axis = 1)

neighborhoods = [col for col in list(forecast.columns) if ('lower' not in col) and ('upper' not in col) ]

def datetime(x):
    return np.array(x, dtype = np.datetime64)

PGH_review['used'] = PGH_review['Central Business District']
PGH_review['Month'] = datetime(PGH_review['Month'])
forecast['Month'] = forecast.index
forecast['Month'] = datetime(forecast['Month'])

forecast['used'] = forecast['Central Business District']
forecast['used upper'] = forecast['Central Business District upper']
forecast['used lower'] = forecast['Central Business District lower']

source = ColumnDataSource(PGH_review)
source2 = ColumnDataSource(forecast)
TOOLS = "pan,wheel_zoom,reset,hover,save"

p1 = figure(x_axis_type='datetime', tools = TOOLS, toolbar_location="below")
p1.width=900
p1.height = 500
p1.grid.grid_line_alpha = 0.8
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Number of Reviews'
p1.xaxis.axis_label_text_font_size = "18pt"
p1.yaxis.axis_label_text_font_size = "18pt"
p1.xaxis.major_label_text_font_size = "12pt"
p1.yaxis.major_label_text_font_size = "12pt"

p1.line('Month', 'used', source = source, color='#33A02C', line_width = 2, line_join='round' ,legend = 'Actual')
p1.circle('Month', 'used', source = source, fill_color="white", line_color='#33A02C', size= 4)
p1.line('Month', 'used', source = source2,  color='#FF0000', line_width = 2, line_join='round',legend = 'Forecast')
p1.circle('Month', 'used', source = source2, fill_color="white", line_color='#FF0000', size= 4)
p1.line('Month', 'used upper', source = source2, color = '#FB9A99', legend = '50% confidence Interval')
p1.line('Month', 'used lower', source = source2, color = '#FB9A99')

#p1.patch(np.append('Month', 'Month'[::-1]), np.append('Central Business District'+' lower', forecast[col+' upper'][::-1]), color='#FB9A99', fill_alpha = 0.2, line_alpha= 0, legend = '95% confidence')


p1.legend.location = "top_left"

hover = p1.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Review Count", "@used"),
]

select = Select(value="Central Business District", options=neighborhoods, title="Select Pittsburgh Neighborhood:")

#dropdown_box = VBox(select, width=100, height=50)

callback = CustomJS(args=dict(source=source, source2=source2), code = """
            console.log(' changed selected option', cb_obj.value);
            var data = source.data;
            var data2 = source2.data;
            var upper = cb_obj.value + ' upper'
            var lower = cb_obj.value + ' lower'
            data['Month'] = data['Month']
            data['used'] = data[cb_obj.value]
            data2['Month'] = data2['Month']
            data2['used'] = data2[cb_obj.value]
            data2['used upper'] = data2[upper]
            data2['used lower'] = data2[lower]
            source.change.emit();
            source2.change.emit();
            """)

select.js_on_change('value', callback)
#select.callback = callback

text = Paragraph(text="""         """, height = 10)
text2 = Paragraph(text="""Select a neighborhood:""")
#show(widgetbox(p))

#layout = column(select, p1, sizing_mode='scale_width')
layout = column(row(widgetbox(text, width = 100), widgetbox(select, width =300)), p1, sizing_mode='scale_width')

script2, div2 = components(layout)
