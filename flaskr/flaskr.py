# flaskr/flaskr.py 

import sqlite3
from flask import Flask, request, session, g, redirect, url_for,\
	abort, render_template, flash
from contextlib import closing


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

# database 경로로 제공받은 어떤 경로들은 오류를 발생시킬 수 있음.
# 데이터베이스 초기화.
def init_db():
	with closing(connect_db()) as db: # closing with 블럭 안에서 연결한 커넥션을 유지하도록 도와줌.
		with app.open_resource('schema.sql','r') as f: # open_resource() 어플리케이션 객체의 함수. -> 리소스 경로의 파일을 열고 그 값을 읽음.
			#  데이터 베이스에 연결하는 스크립트 실행
			db.cursor().executescript(f.read()) # 커서는 전체 스크립트를 실행하는 메소드를 가짐.
			db.commit() # 변경 사항 커밋.


"""
요청이 오기 전, 커넥션을 초기화하고 
사용이 끝난후 커넥션 종료
"""
# reqeust가 실행되기 전에 호출되는 함수. Http 요청이 들어올 때 마다 실행
# 어떠한 인자도 전달할 수 없음.
@app.before_request
def before_request():
	g.db = connect_db()
	# g 객체 -> 각 함수들에 대해 오직 한번의 리퀘스트에 대해서만 유효한 정보를 저장.

# Http 요청이 끝나고 브라우저에 응답하기 전에 실행.
# flask.wrapper.Response 객체를 return해야함.
@app.after_request
def after_request():
	pass

# Http 요청 결과가 브라우저에 응답한 다음 실행.
# after_request 함수에서 예외가 발생할 경우 teardown_request로 전달됨.
@app.teardown_request
def teardown_request():
	g.db.close()



if __name__ == "__main__":
	app.run()
