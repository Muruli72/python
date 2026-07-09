from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello"

@app.route("/hello")
def hello():
    return "Hello Hari! 🚀"

if __name__ == "__main__":
    app.run(debug=True)