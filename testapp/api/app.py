from flask import Flask, render_template

app = Flask(__name__)

@app.route('/info')
def hell():
    print ("test")
    return {'hi', 'hello world'}

@app.route('/')
def test():
    return render_template('index.html')