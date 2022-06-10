# Bachelor Thesis - project description

The aim of this Bachelor Project is to model the medicine consumption at Rigshospitalet. 
This is done by connections orders and consumptions of different departments at Rigshospitalet and and analyzinge tendencies, that can be spotted during the data analysis.  

# Project structure
All data used in this project is confidential and must be requested by the contributers. 
It is important that the data files are used in the correct order - some datafiles are generated in other scripts. Scripts that generate new datafiles will be marked in bold, and all files, which use the new datafile will be right right beneath it in cursive. It is only the order of the scipts marked in bold, that is important. The order is as follows:

**Clean_Data.py** <br />
- Generates the datafiles *order_data.csv* and *con_data.csv*<br />

**Sort_Patients_Weekly.py** <br />
- Generates the datafile *patients_arrived.csv*<br />

**Intersection.py** <br />
- Updates *order_data.csv* and *con_data.csv*<br />

**Order_Portions.py** <br />
- Updates *order_data.csv* to get medicine units for each order<br />

**Get_Matching_Names.py** <br />
- Updates *order_data.csv* and *con_data.csv* <br />

**Delete_All_Non_Keys.py** <br />
- Generates updated *order_data.csv* and *con_data.csv* and names the new files *matched_order_data.csv* and *matched_con_data.csv*<br />

**Explore_Data.py** <br />
- Generates barplot of total unit consumptions and orders for each department. <br />

**ABC.py** <br />
- Divides the medicine into classes A, B and C according to the method.  <br />

**Tendencies.py** <br />
- Generates plot of weekly consumptions, orders and patients for medicines. <br />

**Table_Stats.py** <br />
- Generates a summery of the final dataset. <br />

**Descriptive_Statistics.py** <br />
- Generates the descriptive statistics needed for the project.  <br />

**Weighted_Network.ipynb**  <br />
- Generates a connected network between the departments.  <br />

**Correlations1.py** and **Correlations2.py**  <br />
- Generates the correlation coefficients of the data.  <br />







