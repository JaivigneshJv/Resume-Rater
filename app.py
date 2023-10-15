from flask import Flask, request, jsonify
from src.model import RatingModel
from src.info_extractor import InfoExtractor
import os
from flask_cors import CORS
from tika import parser
from src.utils import loadDefaultNLP


app = Flask(__name__)
CORS(app  , origins="*")

r = RatingModel()

@app.route("/rate_resume", methods=["POST"])
def rate_resume():
    data = request.get_json()
    resume_path = data["resume_path"]
    _type = data["type"]
    mname = data["model_name"]
    dirname = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(
        dirname, "src/models/model_" + _type, mname + ".json"
    )
    r = RatingModel(_type, model_path)
    rating = r.test(resume_path, None)

    nlp = loadDefaultNLP(is_big=False)
    infoExtractor = InfoExtractor(nlp, parser)
    info = infoExtractor.extractFromFile(resume_path)

    return jsonify({"rating": rating},
                   {"info": info})

if __name__ == "__main__":
    app.run(host="192.168.0.101", port=8005, debug=True, threaded=True)