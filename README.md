# Pittsburgh Yelp Review Count Repository:
This repository includes data and files used in predicting the Yelp review count in Pittsburgh PA, and relevant files to push to Heroku. 

+ ### data: 

	+ datacleaning: includes several jupyter notebooks and .csv files. 
	
		+ DataLoading_Formatting.ipynb read in data, clean data and format data for analysis. 
	
		+ PGH_Bokeh.ipynb plots map view of review counts. 
	
		+ SARIMA_All_Neighbors.ipynb fits seasonal arima model for each neighborhood. 
	
		+ The .csv files inside this folder are output after running the scripts. 
	
	+ dataforheroku: includes data files used in the Heroku app. 
	
	
+ ### static: includes style sheets and images for creating the website
+ ### templates: html file for the webpage. 

+ app.py: Flask app that gets results from the plotting scripts and renders the webpage.
+ create_figure.py: creates the map view of percentage of monthly reviews at each neighborhood.
+ ts_plotting.py: creates plot showing the time series of review counts. 
+ conda-requirements: includes packages that are needed to deploy the website through heroku.
