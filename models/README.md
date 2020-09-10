# Oil Price Prediction Project


## Models to evaluate

-  GKFN

| Model  | kernel # | tau | E | SM |  RMSE | R Square |  MAE |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---:|
| Daily | | | | | | | |
| Weekly | | | | | | | |
| Weekly(tau=1) | | | | | | | |
| Monthly (from monthly data) | | | | | | | | 
| Monthly (from weekly data, P = 4) | 21 | 4 | 5 | | 7.580696 | 0.856241 | 5.441237 |
| Monthly (from weekly data, P = 4, tau=1) | 55 | 1 | 10 | 0.131003 | 7.498386 | 0.859346 | 5.305326 |
| Monthly (from weekly data, recursive) | 35 | 1 | 6 | 0.039365 | 7.160154 | 0.871749 | 5.282052 | 
| Weekly (from daily data, augmentation) | 8 | 1 | 6 | 0.223460 | 5.157231 | 0.797327 | 3.303789 |
| Monthly (from daily data, augmentation) |  |  |  |  | | | |

- ARIMA

Hyperparameter settings

| Data  | constant(P,D,Q) | no_constant(P,D,Q)|
|---|:---:|---:|
| Daily | (5,1,3) (3,1,1) (2,1,0) | (2,0,3) |
| Weekly | (3,1,3) (4,1,3) (3,1,2) | (4,0,3) | 
| Monthly | (3,1,1) | (4,0,1) |


Model Performance
| Model  | (P, D, Q) | RMSE | R Square |  MAE |
|---|:---:|:---:|:---:|---:|
| Daily | (5,1,3) | 2.569438 | 0.949691 | 0.9889141 |
| Weekly | (3,1,3) | 2.45381585 | 0.98493735 | 1.69082969 |
| Monthly | (3,1,1) | 6.12858492 | 0.92706412 | 4.67627828 |
