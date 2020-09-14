import numpy as np
import numpy.linalg as lin
import ft as ft
import matplotlib.pyplot as plt
import copy

def train(trX, trY, teX, teY, alpha, loop, Kernel_Num) :
    """model training"""
    log = open('./log.txt', 'w')

    """
        Initializaition
    """
    #initial model parameter

    m = 0 # kernelnumber
    kernelMeans = None
    kernelSigma = None
    kernelWeights = None
    initial_PSI = None
    invPSI = None

    #initial kernel recruiting

    # first / second kernel: indexes of maximum, minimum y
    m += 2 # adding two kernels

    # max
    idx1 = np.argmax(trY)
    x1 = trX[idx1]
    y1 = trY[idx1]
    e1 = y1

    # min
    idx2 = np.argmin(trY)
    x2 = trX[idx2]
    y2 = trY[idx2]
    e2 = y2

    # kernel weights, means, sigma
    kernelWeights = np.array([e1, e2])
    kernelMeans = np.array([x1, x2])
    dist = np.sqrt(np.sum(np.square(x1-x2))) # distance between x1, x2
    sig1, sig2 = alpha*dist, alpha*dist
    kernelSigma = np.array([sig1, sig2])

    # initial_PSI
    initial_PSI = np.ndarray(shape=(2, 2))
    initial_PSI[0][0] = ft.GaussianKernel(x1, kernelMeans[0], sig1)
    initial_PSI[0][1] = ft.GaussianKernel(x1, kernelMeans[1], sig2)
    initial_PSI[1][0] = ft.GaussianKernel(x2, kernelMeans[0], sig1)
    initial_PSI[1][1] = ft.GaussianKernel(x2, kernelMeans[1], sig2)

    # kernel weights
    invPSI = lin.inv(initial_PSI)
    init_y = np.array([y1, y2])
    kernelWeights = np.matmul(invPSI, init_y) # kernelWeights = PSI^-1 * init_y

    """
        Phase 1
    """
    estv = ft.EstimatedNoiseVariance(trY)

    trainerr = []
    validerr = []

    # training with increasing kernel numbers
    while(True):
        err, rmse, rsq, mae = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
        terr, trmse, trsq, trmae = ft.loss(teX, teY, kernelMeans, kernelSigma, kernelWeights)
        log.write(format('train: Phase1 : m = %d, rmse = %f, rsq = %f \nvalidation Phase1 : m = %d, rmse = %f, rsq = %f\n') % (m, rmse, rsq, m, trmse, trsq))
        print(format('train: Phase1 : m = %d, rmse = %f, rsq = %f \nvalidation Phase1 : m = %d, rmse = %f, rsq = %f\n') % (m, rmse, rsq, m, trmse, trsq))
        trainerr.append(rmse)
        validerr.append(trmse)

        if m > Kernel_Num:
            break

        if m % 10 == 0:
            print(m)

        idx = np.argmax(np.abs(err), axis=0)

        x = trX[idx]
        y = trY[idx]
        e = err[idx]

        m, kernelMeans, kernelSigma, kernelWeights, invPSI = ft.Phase1(x, y, e, m, alpha, kernelMeans, kernelSigma, kernelWeights, invPSI)

    # Plot error graph according to kernel numbers
    confintmax, confintmin = ft.EstimatedNoiseVariance(trY)
    print(format("Confidence Interval: [%f, %f]") % (confintmin, confintmax))
    log.write(format("Confidence Interval: [%f, %f]") % (confintmin, confintmax) + '\n')
    plt.plot(trainerr, 'r')
    plt.plot(validerr, 'b')
    plt.legend(["Training Error", "Validation Error"])
    plt.xticks(np.arange(0, 100, 5))
    plt.savefig('./plot.png')
    plt.show()

    '''
        phase 2 & phase 3
        learning kernel parameter
    '''
    # Choose Kernel number here
    #m = 16 # daily*
    #m = 23 # weekly1*
    #m = 62 # weekly2*
    m = 7 # monthly from monthly data
    #m= 30 #weekly_tau1
    #m = 73 #monthly_from_weekly_using_tau1
    #m = 8  # monthly_from_weekly fixed p =4
    #m = 21 #monthly_from_weekly_using_tau1 fixed p =4
    #m = 28  # monthly from monthly data
    #m = 28 # monthly from weekly data
    #m = 28 # weekly_data+, monthly_data+

    # init
    kernelMeans = kernelMeans[:m]
    kernelSigma = kernelSigma[:m]
    kernelWeights = kernelWeights[:m]

    for i in range(loop):
        # phase 2
        B = None
        B = np.identity(m)

        for i in range(len(trX)):
            x = trX[i]
            y = trY[i]
            e = y - ft.output(x, kernelMeans, kernelSigma, kernelWeights)

            if i % 100 == 0 :
                err, rmse, rsq, mae = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
                log.write(format('Phase 2 step rmse = %f, rsq = %f\n') % (rmse, rsq))
                print(format('Phase 2 step rmse = %f, rsq = %f') % (rmse, rsq))

            B, kernelSigma = ft.Phase2(x, y, e, m, B, kernelMeans, kernelSigma, kernelWeights)

        # phase 3
        B = None
        B = np.identity(m)

        for i in range(len(trX)):
            x = trX[i]
            y = trY[i]
            e = y - ft.output(x, kernelMeans, kernelSigma, kernelWeights)

            if i % 100 == 0:
                err, rmse, rsq, mae = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
                log.write(format('Phase 3 step rmse = %f, rsq = %f\n') % (rmse, rsq))
                print(format('Phase 3 step rmse = %f, rsq = %f') % (rmse, rsq))

            B, kernelWeights = ft.Phase3(x, y, e, m, B, kernelMeans, kernelSigma, kernelWeights)

    log.close()
    return m, kernelMeans, kernelSigma, kernelWeights

def predict(X, kernelMeans, kernelSigma, kernelWeights):
    n = len(X)
    Yest = []
    for i in range(n):
        Yest.append(ft.output(X[i], kernelMeans, kernelSigma, kernelWeights))
    return Yest

def evaluate(data, teX, teY, num_kernels, kernelMeans, kernelSigma, kernelWeights):
    """model test"""
    print("== EVALUATE ==")
    f = open('./result.txt', 'w')

    err, rmse, rsq, mae = ft.loss(teX, teY, kernelMeans, kernelSigma, kernelWeights)
    print(format('rmse: %f, R2: %f') % (rmse, rsq))
    f.write(format('rmse: %f, R2: %f, MAE: %f') % (rmse, rsq, mae) + '\n')

    pre = teY - err
    plt.plot(teY, 'r')
    plt.plot(pre, 'b')
    plt.legend(["Test Data", "Prediction"])
    plt.savefig("./kernel" + str(num_kernels) + "_prediction_graph.png")
    plt.show()

    f.close()
    return rmse, rsq, mae