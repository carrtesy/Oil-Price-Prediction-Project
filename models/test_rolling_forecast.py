import GKFN
import ft
import pickle

#mode = "daily"
mode = "weekly_origin"
#mode = "weekly_tau1"
#mode = "weekly_tau1_for_monthly"
#mode = "monthly"
#mode = "weekly_data+"
#mode = "monthly_data+"

dailyfile = open('./daily/wti.csv', 'r')
weeklyfile = open('./weekly/wti_week.csv', 'r')
monthlyfile = open('./monthly/wti_month.csv', 'r')

if(mode == "daily"): # Daily
    print("===DAILY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-08-31')
    E = 7
    tau = 1
elif(mode == "weekly_origin"): # Weekly_original
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
    E = 6
    tau = 1
elif(mode == "weekly_tau1"): # Weekly_tau1
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
    E = 6
    tau = 1
elif(mode == "weekly_tau1_for_monthly"): # Weekly_tau1
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-08-28')
    E = 5
    tau = 4
elif(mode == "monthly"): # Monthly
    print("===MONTHLY DATASET===")
    data = ft.readData(monthlyfile, '1946-01-01', '2020-08-01')
    E = 6
    tau = 1
elif(mode == "weekly_data+"): # weekly_data+
    print("===WEEKLY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-08-31')
    E = 6
    tau = 1
elif(mode == "monthly_data+"): # weekly_data+
    print("===MONTHLY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-08-31')
    E = 5
    tau = 1

P = 1 # P days/weeks/months after
dataX, dataY, _ = ft.extracting(tau, E, P, data,mode)
#test_ratio = 0.3 # for daily/weekly data
test_ratio = 0.2 # for monthly data
test_size = int(len(data) * test_ratio)
print("size of dataset:", len(data))
print("size of test dataset:", test_size)

# Train
trX = dataX[:-test_size]
trY = dataY[:-test_size]

# Test
teX = dataX[-test_size:]
teY = dataY[-test_size:]

# parameter
alpha = 0.5
loop = 5
Kernel_Num = 100

# train or load model
ON_TRAIN = False
model_name = "model_" + mode + "_" + "E" + str(E) + "_" + "tau" + "_" + str(tau) + ".pickle"
if(ON_TRAIN):
    # train model and get hyperparameters
    num_kernels, kernelMeans, kernelSigma, kernelWeights = GKFN.train(trX, trY, teX, teY, alpha, loop, Kernel_Num)
    print("Saving model at file : {}".format(model_name))
    with open(model_name, 'wb') as f:
        pickle.dump([num_kernels, kernelMeans, kernelSigma, kernelWeights], f)
else:
    # load model
    print("Loading model at file : {}".format(model_name))
    with open(model_name, 'rb') as f:
        num_kernels, kernelMeans, kernelSigma, kernelWeights = pickle.load(f)



# evaluate model
rmse, rsq, mae = GKFN.rolling_forecast(teX, teY,
                                       num_kernels,
                                       kernelMeans, kernelSigma, kernelWeights,
                                       loop)