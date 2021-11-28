import pandas as pd
import numpy as np
import statistics

price_df = pd.read_csv('./PricingData.csv')  # read data

# Total Seats Type1
price_df['Total_seats_Type1'] = None
price_df['Seat Fare Type 1'] = price_df['Seat Fare Type 1'].str.split(',')
price_df['Seat Fare Type 1'].fillna(0, inplace=True)
for i in range(0, 30648):
    if(price_df.iloc[i, 0] == 0):
        price_df.iloc[i, 5] = 0
    else:
        price_df.iloc[i, 5] = len(price_df.iloc[i, 0])  # 4

# Total Seats Type2
price_df['Total_seats_Type2'] = None
price_df['Seat Fare Type 2'] = price_df['Seat Fare Type 2'].replace(
    '0', np.nan)
price_df['Seat Fare Type 2'] = price_df['Seat Fare Type 2'].str.split(',')
price_df['Seat Fare Type 2'].fillna(0, inplace=True)
for i in range(0, 30648):
    if(price_df.iloc[i, 1] == 0):
        price_df.iloc[i, 6] = 0
    else:
        price_df.iloc[i, 6] = len(price_df.iloc[i, 1])

# Compute Mean Value on Particular Time & Date
price_df['Seat Fare Type 1 Mean'] = None
for i in range(0, 30648):
    if(price_df.iloc[i, 0] == 0):
        continue
    for j in range(0, len(price_df.iloc[i, 0])):
        price_df.iloc[i, 0][j] = float(price_df.iloc[i, 0][j])
for i in range(0, 30648):
    if(price_df.iloc[i, 0] == 0):
        price_df.iloc[i, 7] = 0
    else:
        price_df.iloc[i, 7] = statistics.mean(price_df.iloc[i, 0])
price_df['Seat Fare Type 2 Mean'] = None
for i in range(0, 30648):
    if(price_df.iloc[i, 1] == 0):
        continue
    for j in range(0, len(price_df.iloc[i, 1])):
        price_df.iloc[i, 1][j] = float(price_df.iloc[i, 1][j])
for i in range(0, 30648):
    if(price_df.iloc[i, 1] == 0):
        price_df.iloc[i, 8] = 0
    else:
        price_df.iloc[i, 8] = statistics.mean(price_df.iloc[i, 1])

# The bus operators with No prices as well as those in both seat fare types
empty_fare = price_df[(price_df['Total_seats_Type1'] == 0)
                      & (price_df['Total_seats_Type2'] == 0)]
uniqueBus = empty_fare['Bus'].unique()
noprice = []
for bus in uniqueBus:
    if((price_df[(price_df['Bus'] == bus)]['Total_seats_Type1'].sum())+(price_df[(price_df['Bus'] == bus)]['Total_seats_Type2'].sum()) == 0):
        noprice.append(bus)
bothprice = []
for bus in price_df['Bus'].unique():
    if((price_df[(price_df['Bus'] == bus)]['Total_seats_Type1'].sum() != 0) & (price_df[(price_df['Bus'] == bus)]['Total_seats_Type2'].sum() != 0)):
        bothprice.append(bus)

# Comparing std dev for seat fare type1
Bus = price_df['Bus'].unique()
Dates = price_df['Service Date'].unique()
std_dev_comp = pd.DataFrame()  # 1
Bus_add = []
Date_add = []
std_add = []
for bus in Bus:  # 2
    for date in Dates:
        std = price_df[(price_df['Bus'] == bus) & (
            price_df['Service Date'] == date)]['Seat Fare Type 1 Mean'].std()
        Bus_add.append(bus)
        Date_add.append(date)
        std_add.append(std)
