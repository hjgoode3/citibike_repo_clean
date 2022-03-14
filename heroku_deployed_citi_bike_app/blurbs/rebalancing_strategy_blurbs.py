from dash import dcc
logistics_blurb = '''
Citibike has live data on bike availability at every station in their dock network and therefore knows which stations need to be rebalanced in real time. However, moving all of these bikes throughout the day requires knowledge of bike availability ahead of time. Employees need to be in the vicinity of docks that have a surplus of bikes so the bikes can be moved to docks with a bike deficit. To help solve this logistics problem, we have created a tool that can be used by Citibike to plan ahead and have employees located at stations with a predicted high bike availability.
'''

ml_blurb = dcc.Markdown('''
A Random Forest Regressor Model was developed to predict bike availability at each station. 
The model was trained on the last full year of data collected from May 1, 2018 - April 30, 2019. 
Features included in model were day and time, latitude and longitude coordinates, weather data, the number of docks and dock classification for each station. 
Stations were classified using a K-Means Model with distance to nearest central business district, distance to nearest subway, distance to nearest bus stop, borough, and zip code as features. 
Future weather data is only available 48 hours into the future, therefore the model only predicts bike availability for the next 48 hour window. The train and test R^2 values for this model are 0.86 and 0.81, respectively. 
Due to lack of computing capacity, performing a sufficiently exhaustive grid search to tune hyperparameters was not feasible given time constraints. As such, the random forest model over fit the training data.

''')

algorithm_blurb = '''
The user will input a day and time in the next 48-hour window. The model then makes a prediction on the bike availability for every station. The user inputs 5 filters: low availability threshold, high availability threshold, maximum distance, minimum cargo size, and maximum total bikes rebalanced. The low and high availability stations based on the proportion of available bikes are identified. The deficit and surplus bike counts needed to reach a healthy proportion are calculated for each of these stations. Stations with high availability are matched with ones with low availability based on their surplus and deficit bike counts under the constraints of maximum distance, minimum cargo size, and maximum total bikes rebalanced. The results are then output to a table as well as a map for visualization purposes.
'''
