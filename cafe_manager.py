menu = {
    "Espresso": 260000,
    "Americano": 270000,
    "Cappucino": 300000,
    "Latte": 300000,
    "Cheescacke": 380000
}

def show_menu():
    for key, value in menu.items():
        print(key,":", value)

def add_item():
    while True:
        try:
            item_name = input("Please write the item's name:  ")
            if item_name in menu:
                print("Item already exists.")
                break
            if item_name == "":
                print("please write a word")
                continue
            item_price = int(input("Please write the item's price:  "))
            menu.update({
            item_name : item_price
            })
            break
        except ValueError:
            print("Please type a number")

def remove_item():
    while True:
        item_name = input("Please write the item's name")
        try:
            del menu[item_name]
            break
        except KeyError:
            print("Item not found")

def search_item():
    while True:
        item_name = input("Please write the item's name:  ")
        try:
            print(item_name, " price is: ",menu[item_name])
            break
        except KeyError:
            print("Item not found")
  
def new_order():
    total = 0
    answer = "yes"
    order = []
    
    while answer == "yes":
        try:
            item_name = input("Please write the item's name: ")
            price = menu[item_name]
            quantity = int(input("How many? "))
            total += quantity * price
            order.append({
                "item name": item_name,
                "item price": price,
                "quantity": quantity,
                "subtotal": quantity * price,
            })
            print(item_name, " * ", quantity, " =",price * quantity, "===> total =", total )
            while True:
                answer = input("Do you want to add anything else?")
                if answer in ["yes", "no"]:
                    break
                print("Please type yes ro no")
                
        except KeyError:
            print("Item not found")
        except ValueError:
            print("Please enter an number:  ")
    if answer == "no":
        print(" === RECEIPT===")
        for item in order:
            print(
                item["item name"], " * ", item["quantity"], 
                "\nprice:", item["item price"],
                "\nSubtotal: ", item["subtotal"],
                "\n-------------------"
            )
        
    print("TOTAL:", total)

if __name__ == "__main__":
    while True:
        print("\n===== Café Manager =====")
        print("1. Show menu")
        print("2. Add item")
        print("3. Remove item")
        print("4. Search item")
        print("5. New order")
        print("6. Exit")
        
        choice = input("choose:  ")
        
        if choice == "1":
            show_menu()
        elif choice == "2":
            add_item()
        elif choice == "3":
            remove_item()
        elif choice == "4":
            search_item()
        elif choice == "5":
            new_order()
        elif choice == "6":
            break
        else:
            print("Invalid choice")