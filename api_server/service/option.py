# 投稿を作成する

import uuid
import datetime


def create_date():
    date = str(datetime.date.today())
    time_list = datetime.datetime.now()
    time = str(time_list.hour) + ":" + str(time_list.minute) + ":" + str(time_list.second)
    date_time = date + " " + time
    return date_time


def create_post(request_dic):
    new_post = {
        "id": str(uuid.uuid4()),
        "user_id": request_dic["user_id"],
        "text": request_dic["text"],
        "parent_post_id": "",
        "comment_count": 0,
        "posted_at": create_date()
    }
    return new_post


def create_comment(request_dic, parent_id):
    print("create")
    new_comment = {
        "id": str(uuid.uuid4()),
        "user_id": request_dic["user_id"],
        "text": request_dic["text"],
        "parent_post_id": parent_id,
        "comment_count": 1,
        "posted_at": create_date()
    }
    return new_comment


def change_count(post_list, parent_id):
    for post in post_list:
        if post["id"] == parent_id:
            post["comment_count"] = post["comment_count"] + 1


if __name__ == '__main__':
    sample_list = [
        {
            'id': 'e40f528e-639b-458e-bd9d-46299a110b85',
            'user_id': 0,
            'text': 'aaa',
            'comment_count': 0,
            'posted_at': '2019-12-07 17:30:37'
        },
        {
            'id': '6db30546-01b0-409d-bb72-99132ad42da8',
            'user_id': 1,
            'text': 'bbb',
            'comment_count': 0,
            'posted_at': '2019-12-07 17:30:38'
        }
    ]

    change_count(sample_list, '6db30546-01b0-409d-bb72-99132ad42da8')
    print(sample_list)
