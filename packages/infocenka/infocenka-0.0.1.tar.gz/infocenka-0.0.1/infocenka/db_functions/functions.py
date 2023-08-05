import psycopg2
import keyring
from sshtunnel import SSHTunnelForwarder
import paramiko
import os
import pandas as pd
import requests
import json
import datetime

def delete_from_armr_db(
        query,
        tunnel_params,
        conn_params):
    try:
        with SSHTunnelForwarder(
                ssh_host = tunnel_params['ssh_host'],
                ssh_username=tunnel_params['ssh_username'],
                ssh_pkey=tunnel_params['ssh_pkey'],
                ssh_port = tunnel_params['ssh_port'],
                remote_bind_address=('127.0.0.1', 5432)) as tunnel:
            conn = psycopg2.connect(
                        host=conn_params['host'],
                        database= conn_params['database'],
                        user=conn_params['ocenka'],
                        password=conn_params['password'],
                        port = tunnel.local_bind_port)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            print('ok')
            conn.close()
            tunnel.close()
    except:
        print("Не удалось")
    finally:
        conn.close()
        tunnel.close()

def get_jsons(tunnel_params, conn_params,
        query ='select activity_json from valuation.export_for_valuation',
        estate_type = None):
    try:
        with SSHTunnelForwarder(
                ssh_host = tunnel_params['ssh_host'],
                ssh_username=tunnel_params['ssh_username'],
                ssh_pkey=tunnel_params['ssh_pkey'],
                ssh_port = tunnel_params['ssh_port'],
                remote_bind_address=tunnel_params['remote_bind_address']
        ) as tunnel:
            conn = psycopg2.connect(
                        host=conn_params['host'],
                        database= conn_params['database'],
                        user=conn_params['user'],
                        password=conn_params['password'],
                        port = tunnel.local_bind_port)
            print('connnection ok')
            cur = conn.cursor()
            cur.execute(query)
            data = list(cur.fetchall())
            if len(data[0])==1:
                data = list(map(lambda x:x[0],data))
            print('ok')
            conn.close()
            tunnel.close()
            if estate_type:
                data = [js for js in data if estate_type in js]
            return(data)
    except Exception as e:
        print(e)
        print("Не удалось")
    finally:
        if conn:
            conn.close()
            tunnel.close()

def get_jsons_from_our_db(
        conn_params,
        query ='select activity_json from public.export_for_valuation',
        estate_type = None):

    """estate_type can be 'apartment', 'house' or 'room'"""
    try:
        conn = psycopg2.connect(
            host=conn_params['host'],
            database=conn_params['database'],
            user=conn_params['user'],
            password=conn_params['password'],
            port = conn_params['port'])

        print('connection: ok')
        cur = conn.cursor()
        cur.execute(query)
        data = list(cur.fetchall())
        if len(data[0])==1:
            data = list(map(lambda x:x[0],data))
        print('get data: ok')
        conn.close()
        if estate_type:
            data =[js for js in data if estate_type in js]
        return(data)
    except:
        print("Не удалось")
    finally:
        if conn is not None:
            conn.close()

def add_to_inform_ocenka_all(tunnel_params,conn_params, data):
    """Добавим оценки
    data: list of tuples (activity_id,
                        modified, preds_knn, preds_rfr, preds_cbr)"""
    try:
        with SSHTunnelForwarder(
                ssh_host = tunnel_params['ssh_host'],
                ssh_username=tunnel_params['ssh_username'],
                ssh_pkey=tunnel_params['ssh_pkey'],
                ssh_port = tunnel_params['ssh_port'],
                remote_bind_address=tunnel_params['remote_bind_address']
                ) as tunnel:

            conn = psycopg2.connect(
                        host=conn_params['host'],
                        database= conn_params['database'],
                        user=conn_params['ocenka'],
                        password=conn_params['password'],
                        port = tunnel.local_bind_port)
            postgres_insert_query = f"""INSERT INTO valuation.inform_ocenka_all
                        (activity_id, modified, preds_knn,\
                         preds_rfr, preds_cbr, credibility)
                        VALUES {data}""".replace('VALUES [', 'VALUES ')[:-1]
            cur = conn.cursor()
            cur.execute(postgres_insert_query)
            conn.commit()
            conn.close()
            tunnel.close()
            return('ok')
    except:
        print("Не удалось")
    finally:
        if conn is not None:
            conn.close()
            tunnel.close()
def add_to_our_inform_ocenka_all(conn_params, data):
    """data: list of tuples (activity_id, modified,
     preds_knn, preds_rfr, preds_cbr)"""
    try:
        conn = psycopg2.connect(
            host=conn_params['host'],
            database=conn_params['database'],
            user=conn_params['user'],
            password=conn_params['password'],
            port = conn_params['port'])
        print('ok')
        postgres_insert_query = f"""INSERT INTO public.export_for_valuation
                    (id, activity_id, modified, activity_json)
                    VALUES {data}""".replace('VALUES [', 'VALUES ')[:-1]

        cur = conn.cursor()
        print('ok')
        cur.execute(postgres_insert_query)
        conn.commit()
        conn.close()
        return('ok')
    except:
        print("Не удалось")
    finally:
        conn.close()
def norm_for_insert(x):
    x = list(x)
    x[1] = str(x[1])
    x[2] = json.dumps(x[2],ensure_ascii=False)
    x = tuple(x)
    return x
def copy_data_to_our_bd(conn_params, tunnel_params_from, conn_params_from):
    """загружаем из БД И.Л. и добавим в нашу базу"""
    if data:
        pass
    else:
        print('load from armr_db...')
        data = get_jsons(tunnel_params_from, conn_params_from)
        data = list(map(norm_for_insert, data))
    s=f"""INSERT INTO public.export_for_valuation (activity_id,\
     modified, activity_json) VALUES (%s,%s,%s)"""
    conn = psycopg2.connect(
        host=conn_params['host'],
        database=conn_params['database'],
        user=conn_params['user'],
        password=conn_params['password'],
        port = conn_params['port'])
    cur = conn.cursor()
    fail=0
    print('add to our table...')
    for i in range(1):
        try:
            cur.execute(s, data[i])
        except:
            fail+=1
    print('УСПЕШНО ДОБАВИЛИ')
    print(f'не удалось дабавить {fail}')
    conn.commit()
    conn.close()
