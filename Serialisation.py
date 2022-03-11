"""
player action(ressource / unit / building)(with+unit) (to+tile):
- playerOne gather r1 with unit1
- playerOne build b1 with unit1
- playerOne changeAge
- playerOne research tech1
- playerOne attack enemy_unit1 with unit1
- playerOne move unit1 to tile1
"""


def form_action(player, action, entity=None, unit=None, tile=None):
    action += str(player)
    action += " "
    action += str(action)

    if entity is not None:
        action += " "
        action += str(object)

    if unit is not None:
        action += " "
        action += "with"
        action += " "
        action += str(object)

    if tile is not None:
        action += " "
        action += "to"
        action += " "
        action += str(object)

    return action


def trad_action(action):
    words = action.split()
    if words[0] in playerList:
        if words[1] == "gather":
            if words[0] and words[2] and words[4]:
                pass
                #words[4].gather(...)
        elif words[1] == "research":
            pass
        elif words[1] == "build":
            pass
        elif words[1] == "changeAge":
            pass
        elif words[1] == "attack":
            pass
        elif words[1] == "move":
            pass
        else:
            #envoyer "commande
            pass


