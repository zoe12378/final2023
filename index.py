import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask,render_template,request,make_response, jsonify #透過request抓前端的值
from datetime import datetime, timezone, timedelta


import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
# 靜態網頁
@app.route('/')
def index():
    homepage = "<br><a href=/webhook3>課程查詢</a><br>"
    return homepage

@app.route("/webhook3", methods=["POST"])
def webhook3():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "hahowclass"):
        rate =  req.get("queryResult").get("parameters").get("title")
        info = ("我是hahow的課程查詢機器人,您選擇的課程是：") + title + "，價錢：\n" + price

        db = firestore.client()
        collection_ref = db.collection("課程")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "課程名稱：" + dict["title"] + "\n"
                result += "開課單位：" + dict["owner_name"] + "\n"
                result += "開課人數: " + dict["student_number"] + "\n\n"
        info += result

    return make_response(jsonify({"hahowText": info}))

if __name__ == '__main__':
    app.run(debug=True)