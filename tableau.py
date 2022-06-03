
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
fig,ax=plt.subplots()

pd.set_option('display.max_columns', None)

path = r"D:/UCD/classes/Business Decision Support System/Tableau/"

filename1 = "flights.csv"
filename2 = "airlines.csv"
filename3 = "airports.csv"
filename4 = "Mapping_Data_Dictionary.xlsx"

flights = pd.read_csv(path + filename1, dtype = {'SCHEDULED_DEPARTURE': 'str', 'DEPARTURE_TIME': 'str', 'SCHEDULED_ARRIVAL': 'str', 'ARRIVAL_TIME': 'str'})
airlines = pd.read_csv(path + filename2)
airports = pd.read_csv(path + filename3)
mapping = pd.read_excel(path + filename4, sheet_name = 'Mapping', usecols = [2, 3])

flights.drop(['TAIL_NUMBER','TAXI_OUT','WHEELS_OFF','SCHEDULED_TIME',\
              'ELAPSED_TIME','WHEELS_ON','TAXI_IN', 'DIVERTED'], axis = 1, inplace = True)

flights['ORIGIN_AIRPORT'] = flights['ORIGIN_AIRPORT'].astype('str')
flights['DESTINATION_AIRPORT'] = flights['DESTINATION_AIRPORT'].astype('str')
mapping['ORIGIN_AIRPORT'] = mapping['ORIGIN_AIRPORT'].astype('str')

flights.dropna(subset = ['DEPARTURE_TIME', 'ARRIVAL_TIME'], inplace = True)
flights['DEPARTURE_TIME'].replace("2400", "0000", inplace = True)
flights['SCHEDULED_ARRIVAL'].replace("2400", "0000", inplace = True)
flights['ARRIVAL_TIME'].replace("2400", "0000", inplace = True)

flights['SCHEDULED_DEPARTURE'] = flights['SCHEDULED_DEPARTURE'].apply(lambda x: datetime.datetime.strptime(x, "%H%M").time())
flights['DEPARTURE_TIME'] = flights['DEPARTURE_TIME'].apply(lambda x: datetime.datetime.strptime(x, "%H%M").time())
flights['SCHEDULED_ARRIVAL'] = flights['SCHEDULED_ARRIVAL'].apply(lambda x: datetime.datetime.strptime(x, "%H%M").time())
flights['ARRIVAL_TIME'] = flights['ARRIVAL_TIME'].apply(lambda x: datetime.datetime.strptime(x, "%H%M").time())

mapping = dict(mapping.values)

flights['ORIGIN_AIRPORT'].replace(mapping, inplace = True)

data = flights.merge(airlines, how = 'left', left_on = 'AIRLINE', right_on = 'IATA_CODE', suffixes=(None, '_long'))

data = data.merge(airports, how = 'left', left_on = 'ORIGIN_AIRPORT', right_on = 'IATA_CODE')

data.rename(columns={'AIRPORT':'AIRPORT_origin_long', \
                     'IATA_CODE_x':'IATA_CODE_airline', \
                         'CITY':'CITY_origin', 'STATE':'STATE_origin', \
                             'LATITUDE':'LATITUDE_origin', \
                                 'LONGITUDE':'LONGITUDE_origin', \
                                     'IATA_CODE_y':'IATA_CODE_airport'}, inplace = True)

data = data.merge(airports, how = 'left', left_on = 'DESTINATION_AIRPORT', right_on = 'IATA_CODE')

data.rename(columns={'AIRPORT':'AIRPORT_destination_long', \
                     'CITY':'CITY_destination', 'STATE':'STATE_destination', \
                         'LATITUDE':'LATITUDE_destination', \
                             'LONGITUDE':'LONGITUDE_destination'}, inplace = True)

data.drop(['IATA_CODE', 'COUNTRY_y', 'COUNTRY_x', 'IATA_CODE_airport'], axis = 1, inplace = True)
                     
data['AIR_SYSTEM_DELAY'].replace(np.nan, 0, inplace = True)
data['SECURITY_DELAY'].replace(np.nan, 0, inplace = True)
data['AIRLINE_DELAY'].replace(np.nan, 0, inplace = True)
data['LATE_AIRCRAFT_DELAY'].replace(np.nan, 0, inplace = True)
data['WEATHER_DELAY'].replace(np.nan, 0, inplace = True)

data.dropna(subset = ['LONGITUDE_destination', 'DEPARTURE_TIME', 'ARRIVAL_DELAY', 'LATITUDE_origin'], inplace = True)

data = data[data['CANCELLED']==0]

data.drop(['CANCELLED', 'CANCELLATION_REASON'], axis = 1, inplace = True)

data['DAY_OF_WEEK'] = data['DAY_OF_WEEK'].map({1:"Sunday", 2:"Monday", 3:"Tuesday", 4:"Wednesday", 5:"Thursday", 6:"Friday", 7:"Saturday"})


"""
col_name = 'WEATHER_DELAY'
IQR = data.describe().loc['75%', col_name] - data.describe().loc['25%', col_name]
upper_extreme = data.describe().loc['75%', col_name] + 1.5*IQR
lower_extreme = data.describe().loc['25%', col_name] - 1.5*IQR
print(data.loc[((data[col_name] > upper_extreme) | (data[col_name] < lower_extreme))])
ax.boxplot(data[col_name])
plt.show()
"""

data.to_csv(path + 'flights_delay_cleaned.csv', encoding = 'utf-8')



