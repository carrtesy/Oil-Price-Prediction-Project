# Oil Price Prediction Project

## Dataset Lists & Sources
- [WTI][wti]
  - Daily
  - Dollars per Barrel, Not seasonally adjusted
  - 1986-01-02 ~ 2020-03-13 
  - U.S. Energy Information Administration, Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma [DCOILWTICO], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/DCOILWTICO, March 24, 2020.
- [Brent][brent] 
  - Daily
  - Dollars per Barrel, Not seasonally adjusted
  - 1987-05-20 ~ 2020-03-13
  - U.S. Energy Information Administration, Crude Oil Prices: Brent - Europe [DCOILBRENTEU], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/DCOILBRENTEU, March 24, 2020.
- [Crude Oil Production][crude oil production]
  - Monthly
  - Thousands Barrels per day, including lease condensates
  - 1973-01-01 ~ 2019-11-01
  - separated into Total, OECD, and non-OECD
  - U.S. Energy Information Administration, International; https://www.eia.gov/international/data/world/petroleum-and-other-liquids/monthly-petroleum-and-other-liquids-production, March 30, 2020.
- [OECD Consumption of Petroleum][Petroleum consumption]
    - Monthly
    - Thousands Barrels per day, refined petroleum products
    - 1980-01-01 ~ 2019-11-01
    - U.S. Energy Information Administration, International; https://www.eia.gov/international/data/world/featured-view/2?pd=5&p=0000000000000000000000000000000000000000000000g&u=0&f=M&v=mapbubble&a=-&i=none&vo=value&&t=C&g=0000000000000000000000000000000000o&l=170-0068001c013kg614808a24sg40e10000gig006g0001o00g2gg08&l=171-00280008013kg614808024k000e00000gg8004g0001o00g&s=312854400000&e=1572566400000, March 30, 2020
- [Henry Hub Natural Gas Spot Price][henry hub]
  - Daily
  - Dollars per Million Btu
  - 1997-01-07 ~ 2020-03-17
  - U.S. Energy Information Administration, Natural Gas; https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm, March 30, 2020


[wti]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/DCOILWTICO.csv
[brent]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/DCOILBRENTEU.csv
[crude oil production]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/crudeoil_production1.csv
[Petroleum consumption]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/crudeoil_consumption_OECD_1.csv
[henry hub]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/henryhubnaturalgas.csv

## Dependency
- python 3.8.1
- pandas 1.0.3
- matplotlib 3.1.3
