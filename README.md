# Inventory Management System

A simple Flask-based inventory management system with REST API, CLI interface, and OpenFoodFacts API integration for managing retail product inventory.

## Features

- **REST API** with full CRUD operations
- **CLI Interface** for easy user interaction
- **OpenFoodFacts Integration** to search and import real product data
- **Mock Database** using in-memory array storage
- **Comprehensive Test Suite** with pytest

---

## Installation and Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

Navigate to your project directory and install the required packages:

```bash
pip install flask requests pytest
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Project Structure

Ensure your project has the following structure:

```
inventory-project/
│
├── app.py              # Flask API application
├── cli.py              # Command-line interface
├── test_app.py         # Test suite
└── requirements.txt    # Dependencies
```

### Step 3: Run the Application

**Terminal 1 - Start the Flask API:**
```bash
python app.py
```

The API will start on `http://localhost:5000`

**Terminal 2 - Run the CLI:**
```bash
python cli.py
```

### Step 4: Run Tests (Optional)

**Terminal 3 - Run the test suite:**
```bash
pytest test_app.py -v
```

---

## API Endpoint Details

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. **GET /inventory**
Fetch all inventory items.

**Response:**
```json
[
  {
    "id": 1,
    "code": "3274080005003",
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds...",
    "quantity": 50,
    "categories": "Plant-based beverages",
    "nutriscore_grade": "a",
    "nova_group": 1
  }
]
```

---

#### 2. **GET /inventory/<id>**
Fetch a single inventory item by ID.

**Example Request:**
```bash
GET /inventory/1
```

**Response (Success - 200):**
```json
{
  "id": 1,
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "quantity": 50
}
```

**Response (Not Found - 404):**
```json
{
  "error": "Item not found"
}
```

---

#### 3. **POST /inventory**
Add a new inventory item.

**Request Body:**
```json
{
  "product_name": "New Product",
  "brands": "Brand Name",
  "code": "1234567890123",
  "ingredients_text": "Ingredients here",
  "quantity": 10,
  "categories": "Category"
}
```

**Response (Success - 201):**
```json
{
  "id": 6,
  "product_name": "New Product",
  "brands": "Brand Name",
  "quantity": 10
}
```

**Response (Error - 400):**
```json
{
  "error": "product_name is required"
}
```

---

#### 4. **PATCH /inventory/<id>**
Update an existing inventory item.

**Example Request:**
```bash
PATCH /inventory/1
```

**Request Body:**
```json
{
  "quantity": 100,
  "product_name": "Updated Name"
}
```

**Response (Success - 200):**
```json
{
  "id": 1,
  "product_name": "Updated Name",
  "quantity": 100
}
```

---

#### 5. **DELETE /inventory/<id>**
Remove an inventory item.

**Example Request:**
```bash
DELETE /inventory/1
```

**Response (Success - 200):**
```json
{
  "message": "Item deleted successfully"
}
```

---

#### 6. **GET /inventory/search/barcode/<barcode>**
Search for a product in OpenFoodFacts database by barcode.

**Example Request:**
```bash
GET /inventory/search/barcode/3274080005003
```

**Response (Success - 200):**
```json
{
  "code": "3274080005003",
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "categories": "Plant-based beverages",
  "nutriscore_grade": "a"
}
```

---

#### 7. **POST /inventory/import/<barcode>**
Import a product from OpenFoodFacts and add it to inventory.

**Example Request:**
```bash
POST /inventory/import/3274080005003
```

**Request Body (Optional):**
```json
{
  "quantity": 25
}
```

**Response (Success - 201):**
```json
{
  "id": 6,
  "code": "3274080005003",
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "quantity": 25
}
```

---

## CLI Usage Examples

### Starting the CLI

```bash
python cli.py
```

You'll see the main menu:

```
==================================================
    INVENTORY MANAGEMENT SYSTEM
==================================================
1. View all items
2. View item by ID
3. Add new item
4. Update item
5. Delete item
6. Search by barcode (OpenFoodFacts)
7. Import from OpenFoodFacts
8. Exit
==================================================
```

---

### Example 1: View All Inventory Items

**Input:**
```
Choice (1-8): 1
```

**Output:**
```
--- INVENTORY LIST ---
ID: 1 | Organic Almond Milk | Brand: Silk | Qty: 50
ID: 2 | Nutella | Brand: Ferrero | Qty: 30
ID: 3 | Coca-Cola | Brand: Coca-Cola | Qty: 100
ID: 4 | Organic Pasta | Brand: Barilla | Qty: 75
ID: 5 | Greek Yogurt | Brand: Fage | Qty: 40
```

---

### Example 2: View Single Item

**Input:**
```
Choice (1-8): 2
Enter item ID: 1
```

