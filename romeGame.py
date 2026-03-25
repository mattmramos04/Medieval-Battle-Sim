roman_army = {
    "morale" : 100,

    "legionaries" : {
        "hp": 100,
        "attack": 20,
        "defense": 10,
        "count": 50
    },
    "cavalry" : {
        "hp": 100,
        "attack": 30,
        "defense": 5,
        "count": 30
    },
    "archers" : {
        "hp": 100,
        "attack": 5,
        "defense": 3,
        "count": 50
    },
    "officers" : {
        "hp": 100,
        "attack": 10,
        "defense": 8,
        "count": 10
    }
}

carthaginian_army = {
    "morale" : 100,
    "legionaries" : {
        "hp": 100,
        "attack": 15,
        "defense": 8,
        "count": 50
    },

    "cavalry" : {
        "hp": 100,
        "attack": 40,
        "defense" : 5,
        "count": 50
    },

    "archers" : {
        "hp" : 100,
        "attack" : 8,
        "defense" : 2,
        "count" : 30
    },

    "officers" : {
        "hp": 100,
        "attack" : 12,
        "defense" : 5,
        "count" : 10
    }
}

traits= {
    "hard_headed" : {
    "name": "Hard Headed",
    "description": "+2 Legion Attack, -1 Legion Defense",
    "effects": {
        "legion_attack": 2,
        "legion_defense": -1
        }
    },

    "aim_for_the_eye" : {
        "name": "Aim For the Eye",
        "description": "+2 Archer Attack, -1 Legion Attack",
        "effects":{
            "archer_attack": 2,
            "legion_attack": -1
        }
    },

    "cowboy" : {
        "name": "Cowboy",
        "description": "+1 Cavalry Attack, -1 Archer Defense",
        "effects": {
            "cavalry_attack": 1,
            "archer_defense": -1
        }
    },

    "slow_and_steady" : {
        "name": "Slow and Steady",
        "description": "+ 2 Cavalry Defense, -1 Cavalry Attack",
        "effects": {
            "cavalry_defense": 2,
            "cavalry_attack": -1
        }
    },

    "chosen_one" : {
        "name": "Chosen One",
        "description": "+4 Legion Attack, -30 Troop Buy Points",
        "effects": {
            "legion_attack": 4,
            "points": -30
        }
    }
}


def resolve_combat(attacker, defender):
    attack_value = attacker["attack"]
    defense_value = defender["defense"]

    damage = attack_value - defense_value
    defender["count"] -= damage

def battle_round(atk_cnt):

    print(f"--- {attack_names[atk_cnt-1]} Attack ---")

    #Before snapshot of armysize
    roman_leg_before = roman_army["legionaries"]["count"]
    roman_cav_before = roman_army["cavalry"]["count"]
    roman_arc_before = roman_army["archers"]["count"]

    carth_leg_before = carthaginian_army["legionaries"]["count"]
    carth_cav_before = carthaginian_army["cavalry"]["count"]
    carth_arc_before = carthaginian_army["archers"]["count"]

    #First full battle
    resolve_combat(roman_army["legionaries"], carthaginian_army["legionaries"])
    resolve_combat(carthaginian_army["legionaries"], roman_army["legionaries"])

    #Second full battle
    resolve_combat(roman_army["cavalry"], carthaginian_army["cavalry"])
    resolve_combat(carthaginian_army["cavalry"], roman_army["cavalry"])

    #Third full battle
    resolve_combat(roman_army["archers"], carthaginian_army["archers"])
    resolve_combat(carthaginian_army["archers"], roman_army["archers"])

    #After snapshot of armysize (losses)
    roman_leg_losses = roman_leg_before - roman_army["legionaries"]["count"]
    roman_cav_losses = roman_cav_before - roman_army["cavalry"]["count"]
    roman_arc_losses = roman_arc_before - roman_army["archers"]["count"]

    carth_leg_losses = carth_leg_before - carthaginian_army["legionaries"]["count"]
    carth_cav_losses = carth_cav_before - carthaginian_army["cavalry"]["count"]
    carth_arc_losses = carth_arc_before - carthaginian_army["archers"]["count"]

    roman_total_losses = roman_arc_losses + roman_leg_losses + roman_cav_losses
    carth_total_losses = carth_arc_losses + carth_leg_losses + carth_cav_losses

    # Morale calculation costs for Rome
    if roman_army["officers"]["count"] > 0:
        roman_army["morale"] -= roman_total_losses // 2
    else:
        roman_army["morale"] -= roman_total_losses

    roman_army["morale"] -= 5

    print(f"Roman Morale: {roman_army['morale']} | Carthage Morale: {carthaginian_army['morale']}")

    # Morale calculation costs for Carthage
    if carthaginian_army["officers"]["count"] > 0:
        carthaginian_army["morale"] -= carth_total_losses // 2
    else:
        carthaginian_army["morale"] -= carth_total_losses
    carthaginian_army["morale"] -= 5

    if roman_army["morale"] > carthaginian_army["morale"]:
        print(f"The Roman army have successfully pushed back the Carthaginians in the {attack_names[atk_cnt-1]} Attack!")
    elif carthaginian_army["morale"] > roman_army["morale"]:
        print(f"The Carthaginian army have successfully pushed back the Romans in the {attack_names[atk_cnt-1]} Attack!")

    if roman_army["morale"] <= 0:
        print("The Romans have retreated! Carthage wins!")
    elif carthaginian_army["morale"] <= 0:
        print("The Carthaginians have retreated! Rome wins!")


atk_cnt = 0
attack_names = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Eigth", "Ninth", "Tenth"]

general_name = input("What is your generals name?: ")
print(f"Hail, General {general_name}! Rome awaits your command.")

while roman_army["morale"] > 0 and carthaginian_army["morale"] > 0 :
    atk_cnt +=1
    battle_round(atk_cnt)
