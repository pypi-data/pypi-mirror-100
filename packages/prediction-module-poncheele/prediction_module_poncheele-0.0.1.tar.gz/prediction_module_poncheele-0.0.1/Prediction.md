# Prediction Challege

## Description 
The goal of the challenge is to predict the number of bicycle passing between 00:01 AM and 09:00 AM on Friday, April 2nd. To reach this gold we used the data from https://docs.google.com/spreadsheets/d/1ssxsl9AIobDofXFohvwxqCPF0tn6dgXpixhiDzus0iE/edit#gid=59478853. 

## Packages 

```python
import prediction_module as pmd
import pmdarima as pm
import pandas as pd
import datetime
import numpy as np
```

## Data
First let's have a look at the data, for this we need to download it, using the package **dowload**. then show part of the dataframe.

```python
df = pmd.Load_db_predict().save_as_df()
```


<img src="data.png" alt="drawing" width="400"/>

We got a column with the sum of bike passing since first day, and a column with the bike passing between the hour and 00:01 AM. 
The data is a time series with irregular steps. To make it regular, we will work with the bike passing a day. For this we use the methode **df_a_day**

```python
df_day = pmd.df_a_day(df).iloc[:-1, ] # (using completed days)
```
Let's plot it to have an idea of the series

<img src="plot.svg" alt="drawing" width="590"/>


We can see that the series as seasonality, each week we have kind of same pattern.
The forecast plan is to use a SARIMA(p,d,q)x(P,D,Q) model, it's an ARIMA ('Auto Regressive Integrated Moving Average') model with a seasonality component. 

- d is the number of differencing required to make the time series stationary
- p is the order of the ‘Auto Regressive’ (AR) term. It refers to the number of lags of Y to be used as predictors
- q is the order of the ‘Moving Average’ (MA) term. It refers to the number of lagged forecast errors that should go into the ARIMA Model.
- P, D and Q are SAR, order of seasonal differencing and SMA terms respectively


Let’s build the SARIMA model using **pmdarima‘s auto_arima()**. To do that, we need to set seasonal=True, set the frequency m=7 (for week) and enforce D=1 (because we have well defined patterns).

```python
smodel = pm.auto_arima(df_day[0], start_p=1, start_q=1,
                         test='adf',
                         max_p=5, max_q=5, m=12,
                         start_P=0, seasonal=True,
                         d=None, D=1, trace=True,
                         error_action='ignore',  
                         suppress_warnings=True, 
                         stepwise=True)
```

This fonction will find the model with lower AIC. Then with this model we use the **smodel.predict()** method to forecast as far as we want (here to April 2nd).

```python
fitted, confint = smodel.predict(n_periods=n_periods, return_conf_int=True)

```
**fitted** is now a list of our predictions (April 1st and 2nd). Those prediction are for a total day passing, we want the bike passing between 00:01 AM and 09:00 AM, on the plot we could see that in the past last days the number of bike are quite simalar let's have a look. 

<img src="9.png" alt="drawing" width="180"/>

To make our prediction on the good interval, we will look at the median of the proportion between 9 o'clock bike's number and full day. Then apply it a little malus (often statement are made past 9) 

```python
prop_9 = [455.0/1906.0,	318.0/1970.0, 344.0/1580.0,
          358.0/1696.0, 371.0/1891.0, 364.0/1945.0]
print("My prediction :", round(fitted[1] * np.median(np.array(prop_9) * 0.95)))
```
Returns  **"My prediction : 330"**

So my prediction for the number of bicycle passing between 00:01 AM and 09:00 AM on Friday, April 2nd is **330 bikes**.

## Visualisation
At this adress you can find a visualisation of the bike passing count each day on a map.

https://poncheele.github.io/Prediction_velo/