**Output:**
```
--- ITEM DETAILS ---
ID: 1
Product: Organic Almond Milk
Brand: Silk
Barcode: 3274080005003
Quantity: 50
Categories: Plant-based beverages
Ingredients: Filtered water, almonds, cane sugar, sea salt
```

---

### Example 3: Add New Item

**Input:**
```
Choice (1-8): 3
Product Name: Organic Honey
Brand: Local Farms
Barcode: 9876543210123
Ingredients: Pure organic honey
Quantity: 15
Categories: Sweeteners
```

**Output:**
```
Success! Added item ID 6: Organic Honey
```

---

### Example 4: Update Item

**Input:**
```
Choice (1-8): 4
Enter item ID: 1

1. Update quantity
2. Update product name
3. Update brand
Choice: 1
New quantity: 75
```

**Output:**
```
Success! Item updated
```

---

### Example 5: Delete Item

**Input:**
```
Choice (1-8): 5
Enter item ID to delete: 2
Delete item 2? (yes/no): yes
```

**Output:**
```
Success! Item deleted
```

---

### Example 6: Search Product by Barcode (OpenFoodFacts)

**Input:**
```
Choice (1-8): 6
Enter barcode: 3017620422003
```

**Output:**
```
Searching...

--- FOUND IN OPENFOODFACTS ---
Product: Nutella
Brand: Ferrero
Categories: Spreads, Chocolate spreads
Nutri-Score: e
```

**Try these real barcodes:**
- `3274080005003` - Organic Almond Milk
- `3017620422003` - Nutella
- `5449000000996` - Coca-Cola
- `8076809513258` - Organic Pasta

---

### Example 7: Import from OpenFoodFacts

**Input:**
```
Choice (1-8): 7
Enter barcode to import: 3017620422003
Initial quantity: 20
```

**Output:**
```
Importing...

Success! Imported: Nutella (ID: 6)
```

---

### Example 8: Exit

**Input:**
```
Choice (1-8): 8
```

**Output:**
```
Goodbye!
```

---

## Code Structure and Maintainability

### app.py - Flask API

**Key Functions:**
- `find_item(item_id)` - Helper to find items by ID
- `fetch_openfoodfacts(barcode)` - Fetches product data from external API
- All routes follow RESTful conventions

**Code Comments:**
```python
# Mock database array
inventory = [...]

# Helper function to find item by ID
def find_item(item_id):
    return next((item for item in inventory if item['id'] == item_id), None)

# GET /inventory - Fetch all items
@app.route('/inventory', methods=['GET'])
def get_all():
    return jsonify(inventory), 200
```

---

### cli.py - Command Line Interface

**Key Functions:**
- `print_menu()` - Displays main menu
- `view_all()` - Shows all inventory items
- `add_item()` - Prompts user to add new item
- `update_item()` - Updates existing item
- `delete_item()` - Removes item from inventory
- `search_barcode()` - Searches OpenFoodFacts
- `import_product()` - Imports from OpenFoodFacts

**Error Handling:**
All functions include try-except blocks to handle:
- Network errors
- Invalid input
- API failures

---

### test_app.py - Test Suite

**Test Coverage:**
- ✅ All CRUD operations (GET, POST, PATCH, DELETE)
- ✅ Success and error cases
- ✅ OpenFoodFacts API integration (mocked)
- ✅ Input validation
- ✅ 15 comprehensive tests

**Running Specific Tests:**
```bash
# Run all tests
pytest test_app.py -v

# Run specific test
pytest test_app.py::test_get_all -v

# Run with coverage
pytest test_app.py --cov=app
```

---

## Troubleshooting

### Issue: "Connection refused" error in CLI

**Solution:** Make sure the Flask API is running first:
```bash
python app.py
```

### Issue: "Module not found" error

**Solution:** Install dependencies:
```bash
pip install flask requests pytest
```

### Issue: Tests failing

**Solution:** Ensure Flask app is running before running tests, or use mocked tests that don't require the server.

---

## Technology Stack

- **Flask** - Web framework for REST API
- **Requests** - HTTP library for external API calls
- **Pytest** - Testing framework
- **OpenFoodFacts API** - External product database

---

## API Rate Limits

OpenFoodFacts API has the following rate limits:
- 100 requests/minute for product queries
- 10 requests/minute for search queries

The app respects these limits through normal usage patterns.

---

## Future Enhancements

- Add persistent database (SQLite or PostgreSQL)
- Implement user authentication
- Add product image display
- Export inventory to CSV
- Add search by product name
- Implement pagination for large inventories

---

## License

This project is for educational purposes.

---

## Contact

For questions or issues, please refer to the course materials or contact your instructor.

---

## Acknowledgments

- **OpenFoodFacts** - For providing free product data API
- **Flask** - For the excellent web framework
- **Python Community** - For amazing libraries and tools