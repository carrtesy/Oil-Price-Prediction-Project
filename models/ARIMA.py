import ft
from statsmodels.tsa.arima_model import ARIMA
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
#weeklyfile = open('./weekly/wti_week.csv', 'r')
#monthlyfile = open('./monthly/wti_month.csv', 'r')

if(mode == "daily"): # Daily
    print("===DAILY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-03-13')
elif(mode == "weekly"): # Weekly_original
    print("===WEEKLY DATASET===")
    #data = ft.readData(weeklyfile, '1986-01-03', '2020-06-26')
elif(mode == "monthly"): # Monthly
    print("===MONTHLY DATASET===")
    #data = ft.readData(monthlyfile, '1960-01-01', '2020-06-01')

# hyperparmeters
test_ratio = 0.3
ARIMA_order = (5, 1, 0)

# train / test split
test_size = int(len(data) * test_ratio)
print("size of dataset:", len(data))
print("size of test dataset:", test_size)

train, test = data[:-test_size], data[-test_size:]

# evaluate models
history = [x for x in train]
predictions = list()

print("=== TESTING ARIMA ==")
for t in range(len(test)):
    model = ARIMA(history, order = ARIMA_order)
    model_fit = model.fit(disp = 0)
    output = model_fit.forecast()
    yhat = output[0][0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)

    # Track the testing process
    print(".", end = "")
    cnt = t + 1
    if(cnt % 100 == 0):
        print("({} / {})".format(t+1, len(test)))
    elif(cnt == len(test)):
        print("({} / {})".format(t+1, len(test)))


print("=== EVALUATE ===")
rmse = mean_squared_error(test, predictions, squared = True)
rsq = r2_score(test, predictions)
mae = mean_squared_error(test, predictions)

print(format('rmse: %f, R2: %f, MAE: %f') % (rmse, rsq, mae))

# Save
df = pd.DataFrame()
df["Estimate"] = pd.Series(predictions)
df["Value"] = pd.Series(test)

print(df.head())

filename = "ARIMA" + "_" + mode + "_" + str(ARIMA_order)
text =  "rmse" + ":" + str(rmse) +  "\n" +\
            "rsq" + ":" + str(rsq) +  "\n" +\
            "mae" + ":" + str(mae)

df.to_csv(filename + ".csv", index=False)

plt.plot(test, 'r')
plt.plot(predictions, 'b')
plt.legend(["Test Data", "Prediction"])
plt.savefig(filename + ".png")
plt.show()

log = open(filename + "_result" + '.txt', 'w')
log.write(text)
log.close()

