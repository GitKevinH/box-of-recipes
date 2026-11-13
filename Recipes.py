import json
from pathlib import Path
from collections import Counter

def start_recipes():
    invalid_count = 0
    while True:
        print("Box of Recipes".center(80))
        print("Browse\n")

        print("Before we dive into any specific recipe, lets narrow down what you're looking")
        print("for. Choose from the options below to filter.\n")

        print("Options for browsing recipes")
        print("1. Browse Recipes by Cuisine - Find something you're craving here!")
        print("2. Browse Recipes by Ingredient - Want to the last of your vegetables?")
        print("3. Browse Recipes by Technique - Let's nail that skill down.")
        print("4. Browse Everything (Warning, this will be large)\n")

        print("00. Go back")
        print("98. Main Menu")
        print("99. Exit\n")

        user_input = input("Please enter your choice: ").strip()

        if user_input == "1":
            invalid_count = 0
            nav = browse_by_cuisine()
            if nav == "main_menu":
                return
        elif user_input in ("00", "98"):
            return
        elif user_input == "99":
            print("Exiting. See you later!")
            exit()
        else:
            print("\nInvalid choice. Please enter a valid number.\n")
            invalid_count += 1
            if invalid_count >= 5:
                reset_input = input("It looks like you might be stuck, do you want to reset and start from the beginning? (y/n): ").strip().lower()
                if reset_input == "y":
                    return
                else:
                    invalid_count = 0

def browse_by_cuisine():
    recipes = load_recipes()
    cuisines = get_category_values(recipes, "cuisine")
    counts = get_category_counts(recipes, "cuisine")
    invalid_count = 0

    while True:
        print("Box of Recipes".center(80))
        print("\n")

        print("Browse by Cusine\n")

        print("Here looking for a certain flavor? Want to dive into a new culture? You're in the")
        print("right spot.\n")

        print("Options for recipes by cuisines:")
        for index, cuisine in enumerate(cuisines, start=1):
            print(f"{index}. {cuisine} ({counts[cuisine]})")
        print()

        print("00. Go back")
        print("98. Main Menu")
        print("99. Exit\n")

        user_input = input("Please enter your choice: ").strip()

        if user_input == "00":
            return "back"
        elif user_input == "98":
            return "main_menu"
        elif user_input == "99":
            print("Exiting. See you later!")
            exit()
        elif user_input.isdigit() and 1 <= int(user_input) <= len(cuisines):
            invalid_count = 0
            selected_cuisine = cuisines[int(user_input) - 1]
            matching_recipes = get_recipes_by_category(recipes, "cuisine", selected_cuisine)
            nav = recipe_list(matching_recipes, f"{selected_cuisine} Recipes")
            if nav == "main_menu":
                return "main_menu"
        else:
            print("\nInvalid choice. Please enter a valid number.\n")
            invalid_count += 1
            if invalid_count >= 5:
                reset_input = input("It looks like you might be stuck, do you want to reset and start from the beginning? (y/n): ").strip().lower()
                if reset_input == "y":
                    return "main_menu"
                else:
                    invalid_count = 0


def load_recipes():
    project_root = Path(__file__).resolve().parent
    file_path = project_root / "Recipes.json"
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_category_counts(recipes, category):
    counts = Counter()

    for recipe in recipes:
        value = recipe.get(category)

        # for ingredients
        if isinstance(value, dict):
            counts.update(value.keys())

        # for technique and cuisine
        elif value is not None:
            counts[value] += 1

    return dict(counts)


def get_category_values(recipes, category):
    values = set()

    for recipe in recipes:
        item = recipe.get(category)
        if isinstance(item, dict):
            values.update(item.keys())
        elif item is not None:
            values.add(item)

    return sorted(values)

