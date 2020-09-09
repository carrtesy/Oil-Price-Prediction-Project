# Oil Price Prediction Project


## Models to evaluate

-  GKFN

| Model  | kernel # | tau | E | SM |  RMSE | R Square |  MAE |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---:|
| Daily | | | | | | | |
| Weekly | | | | | | | |
| Weekly(tau=1) | | | | | | | |
| Monthly (from monthly data) | | | | | | | | 
| Monthly (from weekly data, P = 4) | | | | | | | |
| Monthly (from weekly data, P = 4, tau=1) | | | | | | | |
| Monthly (from weekly data, recursive) | | | | | | | | 
| Weekly (from daily data, augmentation) | | | | | | | |
| Monthly (from daily data, augmentation) | | | | | | | |

- ARIMA

Hyperparameter settings

| Data  | constant(P,D,Q) | no_constant(P,D,Q)|
|---|:---:|:---:|
| Daily | (5,1,3) (3,1,1) (2,1,0) | (2,0,3) |
| Weekly | (3,1,3) (4,1,3) (3,1,2) | (4,0,3) | 
| Monthly | (3,1,1) | (4,0,1) |


Model Performance
| Model  | (P, D, Q) | RMSE | R Square |  MAE |
|---|:---:|:---:|:---:|---:|
| Daily | (5,1,3) | 2.569438 | 0.949691 | 0.9889141 |
| Weekly | (3,1,3) | 2.45381585 | 0.98493735 | 1.69082969 |
| Monthly | (3,1,1) | 6.12858492 | 0.92706412 | 4.67627828 |
