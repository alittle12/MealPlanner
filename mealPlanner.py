
##takes into account the quantities of items used in individual recipes
##helps develop grocery lists and us everything that is purchased


##reads in a .txt file of a recipe in the following format
def createRecipeBook():
    myRecipes ={}
    ingredientList = []
    print("Welcome to your recipe book")
    recipeName = input("What is the name of the recipe: ")
    print("Enter (done) when you're done")
    ingredients = input("Ingredient 1: ")
    counter = 2
    while ingredients.lower() != "done":
        ingredients = input("Ingredient " +str(counter) +": ")
        ingredientList.append(ingredients)
        counter = counter +1
    myRecipes[recipeName] = ingredientList[:-1]
    return myRecipes

##called after a meal a proposed meal is added or if a recipe is checked and all the ingredients exist
def updateCabinet(recipeName, cabinet):
    recipes = recipeSearch()
    recipe = recipes.get(recipeName)
    items = recipe.split(",")
    #loop through the ingredients to get their quantities
    for i in items:
        x = i.split(":")
        item = x[0]
        recipeQuantity = x[1].split("(",1)[0]
        cabinetIngredient = cabinet.get(item)
        cabinetQuantity = str(cabinetIngredient).split("(",1)[0]
        amountRemaining = int(cabinetQuantity)-int(recipeQuantity)
        cabinetQuantity = amountRemaining
        ##update the ingredient amount
        cabinet[item] = str(amountRemaining) + "(oz)"


##allows the user to enter an ingredient and its quantity, this will then be addded to a dictionary later referenced in checkCabinet()
def createCabinet():
    ##need to add things into a cabinet dictionary
    print('Before we can get started this week, what ingredients do you already have?')
    print("Enter (finished) when you've finished entering your ingredients")
    cabinet = {}
    ingredient = input("Ingredient: ")
    quantity = input("quantity: ")
    cabinet[ingredient] = quantity
    while (ingredient != "finished") or (quantity != 'finished'):
        ingredient = input("Ingredient: ")
        if (ingredient == 'finished'):
            print("Cabinet complete!")
            break
        quantity = input("quantity: ")
        cabinet[ingredient] = quantity
        if (quantity == 'finished'):
            print("Cabinet complete!")
            break
    return cabinet

def recipeSearch():
    ##returns a dictionary containing recipe names and their recipes, eventually this dictionary can be populated by reading a recipe.txt file and calling createRecipeBook() inside this function
    recipes = {'Recipe1': 'Rice Vinegar:3 (oz)'}
    return recipes

##this function checks the user's cabinent to see if they have the necessary ingredients for a meal
def checkCabinet(y_n, mealsEntered, cabinet):
    ## use a dictionary to store items and qauntities
    ##cabinetItems = {'Rice Vinegar': '4 (oz)', 'Sugar': '2 (cups)', 'Honey': '3 (oz)', 'Flour': '2 (cups)'}
    #list of meal options
    mealOptions = []
    #recipe dictionary to check cabinet qauntities against
    recipes = recipeSearch()
    #if the user does not know what they want to eat, the following will suggest for them
    if y_n.lower() == 'no':
        mealOptions = []
        #get the name of the first recipe
        for key in recipes:
            #get the value: ingredients associated with the recipe
            itemList = recipes.get(key)
            #split the ingredients into a list called items
            items = itemList.split(",")
            #loop through the ingredients to get their quantities
            for i in items:
                x = i.split(":")
                item = x[0]
                recipeQuantity = x[1].split("(",1)[0]
                ##cabinetQuantity = cabinetItems.get(item)
                cabinetQuantity = cabinet.get(item)
                cabinetQuantity_final = cabinetQuantity.split("(",1)[0]
                if int(cabinetQuantity_final) < int(recipeQuantity):
                    #then there is not enough to make the recipe
                    break
                else:
                    #there is enough ingredients to make the recipe
                    mealOptions.append(key)
                print('Based on what is in the pantry I suggest: ')
                for i in mealOptions:
                    #print out the menu
                    print(i)
                    menuProposal(mealOptions, cabinet)
                return mealOptions
    #the user know what they want and has indicated what they want to eat
    else:
        #load the recipe dictionary to reference
        recipes = recipeSearch()
        groceryList = {}
        for i in mealsEntered:
            #for each meal choice get the associated recipe
            itemList = recipes.get(i)
            #get the ingredients and put them in a list called iems
            items = itemList.split(",")
            for j in items:
                #split that list into quantities
                x = j.split(":")
                item = x[0]
                recipeQuantity = x[1].split("(",1)[0]
                cabinetQuantity = cabinet.get(item)
                cabinetQuantity_final = str(cabinetQuantity).split("(",1)[0]
                if int(cabinetQuantity_final) < int(recipeQuantity):
                    ## add the item to the grocery list
                    groceryList[item] = int(recipeQuantity)-int(cabinetQuantity_final)
                else:
                    #do nothing
                    print("Yay you have everything")
                    updateCabinet(i, cabinet)
                    return groceryList
    return recipes

