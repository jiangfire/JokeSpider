import sqlite3
import hashlib
import time
import os

#It's a db file, use it can store joke without picture
#Version 0.1
#Author JiangFire

def connectDb(name = "funny.db"):
	conn = sqlite3.connect(name)
	if not os.path.exists(name):
		conn.execute('''CREATE TABLE JOKER
      					(ID INTEGER PRIMARY KEY AUTOINCREMENT,
       					JOKE TEXT NOT NULL,
       					MD5  TEXT NOT NULL,
       					DATE TEXT NOT NULL);''')
	return conn

def insertData(conn, joke):
	currenttime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	conn.execute("INSERT INTO JOKER (JOKE,MD5,DATE)" +
      			"VALUES (\"%s\",\"%s\",\"%s\")" % (joke, MD5(joke), currenttime)) #remeory it! text type need double quotes

def MD5(string): #The string type must be bytes
	if type(string) != bytes:
		hash_md5 = hashlib.md5(string.encode())
	else:
		hash_md5 = hashlib.md5(string)
	return hash_md5.hexdigest()

def CConn(conn, close=False):
	if not close:
		conn.commit()
	else:
		conn.commit()
		conn.close()
