import numpy as np
import numpy.linalg as lin
import ft as ft
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sys
import copy

def get_kernel_info(trX, trY, teX, teY, alpha, kernel_num_bdd):
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

    kernelnums = []
    trainerr = []
    validerr = []

    # training with increasing kernel numbers
    while(True):
        if m > kernel_num_bdd:
            break

        err, rmse, rsq, mae = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
        terr, trmse, trsq, trmae = ft.loss(teX, teY, kernelMeans, kernelSigma, kernelWeights)
        log.write(format('train: Phase1 : m = %d, rmse = %f, rsq = %f \nvalidation Phase1 : m = %d, rmse = %f, rsq = %f\n') % (m, rmse, rsq, m, trmse, trsq))
        print(format('train: Phase1 : m = %d, rmse = %f, rsq = %f \nvalidation Phase1 : m = %d, rmse = %f, rsq = %f\n') % (m, rmse, rsq, m, trmse, trsq))
        trainerr.append(rmse)
        validerr.append(trmse)
        kernelnums.append(m)

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
    plt.plot(kernelnums, trainerr, 'r')
    plt.plot(kernelnums, validerr, 'b')
    plt.legend(["Training Error", "Validation Error"])
    plt.xticks(np.arange(0, 100, 5))
    plt.savefig('./plot.png')
    plt.show()

    # return kernel with minimum validation error, and other kernel parameters
    # training error should be more than confintmin
    minkernelnum = 2
    minerr = sys.float_info.max
    for n in range(len(kernelnums)):
        if(trainerr[n] < confintmin):
            break # prevent overfitting
        if(validerr[n] < minerr):
            minkernelnum = kernelnums[n]
            minerr = validerr[n]

    print("Kernel number that minimizes validerr: {}, err: {}".format(minkernelnum, minerr))
    return minkernelnum, kernelMeans, kernelSigma, kernelWeights

def train(data, trX, trY, teX, teY, te_index,
          epochs, num_kernels,
          kernelMeans, kernelSigma, kernelWeights, tau, E, P, target_P, mode):

    """model training"""
    log = open('./log.txt', 'w')
    '''
        phase 2 & phase 3
        learning kernel parameter
    '''

    # init
    kernelMeans = kernelMeans[:num_kernels]
    kernelSigma = kernelSigma[:num_kernels]
    kernelWeights = kernelWeights[:num_kernels]

    # history
    epochs_arr = []
    training_err = []
    testing_err = []
    max_rsq = 0
    best_kernelMeans = None
    best_kernelSigma = None
    best_kernelWeights = None
    best_epoch = None
    best_Yest = None
    f = open('result.txt', 'w')

    for epoch in range(1, epochs+1):
        # phase 2
        B = np.identity(num_kernels)

        for i in range(len(trX)):
            x = trX[i]
            y = trY[i]
            e = y - ft.output(x, kernelMeans, kernelSigma, kernelWeights)

            if i % 100 == 0 :
                err, rmse, rsq, mae = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
                log.write(format('Phase 2 step rmse = %f, rsq = %f\n') % (rmse, rsq))

            B, kernelSigma = ft.Phase2(x, y, e, num_kernels, B, kernelMeans, kernelSigma, kernelWeights)

        # phase 3
        B = np.identity(num_kernels)

        for i in range(len(trX)):
            x = trX[i]
            y = trY[i]
            e = y - ft.output(x, kernelMeans, kernelSigma, kernelWeights)

            if i % 100 == 0:
                err, rmse, rsq, mae = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
                log.write(format('Phase 3 step rmse = %f, rsq = %f\n') % (rmse, rsq))

            B, kernelWeights = ft.Phase3(x, y, e, num_kernels, B, kernelMeans, kernelSigma, kernelWeights)

        err, rmse, rsq, mae = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
        terr, trmse, trsq, trmae = ft.loss(teX, teY, kernelMeans, kernelSigma, kernelWeights)
        print("EPOCH {}: training r2 {}, test r2 {}".format(epoch, rsq, trsq))

        if epoch == 1:
            max_rsq = trsq
            best_epoch = epoch
            best_kernelMeans = kernelMeans
            best_kernelSigma = kernelSigma
            best_kernelWeights = kernelWeights

        # check epoch 75 150 300
        if epoch == 75 or epoch == 150 or epoch == 300:

            Yest, termse, tersq, temae = evaluate(data, teX, teY, te_index, kernelMeans,
                                                    kernelSigma, kernelWeights, tau, E, P, target_P, mode)
            print("Evaluation {}: rmse {} r2 {},MAE {}".format(epoch, termse, tersq, temae))
            f.write(format('epoch : %d, rmse: %f, R2: %f, MAE: %f') % (epoch, termse, tersq, temae) + '\n')

            # update kernel if it is best
            # metric is rsq
            if (tersq > max_rsq):
                max_rsq = tersq
                best_Yest = Yest
                best_epoch = epoch
                best_kernelMeans = kernelMeans
                best_kernelSigma = kernelSigma
                best_kernelWeights = kernelWeights

    f.close()
    print("EPOCH {} selected.".format(best_epoch))
    log.close()
    return best_Yest, num_kernels, best_kernelMeans, best_kernelSigma, best_kernelWeights, best_epoch

