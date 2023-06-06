from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import find_lowest_price
import json 

app = Flask(__name__)
CORS(app)

@app.route('/find-lowest-price')
def find_lowest_price_route():
    item_name = request.args.get('item')
    stores = json.loads(request.args.get('stores'))
    data = find_lowest_price(item_name, stores)
    print("Data returned by find_lowest_price:", data)  
    return jsonify(data)

if __name__ == '__main__':
    app.run()
