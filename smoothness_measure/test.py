import GKFN
import ft_monthly

data = ft_monthly.readData('1960-01-01', '2020-06-01')

# 선택된 E, tau 값을 이용하여 데이터를 재구성합니다.
E = 4
tau = 2
P = 1 # P는 몇일 뒤 값을 예측할 지 설정 해주는 parameter입니다. 예를 들어 하루 뒤 값을 예측하는 것이면 P = 1

# train set 및 test set을 구성합니다.
dataX, dataY  = ft_monthly.extracting(tau, E, P, data)
trX = dataX[:-142]
teX = dataX[-142:]
trY = dataY[:-142]
teY = dataY[-142:]

# parameter를 설정하고 학습을 시킵니다.
alpha = 0.5
loop = 5
Kernel_Num = 100

GKFN.GKFN(trX, trY, teX, teY, alpha, loop, Kernel_Num)

