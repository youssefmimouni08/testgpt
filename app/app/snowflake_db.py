import snowflake.connector
import os
from datetime import datetime
import pytz
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def create_connection_snowflake():
    # connect to Snowflake
    conn = snowflake.connector.connect(
        user=os.environ.get('SNOWFLAKE_USER'),
        password=os.environ.get('SNOWFLAKE_PASSWORD'),
        account=os.environ.get('SNOWFLAKE_ACCOUNT'), #"zv53059.eu-central-1"
    )
    cursor = conn.cursor()
    # define role, database and warehouse
    sql = f"use role {os.environ.get('SNOWFLAKE_ROLE')};"
    cursor.execute(sql)
    sql = f"use database {os.environ.get('SNOWFLAKE_DATABASE')}"
    cursor.execute(sql)
    sql = f"use warehouse {os.environ.get('SNOWFLAKE_WAREHOUSE')}"
    cursor.execute(sql)
    return conn, cursor

def create_schema_table():
    conn, cursor = create_connection_snowflake()
    # create schema
    sql = "create schema if not exists CHATGPT"
    cursor.execute(sql)

    # create table
    sql = """create table if not exists CHATGPT.CHATS (
        foreignid number, 
        datetime timestamp_tz, 
        question varchar, 
        reply varchar
    );"""

    cursor.execute(sql)
    sql = """create table if not exists CHATGPT.SUMMARY (
        id number autoincrement start 1 increment 1, 
        name varchar(50), 
        datetime timestamp_tz, 
        model varchar(30), 
        system varchar
    );"""
    cursor.execute(sql)
    conn.close()

# get the maximum id for the user    
def get_max_id(name,conn,cursor):
    sql = f"select * from CHATGPT.SUMMARY where NAME='{name}'"
    try:
        df = pd.read_sql(sql,conn)
    except:
        return False
    if df.shape[0] == 0:
        return False
    max_id = df["ID"].max()
    return int(max_id)

# get the chat history for the user
def get_chat_history(id,conn,cursor,for_display=False):
    conn, cursor = create_connection_snowflake()
    sql = f"select * from CHATGPT.CHATS where FOREIGNID={id}"
    try:
        df = pd.read_sql(sql,conn).sort_values("DATETIME")
    except:
        return []
    if df.shape[0] == 0:
        return []
    chat_history = []
    if not for_display:
        # for the chat_with_gpt function
        for question,reply in zip(df["QUESTION"],df["REPLY"]):
            chat_history.append({"role":"user","content":question})
            chat_history.append({"role":"assistant","content":reply})
    else:
        # for the home.html
        for question,reply in zip(df["QUESTION"],df["REPLY"]):
            chat_history.append(("user",question))
            chat_history.append(("assistant",reply))
    return chat_history

# get the model and system used for current chat
def get_model_system(id,conn,cursor):
    conn, cursor = create_connection_snowflake()
    sql = f"select MODEL,SYSTEM from CHATGPT.SUMMARY where ID={id}"
    df = pd.read_sql(sql,conn)
    if df.MODEL.isnull().any():
        return np.array([False])
    return df.values[0]

# insert the question and reply into the database
def insert_question_reply(id,question,reply,conn,cursor):
    conn, cursor = create_connection_snowflake()
    tz_tokyo = pytz.timezone('Asia/Tokyo')
    timestamp = datetime.now(tz=tz_tokyo)
    sql = "insert into CHATGPT.CHATS (FOREIGNID,DATETIME,QUESTION,REPLY) values(%s,%s,%s,%s)"
    cursor.execute(sql,(id,timestamp,question,reply))
    conn.commit()

# insert datetime and name when create new chat is pressed
def insert_summary(name,conn,cursor):
    conn, cursor = create_connection_snowflake()
    sql = "insert into CHATGPT.SUMMARY (NAME, DATETIME) values (%s, %s)"
    tz_tokyo = pytz.timezone('Asia/Tokyo')
    time = datetime.now(tz=tz_tokyo)
    cursor.execute(sql, (name, time,))
    conn.commit()

def update_summary(id,username,conn,cursor):
    conn, cursor = create_connection_snowflake()
    sql = f"update CHATGPT.SUMMARY set NAME=%s,DATETIME=%s,MODEL='',SYSTEM='' where ID={id}"
    tz_tokyo = pytz.timezone('Asia/Tokyo')
    time = datetime.now(tz=tz_tokyo)
    cursor.execute(sql, (username,time,))
    conn.commit()

# insert model and system when the first chat is initiated
def insert_model_system(id,model,system,conn,cursor):
    conn, cursor = create_connection_snowflake()
    sql = f"update CHATGPT.SUMMARY set MODEL=%s, SYSTEM=%s where ID={id}"
    cursor.execute(sql,(model,system))
    conn.commit()

def check():
    conn, cursor = create_connection_snowflake()
    sql = "select * from CHATGPT.CHATS"
    df = pd.read_sql(sql,conn)
    print(df)
    sql = "select * from CHATGPT.SUMMARY"
    df = pd.read_sql(sql,conn)
    print(df)
    conn.close()
