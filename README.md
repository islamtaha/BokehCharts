# BokehCharts
simple Bokeh app for importing csv data from web or from csv file from local path and do visualization on the data like data distribution, histogram, probaility density function, cumulative density function and scatter plots

## Intsallation:
1- Install conda

2- Install python requirements

$ conda install --yes --file requirements.txt

3- run bokeh server

$ bokeh serve --show bokehCharts.py

## using
1 - go to http://localhost:5006/bokehCharts in the browser


![Alt text](/img1.jpg?raw=true "Title")

2- enter the url for the csv file on the web (eg : https://assets.datacamp.com/production/course_1639/datasets/titanic.csv) or the location of the path of the csv file on the disk (eg : /relative/path/to/test.csv) 

3- the data will be loaded and u can change the variables to visualize

![Alt text](/img2.jpg?raw=true "Title")




