from bokeh.io import curdoc, output_file, show
from bokeh.layouts import widgetbox, column, layout
from bokeh.models.widgets import TextInput, Button, DataTable, TableColumn, Select
import requests
import pandas as pd
from bokeh.models import ColumnDataSource
from io import StringIO
from bokeh.plotting import figure
import numpy as np
import scipy.special
from bokeh.layouts import gridplot

 
text_input = TextInput(value="http://test.com", title="Url:")
button = Button(button_type = 'success', label='Submit')
select1 = Select(title='x axis variable', options=[])
select2 = Select(title='y axis variable', options=[])

columns = []
sourceplt1 = ColumnDataSource(data={'x':[], 'y':[]})
sourceplt2hist = ColumnDataSource(data={ 'left':[], 'right':[], 'hist':[]})
sourceplt3hist = ColumnDataSource(data={  'left':[], 'right':[], 'hist':[]})
sourceplt2pdf = ColumnDataSource(data={'x':[], 'pdf':[]})
sourceplt3pdf = ColumnDataSource(data={'x':[], 'pdf':[]})
sourceplt2cdf = ColumnDataSource(data={'x':[], 'cdf':[]})
sourceplt3cdf = ColumnDataSource(data={'x':[], 'cdf':[]})


xf = pd.DataFrame({'x':[], 'y':[]})

lstval1 = ' '
lstval2 = ' '

plot1 = figure(title ='Scatter Plot', x_axis_label='', y_axis_label='', width=450)
plot2 = figure(title ='Data Distribution with probability density function for x axis', x_axis_label='', y_axis_label='', background_fill_color="#E8DDCB", width=450)
plot3 = figure(title ='Data Distribution with probability density function for y axis', x_axis_label='', y_axis_label='', background_fill_color="#E8DDCB", width=450)
plot4 = figure(title ='cumulative density function for x axis variable', x_axis_label='', y_axis_label='', background_fill_color="#E8DDCB", width=450)
plot5 = figure(title ='cumulative density function for y axis variable', x_axis_label='', y_axis_label='', background_fill_color="#E8DDCB", width=450)



