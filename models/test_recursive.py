import GKFN
import ft
import pickle

'''
Here we apply
weekly_tau1(best resultweekly_tau1(best result for weekly analysis)
 for weekly analysis)
recursively.

+
add weekly_data+, monthly_data+ using daily data
'''

#mode = "daily"
#mode = "weekly_origin"
#mode = "weekly_tau1"
#mode = "weekly_tau1_for_monthly"
#mode = "monthly"
#mode = "weekly_data+"
mode = "monthly_data+"

dailyfile = open('./daily/wti.csv', 'r')
weeklyfile = open('./weekly/wti_week.csv', 'r')
monthlyfile = open('./monthly/wti_month.csv', 'r')

if(mode == "daily"): # Daily
    print("===DAILY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-03-13')
    E = 5
    tau = 3
elif(mode == "weekly_origin"): # Weekly_original
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-06-26')
    E = 4
    tau = 5
elif(mode == "weekly_tau1"): # Weekly_tau1
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-06-26')
    E = 6
    tau = 1
elif(mode == "weekly_tau1_for_monthly"): # Weekly_tau1
    print("===WEEKLY DATASET===")
    data = ft.readData(weeklyfile, '1986-01-03', '2020-06-26')
    E = 10
    tau = 1
elif(mode == "monthly"): # Monthly
    print("===MONTHLY DATASET===")
    data = ft.readData(monthlyfile, '1960-01-01', '2020-06-01')
    E = 4
    tau = 2
elif(mode == "weekly_data+"): # weekly_data+
    print("===WEEKLY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-03-13')
    E = 5
    tau = 1
elif(mode == "monthly_data+"): # weekly_data+
    print("===MONTHLY DATASET===")
    data = ft.readData(dailyfile, '2000-01-03', '2020-03-13')
    E = 4
    tau = 1

P = 1 # P days/weeks/months after
target_P = 1 # recursive expectation using interval P
gap = target_P - P

dataX, dataY, index = ft.extracting(tau, E, P, data, mode)
test_ratio = 0.3
test_size = int(len(data) * test_ratio)
print("size of dataset:", len(data))
print("size of test dataset:", test_size)

# Train
trX = dataX[:-test_size]
trY = dataY[:-test_size]

# Test
teX = dataX[-test_size:]
teY = dataY[-test_size:]
te_index = index[-test_size:]

# parameter
alpha = 0.5
loop = 5
Kernel_Num = 60


# train or load model
ON_TRAIN = True
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
'''
teX = dataX[-test_size-gap:-gap]
teY = dataY[-test_size:]
te_index = index[-test_size-gap:-gap]
'''
rmse, rsq, mae = GKFN.evaluate(data, teX, teY, te_index, num_kernels, kernelMeans, kernelSigma, kernelWeights, tau, E, P, target_P, mode)