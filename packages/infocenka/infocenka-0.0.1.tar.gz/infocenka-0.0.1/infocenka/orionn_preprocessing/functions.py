import os
import json
import pandas as pd
import numpy as np
from catboost import CatBoost
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import pickle
from tqdm import tqdm_notebook
MODULE_DIR = os.path.dirname(__file__)
TRAIN_EXAMPLE_PATH =  os.path.join(MODULE_DIR, 'temp_train_test_data/trainx_1example.xlsx')
ONE_HOT_ENC_PATH = os.path.join(MODULE_DIR, 'Models/OneHotEncoder/sten_rayon_metro_Encoder_pickle')
MIN_MAX_SCALLER_PATH = os.path.join(MODULE_DIR, 'Models/MinMaxScaler/MinMaxScaller')
KNN_PATH = os.path.join(MODULE_DIR, 'Models/KNearestNeighbours/knnr_pickle')#knn_pickle1
RFR_PATH = os.path.join(MODULE_DIR, 'Models/RandomForest/RandomForestRegressor')#RandomForestRegressor
CBR_PATH = os.path.join(MODULE_DIR, 'Models/CatBoost/Catboost_model_cat_features')

COORD_PATH = os.path.join(MODULE_DIR, 'Models/russian_city_geos.xlsx')

ID_CITY_DICT = os.path.join(MODULE_DIR, 'helpers/spravochnik/id_city_dict.json')#knn_pickle1
ID_METRO_DICT = os.path.join(MODULE_DIR, 'helpers/spravochnik/id_metro_dict.json')#RandomForestRegressor
ID_DISTRICT_DICT = os.path.join(MODULE_DIR, 'helpers/spravochnik/id_district_dict.json')
ID_STEN_DICT = os.path.join(MODULE_DIR, 'helpers/spravochnik/id_sten_dict.json')
POST_FILES_DIR = os.path.join(MODULE_DIR, 'helpers/post_files/')

with open(ID_CITY_DICT, 'r') as f:
    ID_CITY_DICT = json.load(f)
with open(ID_METRO_DICT, 'r') as f:
    ID_METRO_DICT = json.load(f)
with open(ID_DISTRICT_DICT, 'r') as f:
    ID_DISTRICT_DICT = json.load(f)
with open(ID_STEN_DICT, 'r') as f:
    ID_STEN_DICT = json.load(f)
REAL_ESTATE_TYPE_ID = {'1':'Квартира','2':'Комната','3':'Дом'}

COORD = pd.read_excel(COORD_PATH)
COORD = dict(zip(COORD['city_name'].values, COORD[['latitude', 'longitude']].values.tolist()))
with open(RFR_PATH, 'rb') as f:
    RFR = pickle.load(f)
with open(KNN_PATH, 'rb') as f:
    KNN = pickle.load(f)
CBR = CatBoost()
CBR.load_model(CBR_PATH)
def preprocessing1(df, city = 'Нижний Новгород'):
    df.drop('Город',axis=1, inplace=True)
    print(df.shape)
    df = df[['activity_id', #'Год создания',
             'Долгота', 'Широта','Жилая площадь, кв.м','Количество комнат',
             'Материал стен', 'Общая площадь, кв.м', 'Площадь кухни, кв.м',
        'Район', 'Станция метро', 'Этаж', 'Этажность', 'Удельная стоимость'
           ]]
    return(df)
def preproc_for_knn(
                    data,
                    fit_encoder = False,
                    fit_scaller = False,
                    one_hot_enc_save_path ='sten_rayon_metro_Encoder_pickle',
                    min_max_scaler_save_path='MinMaxScaller'
                    ):
    data = data.drop_duplicates(subset = list(data.columns))
    if fit_encoder:
        enc = OneHotEncoder()
        enc.fit(data[['Материал стен', 'Район', 'Станция метро']].values)
        with open(one_hot_enc_save_path,'wb') as f:
            pickle.dump(enc, f)
        print('encoder saved...')
    else:
        with open(ONE_HOT_ENC_PATH,'rb') as f:
            enc = pickle.load(f)
    print(data.shape)

    enc_data = enc.transform(data[['Материал стен', 'Район', 'Станция метро']].values).toarray()
    print(enc_data.shape)
    enc_data = pd.DataFrame(enc_data, columns = enc.get_feature_names(), index=data.index)


    data.drop(['Материал стен', 'Район', 'Станция метро'],axis=1, inplace=True)
    data = pd.concat([data,enc_data], axis=1)

    y = data['Удельная стоимость'].copy()
    index = data['activity_id'].copy()
    data = data.drop(['activity_id','Удельная стоимость'], axis=1)

    if fit_scaller:
        scaler =  MinMaxScaler()
        scaler.fit(data)
        with open(min_max_scaler_save_path, 'wb') as f:
            pickle.dump(scaler, f)
        print('min_max_scaler saved...')
    else:
        with open(MIN_MAX_SCALLER_PATH, 'rb') as f:
            scaler = pickle.load(f)


    data = pd.DataFrame(scaler.transform(data), columns = data.columns, index = data.index)
    data.insert(0, 'activity_id', index.values)
    print(data.shape)
    return(data, y)