std_dev_comp['Bus'] = Bus_add
std_dev_comp['Service Date'] = Date_add  # 3
std_dev_comp['std'] = std_add
std_dev_comp['std'] = std_dev_comp['std'].replace(0.0, np.nan)
std_dev_comp.dropna(axis=0, how='any', inplace=True)
Bus2 = std_dev_comp['Bus'].unique()
sample = pd.DataFrame()
score = pd.DataFrame()
score['Bus'] = Bus2
score['score'] = 0.0
for date in Dates:
    sample = std_dev_comp[std_dev_comp['Service Date'] ==
                          date].sort_values('std', axis=0, ascending=True)
    rows = sample.shape[0]
    # Dividing arranged df into 3 & giving score of 10 to 1st 1/3rd with lowest std dev & corr.
    df_1 = sample.iloc[:int(rows/3), :]
    df_2 = sample.iloc[int(rows/3):int(2*rows/3), :]
    df_3 = sample.iloc[int(2*rows/3):, :]
    for bus in df_1['Bus']:
        score.loc[score['Bus'] == bus, 'score'] += 10.0
    for bus in df_2['Bus']:
        score.loc[score['Bus'] == bus, 'score'] += 9.0
    for bus in df_3['Bus']:
        score.loc[score['Bus'] == bus, 'score'] += 8.0
# Total score possible for a bus to calculate %
Total = pd.DataFrame()
Total['Bus'] = score['Bus']
Total['Total_score'] = 0.0
for bus in Total['Bus']:
    Total.loc[Total['Bus'] == bus, 'Total_score'] = (
        std_dev_comp[std_dev_comp['Bus'] == bus].shape[0])*10

# Comparing std dev for seat Type2
Bus_2 = price_df['Bus'].unique()
Dates_2 = price_df['Service Date'].unique()
std_dev_comp_2 = pd.DataFrame()  # 1
Bus_add = []
Date_add = []
std_add = []
for bus in Bus_2:  # 2
    for date in Dates_2:
        std = price_df[(price_df['Bus'] == bus) & (
            price_df['Service Date'] == date)]['Seat Fare Type 2 Mean'].std()
        Bus_add.append(bus)
        Date_add.append(date)
        std_add.append(std)
std_dev_comp_2['Bus'] = Bus_add
std_dev_comp_2['Service Date'] = Date_add  # 3
std_dev_comp_2['std'] = std_add
std_dev_comp_2['std'] = std_dev_comp_2['std'].replace(0.0, np.nan)
std_dev_comp_2.dropna(axis=0, how='any', inplace=True)
Bus3 = std_dev_comp_2['Bus'].unique()
sample = pd.DataFrame()
score_2 = pd.DataFrame()
score_2['Bus'] = Bus3
score_2['score'] = 0.0
for date in Dates:
    sample = std_dev_comp_2[std_dev_comp_2['Service Date']
                            == date].sort_values('std', axis=0, ascending=True)
    rows = sample.shape[0]
    # Dividing arranged df into 3 & giving score of 10 to 1st 1/3rd with lowest std dev & corr.
    df_1 = sample.iloc[:int(rows/3), :]
    df_2 = sample.iloc[int(rows/3):int(2*rows/3), :]
    df_3 = sample.iloc[int(2*rows/3):, :]
    for bus in df_1['Bus']:
        score_2.loc[score_2['Bus'] == bus, 'score'] += 10.0
    for bus in df_2['Bus']:
        score_2.loc[score_2['Bus'] == bus, 'score'] += 9.0
    for bus in df_3['Bus']:
        score_2.loc[score_2['Bus'] == bus, 'score'] += 8.0
# Total score possible for a bus to calculate %
Total_2 = pd.DataFrame()
Total_2['Bus'] = score_2['Bus']
Total_2['Total_score'] = 0.0
for bus in Total_2['Bus']:
    Total_2.loc[Total_2['Bus'] == bus, 'Total_score'] = (
        std_dev_comp_2[std_dev_comp_2['Bus'] == bus].shape[0])*10

