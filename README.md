# Bachelor Thesis - project description

The aim of this Bachelor Project is to model the medicine consumption at Rigshospitalet. 
The code presented in this repository is developed to forecast the orders of different departments at Rigshospitalet. 
This is done by connections orders and consumptions of different departments at Rigshospitalet and developing forecasting models based on the tendencies, which can be spotted during the data analysis. 

# Project structure

It is important that the data files are used in the correct order - some datafiles are generated in other scripts. Scripts that generate new datafiles will be marked in bold, and all files, which use the new datafile will be right right beneath it in cursive. It is only the order of the scipts marked in bold, that is important. The order is as follows:

**Clean_Data.py** <br />
- Generates the datafiles *order_data.csv* and *con_data.csv*<br />

**sort_patients_weekly.py** <br />
- Generates the datafile *patients_arrived.csv*<br />

**Intersection.py** <br />
- Updates *order_data.csv* and *con_data.csv*<br />

**Order_Portions.py** <br />
- Updates *order_data.csv* to get medicine units for each order<br />

**Get_matching_names.py** <br />
- Updates *order_data.csv* and *con_data.csv* <br />

**Explore_Data.py** <br />
- Generates barplot of total unit consumptions and orders for each department <br />

**Tendencies.py** <br />
- Generates plot of weekly consumptions, orders and patients for each department <br />

**Table_stats.py** <br />
- Generates simple statistics relevant to the project <br />

**Delete_all_non_keys.py** <br />
- Generates updated *order_data.csv* and *con_data.csv* and names the new files *matched_order_data.csv* and *matched_con_data.csv*<br />

# Need packages

* Python3.8 or Python 3.9 (Python 10 can, at the moment, not be used to generate the figures correctly)
* numpy 
* pandas
* matplotlib
* matplotlib.pyplot
* collections
* Pickle
* json
* requests
* re
* bs4
* nltk
* itertools
* networkx
* netwulf
* community
* Seaborn-qqplot
* scipy
* statistics





