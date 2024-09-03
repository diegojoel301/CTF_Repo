from flask import Flask, session

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = True
#app.config['SESSION_REFRESH_EACH_REQUEST'] = True
#app.secret_key = "SEXOANAL"
@app.route('/')
def index():
    session['user_id'] = 1
    session['username'] = "admin"
    return 'CVE-2023-30861!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
