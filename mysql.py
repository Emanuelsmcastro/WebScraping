import pymysql

# Connect to the database

with pymysql.connect(host='127.0.0.1', user='root', passwd='Emanuel2486179300!', db='mysql') as db:
    cursor = db.cursor()
    cursor.execute('USE scraping')
    cursor.execute('SELECT * FROM pages')
    print(cursor.fetchall())

