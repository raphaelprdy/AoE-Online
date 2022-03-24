import pygame
from settings import MAP_SIZE_X, MAP_SIZE_Y

EQ_TABLE = {"tree" : ord('0'), "rock" : ord('A'), "gold" : ord('H'), "berrybush" : ord('O')}
RESSOURCE_LIST = ["wood", "food", "gold", "stone"]

GENERAL_UNIT_LIST = []
GENERAL_BUILDING_LIST = []

UNIT_TYPES = []
BUILDING_TYPES = []


#Global parameters of the game

TEST_MODE = True
IA_MODE = False
SPEED_OF_GAME = 1
MULTIPLAYER_MODE = True


def draw_text(screen, text: str, size: int, color: (int, int, int), pos: (int, int)):
    # create a Font object from the system fonts
    # SysFont(name, size, bold=False, italic=False)

    # font = pygame.font.SysFont(None, size)

    font = pygame.font.SysFont('Times New Roman', size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)


# 2D -> 2.5D
def decarte_to_iso(x, y):
    iso_x = x - y
    iso_y = (x + y) / 2
    return iso_x, iso_y


def iso_to_decarte(iso_x, iso_y):
    y = (2 * iso_y - iso_x) / 2
    x = (2 * iso_y + iso_x) / 2
    return x, y


def scale_image(image, w=None, h=None):
    if (w is None) and (h is None):
        pass
    elif h is None:
        scale = w / image.get_width()
        h = scale * image.get_height()
        image = pygame.transform.scale(image, (int(w), int(h)))
    elif w is None:
        scale = h / image.get_height()
        w = scale * image.get_width()
        image = pygame.transform.scale(image, (int(w), int(h)))
    else:
        image = pygame.transform.scale(image, (int(w), int(h)))

    return image


    #returns RGB_code corresponding to the color argument(red,green,blue)
    #red, green, blue going from 0 to 255, with 255 being the closer to full color and 0 to none/black
def get_color_code(color: str):

    if color == "WHITE":
        return 255, 255, 255

    elif color == "BLACK":
        return 0, 0, 0

    elif color == "GREY":
        return 60, 60, 60

    elif color == "BLUE":
        return 0, 0, 255

    elif color == "GREEN":
        return 0, 255, 0

    elif color == "DARK_GREEN":
        return 0, 190, 20

    elif color == "RED":
        return 255, 0, 0

    elif color == "DARK_RED":
        return 138, 3, 3

    elif color == "DEFEAT_RED":
        return 158, 43, 43

    elif color == "DARK_GRAY":
        return 25, 25, 25

    elif color == "ORANGE":
        return 255, 127, 0

    elif color == "YELLOW":
        return 255, 255, 0

    elif color == "GOLD":
        return 255, 201, 14


#def str_to_entity_class(name: str):
 #   if name == "TownCenter":
  #      return TownCenter
   # elif name == "House":
    #    return House
    #elif name == "Farm":
     #   return Farm

    #elif name == "Villager":
     #   return Villager
    #elif name == "Clubman":
     #   return Clubman
    #elif name == "Bowman":
     #   return Bowman

# this methode return a list of the x nearest free tiles
def tile_founding(x, first_layer, layer_max, map, player, tile_type, MAP=None):
    #here we convert the ressource we want to the corresponding ressource type on the map
    if tile_type == "wood": tile_type = "tree"
    if tile_type == "stone": tile_type = "rock"
    if tile_type == "food": tile_type = "berrybush"

    list_of_tile = []
    nb_of_tile_left_to_found = x
    layer = first_layer
    tc_pos = player.towncenter_pos

    # while we dont have all the tiles we want or the layer max is reached, we keep going
    while nb_of_tile_left_to_found > 0 and layer <= layer_max:
        # we look at the top and bot side of the square formed by the tile of the
        for j in range(layer * 2 + 2):
            # if the tile is empty we add it to the list and we decrease the nb of tile left to found
            pos_x = tc_pos[0] - layer + j
            pos_y = tc_pos[1] - layer - 1
            if 0 <= pos_x < MAP_SIZE_X and 0 <= pos_y < MAP_SIZE_Y and map[pos_x][pos_y]["tile"] == tile_type and \
                    nb_of_tile_left_to_found > 0:
                if tile_type != "" or MAP is None:
                    list_of_tile.append((pos_x, pos_y))
                    nb_of_tile_left_to_found -= 1
                else:
                    if MAP is not None and MAP.collision_matrix[pos_y][pos_x]:
                        list_of_tile.append((pos_x, pos_y))
                        nb_of_tile_left_to_found -= 1

            pos_x = tc_pos[0] - layer + j
            pos_y = tc_pos[1] + layer
            if 0 <= pos_x < MAP_SIZE_X and 0 <= pos_y < MAP_SIZE_Y and map[pos_x][pos_y]["tile"] == tile_type and \
                    nb_of_tile_left_to_found > 0:
                if tile_type != "" or MAP is None:
                    list_of_tile.append((pos_x, pos_y))
                    nb_of_tile_left_to_found -= 1
                else:
                    if MAP is not None and MAP.collision_matrix[pos_y][pos_x]:
                        list_of_tile.append((pos_x, pos_y))
                        nb_of_tile_left_to_found -= 1

        for k in range(1, layer * 2 + 1):
            pos_x = tc_pos[0] - layer
            pos_y = tc_pos[1] - layer - 1 + k
            if 0 <= pos_x < MAP_SIZE_X and 0 <= pos_y < MAP_SIZE_Y and map[pos_x][pos_y]["tile"] == tile_type and \
                    nb_of_tile_left_to_found > 0:
                if tile_type != "" or MAP is None:
                    list_of_tile.append((pos_x, pos_y))
                    nb_of_tile_left_to_found -= 1
                else:
                    if MAP is not None and MAP.collision_matrix[pos_y][pos_x]:
                        list_of_tile.append((pos_x, pos_y))
                        nb_of_tile_left_to_found -= 1

            pos_x = tc_pos[0] + layer + 1
            pos_y = tc_pos[1] - layer - 1 + k
            if 0 <= pos_x < MAP_SIZE_X and 0 <= pos_y < MAP_SIZE_Y and map[pos_x][pos_y]["tile"] == tile_type and \
                    nb_of_tile_left_to_found > 0:
                if tile_type != "" or MAP is None:
                    list_of_tile.append((pos_x, pos_y))
                    nb_of_tile_left_to_found -= 1
                else:
                    if MAP is not None and MAP.collision_matrix[pos_y][pos_x]:
                        list_of_tile.append((pos_x, pos_y))
                        nb_of_tile_left_to_found -= 1

        layer += 1
    return list_of_tile


