from game.game import Game as g
from settings import *
from game.network import *
from game.utils import *
#from .settings import WIDTH
#from .settings import HEIGHT

# to force push : git push -f origin branch_name (our branch name is name)


def main(multi=True, createur=True, servip="192.168.11.139"):
    print("test")
    #intialize pygame
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    #create the screen
    #screen = pygame.display.set_mode((1920,1080))
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #Full screen for many type of screen
    #screen = pygame.display.set_mode((WIDTH,HEIGHT)) #Adjustable in Settings.py


    #Title and Icon
    pygame.display.set_caption("Age of Empire: Homemade Edition")
    icon = pygame.image.load(os.path.join(common_path,'icon.png'))
    pygame.display.set_icon(icon)
    
    if not multi:
        game = g(screen, clock, multi, createur)

    else:
        if createur:
            game = g(screen, clock, multi, createur)
            network = Network(game.map, createur, servip)
            game.network = network
        
        else:
            draw_text(screen,'waiting for connection with the other player',20,(255,0,0),(screen.get_size()[0]/2 - 150, screen.get_size()[1]/2))
            pygame.display.flip()
            network = Network(None, createur, servip)
            network.send_action("/askmap")    
            while network.not_ready:
                network.listen()
            game = g(screen, clock, multi, createur, str_map=network.newmap)
            network.map = game.map
            game.network = network

#Exit game
    running = True
    playing = True
    while running:

        # Add start menu here

        while playing:



            # Start game loop
            game.run()



if __name__ == "__main__":
    main()

