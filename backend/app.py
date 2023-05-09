from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import find_lowest_price

app = Flask(__name__)
CORS(app)

@app.route('/find-lowest-price')
def find_lowest_price_route():
    item = request.args.get('item')
    price, link, store = find_lowest_price(item)
    if price == float('inf'):
        return jsonify({'error': 'No items found'}), 404
    return jsonify({'price': price, 'link': link, 'store': store})

if __name__ == '__main__':
    app.run(debug=True)