##this function allows a user who knows what they want to eat each day to specify such
def mealPlanner(cabinet, knownMeals):
  mealsEntered = input("Enter those meals separated by commas: ")
  print('When do you want to have those meals')
  print("Select which days you want to eat those meals, separated by commas:")
  chosenDays = input(" (1) Monday : \n (2) Tuesday: \n (3) Wednesday: \n (4) Thursday: \n (5) Friday: \n (6) Saturday: \n (7) Sunday:  \n")
  dayList = chosenDays.split(",")
  dayList = [eval(i) for i in dayList]
  daysToPropose = 7-int(knownMeals)
  print('The computer will propose several meal options for the remaining ' + str(daysToPropose) + " days")
  if daysToPropose > 0:
      mealOptions = []
      for i in range(daysToPropose):
          meal = checkCabinet("no","null",cabinet)
          mealOptions.append(meal)
          flat_list = [item for sublist in mealOptions for item in sublist]

  days = ["Monday: ", "Tuesday: ", "Wednesday: ", "Thursday: ", "Friday: ", "Saturday: ", "Sunday: "]
  #dayList = [2,3,4]
  meals = mealsEntered.split(",")
  knownMealsList = [item for sublist in zip(dayList, meals) for item in sublist]
  #mealOptions = ["Recipe1","Recipe1","Recipe1","Recipe1"]
  unchosenDays = []
  for i in range (7):
      if i+1 in dayList:
          continue
      else:
          unchosenDays.append(i+1)
  mealProposalList = [item for sublist in zip(unchosenDays, flat_list) for item in sublist]
  menu = []

  counter = 0
  for i in dayList:
      day = days[int(i)-1]
      menu.insert(int(i)-1, day + ": " +(knownMealsList[counter+1]))
      counter = counter +2
  counter =0
  for i in unchosenDays:
    day = days[i-1]
    menu.insert(i-1, day + ": " +(mealProposalList[counter+1]))
    counter = counter +2
  #print(menu)
  else:
      menu = mealsEntered

  return menu

##this function proposes meal ideas if the user is unsure what to make based on what is in their cabinet, once given the
##proposals the user can decide whether or not to add the recommnedations to their weekly meal plan
def menuProposal(meals, cabinet):
    Meals = []
    counter = 1
    for i in meals:
        print(str(counter) +": " + i)
        counter = counter +1
    mealChoice = input("Use the corresponding number to add a recipe to this week's meals")
    #the number of choices will come from meal planner
    if mealChoice == "1":
        Meals.append(meals[int(mealChoice)-1])
        print("Ok " +meals[int(mealChoice)-1]+ " has been added to your meals this week!")
        updateCabinet(i, cabinet)

    return Meals

##Main function, this welcomes the user to the application and prompts them whether or not they
## know what they want to eat

def main():
    print('Welcome to Meal Planner')
    cabinet = createCabinet()
    y_n = input('Are there specific things you want to eat this week?')
    ##Based on their answer to the prompt above if the user knows what they want to eat they are directed to
    ##use the mealPlanner() method to enter that information and the
    mealsEntered =[]
    while (y_n.lower() != 'yes') or (y_n.lower() != 'no'):
        if y_n.lower() == 'yes':
            knownMeals = input("How many meals do you have planned this week: ")
            #num of meals should be entered here and the below clause should be used if they know all 7 meal
            if(int(knownMeals) <7):
                mealsEntered= mealPlanner(cabinet, int(knownMeals))
                #figure out how to print the menu
                print("What's left in the cabinet: ")
                print(cabinet)
                break

            else:
                mealsEntered= mealPlanner(cabinet, 7)
                recipes = recipeSearch()
                for i in mealsEntered:
                    if recipes.__contains__(i):
                        print(i+ " recipe found, checking to see if you have all the ingredients...")
                        checkCabinet(y_n, mealsEntered,cabinet)
                    else:
                        print('That recipe is not in your records. Would you like to add it?')
                        ##addRecipe()
                #print(mealsEntered)
                print("What's left in the cabinet: ")
                print(cabinet)
        ## if the user is unsure about what to eat with the available ingredients they can query their cabinet and available recipes
        elif y_n.lower() == 'no':
            meals = checkCabinet(y_n, mealsEntered,cabinet)
            menuProposal(meals, cabinet)
            print("What's left in the cabinet: ")
            print(cabinet)
        else:
            print('Please enter (yes) or (no)')
            y_n = input('Are there specific things you want to eat this week?')

#calling main
main()
#
