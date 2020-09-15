import ft
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
import pandas as pd
import numpy as np

# ignore warnings
warnings.filterwarnings("ignore")

#mode = "daily"
#mode = "weekly"
mode = "monthly"

dailyfile = open('./daily/wti.csv', 'r')
weeklyfile = open('./weekly/wti_week.csv', 'r')
monthlyfile = open('./monthly/wti_month.csv', 'r')

def readData(inputfile, startdate, enddate):
    print("Reading dataset: [", startdate, ' ~ ' , enddate , "]")
    f = inputfile
    df = pd.read_csv(f, delimiter = ",", names=['date','values'], header=0)
    threshold=[]
    start=0
    for i in range(len(df.index)):
        if (start == 0) :
            if (startdate == df.date[i]):
                threshold.append(i)
                start=1
            else:
                continue
        else:
            if (enddate == df.date[i]):
                threshold.append(i)
                break
            else:
                continue
    data = pd.DataFrame(data=df.values[threshold[0]:threshold[1],1], dtype=np.float16)
    f.close()
    return data

if(mode == "daily"): # Daily
    print("===DAILY DATASET===")
    data = readData(dailyfile, '2000-01-03', '2020-08-31')
elif(mode == "weekly"): # Weekly_original
    print("===WEEKLY DATASET===")
    data = readData(weeklyfile, '1986-01-10', '2020-08-28')

elif(mode == "monthly"): # Monthly
    print("===MONTHLY DATASET===")
    data = readData(monthlyfile, '1960-01-01', '2020-08-01')
'''
# hyperparmeters
test_ratio = 0.2
ARIMA_order = (3,1,3)

# train / test split
test_size = int(len(data) * test_ratio)
print("size of dataset:", len(data))
print("size of test dataset:", test_size)

#train, extra, test = data[:-test_size-3], data[-test_size-3:-3], data[-test_size:]
train, test = data.values[:-test_size], data.values[-test_size:]

# evaluate models
history = [x for x in train]
print(history[:][0])
predictions = list()

model = ARIMA(history, order=ARIMA_order)
model_fit = model.fit(disp=0, trend='nc')
print(model_fit.summary())
fc, se, conf = model_fit.forecast(len(test), alpha=0.05)

test = pd.Series(test.reshape(test_size), index=range(len(data)-test_size, len(data)))
fc_series = pd.Series(fc, index=range(len(data)-test_size, len(data)))
lower_series = pd.Series(conf[:, 0], index=range(len(data)-test_size, len(data)))
upper_series = pd.Series(conf[:, 1], index=range(len(data)-test_size, len(data)))

plt.figure(figsize=(12,5), dpi=100)
plt.plot(train, label='training')
plt.plot(test, label='actual')
plt.plot(fc_series, label='forecast')
plt.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.15)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.savefig("weekly_ARIMA.png")
plt.show()

# Save
df2 = pd.DataFrame()
df2["Estimate"] = pd.Series(fc_series)
df2["Value"] = pd.Series(test)
df2.to_csv("weekly_ARIMA.csv", index=False)
'''
plt.figure(figsize=(12,5), dpi=100)
plt.plot(data, label='dataset')
plt.title('WTI oil price_monthly')
plt.savefig("oilprice.png")
plt.show()
