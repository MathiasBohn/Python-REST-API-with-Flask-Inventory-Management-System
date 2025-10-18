from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Mock database array
inventory = [
    {"id": 1, "code": "3274080005003", "product_name": "Organic Almond Milk", "brands": "Silk", 
     "ingredients_text": "Filtered water, almonds, cane sugar, sea salt", "quantity": 50, 
     "categories": "Plant-based beverages", "nutriscore_grade": "a", "nova_group": 1},
    {"id": 2, "code": "3017620422003", "product_name": "Nutella", "brands": "Ferrero", 
     "ingredients_text": "Sugar, palm oil, hazelnuts, cocoa, skim milk", "quantity": 30, 
     "categories": "Spreads", "nutriscore_grade": "e", "nova_group": 4},
    {"id": 3, "code": "5449000000996", "product_name": "Coca-Cola", "brands": "Coca-Cola", 
     "ingredients_text": "Carbonated water, sugar, colour, phosphoric acid", "quantity": 100, 
     "categories": "Beverages, Sodas", "nutriscore_grade": "e", "nova_group": 4},
    {"id": 4, "code": "8076809513258", "product_name": "Organic Pasta", "brands": "Barilla", 
     "ingredients_text": "Organic durum wheat semolina", "quantity": 75, 
     "categories": "Pasta", "nutriscore_grade": "a", "nova_group": 1},
    {"id": 5, "code": "4316268596404", "product_name": "Greek Yogurt", "brands": "Fage", 
     "ingredients_text": "Milk and cream, live active yogurt cultures", "quantity": 40, 
     "categories": "Dairy, Yogurts", "nutriscore_grade": "b", "nova_group": 1}
]

next_id = 6

def find_item(item_id):
    return next((item for item in inventory if item['id'] == item_id), None)


def fetch_openfoodfacts(barcode):
    try:
        response = requests.get(
            f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json",
            headers={"User-Agent": "InventorySystem/1.0 (student@example.com)"},
            timeout=10
        )
        data = response.json()
        return data.get('product') if data.get('status') == 1 else None
    except:
        return None

# GET /inventory - Fetch all items
@app.route('/inventory', methods=['GET'])
def get_all():
    return jsonify(inventory), 200

# GET /inventory/<id> - Fetch single item
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_one(item_id):
    item = find_item(item_id)
    return jsonify(item) if item else (jsonify({"error": "Item not found"}), 404)

# POST /inventory - Add new item
@app.route('/inventory', methods=['POST'])
def add_item():
    global next_id
    data = request.get_json()
    
    if not data or 'product_name' not in data:
        return jsonify({"error": "product_name is required"}), 400
    
    new_item = {
        "id": next_id,
        "code": data.get('code', ''),
        "product_name": data.get('product_name'),
        "brands": data.get('brands', ''),
        "ingredients_text": data.get('ingredients_text', ''),
        "quantity": data.get('quantity', 0),
        "categories": data.get('categories', ''),
        "nutriscore_grade": data.get('nutriscore_grade', ''),
        "nova_group": data.get('nova_group', '')
    }
    
    inventory.append(new_item)
    next_id += 1
    return jsonify(new_item), 201

# PATCH /inventory/<id> - Update item
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update fields
    for key in ['code', 'product_name', 'brands', 'ingredients_text', 'quantity', 
                'categories', 'nutriscore_grade', 'nova_group']:
        if key in data:
            item[key] = data[key]
    
    return jsonify(item), 200

# DELETE /inventory/<id> - Remove item
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    inventory.remove(item)
    return jsonify({"message": "Item deleted successfully"}), 200

# GET /inventory/search/barcode/<barcode> - Search OpenFoodFacts
@app.route('/inventory/search/barcode/<barcode>', methods=['GET'])
def search_barcode(barcode):
    product = fetch_openfoodfacts(barcode)
    return jsonify(product) if product else (jsonify({"error": "Product not found"}), 404)

# POST /inventory/import/<barcode> - Import from OpenFoodFacts
@app.route('/inventory/import/<barcode>', methods=['POST'])
def import_barcode(barcode):
    global next_id
    product = fetch_openfoodfacts(barcode)
    
    if not product:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404
    
    quantity = 0
    if request.json:
        quantity = request.json.get('quantity', 0)
    
    new_item = {
        "id": next_id,
        "code": product.get('code', barcode),
        "product_name": product.get('product_name', 'Unknown'),
        "brands": product.get('brands', ''),
        "ingredients_text": product.get('ingredients_text', ''),
        "quantity": quantity,
        "categories": product.get('categories', ''),
        "nutriscore_grade": product.get('nutriscore_grade', ''),
        "nova_group": product.get('nova_group', '')
    }
    
    inventory.append(new_item)
    next_id += 1
    return jsonify(new_item), 201

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)