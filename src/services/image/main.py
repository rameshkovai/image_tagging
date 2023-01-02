from flask import Flask
from services.image.controller.image import image_blueprint

app = Flask(__name__)

app.register_blueprint(image_blueprint)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
