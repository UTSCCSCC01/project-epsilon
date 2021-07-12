from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/info')
def hell():
    print ("test")
    return {'hi': 'hello world'}

@app.route('/')
def test():
    # ideally, we don't render any template in this file
    # all html templates, if any, should go to /public
    return render_template('index.html')

@app.route('/testReact', methods=['GET'])
def testReact():
    return {"title": "I am ready from app.py"}

if __name__ == "__main__":
    app.run(debug=True)