import pandas as pd
from joblib import load
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/predict', methods=['GET'])
def get_prediction():

    carat = float(request.args.get('carat'))
    cut = int(request.args.get('cut'))
    color = int(request.args.get('color'))
    clarity = int(request.args.get('clarity'))
    depth = float(request.args.get('depth'))
    table = float(request.args.get('table'))
    volume = float(request.args.get('volume'))

    features = [carat, cut, color, clarity, depth, table, volume]

    sample = pd.DataFrame([features], columns=["carat", "cut", "color", "clarity", "depth", "table", "volume"])

    model = load('modelRR.joblib')

    predicted_price = int(model.predict(sample))

    return jsonify(features=sample.to_dict(orient='records')[0], predicted_price=predicted_price)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
