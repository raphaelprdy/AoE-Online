from player import *

"""
player action(ressource / unit / building)(with+unit) (to+tile):
- playerOne gather  resource unit
- playerOne build building unit1 pos_x pos_y  *
- playerOne research tech1                    *
- playerOne attack enemy_unit unit
- playerOne move unit pos_x pos_y             *
- playerOne train unit
- playerOne spawn
"""


def form_action(player_name, action, entity=None, unit=None, pos_x=None, pos_y=None):
    serialised_string = ""
    serialised_string += player_name
    serialised_string += "*"
    serialised_string += str(action)

    if entity is not None:
        serialised_string += "*"
        serialised_string += str(entity)

    if unit is not None:
        serialised_string += "*"
        serialised_string += str(unit)

    if pos_x is not None and pos_y is not None:
        serialised_string += "*"
        serialised_string += str(pos_x)
        serialised_string += "*"
        serialised_string += str(pos_y)

    return serialised_string


def trad_action(action):
    words = action.split('*')

    player = name_to_player(words[0])

    if player in player_list:
        if words[1] == "gather":
            if words[2] and words[4]:
                pass
                #words[4].gather(...)

        elif words[1] == "spawn":
            pass
            #TODO

        elif words[1] == "build":
            if words[2] and words[3] and words [4] and words[5]:
                #working_villager.go_to_build(grid_pos, self.hud.selected_tile["name"])
                villager = number_to_unit(int(words[3]), player)
                pos = (int(words[4]), int(words[5]))
                villager.go_to_build(pos, words[2])

        elif words[1] == "research":
            if words[2]:
                player.towncenter.research_tech(words[2])

        elif words[1] == "attack":
            pass
            #TODO

        elif words[1] == "move":
            if words[2] and words[3] and words[4]:
                print(words[2], words[3], words[4])
                unit = number_to_unit(int(words[2]), player)
                pos = (int(words[3]), int(words[4]))
                unit.move_to(pos)
                #TODO (not finished)

        elif words[1] == "train":
            if words[2]:
                pass
                #TODO
                #player.towncenter.train()

        else:
            pass
            #TODO
            # envoyer "commande corrompue"

#returns the player from his name
def name_to_player(player_name):
    for p in player_list:
        if p.name == player_name:
            return p
    return None

#returns the unit from her number in the unit list of the player
def number_to_unit(number, player):
    return player.unit_list[number]
