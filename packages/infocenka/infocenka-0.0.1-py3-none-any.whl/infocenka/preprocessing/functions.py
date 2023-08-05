import pandas as pd

def interquartile_clean(series, w=1.5):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    q3_q1 = q3-q1
    return series.loc[(series> q1-w*q3_q1)&(series< q3+w*q3_q1)]