# Appending
score = score.append(score_2)
Total = Total.append(Total_2)
score.loc[score['Bus'] == '5580f995d6f4d3bcceca7e2db6c77bf7', 'score'] = 208.0
score.loc[score['Bus'] == 'b74673eaf82c5158c4f76797c938c9a0', 'score'] = 131.0
score.loc[score['Bus'] == 'c0e0a47587fbf6247f4f9a22ba22cc80', 'score'] = 195.0
score.loc[score['Bus'] == '6d364920e6c9f9f71b1d881107e639f0', 'score'] = 128.0
score.loc[score['Bus'] == '241f07f1fafbd5405c0139ae4a148a74', 'score'] = 17.0
score.loc[score['Bus'] == '23c7bd7bcab9a19b7da7cae4e3d4659a', 'score'] = 16.0

Total.loc[score['Bus'] == '5580f995d6f4d3bcceca7e2db6c77bf7',
          'Total_score'] = 260.0
Total.loc[score['Bus'] == 'b74673eaf82c5158c4f76797c938c9a0',
          'Total_score'] = 160.0
Total.loc[score['Bus'] == 'c0e0a47587fbf6247f4f9a22ba22cc80',
          'Total_score'] = 240.0
Total.loc[score['Bus'] == '6d364920e6c9f9f71b1d881107e639f0',
          'Total_score'] = 160.0
Total.loc[score['Bus'] == '241f07f1fafbd5405c0139ae4a148a74', 'Total_score'] = 20.0
Total.loc[score['Bus'] == '23c7bd7bcab9a19b7da7cae4e3d4659a', 'Total_score'] = 20.0
score.drop_duplicates(subset='Bus', inplace=True)
Total.drop_duplicates(subset='Bus', inplace=True)

# Handling no. of dates price posted score
for i in range(0, 76):
    if(Total.iloc[i, 1] < 30):
        score.iloc[i, 1] += 5
    elif((Total.iloc[i, 1] >= 30) & (Total.iloc[i, 1] < 5)):
        score.iloc[i, 1] += 15
    elif((Total.iloc[i, 1] >= 50) & (Total.iloc[i, 1] < 100)):
        score.iloc[i, 1] += 25
    elif((Total.iloc[i, 1] >= 100) & (Total.iloc[i, 1] < 200)):
        score.iloc[i, 1] += 35
    elif(Total.iloc[i, 1] >= 200):
        score.iloc[i, 1] += 50
Total['Total_score'] += 50

# Convert to values in [0,1]
for i in range(0, 76):
    score.iloc[i, 1] = score.iloc[i, 1]/Total.iloc[i, 1]
new_score = score.sort_values(by='score', axis=0)
new_score.reset_index(inplace=True)
new_score.drop('index', axis=1, inplace=True)
output = pd.DataFrame()
output['Bus'] = price_df['Bus'].unique()
output['Follows'] = np.NaN
output['Conf_score1'] = 0.0
output['Is Followed By'] = np.NaN
output['Conf_score2'] = 0.0
bus_list = []
for bus in new_score['Bus'].unique():
    if(bus == '8239a4d7ab3b3de7711c6cb7748229bf' or bus == '1d5363d20e0f4941bdf3084f131938b2'):
        continue
    else:
        bus_list.append(bus)
for bus in bus_list:
    bus_index = new_score.loc[new_score['Bus'] == bus, 'Bus'].index
    follows_index = bus_index+1
    followedby_index = bus_index-1
    output.loc[output['Bus'] == bus, 'Follows'] = new_score.iloc[follows_index.tolist()[
        0], 0]
    output.loc[output['Bus'] == bus,
               'Conf_score1'] = new_score.iloc[follows_index.tolist()[0], 1]
    output.loc[output['Bus'] == bus,
               'Is Followed By'] = new_score.iloc[followedby_index.tolist()[0], 0]
    output.loc[output['Bus'] == bus,
               'Conf_score2'] = new_score.iloc[followedby_index.tolist()[0], 1]
output['Follows'].fillna(
    'No prices listed in input dataset for operator', inplace=True)
output.to_csv('./submission_file.csv')
