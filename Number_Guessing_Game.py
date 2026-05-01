import random

print("Welcome to the Guessing Game!")       
while True:
    diff = input("What difficulty? easy 1-10, medium 1-50, hard 1-100: ").lower()
    counter = 1
    if diff == "easy":
        secret = random.randrange(1,11)
        print(secret)
        r = "1-10"
    elif diff == "medium":
        secret = random.randrange(1,51)
        print(secret)
        r = "1-50"
    elif diff == "hard":
        secret = random.randrange(1,101)
        print(secret)
        r = "1-100"
    else:
        print("Enter a valid Difficulty.")
        continue     

    while True:
        x = input(f"Enter a number from {r}: ")
        try:
            x = int(x)
            if x < secret:
                counter+=1
                print("Too low")
            elif x > secret:
                counter+=1
                print("Too high")
            else:
                print(f"Congrats you guess it in {counter} tries.")
                break
        except ValueError:
                print("Enter a number, please try again!")

    again = input("Do you want to play again? Yes or No: ")
    if again.lower() == "yes":
        continue
    else:
        print("Thank you for playing the game. Goodbye!")
        break

    
              


           