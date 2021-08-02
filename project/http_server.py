from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        image = request.args.get('image')
        image_path = '/root/project/faceDect/images'
        image_file = image_path+'/'+image
        with open(image_file, 'rb') as f:
    	    return f.read()
    elif request.method == 'POST':
        un = request.form.get('uname')
        pw = request.form['pwd']
        return 'receive args for POST:%s,%s' % (un, pw)

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