def look_around(pos, map):
    list = []
    if 0 <= pos[0]+1 < MAP_SIZE_X and map[pos[0]+1][pos[1]]["tile"] == "":
        list.append(True)
    else:
        list.append(False)

    if 0 <= pos[0]-1 < MAP_SIZE_X and map[pos[0]-1][pos[1]]["tile"] == "":
        list.append(True)
    else:
        list.append(False)

    if 0 <= pos[1]+1 < MAP_SIZE_Y and map[pos[0]][pos[1] + 1]["tile"] == "":
        list.append(True)
    else:
        list.append(False)

    if 0 <= pos[1]-1 < MAP_SIZE_Y and map[pos[0]][pos[1]-1]["tile"] == "":
        list.append(True)
    else:
        list.append(False)

    return True if any(list) else False


def better_look_around(villager_pos, ressource_pos, map):
    list = []
    if 0 <= ressource_pos[0] + 1 < MAP_SIZE_X and map[ressource_pos[0] + 1][ressource_pos[1]]["tile"] == "" and \
            villager_pos[0] >= ressource_pos[0]:
        list.append(True)
    else:
        list.append(False)

    if 0 <= ressource_pos[0] - 1 < MAP_SIZE_X and map[ressource_pos[0] - 1][ressource_pos[1]]["tile"] == "" and \
            villager_pos[0] <= ressource_pos[0]:
        list.append(True)
    else:
        list.append(False)

    if 0 <= ressource_pos[1] + 1 < MAP_SIZE_Y and map[ressource_pos[0]][ressource_pos[1] + 1]["tile"] == "" and \
            villager_pos[1] >= ressource_pos[1]:
        list.append(True)
    else:
        list.append(False)

    if 0 <= ressource_pos[1] - 1 < MAP_SIZE_Y and map[ressource_pos[0]][ressource_pos[1] - 1]["tile"] == "" and \
            villager_pos[1] <= ressource_pos[1]:
        list.append(True)
    else:
        list.append(False)

    return True if any(list) else False


def is_adjacent_to(pos1, pos2):
    if 0 <= pos1[0] < MAP_SIZE_X and 0 <= pos2[0] < MAP_SIZE_X and 0 <= pos1[1] < MAP_SIZE_Y and \
            0 <= pos2[1] < MAP_SIZE_Y:
        if (abs(pos1[0] - pos2[0]) <= 1 and pos1[1] == pos2[1]) or \
                (abs(pos1[1] - pos2[1]) <= 1 and pos1[0] == pos2[0]):
            return True

        else:
            return False


def find_owner(pos):
    for u in GENERAL_UNIT_LIST:
        unit_pos = list(u.pos)
        if unit_pos == pos:
            return u.owner

    for b in GENERAL_BUILDING_LIST:
        bat_pos= list(b.pos)
        if bat_pos == pos:
            return b.owner