def update():
	link = text_input.value
	r = requests.get(link)
	data = StringIO(r.text)
	df = pd.read_csv(data)
	global xf
	xf = df.copy()
	source = ColumnDataSource(df)
	select1.options.append(' ')
	select2.options.append(' ')
	select1.options = [x for x in xf.columns]
	select2.options = [x for x in xf.columns]
	columns = []
	if len(layout.children) >= 3: 
		layout.children.pop()
		layout.children.pop()
		layout.children.pop()
	for x in df.columns:
		columns.append(TableColumn(title=x, field=x))
	data_table = DataTable(source=source, columns=columns, width=1266, height=400)
	widg = widgetbox(select1, select2)
	c = column(data_table)
	layout.children.append(c)
	layout.children.append(widg)
	plot1.xaxis.axis_label = xf.columns[0]
	plot1.yaxis.axis_label = xf.columns[0]
	sourceplt1.data={'x' : xf[xf.columns[0]], 'y': xf[xf.columns[0]] }
	plot1.circle('x', 'y', source=sourceplt1)
	global lstval1, lstval2
	lstval1 = xf.columns[0]
	lstval2 = xf.columns[0]


	mu, sigma = np.mean(xf[xf.columns[0]]), np.std(xf[xf.columns[0]])
	

	hist, edges = np.histogram(xf[xf.columns[0]], density=True, bins=50)

	x = np.linspace( np.min( xf[xf.columns[0]] ) , np.max( xf[xf.columns[0]] ), 1000)
	pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
	cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2


	sourceplt2hist.data = {'left':edges[:-1], 'right':edges[1:], 'hist':hist }
	sourceplt3hist.data = {  'left':edges[:-1], 'right':edges[1:], 'hist':hist }
	sourceplt2pdf.data = {'x' : x,  'pdf':pdf }
	sourceplt3pdf.data = {'x' : x, 'pdf' : pdf}
	sourceplt2cdf.data = {'x' : x,  'cdf': cdf }
	sourceplt3cdf.data = {'x' : x, 'cdf' : cdf}

	plot2.quad(top='hist', bottom=0, left='left', right='right',
        fill_color="#036564", line_color="#033649",  source=sourceplt2hist)

	plot2.line('x', 'pdf', line_color="#D95B43", line_width=8, alpha=0.7, legend="PDF", source=sourceplt2pdf)
	plot4.line('x', 'cdf', line_color="white", line_width=2, alpha=0.7, legend="CDF", source=sourceplt2cdf)
	plot2.legend.location = "center_right"
	plot2.legend.background_fill_color = "darkgrey"
	plot2.xaxis.axis_label = xf.columns[0]
	plot2.yaxis.axis_label = 'Pr(' + xf.columns[0] +')'


	plot3.quad(top='hist', bottom=0, left='left', right='right',
        fill_color="#036564", line_color="#033649", source=sourceplt3hist)

	plot3.line('x', 'pdf', line_color="#D95B43", line_width=8, alpha=0.7, legend="PDF", source= sourceplt3pdf)
	plot5.line('x', 'cdf', line_color="white", line_width=2, alpha=0.7, legend="CDF", source=sourceplt3cdf)
	plot3.legend.location = "center_right"
	plot3.legend.background_fill_color = "darkgrey"
	plot3.xaxis.axis_label = xf.columns[0]
	plot3.yaxis.axis_label = 'Pr(' + xf.columns[0] +')'

	plot4.legend.location = "center_right"
	plot4.legend.background_fill_color = "darkgrey"
	plot4.xaxis.axis_label = xf.columns[0]
	plot4.yaxis.axis_label = 'Pr(' + xf.columns[0] +')'

	plot5.legend.location = "center_right"
	plot5.legend.background_fill_color = "darkgrey"
	plot5.xaxis.axis_label = xf.columns[0]
	plot5.yaxis.axis_label = 'Pr(' + xf.columns[0] +')'


	layout.children.append(gridplot(plot1,plot2,plot3, plot4, plot5, ncols=3))




def callback1(attr, old, new):
	plot1.xaxis.axis_label=new
	sourceplt1.data = {'x' : xf[new], 'y': xf[lstval2]}
	global lstval1
	lstval1 = new

	mu, sigma = np.mean(xf[new]), np.std(xf[new])
	

	hist, edges = np.histogram(xf[new], density=True, bins=50)

	x = np.linspace(np.min(xf[new]), np.max(xf[new]), 1000)
	pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
	cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2
	plot2.xaxis.axis_label = new
	plot2.yaxis.axis_label = 'Pr(' + new +')'
	plot4.xaxis.axis_label = new
	plot4.yaxis.axis_label = 'Pr(' + new +')'
	sourceplt2hist.data = { 'left':edges[:-1], 'right':edges[1:], 'hist':hist }
	sourceplt2pdf.data = {'x' : x,  'pdf':pdf }
	sourceplt2cdf.data = {'x' : x,  'cdf':cdf }




def callback2(attr, old, new):
	plot1.yaxis.axis_label=new
	sourceplt1.data = {'x' : xf[lstval1], 'y': xf[new]}
	global lstval2
	lstval2 = new

	mu, sigma = np.mean(xf[new]), np.std(xf[new])
	

	hist, edges = np.histogram(xf[new], density=True, bins=50)

	x = np.linspace(np.min(xf[new]), np.max(xf[new]), 1000)
	pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
	cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2
	plot3.xaxis.axis_label = new
	plot3.yaxis.axis_label = 'Pr(' + new +')'
	plot5.xaxis.axis_label = new
	plot5.yaxis.axis_label = 'Pr(' + new +')'
	sourceplt3hist.data = { 'left':edges[:-1], 'right':edges[1:], 'hist':hist }
	sourceplt3pdf.data = {'x' : x,  'pdf':pdf }
	sourceplt3cdf.data = {'x' : x,  'cdf':cdf }




select1.on_change('value', callback1)
select2.on_change('value', callback2)
button.on_click(update)

widget = widgetbox(text_input, button)

layout = layout([[widget]])

curdoc().add_root(layout)