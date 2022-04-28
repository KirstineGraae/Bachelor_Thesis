# Bachelor Thesis - project description

The aim of this Bachelor Project is to model the medicine consumption at Rigshospitalet. 
The code presented in this repository is developed to forecast the orders of different departments at Rigshospitalet. 
This is done by connections orders and consumptions of different departments at Rigshospitalet and developing forecasting models based on the tendencies, which can be spotted during the data analysis. 

# Project structure

It is important that the data files are used in the correct order - some datafiles are generated in other scripts. Scripts that generate new datafiles will be marked in bold, and all files, which use the new datafile will be right right beneath it in cursive. It is only the order of the scipts marked in bold, that is important. The order is as follows:

**Clean_Data.py** <br />
*Explore_Data.py* <br />
*Tendencies.py* 

**Intersection.py** <br />
*Descriptive_statistics.py* <br />

# Need packages

* numpy 
* pandas
* matplotlib.pyplot
* collections





