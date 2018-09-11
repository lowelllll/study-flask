from flask import Flask # WSGI 애플리케이션 
app = Flask(__name__) # Flask class 인스턴스 생성 / 인자 : 모듈 or 패키지 이름 -> 템플릿이나 정적파일을 찾을 때 필요

@app.route('/') # URL route 
def hello_world():  
	return 'Hello World!'

if __name__ == '__main__':
	app.run() # 로컬 서버로 실행. 외부 접근 app.run(host='0.0.0.0')