# returns the angle between the origin tile and the destination tile. Angle goes from 0 to 360, 0 top, 90 right, etc...
def get_angle_between(origin_tile_pos: [int, int], end_tile_pos: [int, int]):
    # first we calculate angle between grid, then we will apply some maths to get the "real" isometric angle
    # if origin == destination, no calcul
    angle = 0

    # linear movement : left right ; y the same, x varies
    if end_tile_pos[1] == origin_tile_pos[1]:
        # from left to right
        if end_tile_pos[0] > origin_tile_pos[0]:
            angle = 90
        # else from right to left
        else:
            angle = 270

    # linear movement : top bottom ; x the same, y varies
    elif end_tile_pos[0] == origin_tile_pos[0]:
        # from top to bottom
        if end_tile_pos[1] > origin_tile_pos[1]:
            angle = 180

        # else from bottom to top
        else:
            angle = 0

    # diagonal movement : top left bottom right ; dx = dy
    elif end_tile_pos[0] - origin_tile_pos[0] == end_tile_pos[1] - origin_tile_pos[1]:
        # if going down
        if end_tile_pos[0] - origin_tile_pos[0] > 0:
            angle = 135

        # else he is going up
        else:
            angle = 315

    # diagonal movement : top right bottom left ; dx = - dy
    elif end_tile_pos[0] - origin_tile_pos[0] == - (end_tile_pos[1] - origin_tile_pos[1]):
        # if going towards top right
        if end_tile_pos[0] - origin_tile_pos[0] > 0:
            angle = 45

        # else he is going bottom left
        else:
            angle = 225

    # transformation to get isometric
    angle = angle + 45

    return angle

def get_char(t):
    #we must verify that the tile exists. If not, we're in big trouble
    assert t
    #if there's nothing on the tile, it's only grass. Grass = 0, variation will be generated later.
    if not t["tile"] :
        return "_"
    #if there's something on the tile we'll find out what it is and get it's variation
    else :
        return chr(EQ_TABLE[t["tile"]] + t["variation"])

def char_to_resource(char) :
    res = {"tile" : "", "variation" : 0}
    if '0' <= char <= '9' :
        res["tile"] = "tree"
        res["variation"] = ord(char) - ord('0')
    elif 'A' <= char <= 'G' :
        res["tile"] = "rock"
        res["variation"] = ord(char) - ord('A')
    elif 'H' <= char <= 'N' :
        res["tile"] = "gold"
        res["variation"] = ord(char) - ord('H')
    elif 'O' <= char <= 'Q' :
        res["tile"] = "berrybush"
        res["variation"] = ord(char) - ord('O')

    return res

def print_str_map(map, raw=True) :
    #use this function ONLY IF you're using a map that has been converted to str.
    assert isinstance(map, list)
    #if we want to see the str map as it is (= without any interpretation), we leave raw to "True"
    if raw :
        #we print each line after each other
        for line in range(len(map)):
            print(map[line])
    
    #else we want to know what each char stands for
    else :
        interpreted_map=[]
        for line in range(len(map)) :
            #we first have to find at which character the line start : we know that it's after the first /, so we have to find / in the line
            cmpt = 0
            i = map[line][cmpt]
            #quite a simple way to find /
            while i != '/' :
                cmpt += 1
                i = map[line][cmpt]
            print(i)
            print(map[line][cmpt]," ",map[line][cmpt+1])
            #we start looking at what's inside the line AFTER /, so at character cmpt+1
            for column in range(cmpt + 1,len(map)) :
                interpreted_map.append("")
                #we convert each char to a ressource with a variation
                ressource = char_to_resource(map[line][column])
                #based on the ressource, we print different letters
                if ressource["tile"] == "tree" :
                    interpreted_map[line] += 'T'
                elif ressource["tile"] == "rock" :
                    interpreted_map[line] += 'r'
                elif ressource["tile"] == "berrybush" :
                    interpreted_map[line] += 'b'
                elif ressource["tile"] == "gold" :
                    interpreted_map[line] += 'g'
                else :
                    interpreted_map[line] += '_'

        #we only print what the map contains, not the checksums, because they are useless if we don't see the variation at the same time
        for line in range(len(map)):
            divided_line = interpreted_map[line].split('/')
            print(divided_line[0])
        #prompt which explains to the person reading the map what each letter on the map stands for
        print("Légende : _ = grass (not g to ease the reading), T = tree, g = gold, b = berrybush, r = rock")

def is_verified(str_map):
    #use this funtion ONLY with a str_map
    assert isinstance(str_map, list)
    #we split each line of the str_map : first element is the number of the line, second is the resources of the line, third is the checksum of the line and last is the checksum of the column
    for line in range(len(str_map)):
        #initialize the checksums to 0
        line_checksum = 0
        column_checksum = 0
        #we get the current line and divide it to get all of its caracteristics
        curr_line = str_map[line].split('/')
        #we check every character in the current line
        for char in range(len(str_map)):
            #we add the ascii value of the character to the first checksum
            line_checksum += ord(curr_line[1][char])
            offset = 1 if char < 10 else 2
            column_checksum += ord(str_map[char][line + offset + 1])
        if str(line_checksum) != curr_line[2] or str(column_checksum) != curr_line[3]:
            print("WRONG CHECKSUM")


def unit_to_list_index(unit):
    index = 0
    for u in unit.owner.unit_list:
        if u == unit:
            return index
        index += 1