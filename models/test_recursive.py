import GKFN_recursive
import ft
import pickle
import matplotlib.dates as mdates
from dateutil.rrule import FR

'''
Here we apply
weekly_tau1(best resultweekly_tau1(best result for weekly analysis)
 for weekly analysis)
recursively.

+
add weekly_data+, monthly_data+ using daily data
'''

'''
import data
'''
#mode = "daily"
#mode = "weekly_origin"
#mode = "weekly_tau1"
#mode = "weekly_tau1_for_monthly"
mode = "monthly"
#mode = "weekly_data+"
#mode = "monthly_data+"

dailyfile = open('./daily/wti.csv', 'r')
weeklyfile = open('./weekly/wti_week.csv', 'r')
monthlyfile = open('./monthly/wti_month.csv', 'r')

if(mode == "daily"): # Daily
    print("===DAILY DATASET===")
    dates, data = ft.readData(dailyfile, '1986-01-02', '2020-08-31')
    E = 7
    tau = 1
elif(mode == "weekly_origin"): # Weekly_original
    print("===WEEKLY DATASET===")
    dates, data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
    E = 6
    tau = 1
elif(mode == "weekly_tau1"): # Weekly_tau1
    print("===WEEKLY DATASET===")
    dates, data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
    E = 6
    tau = 1
elif(mode == "weekly_tau1_for_monthly"): # Weekly_tau1
    print("===WEEKLY DATASET===")
    dates, data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
    E = 5
    tau = 4
elif(mode == "monthly"): # Monthly
    print("===MONTHLY DATASET===")
    dates, data = ft.readData(monthlyfile, '1986-01-01', '2020-08-01')
    E = 6
    tau = 1
elif(mode == "weekly_data+"): # weekly_data+
    print("===WEEKLY DATASET===")
    dates, data = ft.readData(dailyfile, '1986-01-02', '2020-08-31')
    E = 6
    tau = 1
elif(mode == "monthly_data+"): # weekly_data+
    print("===MONTHLY DATASET===")
    dates, data = ft.readData(dailyfile, '1986-01-02', '2020-08-31')
    E = 5
    tau = 1

'''
data preprocessing
'''

P = 1 # P days/weeks/months after
target_P = 4
gap = target_P - P
dataX, dataY, index, dateY = ft.extracting(tau, E, P, data, dates, mode)

test_ratio = 0.2
test_size = int(len(data) * test_ratio)
print("size of dataset:", len(data))
print("size of test dataset:", test_size)

# Train
trX = dataX[:-test_size]
trY = dataY[:-test_size]
trYdate = dateY[:-test_size]

# Test
teX = dataX[-test_size-gap:-gap]
teY = dataY[-test_size:]
teYdate = dateY[-test_size-gap:-gap]
te_index = index[-test_size-gap:-gap]

'''
train
'''
# parameter
alpha = 0.5
EPOCHS = 25
MAX_KERNEL = 100

# train or load model
ON_TRAIN = True
model_name = "model_" + mode + "_" + "E" + str(E) + "_" + "tau" + "_" + str(tau) + ".pickle"
if(ON_TRAIN):
    # train model and get hyperparameters
    print("=== Phase 1: setting kernel numbers ===")
    m, kernelMeans, kernelSigma, kernelWeights = GKFN_recursive.get_kernel_info(trX, trY, teX, teY, alpha, kernel_num_bdd= MAX_KERNEL)

    print("=== Phase 2 & 3: training ===")
    num_kernels, kernelMeans, kernelSigma, kernelWeights =\
        GKFN_recursive.train(trX, trY, teX, teY,
                epochs = EPOCHS, num_kernels= m,
                kernelMeans = kernelMeans, kernelSigma=kernelSigma, kernelWeights=kernelWeights
                )
    print("Saving model at file : {}".format(model_name))
    with open(model_name, 'wb') as f:
        pickle.dump([num_kernels, kernelMeans, kernelSigma, kernelWeights], f)
else:
    # load model
    print("Loading model at file : {}".format(model_name))
    with open(model_name, 'rb') as f:
        num_kernels, kernelMeans, kernelSigma, kernelWeights = pickle.load(f)

'''
evaluate
'''

# plot formatters
formatter = mdates.DateFormatter("%Y-%m-%d") # date format for plotting
locater = mdates.DayLocator(interval = 180) # for daily data
#locater = mdates.WeekdayLocator(byweekday = FR, interval = 26) # weekly
#locater = mdates.MonthLocator(bymonthday = 1, interval = 6) # monthly

rmse, rsq, mae = GKFN_recursive.evaluate(data, teX, teY, teYdate, te_index,
                               num_kernels, kernelMeans, kernelSigma, kernelWeights,
                               tau, E, P, target_P, mode,
                               formatter, locater)