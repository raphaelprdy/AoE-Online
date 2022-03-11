from player import *
from utils import name_to_player

"""
player action(ressource / unit / building)(with+unit) (to+tile):
- playerOne gather r1 with unit1
- playerOne build b1 with unit1
- playerOne changeAge
- playerOne research tech1
- playerOne attack enemy_unit1 with unit1
- playerOne move unit1 to tile1
"""


def form_action(player_name, action, entity=None, unit=None, tile=None):
    action += player_name
    action += " "
    action += str(action)

    if entity is not None:
        action += " "
        action += str(entity)

    if unit is not None:
        action += " "
        action += "with"
        action += " "
        action += str(unit)

    if tile is not None:
        action += " "
        action += "to"
        action += " "
        action += str(tile)

    return action


def trad_action(action):
    words = action.split()

    player = name_to_player(words[0])

    if player in playerList:
        if words[1] == "gather":
            if words[0] and words[2] and words[4]:
                pass
                #words[4].gather(...)
        elif words[1] == "research":
            pass
        elif words[1] == "build":
            pass
        elif words[1] == "changeAge":
            if words[2]:
                player.towncenter.research_tech(words[2])
        elif words[1] == "attack":
            pass
        elif words[1] == "move":
            pass
        else:
            #envoyer "commande corrompue"
            pass


