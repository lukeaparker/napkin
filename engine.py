import sys
from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('paint.html')
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

    