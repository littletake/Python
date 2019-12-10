# mysqlとの連携の練習

import MySQLdb

if __name__ == '__main__':
    # 接続する
    conn = MySQLdb.connect(
     user='root',
     passwd='root',
     host='localhost',
     db='sample_db'
    )
    cursor = conn.cursor()

    sql = "SELECT id FROM test_users"
    rows = cursor.execute(sql)
    print(rows)
    # # 取り出した10件を一つずつ表示 --- (*3)
    # for n in rows:
    #     print(n)

    # 接続を閉じる
    cursor.close()
    conn.close()
