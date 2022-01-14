
ingredients = []
while True:
    user_input = input("Enter your ingredient or type done: ")
    if user_input=="done":
        break
    ingredients.append(user_input)

print("Your ingredients are: ")
print(*ingredients, sep = ", ") 

