from flask import Flask, render_template, request, redirect, flash, session, send_from_directory
from flask_session import Session
import os
from datetime import datetime,timedelta
from config import Config
from chatgpt import chat_with_gpt
from snowflake_db import *
import time
from MS_authentication import *

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=30) 
app.config.from_object(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
PORT = 80
config = Config()
redirect_url = os.environ["redirect_url"]
OPERATION_CHECK = False
if OPERATION_CHECK:
    DEBUG = True
else:
    DEBUG = False

purpose_map = {
    "question": "Ask Question",
    "summarization": "Summarize" 
}


# Define the login route
@app.route("/",methods=["GET","POST"])
def login():
    if OPERATION_CHECK:
        return redirect("/home")
    if session.get("login"):
        return redirect("/home")
    auth_url = build_auth_url()
    return render_template("MSlogin.html",url=auth_url)

# This route is used to get the access token
@app.route("/getToken")
def get_access_token():
    try:
        cache = load_cache(session)
        result = build_msal_app(cache).acquire_token_by_authorization_code(request.args['code'],
                                                                            scopes=["User.Read"],
                                                                            redirect_uri=redirect_url)
        if "error" in result:
            session["messages"] = ["result"]
            session["message_tag"] = "rounded-0 alert alert-danger"
            return redirect("/")
        session["username"] = result.get("id_token_claims").get("name")
        save_cache(cache,session)
        session["login"] = True
        return redirect("/home")
    except:
        flash("Failed in login")
        return redirect("/")

# This route is the main page of the application
@app.route("/home",methods=["GET","POST"])
def home():
    if not session.get("login") and not OPERATION_CHECK:
        return redirect("/")
    username = session.get("username")
    if OPERATION_CHECK:
        username = "OPERATION_CHECK"
    if not username:
        return redirect("/")
    conn, cursor = create_connection_snowflake()
    # take out messages from the session
    messages = session.get("messages")
    message_tag = session.get("message_tag")
    session["messages"] = None
    session["message_tag"] = None
    if request.method == "GET":
        max_id = get_max_id(username, conn, cursor)
        # if the user is new, insert the user into the database
        if not max_id:
            insert_summary(username, conn, cursor)
            max_id = get_max_id(username, conn, cursor)
        model_system = get_model_system(max_id, conn, cursor)
        # if new chat, model and system are not fixed and can be modified
        model_list = config.gpt_models
        selected_model = None
        selected_purpose = {}
        if model_system[0]:
            selected_model = [model_system[0]]
            selected_purpose = model_system[1]
            if selected_purpose not in purpose_map.keys():
                selected_purpose = "question"
            selected_purpose = {purpose_map[selected_purpose]:selected_purpose}
        chat_history = get_chat_history(max_id,conn,cursor,for_display=True)
        conn.close()
        return render_template("home.html",models=model_list,chat_history=chat_history,
                               username=username,messages=messages,default_model=config.gpt_models[0],
                               message_tag=message_tag,selected_model=selected_model,
                               selected_purpose=selected_purpose.items())
    else:
        if session.get("login") is None and not OPERATION_CHECK:
            conn.close()
            return redirect("/")
        question = request.form.get("chat-input")
        if question is None:
            session["messages"] = ["Input Error"]
            session["message_tag"] = "rounded-0 alert alert-danger"
            flash("Input Error")
            conn.close()
            return redirect("/home")
        question = question.strip()
        if question == "":
            session["messages"] = ["Please input something in question"]
            session["message_tag"] = "rounded-0 alert alert-danger"
            conn.close()
            return redirect("/home")
        max_id = get_max_id(username,conn,cursor)
        model_system = get_model_system(max_id,conn,cursor)
        if not model_system[0]:
            model = request.form.get("model")
            purpose = request.form.get("purpose")
            insert_model_system(max_id,model,purpose,conn,cursor)
        else:
            model = model_system[0]
            purpose = model_system[1]
        chat_history = get_chat_history(max_id,conn,cursor)
        chat_history.append(
            {"role": "user", "content": question}
        )
        reply,chat_history = chat_with_gpt(model,purpose,chat_history)
        if not chat_history:
            session["messages"] = [reply]
            session["message_tag"] = "rounded-0 alert alert-danger"
            conn.close()
            return redirect("/home")
        insert_question_reply(max_id,question,reply,conn,cursor)
        conn.close()
        return redirect("/loaded")

@app.route("/loaded")
def on_loaded():
    return redirect("/home")
   
# This route is used to start new chat
@app.route("/new",methods=["GET","POST"])
def new():
    if not session.get("login") and not OPERATION_CHECK:
        return redirect("/")
    username = session.get("username")
    if OPERATION_CHECK:
        username = "OPERATION_CHECK"
    conn, cursor = create_connection_snowflake()
    if username:
        max_id = get_max_id(username,conn,cursor)
        chat_history = get_chat_history(max_id,conn,cursor)
        if not chat_history:
            update_summary(max_id,username,conn,cursor)
            return redirect("/home")
        insert_summary(username,conn,cursor)
        conn.close()
    else:
        conn.close()
        return redirect("/")
    return redirect("/home")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# This route is used to define the favicon
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join("static","image"),"AP.ico")
        
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=PORT,debug=DEBUG)
