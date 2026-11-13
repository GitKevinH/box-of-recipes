import Recipes

def welcome_message():
    print("Box of Recipes".center(80))
    print("Greeting\n")

    print("Oi! Welcome to my Box of Recipes! In this box you shall find numerous recipes")
    print("that will (hopefully) fit your fancy! There are many to choose from so dive right")
    print("in!\n")

    print("In this application you can find recipes that might satisfy your craving, help you")
    print("hone your skills, or just use up the last of an ingredient on hand.\n")

    print("Begin by entering the number for the corresponding menu items and feel free to")
    print("explore all the recipes we have to offer!\n\n")

def welcome_options():
    print("1. Browse Recipes")
    print("99. Exit\n")

    print("Please enter your choice: ")


def start():
    while True:
        welcome_message()
        welcome_options()
        user_input = input().strip()
        if user_input == "1":
            print("Let's jump in!")
            Recipes.start_recipes()
        elif user_input == "99":
            print("Exiting. See you later!")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    start()
