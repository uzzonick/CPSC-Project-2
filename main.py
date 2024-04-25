"""
Author:         Nick Uzzo
Date:           04/25/24
Assignment:     Project 2
Course:         CPSC1051
Lab Section:    02

CODE DESCRIPTION: This program creates the game Brave Quest

"""

import random 
import json  #imports JSON module for file I/O

class Character:
    #base class for characters player and enemy
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack
    
    def alive_or_dead(self):
        #returns True if character is alive (health above 0)
        return self.health > 0 
    
    def take_damage(self, damage):
        #reduces character's health by the given damage
        self.health -= damage

def save_game(player):
#function for saving game to a JSON file
    with open("game_state.json", "w") as file:
        json.dump(player.__dict__, file)

def load_game():
#function to load game state from JSON file
    try:
        with open("game_state.json", "r") as file:
            data = json.load(file)
            #creates a new Player object using the loaded data
            player = Player(**data)
            return player
    except FileNotFoundError:
        #if file does not exist, it returns nothing
        return None

def prompt_load_game():
#function to prompt the player to load a saved game
    print("Do you want to load a saved game? (Y/N)")
    choice = input().upper()
    if choice == "Y":
        return load_game()
    else:
        return None

class Player(Character):
    #class for the Player of the game
    def __init__(self, name, health=150, level=1, money=20, attack=10, inventory=None):
        super().__init__(name, health, attack)
        self.level = level
        self.money = money
        self.inventory = inventory if inventory is not None else []

    def alive_or_dead(self):
        #returns true if player is alive (health above 0)
        return self.health > 0 

    def take_damage(self, damage):
        #takes away the damage amount from your points
        self.health -= damage

    def attack_enemy(self, enemy):
        #picks a random number from your max attack number and damages the enemy with that amount
        damage_to_enemy = random.randint(1, self.attack)
        enemy.take_damage(damage_to_enemy)
        #prints how much you have damaged enemy
        print(f'\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{self.name} has attacked for {damage_to_enemy} damage!')

    def add_money(self, amount_money):
        #adds the money you have earned to your total amount
        self.money += amount_money
        #prints out the money you have earned
        print(f'${amount_money} earned!')

    def level_up(self, amount_experience, name):
        #adds a level and 2 attack to your player if you have defeated an enemy 
        self.level += amount_experience 
        self.attack += 2
        #prints the current level with added attack
        print(f"{self.name} is now level {self.level}. \nAttack + 2\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def purchase_item(self, item):
        #purchasing items
        if self.money >= item.cost:
            #if you have enough money then you buy the item
            self.inventory.append(item)
            self.money -= item.cost
            #takes away money you have speant
            print(f"\n{item.name} bought for ${item.cost}\n")
            #once you have bought item, health or attack increases
            if item.name == "Food":
                self.health += 25
            elif item.name == "Magical Weapon":
                self.attack += 5
            elif item.name == "Flaming Crossbow":
                self.attack += 75        
        else:
            #for if you don't have enough money
            print('\nNot enough money\n')

def add_enemy():
    #list of possible enemies with their stats
    enemies = [Enemy("Dragon", 125, 20, 15, 1),
               Enemy("Alien", 100, 10, 10, 1),
               Enemy("Skeleton", 100, 8, 8, 1),
               Enemy("Creeper", 10, 100, 50, 1),
               ]
    #returns a random enemy
    return random.choice(enemies)

class Enemy(Character):
    #class for enemy
    def __init__(self, name, health, attack, money, experience):
        super().__init__(name, health, attack)
        self.money = money
        self.experience = experience

    def alive_or_dead(self):
        #returns true if enemy is alive (health above 0)
        return self.health > 0 

    def take_damage(self, damage):
        #takes away the damage amount from enemy's points
        self.health -= damage

    def attack_player(self, player):
        #picks a random number from enemy max attack number and damages the player with that amount
        damage_to_player = random.randint(1, self.attack)
        player.take_damage(damage_to_player)
        #prints out how much you have been attacked for
        print(f'{self.name} has attacked you for {damage_to_player} damage!')

class Item:
    #class for item
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description
    
    def __str__(self):
        #returns the item and its description
        return f"{self.name} - {self.description}"

class Description:
    #class for description of enemy
    def __init__(self, description):
        self.description = description
    
    def __str__(self):
        #returns the description of the enemy
        return f"{self.description}"

def main():
    #loads game
    saved_player = prompt_load_game()
    if saved_player:
        #if they choose to play saved game then it will resume
        player = saved_player
        print("Loaded saved game.")
    else:
        #if no saved game found it starts a new game
        print("What's your name?")
        player_name = str(input())
        player = Player(player_name)
        #welcomes user to the game
        print(f"\n++++++++++++++++++++\nWelcome to Brave Quest {player_name}! \nHere are your stats:\n")
        print(f"{display_stats(player)}")
        print(f"++++++++++++++++++++\n\nPlease choose an option to begin the game:")
    game_not_over = True
    while game_not_over:
        #main menu that repeats
        print("\nA - Fight")
        print("B - Buy items")
        print("C - View your items")
        print("D - View your stats")
        print("E - View enemy stats")
        print("F - Quit game\n")
        option = input().upper()

        if option == "A":
            #fighing enemy
            enemy = add_enemy()
            #adds enemy
            if enemy.name == "Dragon":
                #prints out the picture of a dragon
                print("\n\n        |     |\n       ((     ))\n   ===  \\_v_//  ===\n     ====|_^_|====\n     ===/ O O \===\n     = | /_ _\ | =\n    =   \/_ _\/   =\n         \_ _/\n         (o_o)\n          VwV")
            elif enemy.name == "Skeleton":
                #prints out the picture of a skeleton
                print("\n\n     /.-.\ \n     \o.o/\n      |=|\n     __|__\n   //.=|=.\\\ \n  // .=|=. \\\ \n  \\\ .=|=. // \n   \\\(_=_)// \n    \:| |:/\n     || ||\n     \/ \/\n     || ||\n     || ||\n    ==' '==")
            elif enemy.name == "Alien":
                #prints out the picture of a alien
                print("\n\n    o   o\n     \-/\n    \O O/\n     \=/\n    .-|-.\n   //\ /\\\n _// / \ \\_\n=./ |.-.| \.=\n    || ||\n    || ||    \n  __|| ||__  ")
            elif enemy.name == "Creeper":
                #prints out the picture of a creeper
                print("\n\n██████████\n█░░░░░░░░█\n█░██░░██░█\n█░░░██░░░█\n█░░████░░█\n█░░█░░█░░█\n█░░░░░░░░█\n██████████\n──█░░░░█\n──█░░░░█\n──█░░░░█\n──█░░░░█\n──█░░░░█\n──█░░░░█\n██████████\n█░░░██░░░█\n█░░░██░░░█\n█▄█▄██▄█▄█")
            print(f"\nYour enemy is the {enemy.name}. Fight!")
            while player.alive_or_dead() and enemy.alive_or_dead():
                #allows user to attack as long as both are alive
                print("Here's your options: \nA - Attack\nR - Run Away\n")
                choice = input().lower()
                if choice == 'a':
                    #attacks the enemy and returns the health of both the player and enemy. 
                    player.attack_enemy(enemy)
                    if enemy.alive_or_dead():
                        #if the enemy is still alive after attack, then player is attacked as well. 
                        enemy.attack_player(player)
                    if player.health < 0:
                        #avoids printing negative health
                        player.health = 0
                    if enemy.health < 0:
                        #avoids printing negative health
                        enemy.health = 0
                    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nPlayer health: {player.health}\nEnemy health: {enemy.health}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    
                elif choice == "r":
                    #runs away from the enemy
                    break
                else:
                    #doesn't allow invalid options
                    print("Please enter a valid option")
            if enemy.name == "Dragon" and not enemy.alive_or_dead():
                #if you have defeated dragon then you win
                print(" -ˋˏ ༘⋆ ༘⋆ ༘⋆ ༘  You Won! 😀 ༘⋆ ༘⋆⋆-ˋˏ")
                break
            if player.alive_or_dead() and not enemy.alive_or_dead():
                #adds money and level to player if the player is alive and enemy is dead
                player.add_money(enemy.money)
                player.level_up(enemy.experience, enemy.name)
            if not player.alive_or_dead():
                #quits game if you have been defeated
                print("You have been defeated! 😬")
                break

        elif option == "B":
            #item shop with descriptions of items
            print("\n=====================\nWelcome to shop!\nHere's what you can buy:\n")
            print("\nW - $30 Magical Weapon (Adds 5 to attack)\nF - $10 Food (Adds 25 to health)\nC - $60 Flaming Crossbow\nE - Exit\n=====================")
            print("\nWhat would you like?\n")
            choice = input().lower()
            if choice == "w":
                #magical weapon option
                player.purchase_item(Item("Magical Weapon", 30, "Adds 5 to attack"))
            elif choice == "f":
                #food option
                player.purchase_item(Item("Food", 10, "Adds 25 to health"))
            elif choice == "c":
                #crossbow option
                player.purchase_item(Item("Flaming Crossbow", 60, "Adds 75 to attack once"))
            elif choice == "e":
                #exits the shop
                continue
            else:
                print("\nPlease choose a valid option")
        
        elif option == "C":
            #if there is something in the player inventory, it will print the items
            if player.inventory:
                for item in player.inventory:
                    print(item)
            else:
                print("\nNo items in inventory\n")

        elif option == "D":
            #prints the player stats 
            print("\n++++++++++++++++++++")
            print(display_stats(player))
            print("++++++++++++++++++++\n")

        elif option == "E":
            #lets you read what the enemies have to say about themselves
            print("\nPlease choose an enemy to read about:\n")
            print("A - Dragon\nB - Skeleton\nC - Alien\nD - Creeper\n")
            choice = input().lower()
            valid = True
            while valid:
                if choice == "a":
                    #description for dragon
                    print(Description("\nAs the Dragon, I am the toughest of them all, you might not want to attack me first"))
                    valid = False
                elif choice == "b":
                    #description for skeleton
                    print(Description("\nI, the Skeleton, can easily beat you if you don't pay attention closely"))
                    valid = False
                elif choice == "c":
                    #description for alien
                    print(Description("\n%#$&*@#$%>>@#$>@:@::@???????"))
                    valid = False
                elif choice == "d":
                    #description for creeper
                    print(Description("\nIf you like to gamble then choose me. Or don't..."))
                    valid = False
                else:
                    #only accepts valid inputs
                    print("\nPlease choose a valid choice\n")
                    print("A - Dragon\nB - Skeleton\nC - Alien\nD - Creeper\n")
                    choice = input().lower()
                    valid = True

        elif option == "F":
            #quits the game and asks them if they want to save
            print("Game over. Thank you for playing")
            print("\nDo you want to save the game? (Y/N)")
            save_choice = input().upper()
            if save_choice == "Y":
                #saves game
                save_game(player)
                print("Game saved successfully.")
            break
        else:
            #doesn't allow invalid choices
            print("Please choose a valid choice")
        

def display_stats(player):
    #function for displaying the player's stats
    return f"Health: {player.health}\nAttack: {player.attack}\nMoney: ${player.money}"
    
if __name__ == "__main__":
    #runs main function 
    main()



    