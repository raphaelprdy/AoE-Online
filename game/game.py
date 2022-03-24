from .camera import Camera
from .map import *
from .utils import draw_text, find_owner, IA_MODE
from .hud import Hud
from .animation import *
#from .AI import AI
from.new_AI import new_AI
from time import sleep

from Serialisation import *


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        # hud
        self.hud = Hud(self.width, self.height, self.screen)

        # entities list (units, buildings, etc...)
        self.entities = []

        #str_map for tests
        self.str_map2 = ['0/01234567890123456789012345678901234567890123456789/0000/0000',
                         '1/01234567890123456789012345678901234567890123456789/0000/0000',
                         '2/01234567890123456789012345678901234567890123456789/0000/0000',
                         '3/01234567890123456789012345678901234567890123456789/0000/0000',
                         '4/01234567890123456789012345678901234567890123456789/0000/0000',
                         '5/01234567890123456789012345678901234567890123456789/0000/0000',
                         '6/01234567890123456789012345678901234567890123456789/0000/0000',
                         '7/01234567890123456789012345678901234567890123456789/0000/0000',
                         '8/01234567890123456789012345678901234567890123456789/0000/0000',
                         '9/01234567890123456789012345678901234567890123456789/0000/0000',
                         '10/01234567890123456789012345678901234567890123456789/0000/0000',
                         '11/01234567890123456789012345678901234567890123456789/0000/0000',
                         '12/01234567890123456789012345678901234567890123456789/0000/0000',
                         '13/01234567890123456789012345678901234567890123456789/0000/0000',
                         '14/01234567890123456789012345678901234567890123456789/0000/0000',
                         '15/01234567890123456789012345678901234567890123456789/0000/0000',
                         '16/01234567890123456789012345678901234567890123456789/0000/0000',
                         '17/01234567890123456789012345678901234567890123456789/0000/0000',
                         '18/01234567890123456789012345678901234567890123456789/0000/0000',
                         '19/01234567890123456789012345678901234567890123456789/0000/0000',
                         '20/01234567890123456789012345678901234567890123456789/0000/0000',
                         '21/01234567890123456789012345678901234567890123456789/0000/0000',
                         '22/01234567890123456789012345678901234567890123456789/0000/0000',
                         '23/01234567890123456789012345678901234567890123456789/0000/0000',
                         '24/01234567890123456789012345678901234567890123456789/0000/0000',
                         '25/01234567890123456789012345678901234567890123456789/0000/0000',
                         '26/01234567890123456789012345678901234567890123456789/0000/0000',
                         '27/01234567890123456789012345678901234567890123456789/0000/0000',
                         '28/01234567890123456789012345678901234567890123456789/0000/0000',
                         '29/01234567890123456789012345678901234567890123456789/0000/0000',
                         '30/01234567890123456789012345678901234567890123456789/0000/0000',
                         '31/01234567890123456789012345678901234567890123456789/0000/0000',
                         '32/01234567890123456789012345678901234567890123456789/0000/0000',
                         '33/01234567890123456789012345678901234567890123456789/0000/0000',
                         '34/01234567890123456789012345678901234567890123456789/0000/0000',
                         '35/01234567890123456789012345678901234567890123456789/0000/0000',
                         '36/01234567890123456789012345678901234567890123456789/0000/0000',
                         '37/01234567890123456789012345678901234567890123456789/0000/0000',
                         '38/01234567890123456789012345678901234567890123456789/0000/0000',
                         '39/01234567890123456789012345678901234567890123456789/0000/0000',
                         '40/01234567890123456789012345678901234567890123456789/0000/0000',
                         '41/01234567890123456789012345678901234567890123456789/0000/0000',
                         '42/01234567890123456789012345678901234567890123456789/0000/0000',
                         '43/01234567890123456789012345678901234567890123456789/0000/0000',
                         '44/01234567890123456789012345678901234567890123456789/0000/0000',
                         '45/01234567890123456789012345678901234567890123456789/0000/0000',
                         '46/01234567890123456789012345678901234567890123456789/0000/0000',
                         '47/01234567890123456789012345678901234567890123456789/0000/0000',
                         '48/01234567890123456789012345678901234567890123456789/0000/0000',
                         '49/01234567890123456789012345678901234567890123456789/0000/0000']

        self.str_map = ["0/__________________________________1397006792935___/4200/3941",
                        "1/_________________________________22299026505023___/4139/3945",
                        "2/6_______________________________624412003640555___/4051/3992",
                        "3/_______________________________312537265717469____/4113/4027",
                        "4/_____________________________55839235064388523____/4030/4078",
                        "5/____OD___Q__________________77666205486491126_____/3974/4087",
                        "6/__________________________7401198110188880693_____/3940/4251",
                        "7/___________________________33210483470757664______/4021/4319",
                        "8/____________________________873513500205460______Q/4080/4368",
                        "9/_____________________________521070759347_________/4236/4456",
                        "10/__G__________________B_____O__2348916472__________/4257/4597",
                        "11/_1___P__GO_____________________77466742______A____/4286/4500",
                        "12/_____F_____Q_____I______P_O______4793_____________/4493/4452",
                        "13/_______________2___________________C_______A______/4647/4292",
                        "14/___________9______________________________________/4712/4339",
                        "15/__________________________________________________/4750/4279",
                        "16/_7__9________________________N____________________/4655/4380",
                        "17/_______________6__________________________________/4709/4350",
                        "18/_____________022696__9_____I__________L___H__6__1_/4304/4562",
                        "19/____________3076623_____O_B_______________________/4403/4703",
                        "20/____________3672422_A_____________________________/4417/4702",
                        "21/____________9488344_____________F_________________/4436/4683",
                        "22/_____________20866________________627________H____/4388/4631",
                        "23/___________________________M____0355339___________/4431/4362",
                        "24/_____________D_________________1904559259_________/4302/4225",
                        "25/_____________________________1584511350115O_______/4163/4201",
                        "26/___________A________________012679936857990_______/4096/3989",
                        "27/__B9_Q_____________________491357552786993793I_2__/3858/3818",
                        "28/_________________H________532139520270970387172___/3823/3684",
                        "29/2900_____________________0372565508523358599347007/3509/3396",
                        "30/619580P__________________5771604189310664957359204/3419/3389",
                        "31/09624283________________47999374399552838293534628/3332/3303",
                        "32/643826085______________525147589903989172660429210/3224/3156",
                        "33/286136237_____________7554236897126010024152779444/3164/3082",
                        "34/9369767854_______J____9127488498997546257073575163/3158/2993",
                        "35/5594254218____________6678203899207142537086665163/3139/2964",
                        "36/2045649252_____________574740381642497652162513956/3172/3023",
                        "37/2378887313__________M__087366845087028266304590296/3167/3091",
                        "38/697715087_M____________821532579971851494104524525/3208/3046",
                        "39/84782621________________12701037143698213113763256/3282/3172",
                        "40/66104081________________54867104953113829245823249/3293/3252",
                        "41/0310350__________________8633509593603314210450719/3355/3280",
                        "42/467846_________________HJ_503186810650184769353175/3433/3319",
                        "43/72823______________________44273040792205749130840/3541/3400",
                        "44/3540N______________________63436605926465044497150/3575/3471",
                        "45/539__________89___P________K6363423781264339293118/3574/3500",
                        "46/5____AQ_J__502655______4____9969946566064691698787/3447/3686",
                        "47/__________18247187________2__426068669763084482210/3472/3793",
                        "48/_________052875583_____H1____35794564712586363987_/3469/3842",
                        "49/________8105668179_0_________2362303735484233134__/3457/3933"]
        # map
        self.map = Map(self.hud, self.entities, 50, 50, self.width, self.height)

        # camera
        self.camera = Camera(self.width, self.height, self.map)
        self.hud.camera = self.camera

        self.timer = self.map.timer


        # on centre la camera au milieu de la carte
        #th_x = self.map.place_x
        th_x = 25
        #th_y = self.map.place_y
        th_y = 25
        cam_x = (iso_to_decarte(th_x*64, th_y*32)[0]) - 4050
        cam_y = (iso_to_decarte(th_x*64, th_y*32)[1]) - 1200
        self.camera.scroll = pygame.Vector2(cam_x, cam_y)

        # IA
        if IA_MODE:
            # we chose a behaviour between all the behaviours we defined
            self.behaviour_possible = ["neutral", "defensive", "aggressive", "pacifist"]

            if TEST_MODE or MAIN_PLAYER != playerOne:
                self.AI_1 = new_AI(playerOne, self.map, self.behaviour_possible[2])

            if TEST_MODE or MAIN_PLAYER != playerTwo:
                self.AI_2 = new_AI(playerTwo, self.map, self.behaviour_possible[0])

            if TEST_MODE or MAIN_PLAYER != playerThree:
                self.AI_3 = new_AI(playerThree, self.map, self.behaviour_possible[3])

        #defeated player
        self.defeated_player = None

        # chat
        self.chat_color = (40, 40, 40, 150)
        self.input_box = pygame.Rect(self.width // 2 - 70, self.height // 2 - 16, 140, 45)

        self.is_chat_activated = False
        self.chat_enabled = True
        self.display_msg_flag = False
        self.chat_text = ""
        self.chat_text_color = get_color_code("WHITE")
        self.chat_display_timer = pygame.time.get_ticks()

        self.victory = pygame.image.load("resources/assets/Images_for_in_game_menu_Oussama/Victory.png")
        self.defeat = pygame.image.load("resources/assets/Images_for_in_game_menu_Oussama/defeat.png")

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(120)
            self.events()
            self.update()
            self.draw()
            if IA_MODE:
                if TEST_MODE or MAIN_PLAYER != playerOne:
                    self.AI_1.run()

                if TEST_MODE or MAIN_PLAYER != playerTwo:
                    self.AI_2.run()

                if TEST_MODE or MAIN_PLAYER != playerThree:
                    self.AI_3.run()

    def events(self):
        mouse_pos = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # USER PRESSED A KEY
            if event.type == pygame.KEYDOWN:
                # chat mode
                if self.is_chat_activated:
                    # if escape, we leave chat and clear what was written
                    if event.key == pygame.K_ESCAPE:
                        self.is_chat_activated = False

                    # if pressing backspace, we have to remote the last character of the message
                    elif event.key == pygame.K_BACKSPACE:
                        self.chat_text = self.chat_text[:-1]

                    # if press enter again, we display the message, do some stuff if cheatcode, and disable chat
                    elif event.key == pygame.K_RETURN:
                        self.display_msg_flag = True
                        self.is_chat_activated = False
                        if self.chat_text == "PICSOU":
                            MAIN_PLAYER.update_resource("WOOD", 10000)
                            MAIN_PLAYER.update_resource("FOOD", 10000)
                            MAIN_PLAYER.update_resource("GOLD", 10000)
                            MAIN_PLAYER.update_resource("STONE", 10000)
                            self.chat_text = "CHEAT CODE ACTIVATED : PICSOU"
                        elif self.chat_text == "BIGDADDY":
                            self.map.spawn_dragon(MAIN_PLAYER, self.camera)
                            self.chat_text = "CHEAT CODE ACTIVATED : BIGDADDY"
                        elif self.chat_text == "DESTROY":
                            for u in GENERAL_UNIT_LIST:
                                u.attack_dmg *= 5
                                u.max_health *= 10
                                u.current_health *= 10
                            self.chat_text = "CHEAT CODE ACTIVATED : DESTROY"

                    # we store the letter
                    else:
                        self.chat_text += event.unicode

                # else if chat is not activated
                else:
                    if event.key == pygame.K_ESCAPE:
                        # Quit game if chat wasnt activated
                        pygame.quit()
                        sys.exit()

                    elif event.key == pygame.K_LCTRL:
                        pos_x = MAIN_PLAYER.towncenter_pos[0] + 1
                        pos_y = MAIN_PLAYER.towncenter_pos[1] + 2
                        #self.map.map[pos_x][pos_y]["tile"] = "tree"
                        #self.map.map[pos_x][pos_y]["collision"] = True
                        #self.map.map[pos_x][pos_y]["max_health"] = 10
                        #self.map.map[pos_x][pos_y]["health"] = 10
                        #self.map.map[pos_x][pos_y]["variation"] = 0

                        #self.map.resources_list.append(self.map.map[pos_x][pos_y])

                        # FORM ACTION a changé de nom : deserialize
                        #action = serialize(player_name=MAIN_PLAYER.name, action="move", triggering_unit=0, pos_x=pos_x, pos_y=pos_y)
                        #action = serialize(player_name=MAIN_PLAYER.name, action="build", entity="Tower", triggering_unit=0, pos_x=pos_x, pos_y=pos_y)
                        #action = serialize(player_name=MAIN_PLAYER.name, action="research", entity="Advance to Feudal Age")
                        #action = serialize(player_name=MAIN_PLAYER.name, action="gather", triggering_unit=0, pos_x=pos_x, pos_y=pos_y)
                        action = serialize(player_name=MAIN_PLAYER.name, action="train", entity="Clubman")

                        print(action)
                        deserialize(action, self.map)

                    elif event.key == pygame.K_LALT:
                        for x in range (0,50):
                            for y in range (0,50):
                                pseudo_serialize = ("Lucien*clear*"+str(x)+"*"+str(y))
                                if not deserialize(pseudo_serialize, world=self.map):
                                    print("Deserialization clear succès")
                                else:
                                    print("Code deserialize :" + "ECHEC deserialisation: action corrompue\n")

                    # Enable - Disable health bars
                    elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                        global ENABLE_HEALTH_BARS
                        ENABLE_HEALTH_BARS = not ENABLE_HEALTH_BARS

                    # if enter button is pressed, chat stuff happens (for cheatcodes)
                    elif event.key == pygame.K_RETURN and self.chat_enabled:
                        self.is_chat_activated = True

            # USER PRESSED A MOUSEBUTTON
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #if we left click on the display tech tree button
                if event.button == 1:
                    if self.map.hud.tech_tree_rect.collidepoint(mouse_pos):
                        self.map.hud.tech_tree_display_flag = False if self.map.hud.tech_tree_display_flag else True

                    elif self.map.hud.optimize_button_rect.collidepoint(mouse_pos):
                        print("TEST BUTTON")
                        self.map.hud.minimap_enabled = False if self.map.hud.minimap_enabled else True

                # if we left click on the action panel and a building/unit is selected
                if self.hud.bottom_left_menu is not None and self.map.hud.examined_tile is not None:
                    entity = self.map.hud.examined_tile
                    # if the examined entity belongs to us (or we are in debug mode)
                    #if entity.owner == MAIN_PLAYER or TEST_MODE:
                    if True:
                        # for every button in action panel
                        for button in self.hud.bottom_left_menu:
                            #if the button is pressed
                            if button["rect"].collidepoint(mouse_pos):
                                #STOP BUTTON
                                if button["name"] == "STOP":
                                    entity.owner.refund_entity_cost(entity.unit_type_currently_trained)
                                    entity.queue -= 1
                                    # no more units to create
                                    if entity.queue == 0:
                                        entity.is_working = False
                                        entity.unit_type_currently_trained = None
                                else:
                                    # we only do the actions corresponding to the button if player has enough resources/requirements are met
                                    if button["affordable"]:
                                        # if it was villager button, we train one
                                        if button["name"] == "Villager" and not self.hud.examined_tile.is_being_built:
                                            entity.train(Villager)
                                        elif button["name"] == "Clubman" and not self.hud.examined_tile.is_being_built:
                                            entity.train(Clubman)
                                        # if it was an advancement research, we... research it. Makes sense right ?
                                        elif button["name"] == "Advance to Feudal Age" \
                                                or button["name"] == "Advance to Castle Age"\
                                                or button["name"] == "Advance to Imperial Age" \
                                                or button["name"] == "Research Improved Masonry" \
                                                or button["name"] == "Research Reinforced Masonry" \
                                                or button["name"] == "Research Imbued Masonry" \
                                                or button["name"] == "Research Iron Swords" \
                                                or button["name"] == "Research Steel Swords" \
                                                or button["name"] == "Research Mithril Swords" \
                                                or button["name"] == "Research Iron Armors" \
                                                or button["name"] == "Research Steel Armors" \
                                                or button["name"] == "Research Mithril Armors" \
                                                or button["name"] == "Research Iron Arrows" \
                                                or button["name"] == "Research Iron Horseshoes" \
                                                or button["name"] == "Research Super Cows":
                                            entity.research_tech(button["name"])
                                            serialize(PlayerOne, "research", button["name"])
                                        # else it is a building
                                        else:
                                            self.hud.selected_tile = button


                    #to have informations about the villager if he is selected
                    if type(entity) == Villager:
                        this_villager = self.map.units[entity.pos[0]][entity.pos[1]]
                        #("Info about villager, print is in game, events")
                        this_villager.print_state()

                #BOOM WHEN RIGHT CLICKING
                if event.button == 3:  # RIGHT CLICK
                    # right click, gathering and moving units (fighting in future)
                    grid_pos = self.map.mouse_to_grid(mouse_pos[0], mouse_pos[1], self.camera.scroll)
                    if 0 <= grid_pos[0] < self.map.grid_length_x and 0 <= grid_pos[1] < self.map.grid_length_y:

                        # There is a bug with collecting ressources on the side of the map !!!

                        if self.map.hud.examined_tile is not None and (self.map.hud.examined_tile.name == "Villager" or
                                                                       self.map.hud.examined_tile.name == "Clubman" or
                                                                       self.map.hud.examined_tile.name == "Black Dragon"):
                            villager_pos = self.map.hud.examined_tile.pos
                            this_villager = self.map.units[villager_pos[0]][villager_pos[1]]

                            #print(this_villager.owner, MAIN_PLAYER)
                            if this_villager.owner == MAIN_PLAYER or TEST_MODE:
                                pos_mouse = self.map.mouse_to_grid(mouse_pos[0], mouse_pos[1], self.camera.scroll)
                                pos_x = pos_mouse[0]
                                pos_y = pos_mouse[1]
                                # ATTACK
                                if (self.map.units[pos_x][pos_y] is not None
                                    or self.map.buildings[pos_x][pos_y] is not None) \
                                        and not this_villager.owner == find_owner([pos_x, pos_y]):
                                    # attack !
                                    this_villager.go_to_attack((pos_x, pos_y))

                                # ONLY MOVEMENT
                                if isinstance(this_villager, Villager) and self.map.collision_matrix[grid_pos[1]][grid_pos[0]] and \
                                        not this_villager.is_gathering and this_villager.targeted_ressource is None and \
                                        not this_villager.is_attacking:
                                    this_villager.move_to(self.map.map[grid_pos[0]][grid_pos[1]])
                                elif isinstance(this_villager, Clubman) and self.map.collision_matrix[grid_pos[1]][grid_pos[0]] and \
                                        not this_villager.is_attacking:
                                    this_villager.move_to(self.map.map[grid_pos[0]][grid_pos[1]])
                                elif isinstance(this_villager, Dragon) and self.map.collision_matrix[grid_pos[1]][
                                    grid_pos[0]] and \
                                     not this_villager.is_attacking:
                                    this_villager.move_to(self.map.map[grid_pos[0]][grid_pos[1]])

                                # we check if the tile we right click on is a ressource and if its on an adjacent tile of
                                # the villager pos, and if the villager isnt moving if the tile next to him is a ressource
                                # and we right click on it and he is not moving, he will gather it
                                if isinstance(this_villager, Villager) and not this_villager.searching_for_path \
                                        and (self.map.map[pos_x][pos_y]["tile"] in ["tree", "rock", "gold", "berrybush"])\
                                        and this_villager.gathered_ressource_stack < this_villager.stack_max and \
                                        (this_villager.stack_type is None or
                                         this_villager.stack_type == self.map.map[pos_x][pos_y]["tile"]):

                                    this_villager.go_to_ressource((pos_x, pos_y))

                                if isinstance(this_villager, Villager) and this_villager.gathered_ressource_stack >= this_villager.stack_max \
                                        or (this_villager.owner.towncenter.pos[0] <= pos_x <=
                                        this_villager.owner.towncenter.pos[0]+1
                                            and this_villager.owner.towncenter.pos[1] <= pos_y <=
                                        this_villager.owner.towncenter.pos[1]-1):
                                    this_villager.go_to_townhall()

    def update(self):
        self.camera.update()
        self.hud.update(self.screen)
        self.map.update(self.camera, self.screen)
        for an_entity in self.entities:
            an_entity.update()

        for p in player_list:
            if p.towncenter is None:
                self.is_chat_activated = False
                self.display_msg_flag = True
                self.chat_text = str(p.name) + " has been defeated"

                player_list.remove(p)
                self.timer = self.map.timer
                self.defeated_player =  p

        time = pygame.time.get_ticks()
        if time - self.timer > 3000:
            if self.defeated_player is not None and self.defeated_player == MAIN_PLAYER:
                print("DEFEAT")
                self.screen.fill((0, 0, 0))
                pos_x = (self.width - self.defeat.get_width())/2
                pos_y = (self.height - self.defeat.get_height())/2

                pos_text_x = (self.width - self.defeat.get_width()*0.35)/2
                pos_text_y = (self.height - self.defeat.get_height()*0.2)/2

                self.screen.blit(self.defeat, (pos_x, pos_y))

                draw_text(self.screen, "DEFEAT", 110, get_color_code("DARK_GRAY"), (pos_text_x, pos_text_y))

                pygame.display.flip()
                sleep(3)

                pygame.quit()
                sys.exit()
            else:
                if len(player_list) == 1:
                    player_list[0].victory()
                    print("VICTORY")

                    self.screen.fill((0, 0, 0))
                    pos_x = (self.width - self.defeat.get_width()) / 2
                    pos_y = (self.height - self.defeat.get_height()) / 2

                    pos_text_x = (self.width - self.defeat.get_width() * 0.4) / 2
                    pos_text_y = (self.height - self.defeat.get_height() * 0.2) / 2

                    self.screen.blit(self.victory, (pos_x, pos_y))

                    draw_text(self.screen, "VICTORY", 110, get_color_code("GOLD"), (pos_text_x, pos_text_y))

                    pygame.display.flip()
                    sleep(3)

                    pygame.quit()
                    sys.exit()
                self.defeated_player = None


    # GAME DISPLAY
    def draw(self):
        now = pygame.time.get_ticks()
        # BLACK BACKGROUND
        self.screen.fill((0,0,0))
        #the map display was moved inside the hud class
        self.map.draw(self.screen, self.camera)
        # drawing the hud, must be last but before fps and cursor
        self.hud.draw(self.screen, self.map, self.camera)
        # MOUSE CURSOR - we disable the default one and create a new one at the current position of the mouse
        # MUST BE LAST TO SEE IT AND NOT BE HIDDEN BEHIND OTHER THINGS
        #pygame.mouse.set_visible(False)
        #standard_cursor_rect = standard_cursor.get_rect()
        #standard_cursor_rect.center = pygame.mouse.get_pos()  # update position
        #self.screen.blit(standard_cursor, standard_cursor_rect)  # draw the cursor
        # chat

        txt_surface = chatFont.render(self.chat_text, True, get_color_code("RED"))
        # Resize the box if the text is too long.
        if self.is_chat_activated:
            width = max(200, txt_surface.get_width() + 10)
            self.input_box.w = width
            # Blit the input_box rect outside.
            pygame.draw.rect(self.screen, get_color_code("GOLD"), self.input_box, 2)
            self.chat_surface = pygame.Surface((width, 44), pygame.SRCALPHA)
            self.chat_surface.fill(self.chat_color)
            self.chat_rect = self.chat_surface.get_rect(topleft=(0, 0))
            # display grey rectangle
            self.screen.blit(self.chat_surface, (self.input_box.x, self.input_box.y + 1))

            # Blit the text.
            self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # message written and pressed enter again, it displays a message on the screen for a few seconds
        if self.display_msg_flag:
            self.chat_enabled = False
            draw_text(self.screen, self.chat_text, 30, get_color_code("WHITE"), (10, 130))
            # if message has been displayed more than 5 secs, we make it disappear
            if now - self.chat_display_timer > 5000:
                self.display_msg_flag = False
                self.chat_text = ""
                self.chat_display_timer = now
                self.chat_enabled = True

        #Draw FPS, must be the last to shown -> put it right on top of the display.flip
        draw_text(self.screen,'fps={}'.format(round(self.clock.get_fps())),20,(255,0,0),(5,55))
        pygame.display.flip()
