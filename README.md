# Oil Price Prediction Project

## Dataset Lists & Sources
### Outputs
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

### Inputs
- [Crude Oil Production][crude oil production]
  - Monthly
  - Thousands Barrels per day, including lease condensates
  - 1973-01-01 ~ 2019-11-01
  - categorized into Total, OECD, and non-OECD
  - U.S. Energy Information Administration, International; https://www.eia.gov/international/data/world/petroleum-and-other-liquids/monthly-petroleum-and-other-liquids-production, March 30, 2020.
- [OECD Consumption of Petroleum][petroleum consumption]
  - Monthly
  - Million Barrels per day
  - 1997-01-01 ~ 2019-11-01
  - U.S. Energy Information Administration, International; https://www.eia.gov/outlooks/steo/data/browser, March 30, 2020.
- [OECD Consumption of Refined Petroleum Products][refined consumption]
    - Monthly
    - Thousands Barrels per day, refined petroleum products
    - 1980-01-01 ~ 2019-11-01
    - U.S. Energy Information Administration, International; https://www.eia.gov/international/data/world, March 30, 2020.
- [Henry Hub Natural Gas Spot Price][henry hub]
  - Daily
  - Dollars per Million Btu
  - 1997-01-07 ~ 2020-03-17
  - U.S. Energy Information Administration, Natural Gas; https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm, March 30, 2020.
- [Rest of the US Tight Oil Production][tight oil]
  - Monthly
  - Million Barrels per day
  - 2020-01-01 ~ 2020-02-01
  - U.S. Energy Information Administration, Petroleum & Other Liquids; https://www.eia.gov/petroleum/data.php#crude, March 30, 2020.
- [Total Stocks of Petroleum and Other Liquids][total stock]
  - Monthly
  - Thousand Barrels
  - categorized into U.S. Ending Stocks of Crude Oil and Petroleum, Crude Oil only, Total Petroleum products, Hydrocarbon Gas Liquids, Natural Gas Liquids, and Residual Fuel Oil
  - 1936-01-01 ~ 2019-12-01
  - U.S. Energy Information Administration, Petroleum & Other Liquids; https://www.eia.gov/dnav/pet/pet_stoc_typ_d_nus_SAE_mbbl_m.htm, March 30, 2020.
- [SPR Stocks of Crude Oil][SPR stock]
  - Monthly
  - Thousand Barrels, U.S. Ending Stocks of Crude Oil in Strategic Petroleum Reserve(SPR)
  - 1977-10-01 ~ 2019-12-01
  - U.S. Energy Information Administration, Petroleum & Other Liquids; https://www.eia.gov/dnav/pet/pet_stoc_typ_d_nus_SAS_mbbl_m.htm, March 30, 2020.
- [non-SPR Stocks of Crude Oil][nonSPR stock]
  - Monthly
  - Thousand Barrels, U.S. Ending Stocks excluding SPR of Crude Oil
  - 1956-01-01 ~ 2019-12-01
  - U.S. Energy Information Administration, Petroleum & Other Liquids; https://www.eia.gov/dnav/pet/pet_stoc_typ_d_nus_SAX_mbbl_m.htm, March 30, 2020.
- [U.S. Supply of Crude Oil][US supply]
  - Monthly
  - Thousand Barrels
  - 1920-01-01 ~ 2019-12-01
  - categorized into US Field Production of Crude Oil, US crude oil imports excluding SPR, and US crude oil SPR imports
  - U.S. Energy Information Administration, Petroleum & Other Liquids; https://www.eia.gov/dnav/pet/pet_cons_psup_dc_nus_mbbl_m.htm, March 30, 2020.

[wti]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/DCOILWTICO.csv
[brent]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/DCOILBRENTEU.csv
[crude oil production]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/crudeoil_production1.csv
[refined consumption]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/OECD_consumption_refinedpetroleum_1.csv
[petroleum consumption]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/OECD_consumption_petroleum_1.csv
[tight oil]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/US-tight-oil-production.csv
[henry hub]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/henryhubnaturalgas.csv
[total stock]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/total_stocks.csv
[SPR stock]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/SPR_stocks.csv
[nonSPR stock]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/Non-SPR_stocks.csv
[US supply]: https://github.com/dongminkim0220/Oil-Price-Prediction-Project/blob/master/dataset/crudeoil_supplysummary.csv

## Dependency
- python 3.8.1
- pandas 1.0.3
- matplotlib 3.1.3
