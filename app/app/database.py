import sqlite3 as sq
import pandas as pd
import datetime
import numpy as np

# create the database
def create_database():
    conn = sq.connect("db\chatgpt.db")
    cur = conn.cursor()
    sql = "create table if not exists summary (id integer primary key autoincrement, name text, datetime timestamp, model text, system text)"
    cur.execute(sql)
    sql = "create table if not exists chat (id integer, datetime timestamp, question text, reply text)"
    cur.execute(sql)
    conn.close()

# get the maximum id for the user    
def get_max_id(name):
    conn = sq.connect("db/chatgpt.db")
    sql = f"select * from summary where name='{name}'"
    try:
        df = pd.read_sql(sql,conn)
    except:
        conn.close()
        return False
    conn.close()
    if df.shape[0] == 0:
        return False
    max_id = df.loc[df["id"]==df["id"].max(),"id"].values[0]
    return int(max_id)

# get the chat history for the user
def get_chat_history(id,for_display=False):
    conn = sq.connect("db/chatgpt.db")
    sql = f"select * from chat where id={id}"
    try:
        df = pd.read_sql(sql,conn).sort_values("datetime")
    except:
        conn.close()
        return []
    conn.close()
    if df.shape[0] == 0:
        return []
    chat_history = []
    if not for_display:
        # for the chat_with_gpt function
        for question,reply in zip(df["question"],df["reply"]):
            chat_history.append({"role":"user","content":question})
            chat_history.append({"role":"assistant","content":reply})
    else:
        # for the home.html
        for question,reply in zip(df["question"],df["reply"]):
            chat_history.append(("user",question))
            chat_history.append(("assistant",reply))
    return chat_history

# get the model and system used for current chat
def get_model_system(id):
    conn = sq.connect("db/chatgpt.db")
    sql = f"select model,system from summary where id={id}"
    df = pd.read_sql(sql,conn)
    conn.close()
    if df.model.isnull().any():
        return np.array([False])
    return df.values[0]

# insert the question and reply into the database
def insert_question_reply(id,question,reply):
    conn = sq.connect("db/chatgpt.db")
    cur = conn.cursor()
    timestamp = int(datetime.datetime.now().timestamp())    
    sql = "insert into chat (id,datetime,question,reply) values(?,?,?,?)"
    cur.execute(sql,(id,timestamp,question,reply))
    conn.commit()
    conn.close()

# insert the summary for the user
def insert_summary(name):
    conn = sq.connect("db/chatgpt.db")
    cur = conn.cursor()
    timestamp = int(datetime.datetime.now().timestamp())
    sql = "insert into summary (name,datetime) values(?,?)"
    cur.execute(sql,(name,timestamp))
    conn.commit()
    conn.close()

# insert the model and system used for the current chat
def insert_model_system(id,model,system):
    conn = sq.connect("db/chatgpt.db")
    cur = conn.cursor()
    sql = f"update summary set model=?, system=? where id={id}"
    cur.execute(sql,(model,system))
    conn.commit()
    conn.close()

# only used for debugging
def check(name):
    conn = sq.connect("db/chatgpt.db")
    cur = conn.cursor()
    sql = "select * from summary"
    print("all summary: ",pd.read_sql(sql,conn))
    sql = "select * from chat"
    print("all chat: ",pd.read_sql(sql,conn))
    sql = f"select * from summary where name='{name}'"
    print("summary for name: ",cur.execute(sql).fetchall())
    max_id = get_max_id(name)
    sql = f"select * from chat where id='{max_id}'"
    print("chat for max id: ",cur.execute(sql).fetchall())
    conn.close()

# only used for checking the frequency of chat
def get_chat_frequency():
    conn = sq.connect("db/chatgpt.db")
    sql = "select * from summary"
    df = pd.read_sql(sql,conn)
    conn.close()
    freq = df.value_counts("name")
    return freq

#if __name__ == "__main__":
#    create_database()