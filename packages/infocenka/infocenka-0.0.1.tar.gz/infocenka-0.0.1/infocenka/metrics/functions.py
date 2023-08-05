import numpy as np
import pandas as pd
def interquartile_clean(series, w=1.5):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    q3_q1 = q3-q1
    return series.loc[(series> q1-w*q3_q1)&(series< q3+w*q3_q1)]
def mdape(pred, true):
    return(np.median(np.abs(pred - true)/true))
def all_info(preds, testy):

    err=np.abs(preds -testy.values)/testy.values
    res_data = pd.DataFrame({'Удельная цена, руб./кв.м':testy,
                            'Электронная цена':np.round(preds),
                            'APE': err,
                            'Безразмерная цена': preds/testy,
                            'Нижняя граница': np.round(preds - 2*np.median(err)*preds),
                            'Верхняя граница': np.round(preds + 2*np.median(err)*preds),
                                    })
    res_data = np.round(res_data, 3)
    res_data.index = testy.index
    return(res_data)
def get_info_about_score(data):
        score_info = {"MdAPE": round(np.median(data['APE']), 3),
                      "std": round(np.std(data['APE']), 3),
#                       "Часть данных %\n(ошибка <= 10%)":np.round(100*sum(data['Ошибка']<=0.1)/len(data) if len(data)>0 else -1),
#                       "Часть данных %\n(ошибка > 10%)": np.round(100*sum(data['Ошибка']>0.1)/len(data) if len(data)>0 else -1),
#                       "Часть данных %\n(ошибка > 25%)":np.round(100*sum(data['Ошибка']>0.25)/len(data) if len(data)>0 else -1),
#                       "Часть данных %\n(ошибка > 33%)":np.round(100*sum(data['Ошибка']>0.33)/len(data) if len(data)>0 else -1),
                      "Часть данных %\n(ошибка > 30%)":np.round(100*sum(data['APE']>0.30)/len(data) if len(data)>0 else -1),
                      "Кол-во данных": len(data)
                      }
        # print(score_info)
        df_info = pd.DataFrame(score_info, index=range(1))
        return(df_info)
def merge_train_test(train, test):#->MERGE TRAIN ANDE TEST INFOS (CITY,TRAIN_MEDIAN, TEST_MEDIAN, ...)
    dic={}
    train = train.add_suffix('\n(Обучающая)')
    test = test.add_suffix('\n(Тестовая)')
    for i in range(len(train.columns)):
        col_i = 0
        dic[train.columns[i]] = train.iloc[:,i]
        dic[test.columns[i]] = test.iloc[:,i]
        # print(all_inf_train.columns[i])
    res_info = pd.DataFrame(dic)
#     res_info.drop('Город\n(Обучающая)', axis=1,inplace=True)
    return(res_info)
