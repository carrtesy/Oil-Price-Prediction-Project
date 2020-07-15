import numpy as np
import numpy.linalg as lin
import ft as ft
import matplotlib.pyplot as plt

def GKFN(trX, trY, teX, teY, alpha, loop, Kernel_Num) :
    """model training"""
    f = open('./result.txt', 'w')
    log = open('./log.txt', 'w')


    #initial model parameter
    m = 0 # kernelnumber
    kernelMeans = None
    kernelSigma = None
    kernelWeights = None
    invPSI = None

    #initial kernel recruiting

    #첫번쨰 커널, 두번째 커널: y값이 가장 큰 index와 가장 작은 index
    idx1 = np.argmax(trY)
    x1 = trX[idx1]
    y1 = trY[idx1]
    e1 = y1

    idx2 = np.argmin(trY)
    x2 = trX[idx2]
    y2 = trY[idx2]
    e2 = y2

    m += 2
    kernelWeights = np.array([e1, e2])
    kernelMeans = np.array([x1, x2])

    dist = np.sqrt(np.sum(np.square(x1-x2))) #x1,x2사이 거리
    sig1, sig2 = alpha*dist, alpha*dist
    kernelSigma = np.array([sig1, sig2])
    initial_PSI = None
    initial_PSI = np.ndarray(shape=(2,2))
    initial_PSI[0][0] = ft.GaussianKernel(x1,kernelMeans[0],sig1)
    initial_PSI[0][1] = ft.GaussianKernel(x1,kernelMeans[1],sig2)
    initial_PSI[1][0] = ft.GaussianKernel(x2,kernelMeans[0],sig1)
    initial_PSI[1][1] = ft.GaussianKernel(x2,kernelMeans[1],sig2)

    invPSI = lin.inv(initial_PSI)
    init_y = np.array([y1,y2])
    kernelWeights = np.matmul(invPSI, init_y)


    #Phase 1
    estv = ft.EstimatedNoiseVariance(trY)
    # print(np.sqrt(estv))

    trainerr = []
    validerr = []

    # 커널 수를 늘려가며 학습을 합니다.
    while(True):
        err, rmse, rsq = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
        terr, trmse, trsq = ft.loss(teX, teY, kernelMeans, kernelSigma, kernelWeights)
        log.write(format('train: Phase1 : m = %d, rmse = %f, rsq = %f \nvalidation Phase1 : m = %d, rmse = %f, rsq = %f\n') % (m, rmse, rsq, m, trmse, trsq))
        print(format('train: Phase1 : m = %d, rmse = %f, rsq = %f \nvalidation Phase1 : m = %d, rmse = %f, rsq = %f\n') % (m, rmse, rsq, m, trmse, trsq))
        trainerr.append(rmse)
        validerr.append(trmse)

        if m > Kernel_Num:
            break
    #    if (rmse**2) < estv:
    #        break
    #    if rsq > 0.9:
    #        break
    ##    if np.abs(temp-rsq) < 1e-5:
    #        break
    #
    #    temp = rsq

        if m % 10 == 0:
            print(m)

        idx = np.argmax(np.abs(err), axis=0)

        x = trX[idx]
        y = trY[idx]
        e = err[idx]

        m, kernelMeans, kernelSigma, kernelWeights, invPSI = ft.Phase1(x, y, e, m, alpha, kernelMeans, kernelSigma, kernelWeights, invPSI)


    ## 커널수에 따른 에러
    confintmax, confintmin = ft.EstimatedNoiseVariance(trY)
    print(confintmax)
    print(confintmin)
    plt.plot(trainerr,'r')
    plt.plot(validerr,'b')
    plt.legend(["Training Error", "Validation Error"])
    plt.xticks(np.arange(0,100,5))#x축 눈금
    plt.savefig('./plot.png')
    plt.show()

    f.write(format("Confidence Interval: [%f, %f]") % (confintmin, confintmax) + '\n')

    # 커널 몇개를 할것인가?
    #m = 45 # daily
    #m = 28 # weekly
    #m= 30 #weekly_tau1
    m = 73 #monthly_from_weekly_using_tau1
    #m = 35  # monthly from monthly data
    #m = 28 # monthly from weekly data

    kernelMeans = kernelMeans[:m]
    kernelSigma = kernelSigma[:m]
    kernelWeights = kernelWeights[:m]

    #Phase 2 & Phase3 : kernel parameter 학습
    for i in range(loop):
        B = None
        B = np.identity(m)

        for i in range(len(trX)):
            x = trX[i]
            y = trY[i]
            e = y - ft.output(x, kernelMeans, kernelSigma, kernelWeights)

            if i % 100 == 0 :
                err, rmse, rsq = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
                log.write(format('Phase 2 step rmse = %f, rsq = %f\n') % (rmse, rsq))
                print(format('Phase 2 step rmse = %f, rsq = %f') % (rmse, rsq))

            B, kernelSigma = ft.Phase2(x, y, e, m, B, kernelMeans, kernelSigma, kernelWeights)

        B = None
        B = np.identity(m)

        for i in range(len(trX)):
            x = trX[i]
            y = trY[i]
            e = y - ft.output(x, kernelMeans, kernelSigma, kernelWeights)

            if i % 100 == 0:
                err, rmse, rsq = ft.loss(trX, trY, kernelMeans, kernelSigma, kernelWeights)
                log.write(format('Phase 3 step rmse = %f, rsq = %f\n') % (rmse, rsq))
                print(format('Phase 3 step rmse = %f, rsq = %f') % (rmse, rsq))

            B, kernelWeights = ft.Phase3(x, y, e, m, B, kernelMeans, kernelSigma, kernelWeights)

    """model test"""

    err, rmse, rsq = ft.loss(teX, teY, kernelMeans, kernelSigma, kernelWeights)
    print(format('rmse: %f, R2: %f') % (rmse, rsq))
    f.write(format('rmse: %f, R2: %f') % (rmse, rsq) + '\n')

    pre = teY - err
    plt.plot(teY, 'r')
    plt.plot(pre, 'b')
    plt.legend(["Test Data", "Prediction"])
    plt.savefig("./kernel" + str(m) + "_prediction_graph.png")
    plt.show()

    log.close()
    f.close()
    return rmse, rsq
