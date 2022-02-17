# replace cooking action verbs that are included in the ingredient list (e.g. minced, peeled)
# From the website, most ingredients are described with action verbs e.g. 10g minced garlic. 
# In order to shorten the list of ingredients, this function removes any action verbs that are not
# necessary to the ingredient list. 

def replaceUnits(text):
    text=text.replace("tablespoons", "tbsp")
    text=text.replace("tablespoon", "tbsp")
    text=text.replace("teaspoons", "tsp")
    text=text.replace("teaspoon", "tsp")
    text=text.replace("pounds", "lbs")
    text=text.replace("pound", "lb")
    text=text.replace("ounce", "oz")
    lst = ["or to taste", "to taste", "lengthwise", "diced", "chopped", "minced", "cooked", "beaten", "peeled"]
    find_next=False
    for i in lst:
        words = text.split(" ")
        for word in words:
            if find_next:
                if word=="and":
                    text=text.replace(word, "")
                find_next=False
            if word==i:   
                find_next=True
        text=text.replace(i , "")
    return text