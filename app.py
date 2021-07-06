from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route('/')
def view_stream():
    return render_template('paint.html')
