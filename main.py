import random

while True:  # Main game restart loop
    # Game Setup
    print("Welcome to Bombaclat Roulette!")
    num_players = int(input("How many players will participate? "))
    while num_players < 2:
        print("You need at least 2 players to play the game.")
        num_players = int(input("How many players will participate? "))

    # Ask for the starting amount of Thief Bags
    starting_thief_bags = 0

    players = [f"Player {i + 1}" for i in range(num_players)]
    out_chance = 0.05  # Probability of a player getting out
    disease_chance = 0.1  # Probability of a player getting a disease
    horse_move_chance = 0.2  # Probability of pulling the horse move
    wolves_chance = 0.05  # Probability of wolves appearing
    thief_bag_success_chance = 0.5  # Chance of successfully stealing
    campfire_chance = 0.05  # Probability of triggering the campfire event

    cabin_chance = 0.1  # Probability of triggering the cabin event
    cabin_items = ["Gun", "Life", "Money (50 gold)", "Thief bag"]  # Possible rewards from the cabin

    player_money = [0] * len(players)
    player_guns = [0] * len(players)
    player_lives = [0] * len(players)
    player_diseased = [0] * len(players)
    player_disease_names = [None] * len(players)
    campfire_skip_turns = [0] * len(players)
    player_thief_bags = [starting_thief_bags] * len(players)  # Set starting thief bags

    disease_names = [
        "Low taper fade",
        "MASSIVE flu",
        "Bone cancer",
        "Crippling depression",
        "Beta syndrome"
    ]

    item_shop = {
        "Gun": 40,
        "Life": 30,
        "Potion": 20,
        "Thief bag": 60
    }

    # Main Game Loop
    while len(players) > 1:
        i = 0
        while i < len(players):  # Handle dynamic player list
            if campfire_skip_turns[i] > 0:
                print(f"{players[i]} is skipping their turn due to an event! ({campfire_skip_turns[i]} turns left)")
                campfire_skip_turns[i] -= 1
                i += 1
                continue

            input_action = input(f"{players[i]}, press Enter to continue: ")

            if random.random() < campfire_chance:
                print(f"{players[i]} triggered the campfire! Their turn will be skipped for 2 turns, but they gain an extra life.")
                player_lives[i] += 1
                campfire_skip_turns[i] = 2
                i += 1
                continue

            if random.random() < cabin_chance:
                item = random.choice(cabin_items)
                print(f"{players[i]} was sent to the cabin! They skip their next 2 turns and receive a {item}.")
                campfire_skip_turns[i] = 2
                if item == "Gun":
                    player_guns[i] += 1
                elif item == "Life":
                    player_lives[i] += 1
                elif item == "Money (50 gold)":
                    player_money[i] += 50
                elif item == "Thief bag":
                    print(f"{players[i]} received a Thief bag! They can now steal from other players.")
                    player_thief_bags[i] += 1  # Increase Thief Bags
                i += 1
                continue

            if random.random() < wolves_chance:
                print("A pack of wolves appears!")
                if player_guns[i] > 0:
                    print(f"{players[i]} uses a gun to fend off the wolves!")
                    player_guns[i] -= 1
                elif player_lives[i] > 0:
                    print(f"{players[i]} sacrifices a life to escape the wolves!")
                    player_lives[i] -= 1
                else:
                    print(f"{players[i]} is overwhelmed by the wolves and is out!")
                    players.pop(i)
                    player_money.pop(i)
                    player_guns.pop(i)
                    player_lives.pop(i)
                    player_diseased.pop(i)
                    player_disease_names.pop(i)
                    player_thief_bags.pop(i)  # Remove Thief Bags
                    campfire_skip_turns.pop(i)
                    continue

            player_money[i] += 10

            if player_diseased[i] > 0:
                player_diseased[i] += 1
                if player_diseased[i] > 2:
                    print(f"{players[i]} succumbs to {player_disease_names[i]} and is out!")
                    players.pop(i)
                    player_money.pop(i)
                    player_guns.pop(i)
                    player_lives.pop(i)
                    player_diseased.pop(i)
                    player_disease_names.pop(i)
                    player_thief_bags.pop(i)
                    campfire_skip_turns.pop(i)
                    continue
                else:
                    print(f"{players[i]} is suffering from {player_disease_names[i]}! ({2 - player_diseased[i]} turns left)")

            elif random.random() < disease_chance:
                disease = random.choice(disease_names)
                print(f"{players[i]} has caught {disease}!")
                player_diseased[i] = 1
                player_disease_names[i] = disease

            if random.random() < out_chance:
                print(f"{players[i]} is out!")
                players.pop(i)
                player_money.pop(i)
                player_guns.pop(i)
                player_lives.pop(i)
                player_diseased.pop(i)
                player_disease_names.pop(i)
                player_thief_bags.pop(i)
                campfire_skip_turns.pop(i)
                continue

            i += 1

        for i in range(len(players)):
            print(f"{players[i]}, you have {player_money[i]} gold.")
            while True:
                # Check if the player's turn is skipped
                if campfire_skip_turns[i] > 0:
                    print(f"{players[i]}, you cannot access the shop because your turn is skipped!")
                    break

                # Display inventory at the start of the shop
                print("\nYour Inventory:")
                print(f"- Guns: {player_guns[i]}")
                print(f"- Lives: {player_lives[i]}")
                print(f"- Thief Bags: {player_thief_bags[i]} (can steal if you have at least 1)")
                print(f"- Diseased: {'Yes, suffering from ' + player_disease_names[i] if player_diseased[i] else 'No'}")
                print("Item Shop:")
                for item, price in item_shop.items():
                    print(f"- {item}: {price} gold")
                choice = input("What do you want to buy? (Enter 'exit' to leave the shop): ").capitalize()
                if choice == "Exit":
                    break
                elif choice in item_shop:
                    if player_money[i] >= item_shop[choice]:
                        player_money[i] -= item_shop[choice]
                        if choice == "Gun":
                            player_guns[i] += 1
                        elif choice == "Life":
                            player_lives[i] += 1
                        elif choice == "Potion":
                            if player_diseased[i] > 0:
                                print(f"You used a Potion and cured {player_disease_names[i]}!")
                                player_diseased[i] = 0
                                player_disease_names[i] = None
                            else:
                                print("You used a Potion, but you weren't diseased.")
                        elif choice == "Thief bag":
                            print(f"You purchased a Thief bag! You can now steal from other players.")
                            player_thief_bags[i] += 1  # Increase Thief Bags
                    else:
                        print(f"You don't have enough gold to buy {choice}.")
                else:
                    print("Invalid choice.")

            # After exiting the shop, ask about using the Thief Bag if the player has one
            if player_thief_bags[i] > 0:
                use_thief_bag = input(f"Do you want to use your Thief bag to steal from another player? (yes/no): ").lower()
                if use_thief_bag == "yes":
                    target = input(f"Enter the name of the player you want to steal from: ")
                    if target in players and target != players[i]:
                        target_index = players.index(target)
                        if random.random() < thief_bag_success_chance:
                            stolen_amount = min(20, player_money[target_index])
                            player_money[i] += stolen_amount
                            player_money[target_index] -= stolen_amount
                            print(f"You stole {stolen_amount} gold from {target}!")
                        else:
                            print(f"Your attempt to steal from {target} failed!")

    print(f"{players[0]} wins the game!")
    print("\nGame restarting...\n")
