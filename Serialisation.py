from player import *

"""
player action(ressource / unit / building)(with+unit) (to+tile):
- playerOne gather  resource unit
- playerOne build building unit1 pos_x pos_y  *
- playerOne research tech1                    *
- playerOne attack enemy_unit unit
- playerOne move unit pos_x pos_y             *
- playerOne train unit
- playerOne spawn pos_x pos_y
- playerOne clear pos_x pos_y
"""


# transforms an in-game action (actions available are listed above) into an str. Will be used to easily send data for
# multiplayer games
def serialize(player_name: str, action: str, entity=None, triggering_unit=None, pos_x: int = None,
              pos_y: int = None) -> str:
    """
        Args:
            player_name: le joueur à l origine de l action à sérialiser / propriétaire de l entité
            action: (string) un mot clé décrivant l’action à sérialiser
            entity: argument polyvalent dont le type dépend de l’action... unité type, bâtiment à construire, etc...
            triggering_unit: l unité qui déclenche l action à sérialiser
            pos_x: (int) la position en x de l unité ou la tile
            pos_y: (int) la position en y de l unité ou la tile

        Returns: une chaîne de caractères ; chaque mot clé est séparé par *
    """

    serialised_string = ""
    serialised_string += player_name
    serialised_string += "*"
    serialised_string += str(action)

    if entity is not None:
        serialised_string += "*"
        serialised_string += str(entity)

    if triggering_unit is not None:
        serialised_string += "*"
        serialised_string += str(triggering_unit)

    if pos_x is not None and pos_y is not None:
        serialised_string += "*"
        serialised_string += str(pos_x)
        serialised_string += "*"
        serialised_string += str(pos_y)

    return serialised_string


# transforms a str created with the serialize method to the corresponding in-game action
# Mainly used to receive actions from other players in multiplayer games into your local version of the map.
def deserialize(action: str, world=None) -> int:
    """
        Args:
            action: (string) une séquence de mots clés décrivant l’action à sérialiser; chaque mot clé est séparé
            par une *
            world: la map locale sur laquelle appliquer l action

        Returns: 0 si l action a été implémentée avec succès sur la map. -1 autrement (data transmises sans doute
        corrompues)
    """
    words = action.split('*')

    player = name_to_player(words[0])

    if player in player_list:

        if words[1] == "gather":
            if words[2] and words[4]:
                pass
                # words[4].gather(...)

        # playerOne*spawn*pos_x*pox_y
        # utilisé pour communiquer l emplacement de départ d un joueur
        elif words[1] == "spawn":
            if words[2] and words[3] and world:
                corner_pos_x = int(words[2])
                corner_pos_y = int(words[3])
                world.place_starting_units(player, (corner_pos_x, corner_pos_y))
                return 0
            # la commande n'a pas été reconnue ou des mots clés manquent; PANIC
            else:
                return -1

        elif words[1] == "build":
            if words[2] and words[3] and words[4] and words[5]:
                # working_villager.go_to_build(grid_pos, self.hud.selected_tile["name"])
                villager = number_to_unit(int(words[3]), player)
                pos = (int(words[4]), int(words[5]))
                villager.go_to_build(pos, words[2])

        elif words[1] == "research":
            if words[2]:
                player.towncenter.research_tech(words[2])

        elif words[1] == "attack":
            pass
            # TODO

        elif words[1] == "move":
            if words[2] and words[3] and words[4]:
                print(words[2], words[3], words[4])
                unit = number_to_unit(int(words[2]), player)
                pos = (int(words[3]), int(words[4]))
                unit.move_to(pos)
                # TODO (not finished)

        elif words[1] == "train":
            if words[2]:
                pass
                # TODO
                # player.towncenter.train()

        #clear enlève les ressources ; pas les unités ni les bâtiments; Fonction testée avec alt_gauche en jeu
        elif words[1] == "clear":
            if words[2] and words[3] and world:
                # convert str to int for our clear_tile function
                tile_pos_x = int(words[2])
                tile_pos_y = int(words[3])
                world.clear_tile(tile_pos_x, tile_pos_y)
                return 0

            else:
                return -1

        # la commande n'a pas été reconnue ou des mots clés manquent; PANIC
        else:
            return -1


# returns the player from his name
def name_to_player(player_name):
    for p in player_list:
        if p.name == player_name:
            return p
    return None


# returns the unit from her number in the unit list of the player
def number_to_unit(number, player):
    return player.unit_list[number]
