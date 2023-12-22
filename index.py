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
    homepage = "<br><a href=/webhook3>3</a>"
    homepage += "<br><a href=/webhook4>4</a>"
    homepage += "<br><a href=/webhook5>5</a>"
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
        info = "我是hahow的課程查詢機器人,您選擇的課程是：" + title + "，價錢：\n" + price
        db = firestore.client()
        collection_ref = db.collection("課程")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["title"]:
                result += "課程名稱：" + dict["title"] + "\n"
                result += "開課單位：" + dict["owner_name"] + "\n"
                result += "開課人數: " + dict["student_number"] + "\n\n"
        info += result

    return make_response(jsonify({"fulfillmentText": info}))


@app.route("/webhook4", methods=["POST"])
def webhook4():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]
    #action 叫 courseChoice
    if (action == "courseChoice"):
        #action 裡的 PARAMETER NAME 是 title
        title =  req["queryResult"]["parameters"]["title"]
        info = "我是hahow的課程查詢機器人,您選擇的課程是：" + title + "，相關課程：\n"

        db = firestore.client()
        #firebase 的名字叫 課程
        collection_ref = db.collection("課程")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if title in dict["title"]:
                result += "課程名稱：" + dict["title"] + "\n"
                result += "開課單位：" + dict["owner_name"] + "\n"
                result += "開課人數: " + str(dict["student_number"]) + "\n\n"
        info += result
    #開一個Intent
    #action 叫 hahowclass
    elif (action == "hahowclass"):
        #action 裡的 PARAMETER NAME 是 owner_name、any
        keyword =  req.get("queryResult").get("parameters").get("any")
        info = "我是hahow的課程查詢機器人,您要查詢的課程單位是："+ keyword +"\n\n"
    return make_response(jsonify({"fulfillmentText": info}))




@app.route("/webhook5", methods=["POST"])
def webhook5():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]
    #action 叫 courseChoice
    if (action == "courseChoice"):
        #action 裡的 PARAMETER NAME 是 title
        title =  req["queryResult"]["parameters"]["title"]
        info = "我是hahow的課程查詢機器人,您選擇的課程是：" + title + "，相關課程：\n"

        db = firestore.client()
        #firebase 的名字叫 課程
        collection_ref = db.collection("課程")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if title in dict["title"]:
                result += "課程名稱：" + dict["title"] + "\n"
                result += "開課單位：" + dict["owner_name"] + "\n"
                result += "開課人數: " + str(dict["student_number"]) + "\n\n"
        info += result
    #開一個Intent
    #action 叫 hahowclass
    elif (action == "hahowclass"):
        #action 裡的 PARAMETER NAME 是 owner_name、any
        owner_name =  req.get("queryResult").get("parameters").get("owner_name")
        info = "我是hahow的課程查詢機器人,您要查詢開課單位："+ owner_name +"\n\n"
        if (question == "開課單位"):
            db = firestore.client()
            collection_ref = db.collection("課程")
            docs = collection_ref.get()
            found = False
            for doc in docs:
                dict = doc.to_dict()
                if owner_name in dict["owner_name"]:
                    found = True 
                    info += "課程名稱：" + dict["title"] + "\n"
                    info += "開課單位：" + dict["owner_name"] + "\n"
                    info += "價錢：" + str(dict["price"]) + "\n"
                    info += "開課人數: " + str(dict["student_number"]) + "\n\n"
            if not found:
                info += "很抱歉，目前無符合這個關鍵字的相關課程喔"

    return make_response(jsonify({"fulfillmentText": info}))




if __name__ == '__main__':
    app.run(debug=True)