def json_to_df1(js, parse_more_features=False):
    df = pd.DataFrame()
    for obj in tqdm_notebook(js):
        d = {}
        if parse_more_features:
            try:
                d['Выстоа потолков'] = obj['apartment']['ceiling_height']
            except:
                d['Выстоа потолков'] = None
            try:
                d['Год постройки от'] = obj['apartment']['building_year_from']
            except:
                d['Год постройки от'] = None
            try:
                d['Год постройки до'] = obj['apartment']['building_year_to']
            except:
                d['Год постройки до'] = None
            try:
                d['Кол-во лифтов'] = obj['apartment']['lift_passenger_qty']
            except:
                d['Кол-во лифтов'] = None
            try:
                d['Зона _id'] = obj['real_estate']['ag_zone_id']
            except:
                d['Зона _id'] = None
        try:
            d['activity_id'] = obj['activity']['activity_id']
            if d['activity_id']==None:
                d['activity_id'] = -1
        except:
            d['activity_id'] = -1
        try:
            #На самом деле перевый эл. в списке это долгота а вторая широта
            lat, lon =  list(map(lambda x: float(x) if isinstance(x,str) else x, obj['real_estate']['ag_coordinates']))#Широта, долгота
        except:
            lat, lon = None, None
        d['Широта'] = lat
        d['Долгота'] = lon

        try:
            d['Тип недвижимости'] = REAL_ESTATE_TYPE_ID[str(obj['real_estate']['real_estate_type_id'])]
        except:
            d['Тип недвижимости'] = None
        try:
            d['Общая площадь, кв.м'] = obj['apartment']['area_total']
        except:
            d['Общая площадь, кв.м'] = None
        try:
            d['Жилая площадь, кв.м'] = obj['apartment']['area_living']
        except:
            d['Жилая площадь, кв.м'] = None
        try:
            d['Площадь кухни, кв.м'] = obj['apartment']['area_kitchen']
        except:
            d['Площадь кухни, кв.м'] = None

        try:
            d['Этажность'] = obj['apartment']['floors_qty']
        except:
            d['Этажность'] =None
        try:
            d['Этаж'] = obj['apartment']['floor_from']
        except:
            d['Этаж'] =None
        try:
            d['Количество комнат'] = obj['apartment']['room_qty_id']-1
        except:
            d['Количество комнат'] = None
        try:
            d['Материал стен'] = ID_STEN_DICT[str(obj['apartment']['wall_material_id'])]
        except:
            d['Материал стен'] = None
        try:
            if isinstance(obj['real_estate']['ag_metro_ids'], list):
                d['Станция метро'] = ID_METRO_DICT[str(obj['real_estate']['ag_metro_ids'][0])]
            else:
                d['Станция метро']  = ID_METRO_DICT[str(obj['real_estate']['ag_metro_ids'])]
        except:
            d['Станция метро'] = None
        try:
            d['Район'] = ID_DISTRICT_DICT[str(obj['real_estate']['ag_city_district_id'])]#['ag_region_district_id']
        except:
            d['Район'] = None
        try:
            d['Город'] = ID_CITY_DICT[str(obj['real_estate']['ag_city_or_region_id'])]
        except:
            d['Город'] = None
        try:
            d['Удельная стоимость'] = obj['offer_sale']['price_for_meter']
        except:
            d['Удельная стоимость'] = None
        df = df.append(d, ignore_index=True)
        # df.insert(0, 'activity_id',  range(len(df)))

        df['activity_id'] = df['activity_id'].astype(int)
        df = df.drop_duplicates(subset=df.columns)
    return df
