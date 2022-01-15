import webbrowser

ingredients = []

def printIngredients(ingredient_list): 
    print("Your ingredients are: ")
    print(*ingredient_list, sep = ", ") 

def readIngredients():
    while True:
        user_input = input("Enter your ingredient or type done: ")
        if user_input=="done":
            break
        ingredients.append(user_input)
    printIngredients(ingredients)

    edit = False
    user_input = input("Would you like to add/remove ingredients? (Y/N): ")

    if (user_input == 'Y'):
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

#https://www.allrecipes.com/search/results/?IngIncl=egg&IngIncl=cheese&IngIncl=bacon
def inputSearch(ingredients_list):
    search = "https://www.allrecipes.com/search/results/?IngIncl="
    if (len(ingredients) == 1):
        search += ingredients[0]
    elif (len(ingredients) > 1):
        for ingredient in ingredients:
            search += "&IncIncl=" + ingredient
    
    webbrowser.open(search)

def main():
    readIngredients()
    inputSearch(ingredients)

if __name__ == "__main__":
    main()
        


