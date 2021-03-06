from player import *


# transforms an in-game action (actions available are listed above) into an str. Will be used to easily send data for
# multiplayer games
def serialize(player_name: str, action: str, entity=None, triggering_unit=None, pos_x: int = None,
              pos_y: int = None) -> str:
    """
        Args:
            player_name: (string) le nom du joueur à l origine de l action à sérialiser / propriétaire de l entité
            action: (string) un mot clé décrivant l’action à sérialiser
            entity: argument polyvalent dont le type dépend de l’action... unité type, bâtiment à construire, etc...
            triggering_unit: l unité qui déclenche l action à sérialiser ou sa position dans la liste d'unité du joueur
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

    return add_checksum(serialised_string)


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

    if not verify_checksum(action):
        #TODO faire la fonction pour faire renvoyer le message si checksum pas bon
        return -1
    else:
        action = action.split("/")[0]


    words = action.split('*')

    player = name_to_player(words[0])

    if player in player_list:

        #gather permet de faire en sorte qu'un villageois passé en paramètre aille récolter une ressource dont la
        #position est passée en paramètre
        if words[1] == "gather":
            if words[2] and words[3] and words[4]:
                villager = number_to_unit(int(words[2]), player)
                pos = (int(words[3]), int(words[4]))
                villager.go_to_ressource((pos[0], pos[1]))
                return 0
            else:
                return -1

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

        # build fait en sorte qu'un villageois passé en paramètre aille construire un batiment passé en paramètre sur
        # une tile passée en paramètre
        elif words[1] == "build":
            if words[2] and words[3] and words[4] and words[5]:

                villager = number_to_unit(int(words[3]), player)
                pos = (int(words[4]), int(words[5]))
                villager.go_to_build(pos, words[2])
                return 0
            else:
                return -1

        # research permet de rechercher une technologie passée en paramètre, ou de passer d'âge
        elif words[1] == "research":
            if words[2]:
                player.towncenter.research_tech(words[2])
                return 0
            else:
                return -1

        elif words[1] == "attack":
            if words[2] and words[3] and words[4]:
                triggering_unit = number_to_unit(int(words[2]), player)
                target_pos = (int(words[3]), int(words[4]))
                triggering_unit.go_to_attack(target_pos)


        #move fait en sorte qu'un villageois bouge vers la tile dont on a passé les coordonnés en paramètre
        elif words[1] == "move":
            if words[2] and words[3] and words[4]:
                print(words[2], words[3], words[4])
                unit = number_to_unit(int(words[2]), player)
                pos = (int(words[3]), int(words[4]))
                unit.move_to(world.map[pos[0]][pos[1]])
                return 0
            else:
                return -1

        #train permet d'entrainer une unité du type qu'on passe en paramètre
        elif words[1] == "train":
            if words[2]:
                if words[2] == "Villager":
                    unit_to_train = str_to_type(words[2])
                    player.towncenter.train(unit_to_train)
                    return 0
                else:
                    if player.barrack_list:
                        unit_to_train = str_to_type(words[2])
                        player.barrack_list[0].train(unit_to_train)
                        return 0
                    else:
                        return -1

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
        
        #permet à une unité de retourner au townhall pour se vider de ses ressources
        elif words[1] == "townhall":
            if words[2] and world:
                unit = number_to_unit(int(words[2]), player)
                unit.go_to_townhall()
                return 0

            else:
                return -1
        
        # la commande n'a pas été reconnue ou des mots clés manquent; PANIC
        else:
            return -1

def add_checksum(serialised_string):
    checksum = 0
    serialised_string += "/"
    for c in serialised_string:
        checksum += ord(c)
    return serialised_string+str(checksum)

def verify_checksum(serialised_string):
    new_checksum = 0
    old_checksum = 0
    for i in range(len(serialised_string)):
        if serialised_string[i] == "/":
            new_checksum += ord("/")
            old_checksum = int(serialised_string[i+1:])
            break
        else:
            new_checksum += ord(serialised_string[i])

    return True if old_checksum == new_checksum else False



# returns the player from his name
def name_to_player(player_name):
    for p in player_list:
        if p.name == player_name:
            return p
    return None


# returns the unit from her number in the unit list of the player
def number_to_unit(number, player):
    return player.unit_list[number]

def str_to_type(string):
    if string == "Villager":
        return Villager
    elif string == "Clubman":
        return Clubman



##########################################################TESTS#########################################################

#action = serialize(player_name="PlayerOne", action="attack",
#                                                           triggering_unit=1, pos_x=25, pos_y=25)

#new_action = add_checksum(action)

#deserialize(new_action)
