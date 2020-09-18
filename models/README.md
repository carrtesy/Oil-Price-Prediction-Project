# Oil Price Prediction Project
## New Version

### Smoothness Measure
- daily
    
    ![daily](./daily/sm_3d.png)
- weekly

    ![weekly](./weekly/sm_3d.png)
- monthly
    
    ![monthly](./monthly/sm_3d.png)
        

### Models to evaluate

-  GKFN

| Model  | kernel # | tau | E | SM |  RMSE | R Square |  MAE |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Daily |  |  |  |  |  |  |  |
| *Weekly* | 85 | 1 | 7 | 0.039365 | 3.276904 | 0.973138 | 2.231803 |
| Monthly (from monthly data) | 7 | 1 | 6 | 0.127713 | 50.732332 | -3.976902 | 36.233607 |
| Monthly (from weekly data, P = 4) | 21 | 4 | 5 | 0.062536 | 7.580696 | 0.856241 | 5.441237 |
| Monthly (from weekly data, P = 4, tau=1) | 55 | 1 | 10 | 0.131003 | 7.498386 | 0.859346 | 5.305326 |
| Monthly (from weekly data, recursive) | 35 | 1 | 6 | 0.039665 | 7.160154 | 0.871749 | 5.282052 | 
| Weekly (from daily data, augmentation) | 8 | 1 | 6 | 0.223460 | 5.157231 | 0.797327 | 3.303789 |
| Monthly (from daily data, augmentation) | 28 | 1 | 5 | 0.163670 | 7.535780  | 0.567268 | 5.051230 |

- ARIMA

Hyperparameter settings

| Data  | constant(P,D,Q) | no_constant(P,D,Q)|
|---|:---:|:---:|
| Daily | (6,1,3) (3,1,1) | (5,1,3) (6,1,3) (1,1,3) |
| Weekly | (3,1,3) (4,1,3) (3,1,2) | (3,1,3) (4,1,3) (3,1,2) | 
| Monthly | (4,1,3) (1,1,3) (1,1,0) | (1,1,3) (1,1,0) |


Model Performance

| Model  | (P, D, Q) | RMSE | R Square |  MAE |
|---|:---:|:---:|:---:|:---:|
| Daily | (3,1,1)c | 2.15923827 | 0.988697 | 0.99930792 |
| Weekly | (3,1,3)nc | 2.45381585 | 0.98493735 | 1.69082969 |
| Monthly | (1,1,0)nc | 5.397045546 | 0.9259493015 | 4.20185773 |
