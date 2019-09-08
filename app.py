from flask import Flask
from blueprint.form import form_review

app = Flask(__name__)
app.register_blueprint(form_review)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
