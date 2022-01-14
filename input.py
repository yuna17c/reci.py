def printIngredients(ingredients): 
    print("Your ingredients are: ")
    print(*ingredients, sep = ", ") 

ingredients = []
while True:
    user_input = input("Enter your ingredient or type done: ")
    if user_input=="done":
        break
    ingredients.append(user_input)

printIngredients(ingredients)

edit = False
edit_input = input("Would you like to add/remove ingredients? (Y/N): ")

if (edit_input == 'Y'):
    edit = True
    print("Type 'add ____' or 'remove ____' to add/remove ingredients. Otherwise type 'done'.")

while edit:
    user_input = input()
    if user_input == 'done':
        printIngredients(ingredients)
        break
    if user_input[0:3].lower() == "add" and (user_input[4:] not in ingredients):
        ingredients.append(user_input[4:])
        printIngredients(ingredients)
    elif user_input[0:6].lower() == "remove" and (user_input[7:] in ingredients):
        ingredients.remove(user_input[7:])
        printIngredients(ingredients)
    else:
        print("Invalid input. Try again. :3")
    
        