def updateWeights(X, y, num_kernels, kernelMeans, kernelSigma, kernelWeights, loop):
    for i in range(loop):
    # phase 2
        B = np.identity(num_kernels)
        e = y - ft.output(X, kernelMeans, kernelSigma, kernelWeights)
        B, kernelSigma = ft.Phase2(X, y, e, num_kernels, B, kernelMeans, kernelSigma, kernelWeights)


    # phase 3
        B = np.identity(num_kernels)
        e = y - ft.output(X, kernelMeans, kernelSigma, kernelWeights)
        B, kernelWeights = ft.Phase3(X, y, e, num_kernels, B, kernelMeans, kernelSigma, kernelWeights)

    return kernelMeans, kernelSigma, kernelWeights

def predict(X, kernelMeans, kernelSigma, kernelWeights):
    n = len(X)
    Yest = []
    for i in range(n):
        Yest.append(ft.output(X[i], kernelMeans, kernelSigma, kernelWeights))
    return Yest

def rolling_forecast(teX, teY, num_kernels, kernelMeans, kernelSigma, kernelWeights):
    """
    model test, rolling forecast
    """

    # forecast and update
    n = len(teX)
    Yest = []

    for i in range(n):
        # forecast
        Yhat = ft.output(teX[i], kernelMeans, kernelSigma, kernelWeights)
        Yest.append(Yhat)
        # update
        kernelMeans, kernelSigma, kernelWeights = \
            updateWeights(teX[i], teY[i],
                          num_kernels,
                          kernelMeans, kernelSigma, kernelWeights)

    # evaluate
    err, rmse, rsq, mae = ft.loss_with_prediction_array(teY, Yest)

    return Yest, rmse, rsq, mae

def predict(X, kernelMeans, kernelSigma, kernelWeights):
    # vector prediction
    if(isinstance(X[0], list)):
        n = len(X)
        Yest = []
        for i in range(n):
            Yest.append(ft.output(X[i], kernelMeans, kernelSigma, kernelWeights))
        Yest = np.array(Yest)
        return Yest
    # scalar prediction
    else:
        return ft.output(X, kernelMeans, kernelSigma, kernelWeights)

def evaluate(data, teX, teY, index_arr,
             kernelMeans, kernelSigma, kernelWeights,
             tau, E, original_P, target_P, mode):

    """model test"""
    print("== EVALUATE ==")
    f = open('result.txt', 'w')

    # recursive application
    assert(target_P % original_P == 0) # check if target P can be achieved using n step applications of interval original_P
    gap = target_P - original_P
    loop = gap + 1
    print("Iterative Application for {} times".format(loop))

    Y_hat = []
    print(len(teX))
    for idx, x_element in enumerate(teX):
        data_copy = copy.deepcopy(data)
        data_at = index_arr[idx] - gap
        x = x_element
        for i in range(0, loop):
            y_h = predict(x, kernelMeans, kernelSigma, kernelWeights)
            # update value by prediction
            data_copy[data_at] = y_h
            x, data_at = ft.extracting_on_index(tau, E, original_P, data_copy, data_at, mode)
        Y_hat.append(y_h)

    err, rmse, rsq, mae = ft.loss_with_prediction_array(teY, Y_hat)

    return Y_hat, rmse, rsq, mae

def plot_prediction(teY, teYdate, Yest,
                         num_kernels, epoch, formatter, locater):
    """
            plot
        """
    dates = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in teYdate]
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().xaxis.set_major_locator(locater)

    plt.plot(dates, teY, 'r')
    plt.plot(dates, Yest, 'b')
    plt.legend(["Test Data", "Prediction"])
    plt.savefig("./kernel" + str(num_kernels) + "_epoch"+ str(epoch)+"_prediction_graph.png")
    plt.show()
    return
