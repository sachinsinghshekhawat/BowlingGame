from flask import Flask, render_template
from GameAPI.Game import game_bp
application = Flask(__name__, static_url_path="/static")
application.register_blueprint(game_bp,url_prefix="/")

@application.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    application.run()