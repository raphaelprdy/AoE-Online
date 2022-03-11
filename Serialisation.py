from player import *

"""
player action(ressource / unit / building)(with+unit) (to+tile):
- playerOne gather r1 unit1
- playerOne build b1 unit1
- playerOne research tech1                  *
- playerOne attack enemy_unit1 unit1
- playerOne move unit1 tile1
- playerOne train unit
- playerOne spawn
"""


def form_action(player_name, action, entity=None, unit=None, tile=None):
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

    if tile is not None:
        serialised_string += "*"
        serialised_string += str(tile)

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
        elif words[1] == "build":
            if words[2] and words[3]:
                pass
        elif words[1] == "research":
            if words[2]:
                player.towncenter.research_tech(words[2])
        elif words[1] == "attack":
            pass
        elif words[1] == "move":
            pass
        elif words[1] == "train":
            if words[2]:
                pass
                #player.towncenter.train()
        else:
            #envoyer "commande corrompue"
            pass


