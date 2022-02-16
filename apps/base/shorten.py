def replaceUnits(text):
    text=text.replace("tablespoons", "tbsp")
    text=text.replace("tablespoon", "tbsp")
    text=text.replace("teaspoons", "tsp")
    text=text.replace("teaspoon", "tsp")
    text=text.replace("pounds", "lbs")
    text=text.replace("pound", "lb")
    text=text.replace("ounce", "oz")
    lst = ["or to taste", "to taste", "lengthwise", "diced", "chopped", "minced", "cooked", "beaten"]
    find_next=False
    for i in lst:
        words = text.split(" ")
        for word in words:
            #print(word, i)
            if find_next:
                if word=="and":
                    text=text.replace(word, "")
                find_next=False
            if word==i:   
                find_next=True
        text=text.replace(i , "")
    return text

newtext = replaceUnits("hello I am diced and minced")
print(newtext)