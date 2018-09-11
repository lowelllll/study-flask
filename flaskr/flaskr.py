# flaskr/flaskr.py 

import sqlite3
from flask import Flask, request, session, g, redirect, url_for,\
	abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create little application :)
app = Flask(__name__)
app.config.from_object(__name__) # 인자로 주어진 객체를 설정 값을 읽어오기 위해 살펴봄.
				# 그곳에 정의된 모든 대문자 변수를 찾음.

# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# 환경 변수 호출해 설정값 로드. FLASKR_SETTINGS에 명시된 파일이 로드되면 기본 설정 값들은 덮어쓰게됨.
# slient 스위치는 해당 환경변수가 존재하지 않아도 Flask가 작동하도록 함.

def connect_db(): # 커넥션을 얻어옴
	return sqlite3.connect(app.config['DATABASE'])


if __name__ == "__main__":
	app.run()
