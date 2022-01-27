import pandas as pd
import re

df = pd.read_csv('fridge.csv', sep=',', header=0)

item_num = df["ItemNum"].tolist()
food_item = df["FoodItem"].tolist()
expiry_date = df["ExpiryDate"].tolist()
curr_item = len(df.index) + 1

def errMsg():
    print("Invalid input. Try again.")

def addName():
    user_input = input("Please enter the food item name: ")
    while True:
        user_input2 = input("You typed '" + user_input + "'. Is this correct (Y/N)?: ")
        if user_input2.lower() == "y":
            return user_input
        elif user_input2.lower() == "n":
            addName()
            break
        else:
            errMsg()
            continue

def addDate():
    user_input = input("Please enter the expiry date (MM/DD/YYYY): ")
    while True:
        # this date regex is wrong LOL
        if re.match(r"^((0[1-9])|(1[0-2]))\/(0[1-9]|[1-2][0-9]|3[0-1])\/20[0-2][0-9]$", user_input):
            user_input2 = input("You typed '" + user_input + "'. Is this correct (Y/N)?: ")
            while True:
                if user_input2.lower() == "y":
                    return user_input
                elif user_input2.lower() == "n":
                    addDate()
                    break
                else:
                    errMsg()
                    continue
            break
        else:
            errMsg()
            addDate()
            break

def addItems(curr_item):
    while True:
        name = addName()
        date = addDate()
        item_num.append(curr_item)
        food_item.append(name)
        expiry_date.append(date)
        curr_item += 1
        user_input = input("Food item added. Add more (Y/N)?: ")
        if user_input.lower() == "n":
            break
        elif user_input.lower() != "y":
            errMsg()

def removeItems(curr_item):
    while True:
        user_input = input("Please enter the number of the food item you would like to remove: ")
        if (user_input.isnumeric()) and (int(user_input) < curr_item):
            curr_item -= 1
            food_item.pop(curr_item - 1)
            expiry_date.pop(curr_item - 1)
            item_num.pop(curr_item - 1)
            user_input = input("Food item removed. Remove more (Y/N)?: ")
            if user_input.lower() == "n":
                break
            elif user_input.lower() != "y":
                errMsg()
        else:
            errMsg()

if __name__ == "__main__":
    user_input = input("Would you like to add or remove food items? (add/remove): ")
    if user_input.lower() == "add":
        addItems(curr_item)

    elif user_input.lower() == "remove":
        removeItems(curr_item)

    else:
        errMsg()

new_data = {'ItemNum': item_num, 'FoodItem': food_item, 'ExpiryDate': expiry_date}
new_df = pd.DataFrame(data=new_data)
new_df['ExpiryDate'] = pd.to_datetime(new_df['ExpiryDate'])
new_df.to_csv('fridge.csv', index=False)

