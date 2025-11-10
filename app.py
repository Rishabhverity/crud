from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory cart store
cart = []

# ---------- Create (Add to cart) ----------
@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    if not data or 'name' not in data or 'qty' not in data:
        return jsonify({"error": "Missing 'name' or 'qty' field"}), 400
    
    item_id = len(cart) + 1
    item = {
        "id": item_id,
        "name": data['name'],
        "qty": data['qty']
    }
    cart.append(item)
    return jsonify({"message": "Item added to cart", "item": item}), 201

# ---------- Read (View cart) ----------
@app.route('/api/cart', methods=['GET'])
def get_cart():
    return jsonify({"cart": cart}), 200

# ---------- Update (Modify an item) ----------
@app.route('/api/cart/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    data = request.get_json()
    for item in cart:
        if item['id'] == item_id:
            item['name'] = data.get('name', item['name'])
            item['qty'] = data.get('qty', item['qty'])
            return jsonify({"message": "Item updated", "item": item}), 200
    return jsonify({"error": "Item not found"}), 404

# ---------- Delete (Remove an item) ----------
@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
def delete_cart_item(item_id):
    global cart
    cart = [item for item in cart if item['id'] != item_id]
    return jsonify({"message": f"Item {item_id} deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
