# main部分
# (flag) 0 == 正常, -1 == 異常

from bottle import route, run, request, HTTPResponse
import os
import json
import mysql.connector
from service import option

DATABASE = "sample_db"
conn = mysql.connector.connect(
        host='localhost',
        user='root',
        database=DATABASE
)
cur = conn.cursor()
cur.execute("select * from test_users;")
USER_LIST = cur.fetchall()

FILEPATH = os.getcwd() + "/" + "test.txt"
request_list = []


# 新規投稿のuser_id確認
def confirm_user(user_id):
    for user_info in USER_LIST:
        if user_id != user_info[0]:
            return "登録ユーザーではありません"
        else:
            return "OK"


# 投稿文の文字数確認
def confirm_text_len(text):
    if len(text) <= 0 or len(text) >= 101:
        return "文字数は1文字以上100文字以下です"
    else:
        return "OK"


# コメント先の投稿確認
def confirm_post(post_id):
    flag = -1
    for post in request_list:
        if post_id == post["id"]:
            flag = 0
    if flag != 0:
        return "コメント先の投稿が見当たりません"
    else:
        return "OK"


# response作成
def create_response(flag, message):
    if flag == 0:
        body = json.dumps({"result": "OK"})
        response = HTTPResponse(status=200, body=body)
        response.set_header('Content-Type', 'application/json')
        return response
    else:
        print(message)
        body = json.dumps({
            "result": "NG",
            "message": message
        })
        response = HTTPResponse(status=400, body=body)
        response.set_header('Content-Type', 'application/json')
        return response


# 投稿一覧表示
@route("/posts")
def show_posts():
    all_posts = {
        "posts": request_list
    }
    body = json.dumps(all_posts)
    response = HTTPResponse(status=200, body=body)
    response.set_header('Content-Type', 'application/json')
    return response


# 新規投稿作成
@route("/posts/create", method="POST")
def create_post():
    request_dic = request.json  # dic型
    # エラー確認
    message = confirm_user(request_dic["user_id"])
    if message != "OK":
        return create_response(-1, message)
    elif confirm_text_len(request_dic["text"]) != "OK":
        message = confirm_text_len(request_dic["text"])
        return create_response(-1, message)
    else:
        request_list.append(option.create_post(request_dic))
        print(request_list)
        return create_response(0, message)


# コメント一覧表示
@route("/posts/<post_id>/comments")
def show_comments(post_id):
    comment_list = []
    # 検索
    for post in request_list:
        if post_id == post["parent_post_id"]:
            comment_list.append(post)

    all_comments = {
        "comments": comment_list
    }
    body = json.dumps(all_comments)
    response = HTTPResponse(status=200, body=body)
    response.set_header('Content-Type', 'application/json')
    return response


# コメント作成
@route("/posts/<post_id>/comments/create", method="POST")
def create_comment(post_id):
    request_dic = request.json
    # エラー確認
    message = confirm_post(post_id)
    if message != "OK":
        return create_response(-1, message)
    elif confirm_user(request_dic["user_id"]) != "OK":
        message = confirm_user(request_dic["user_id"])
        return create_response(-1, message)
    elif confirm_text_len(request_dic["text"]) != "OK":
        message = confirm_text_len(request_dic["text"])
        return create_response(-1, message)
    else:
        request_list.append(option.create_comment(request_dic, post_id))
        print(request_list)
        return create_response(0, message)


run(host="0.0.0.0", port=8080, debug=True)
