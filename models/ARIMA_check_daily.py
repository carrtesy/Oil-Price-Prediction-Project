import ft
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
import pandas as pd


# ignore warnings
warnings.filterwarnings("ignore")

mode = "daily"
#mode = "weekly"
#mode = "monthly"

dailyfile = open('./daily/wti.csv', 'r')
weeklyfile = open('./weekly/wti_week.csv', 'r')
#monthlyfile = open('./monthly/wti_month.csv', 'r')

if(mode == "daily"): # Daily
    print("===DAILY DATASET===")
    data = ft.readData(dailyfile, '1986-01-02', '2020-08-30')
elif(mode == "weekly"): # Weekly_original
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
elif(mode == "monthly"): # Monthly
    print("===MONTHLY DATASET===")
    #data = ft.readData(monthlyfile, '1960-01-01', '2020-06-01')

# hyperparmeters
test_ratio = 0.2
##ARIMA_order = (2, 0, 0)

# train / test split
test_size = int(len(data) * test_ratio)
print("size of dataset:", len(data))
print("size of test dataset:", test_size)

train = data

# evaluate models
history = [x for x in train]

predictions = list()

# no constant ARIMA order check
'''
for d in range(2):
    for i in range(1,8):
        for j in range(4):
            try :
                ARIMA_order = (i,d,j)
                model = ARIMA(history, order = ARIMA_order)
                model_fit = model.fit(disp = 0, trend='nc')
                print(model_fit.summary())
                print(model_fit.aic)
            except:
                pass
# (1,0,0) 30667 (1,0,1) 30417 (1,0,2) 30414 (2,0,0) 30437 (2,0,1) 30415 (2,0,2) 30416 (2,0,3) 30409
# (3,0,0) 30415 (3,0,2) 30418 (4,0,1) 30410 (7,0,3) 30406 (1,1,0) 30426 (1,1,1) 30404 (1,1,3) 30399
# (2,1,0) 30404 (3,1,1) 30399 (5,1,3) 30386 (6,1,3) 30395

#(6,1,3)>(5,1,3)>(1,1,3)

'''


# constant ARIMA order check
print("-----constant-----")
for d in range(2):
    for i in range(7):
        for j in range(4):
            try:
                ARIMA_order = (i,d,j)
                model = ARIMA(history, order = ARIMA_order)
                model_fit = model.fit(disp = 0,trend='c')
                print(model_fit.summary())
                print(model_fit.aic)
            except:
                pass
# (1,0,0) 30644 (1,0,1) 30416 (1,0,2) 30413 (2,0,0) 30435 (2,0,1) 30413 (2,0,3) 30406 (3,0,0) 30413 (4,0,1) 30409
# (1,1,0) 30428 (1,1,3) 30401 (2,1,0) 30406 (3,1,1) 30401 (4,1,1) 30403 (5,1,3) 30388 (6,1,3) 30397

# (5,1,3) > (6,1,3) > (3,1,1) > (4,1,1)
