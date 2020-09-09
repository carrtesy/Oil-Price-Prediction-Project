import ft
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
import pandas as pd


# ignore warnings
warnings.filterwarnings("ignore")

#mode = "daily"
#mode = "weekly"
mode = "monthly"

dailyfile = open('./daily/wti.csv', 'r')
weeklyfile = open('./weekly/wti_week.csv', 'r')
monthlyfile = open('./monthly/wti_month.csv', 'r')

if(mode == "daily"): # Daily
    print("===DAILY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-08-30')
elif(mode == "weekly"): # Weekly_original
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
elif(mode == "monthly"): # Monthly
    print("===MONTHLY DATASET===")
    data = ft.readData(monthlyfile, '1960-01-01', '2020-08-01')

# hyperparmeters
test_ratio = 0.2


# train / test split
test_size = int(len(data) * test_ratio)
print("size of dataset:", len(data))
print("size of test dataset:", test_size)

train = data

# evaluate models
history = [x for x in train]

predictions = list()

# no constant ARIMA order check

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
# (1,0,0), (1,0,1) (1,0,2), (2,0,0), (4,0,0), (4,0,1), (1,1,0) (1,1,3), (3,1,1), (4,1,3)

# check AIC
'''
model = ARIMA(history, order=(1,0,0))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3874
model = ARIMA(history, order=(1,0,1))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3777
model = ARIMA(history, order=(1,0,2))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3757
model = ARIMA(history, order=(2,0,0))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3760
model = ARIMA(history, order=(4,0,0))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3757
model = ARIMA(history, order=(4,0,1))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3749
model = ARIMA(history, order=(1,1,0))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3751
model = ARIMA(history, order=(1,1,3))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3749
model = ARIMA(history, order=(3,1,1))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3738
model = ARIMA(history, order=(4,1,3))
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.aic) #3720
'''
#(4,1,3)>(3,1,1)>(1,1,3)


# constant ARIMA order check
print("----constant----")
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
# (1,0,0), (1,0,1), (1,0,2), (2,0,0), (4,0,0), (4,0,1), (4,0,2)

#check AIC
'''
model = ARIMA(history, order=(1,0,0))
model_fit = model.fit(disp=0, trend='c')
print(model_fit.aic) #3873
model = ARIMA(history, order=(1,0,1))
model_fit = model.fit(disp=0, trend='c')
print(model_fit.aic) #3776
model = ARIMA(history, order=(1,0,2))
model_fit = model.fit(disp=0, trend='c')
print(model_fit.aic) #3756
model = ARIMA(history, order=(2,0,0))
model_fit = model.fit(disp=0, trend='c')
print(model_fit.aic) #3758
model = ARIMA(history, order=(4,0,0))
model_fit = model.fit(disp=0, trend='c')
print(model_fit.aic) #3756
model = ARIMA(history, order=(4,0,1))
model_fit = model.fit(disp=0, trend='c')
print(model_fit.aic) #3749
model = ARIMA(history, order=(4,0,2))
model_fit = model.fit(disp=0, trend='c')
print(model_fit.aic) #3750

'''
#(4,0,1)
