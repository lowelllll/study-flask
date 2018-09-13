# flaskr/flaskr.py 
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for,\
	abort, render_template, flash
from contextlib import closing

# create little application :)
app = Flask(__name__)
app.config.from_object(__name__) # 인자로 주어진 객체를 설정 값을 읽어오기 위해 살펴봄.
				# 그곳에 정의된 모든 대문자 변수를 찾음.

# configuration
app.config.update(dict(
	DATABASE = '/tmp/flaskr.db',
	DBUG = True,
	SECRET_KEY = 'development key',
	USERNAME = 'admin',
	PASSWORD = 'default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# 환경 변수 호출해 설정값 로드. FLASKR_SETTINGS에 명시된 파일이 로드되면 기본 설정 값들은 덮어쓰게됨.
# slient 스위치는 해당 환경변수가 존재하지 않아도 Flask가 작동하도록 함.

def connect_db(): # 커넥션을 얻어옴
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

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
def after_request(response):
	return response

# Http 요청 결과가 브라우저에 응답한 다음 실행.
# after_request 함수에서 예외가 발생할 경우 teardown_request로 전달됨.
@app.teardown_request
def teardown_request(exception):
	g.db.close()



# ---- view ---- #
@app.route('/')
def show_entries():
	"""
		작성된 글을 보여주는 뷰
	:return:
	"""
	cur = g.db.execute('select title,text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)


@app.route('/add',methods=['POST'])
def add_entry():
	"""
		새로운 글을 추가하는 뷰
		POST 요청에만 응답함.
	:return:
	"""
	if not session.get('logged_in'): # 로그인 되어있는지 확인. session에서 logged_in 키가 존재하고 값이 True인지 검사
		abort(401)
	g.db.execute('insert into entries (title,text) values (?,?)',
				 [request.form['title'],request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted') # 메세지로 새로 작성된 글에 대한 정보를 보여줌
	return redirect(url_for('show_entries')) # redirection


@app.route('/login', methods=['GET','POST'])
def login():
	"""
		로그인 뷰.
		설정에서 셋팅한 값과 비교하여 세션의 logged_in 키에 값을 설정해 로그인/로그아웃 상태를 결정.
	:return:
	"""
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries',error=error)) # login 성공
	return render_template('login.html',error=error) # login 실패

@app.route('/logout')
def logout():
	"""
		로그아웃 뷰
	:return:
	"""
	session.pop('logged_in',None) # 해당 키가 존재하면 값 remove
	flash('You were logged out')
	return redirect(url_for('show_entries'))


if __name__ == "__main__":
	app.run()
