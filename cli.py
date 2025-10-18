import requests

BASE_URL = "http://localhost:5000"

def print_menu():
    print("\n" + "=" * 50)
    print("    INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. View all items")
    print("2. View item by ID")
    print("3. Add new item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Search by barcode (OpenFoodFacts)")
    print("7. Import from OpenFoodFacts")
    print("8. Exit")
    print("=" * 50)

def view_all():
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        if response.status_code == 200:
            items = response.json()
            print("\n--- INVENTORY LIST ---")
            for item in items:
                print(f"ID: {item['id']} | {item['product_name']} | Brand: {item['brands']} | Qty: {item['quantity']}")
        else:
            print(f"Error: {response.json().get('error')}")
    except Exception as e:
        print(f"Error: {e}")

def view_one():
    try:
        item_id = input("Enter item ID: ")
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        
        if response.status_code == 200:
            item = response.json()
            print("\n--- ITEM DETAILS ---")
            print(f"ID: {item['id']}")
            print(f"Product: {item['product_name']}")
            print(f"Brand: {item['brands']}")
            print(f"Barcode: {item['code']}")
            print(f"Quantity: {item['quantity']}")
            print(f"Categories: {item['categories']}")
            print(f"Ingredients: {item['ingredients_text']}")
        else:
            print("Error: Item not found")
    except Exception as e:
        print(f"Error: {e}")

def add_item():
    try:
        product_name = input("Product Name: ")
        if not product_name:
            print("Error: Product name required")
            return
        
        item_data = {
            "product_name": product_name,
            "brands": input("Brand: "),
            "code": input("Barcode: "),
            "ingredients_text": input("Ingredients: "),
            "quantity": int(input("Quantity: ") or 0),
            "categories": input("Categories: ")
        }
        
        response = requests.post(f"{BASE_URL}/inventory", json=item_data)
        
        if response.status_code == 201:
            item = response.json()
            print(f"\nSuccess! Added item ID {item['id']}: {item['product_name']}")
        else:
            print(f"Error: {response.json().get('error')}")
    except Exception as e:
        print(f"Error: {e}")

def update_item():
    try:
        item_id = input("Enter item ID: ")
        print("\n1. Update quantity")
        print("2. Update product name")
        print("3. Update brand")
        choice = input("Choice: ")
        
        update_data = {}
        if choice == "1":
            update_data['quantity'] = int(input("New quantity: "))
        elif choice == "2":
            update_data['product_name'] = input("New name: ")
        elif choice == "3":
            update_data['brands'] = input("New brand: ")
        else:
            print("Invalid choice")
            return
        
        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=update_data)
        
        if response.status_code == 200:
            print("Success! Item updated")
        else:
            print(f"Error: {response.json().get('error')}")
    except Exception as e:
        print(f"Error: {e}")

def delete_item():
    try:
        item_id = input("Enter item ID to delete: ")
        confirm = input(f"Delete item {item_id}? (yes/no): ")
        
        if confirm.lower() == 'yes':
            response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
            if response.status_code == 200:
                print("Success! Item deleted")
            else:
                print("Error: Item not found")
    except Exception as e:
        print(f"Error: {e}")

def search_barcode():
    try:
        barcode = input("Enter barcode: ")
        print("Searching...")
        
        response = requests.get(f"{BASE_URL}/inventory/search/barcode/{barcode}")
        
        if response.status_code == 200:
            product = response.json()
            print("\n--- FOUND IN OPENFOODFACTS ---")
            print(f"Product: {product.get('product_name')}")
            print(f"Brand: {product.get('brands')}")
            print(f"Categories: {product.get('categories')}")
            print(f"Nutri-Score: {product.get('nutriscore_grade')}")
        else:
            print("Product not found")
    except Exception as e:
        print(f"Error: {e}")

def import_product():
    try:
        barcode = input("Enter barcode to import: ")
        quantity = int(input("Initial quantity: ") or 0)
        
        print("Importing...")
        response = requests.post(
            f"{BASE_URL}/inventory/import/{barcode}",
            json={"quantity": quantity}
        )
        
        if response.status_code == 201:
            item = response.json()
            print(f"\nSuccess! Imported: {item['product_name']} (ID: {item['id']})")
        else:
            print("Error: Product not found in OpenFoodFacts")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("\nWelcome! Make sure Flask is running on http://localhost:5000")
    
    while True:
        print_menu()
        choice = input("\nChoice (1-8): ")
        
        if choice == "1":
            view_all()
        elif choice == "2":
            view_one()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_barcode()
        elif choice == "7":
            import_product()
        elif choice == "8":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()