def get_recipes_by_category(recipes, category, selected_value):
    recipes_from_catagory = []
    for recipe in recipes:
        item = recipe.get(category)
        if isinstance(item, dict) and selected_value in item:
            recipes_from_catagory.append(recipe)
        elif item == selected_value:
            recipes_from_catagory.append(recipe)
    return recipes_from_catagory


def recipe_list(matching_recipes, type_of_recipes):
    invalid_count = 0
    while True:
        print("Box of Recipes".center(80))
        print(f"\n{type_of_recipes}\n")

        for index, recipe in enumerate(matching_recipes, start=1):
            print(f"{index}. {recipe['title']} ({recipe['total_time']})")
        print()

        print("00. Go back")
        print("98. Main Menu")
        print("99. Exit\n")

        user_input = input("Please enter your choice: ").strip()

        if user_input == "00":
            return "back"
        elif user_input == "98":
            return "main_menu"
        elif user_input == "99":
            print("Exiting. See you later!")
            exit()
        elif user_input.isdigit() and 1 <= int(user_input) <= len(matching_recipes):
            invalid_count = 0
            selected_recipe = matching_recipes[int(user_input) - 1]
            nav = recipe_details(selected_recipe)
            if nav == "main_menu":
                return "main_menu"
        else:
            print("\nInvalid choice. Please enter a valid number.\n")
            invalid_count += 1
            if invalid_count >= 5:
                reset_input = input("It looks like you might be stuck, do you want to reset and start from the beginning? (y/n): ").strip().lower()
                if reset_input == "y":
                    return "main_menu"
                else:
                    invalid_count = 0


def recipe_details(recipe):
    invalid_count = 0
    while True:
        print("Box of Recipes".center(80))
        print(f"\n{recipe['title']}\n")

        rating = f"{recipe['rating']}/5" if recipe.get("rating") is not None else "Unrated"
        print(f"Cuisine: {recipe['cuisine']} | Technique: {recipe['technique']} | Time: {recipe['total_time']} | Rating: {rating}\n")

        print("Ingredients:")
        for ingredient, amount in recipe["ingredients"].items():
            print(f"  - {ingredient}: {amount}")
        print()

        print("Instructions:")
        for step_num, step in enumerate(recipe["instructions"], start=1):
            print(f"  {step_num}. {step}")
        print()

        print("1. Rate Recipe")
        print("00. Go back")
        print("98. Main Menu")
        print("99. Exit\n")

        user_input = input("Please enter your choice: ").strip()
        invalid_count = 0
        if user_input == "1":
            while True:
                user_rating = input("Enter a rating (1 - 5): ").strip()
                try:
                    updated_rating = float(user_rating)
                    if 1 <= updated_rating <= 5:
                        updated_rating = int(updated_rating) if updated_rating.is_integer() else round(updated_rating, 1)
                        recipe["rating"] = updated_rating
                        update_recipe_rating(recipe["title"], updated_rating)
                        print(f"\nRating updated to {updated_rating}/5!\n")
                        break
                    else:
                        print("\nPlease enter a number between 1 and 5.\n")
                except ValueError:
                    print("\nInvalid rating. Please enter a number between 1 and 5.\n")

        elif user_input == "00":
            return "back"
        elif user_input == "98":
            return "main_menu"
        elif user_input == "99":
            print("Exiting. See you later!")
            exit()
        else:
            print("\nInvalid choice. Please enter a valid number.\n")
            invalid_count += 1
            if invalid_count >= 5:
                reset_input = input("It looks like you might be stuck, do you want to reset and start from the beginning? (y/n): ").strip().lower()
                if reset_input == "y":
                    return "main_menu"
                else:
                    invalid_count = 0

def save_recipes(recipes):
    project_root = Path(__file__).resolve().parent
    file_path = project_root / "Recipes.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(recipes, file)


def update_recipe_rating(recipe_title, updated_rating):
    recipes = load_recipes()
    for r in recipes:
        if r["title"] == recipe_title:
            r["rating"] = updated_rating
            break
    save_recipes(recipes)