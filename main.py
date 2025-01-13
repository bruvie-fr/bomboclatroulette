import random

while True:  # Main game restart loop
    # Game Setup
    print("Welcome to Bombaclat Roulette!")
    num_players = int(input("How many players will participate? "))
    while num_players < 2:
        print("You need at least 2 players to play the game.")
        num_players = int(input("How many players will participate? "))

    starting_thief_bags = 0
    players = [f"Player {i + 1}" for i in range(num_players)]
    out_chance = 0.05  # Probability of a player getting out
    disease_chance = 0.1  # Probability of a player getting a disease
    wolves_chance = 0.05  # Probability of wolves appearing
    thief_bag_success_chance = 0.5  # Chance of successfully stealing
    campfire_chance = 0.05  # Probability of triggering the campfire event

    cabin_chance = 0.15  # Probability of triggering the cabin event
    cabin_items = ["Gun", "Life", "Money (50 gold)", "Thief bag"]

    player_money = [0] * len(players)
    player_guns = [0] * len(players)
    player_lives = [1] * len(players)
    player_diseased = [0] * len(players)
    player_disease_names = [None] * len(players)
    campfire_skip_turns = [0] * len(players)
    player_thief_bags = [starting_thief_bags] * len(players)

    disease_names = [
        "Low taper fade",
        "Massive flu",
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
        while i < len(players):
            if campfire_skip_turns[i] > 0:
                print(f"{players[i]} is skipping their turn due to an event! ({campfire_skip_turns[i]} turns left)")
                campfire_skip_turns[i] -= 1
                i += 1
                continue

            input(f"{players[i]}, press Enter to continue: ")

            # Allow the player to use items at the start of their turn
            while True:
                print(f"{players[i]}'s inventory: Guns: {player_guns[i]}, Lives: {player_lives[i]}, Thief Bags: {player_thief_bags[i]}")
                if player_diseased[i] > 0:
                    print(f"WARNING: You are diseased with {player_disease_names[i]}! Use a Potion to cure it.")

                use_item = input("Do you want to use an item? (yes/no): ").lower()
                if use_item == "yes":
                    item_choice = input("What do you want to use? (Gun/Potion/Thief bag): ").capitalize()
                    if item_choice == "Gun" and player_guns[i] > 0:
                        attack_choice = input("Do you want to use the gun for defense or attack another player? (defense/attack): ").lower()
                        if attack_choice == "attack":
                            target_player = int(input("Which player do you want to attack? Enter their number (1, 2, etc.): ")) - 1
                            if target_player < 0 or target_player >= len(players) or target_player == i:
                                print("Invalid target.")
                            else:
                                if player_lives[target_player] > 0:
                                    print(f"{players[i]} attacks {players[target_player]} with the gun!")
                                    player_lives[target_player] -= 1
                                    if player_lives[target_player] == 0:
                                        print(f"{players[target_player]} has lost all lives and is out!")
                                        players.pop(target_player)
                                        player_money.pop(target_player)
                                        player_guns.pop(target_player)
                                        player_lives.pop(target_player)
                                        player_diseased.pop(target_player)
                                        player_disease_names.pop(target_player)
                                        player_thief_bags.pop(target_player)
                                        campfire_skip_turns.pop(target_player)
                                    else:
                                        print(f"{players[target_player]} has {player_lives[target_player]} lives left.")
                                player_guns[i] -= 1
                        elif attack_choice == "defense":
                            print(f"{players[i]} uses a Gun for defense!")
                            player_guns[i] -= 1
                            continue  # Skip the rest of the turn to ensure the player with defense doesn't get attacked
                    elif item_choice == "Potion" and player_diseased[i] > 0:
                        print(f"{players[i]} uses a Potion and cures their disease ({player_disease_names[i]}).")
                        player_diseased[i] = 0
                        player_disease_names[i] = None
                    elif item_choice == "Potion":
                        print("You are not diseased, so the Potion has no effect.")
                    elif item_choice == "Thief bag" and player_thief_bags[i] > 0:
                        target_player = int(input("Which player do you want to steal from? Enter their number (1, 2, etc.): ")) - 1
                        if target_player < 0 or target_player >= len(players) or target_player == i:
                            print("Invalid target.")
                        else:
                            if random.random() < thief_bag_success_chance:
                                stolen_gold = random.randint(10, 30)
                                stolen_gold = min(stolen_gold, player_money[target_player])  # Ensure they have enough to steal
                                player_money[target_player] -= stolen_gold
                                player_money[i] += stolen_gold
                                print(f"{players[i]} successfully stole {stolen_gold} gold from {players[target_player]}!")
                            else:
                                print(f"{players[i]} failed to steal from {players[target_player]}.")
                            player_thief_bags[i] -= 1
                    else:
                        print("Invalid choice or insufficient items.")
                    break
                else:
                    break

            # Gameplay Events and Random Triggers
            if random.random() < campfire_chance:
                print(f"{players[i]} triggered the campfire! Their turn will be skipped for 2 turns, but they gain an extra life.")
                player_lives[i] += 1
                campfire_skip_turns[i] = 2
                i += 1
                continue

            if random.random() < cabin_chance:
                item = random.choice(cabin_items)
                print(f"{players[i]} found a hidden cabin and received a {item}!")
                if item == "Gun":
                    player_guns[i] += 1
                elif item == "Life":
                    player_lives[i] += 1
                elif item == "Money (50 gold)":
                    player_money[i] += 50
                elif item == "Thief bag":
                    player_thief_bags[i] += 1
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
                    player_thief_bags.pop(i)
                    campfire_skip_turns.pop(i)
                    continue

            # Add Gold for Surviving the Turn
            player_money[i] += 10

            # Disease Mechanic
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

            elif random.random() < disease_chance:
                disease = random.choice(disease_names)
                print(f"{players[i]} has caught {disease}!")
                player_diseased[i] = 1
                player_disease_names[i] = disease

            i += 1

        # End of Round Store
        for i in range(len(players)):
            print(f"\n{players[i]}, you have {player_money[i]} gold.")
            while True:
                print("\nItem Shop:")
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
                            print("Potion added to inventory.")
                        elif choice == "Thief bag":
                            player_thief_bags[i] += 1
                    else:
                        print(f"You don't have enough gold to buy {choice}.")
                else:
                    print("Invalid choice.")

    # Game End
    if len(players) == 1:
        print(f"\nCongratulations! {players[0]} is the winner of Bombaclat Roulette!")
    else:
        print("\nThe game ended with no winner!")

    # Restart Game Prompt
    restart = input("\nDo you want to play again? (yes/no): ").lower()
    if restart != "yes":
        print("Thanks for playing Bombaclat Roulette! Goodbye!")
        break
