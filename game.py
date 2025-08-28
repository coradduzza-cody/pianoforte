import pygame
import pygame_menu
import pygame.gfxdraw
from pygame.locals import *
import sys

class Game:

# INIZIALIZZAZIONE GIOCO

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)  # Allow up to 32 overlapping sounds

        self.res = (1000, 900)
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Shooter Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.bg = (180, 191, 209)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # Preload all notes for all heights
        self.sounds = {}
        self.notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        for h in range(1, 8):
            for n in self.notes:
                path = f"piano-mp3/{n}{h}.mp3"
                self.sounds[f"{n}{h}"] = pygame.mixer.Sound(path)       

    # MENU' SETUP

        self.menu = pygame_menu.Menu('PIANO SIMULATOR', 600, 600,
                                    theme=pygame_menu.themes.THEME_BLUE)
        
        self.menu.add.text_input('Name : ', default='Player', font_size=30, font_color=(0, 0, 0), 
                                 background_color=(180, 191, 209)
                                 ,margin=(0, 20)
                                 ,padding=(10, 20))
        self.menu.add.button('Play', self.play, font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
        self.menu.add.button('Quit', pygame_menu.events.EXIT, font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))

# FUNZIONAMENTO GIOCO

    def play(self):
        run = True
        sound_height = 4

        font = pygame.font.Font(None, 50)

        # Track which keys were pressed last frame
        prev_keys = pygame.key.get_pressed()

    #CARICAMENTO IMMAGINE PIANO

        pianoImg = pygame.image.load("images/piano_keys.jpg")
        pianoImg = pygame.transform.scale(pianoImg, (900, 300))

    # LOOP PRINCIPALE

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.bg)

            # Always draw the piano image every frame
            self.screen.blit(pianoImg, (50, 250))

        # GESTIONE e DISPLAY INPUT 

            keys = pygame.key.get_pressed()
            note_name = ""

            # Only play sound on key DOWN event (not while held)
            def key_just_pressed(key):
                return keys[key] and not prev_keys[key]

            if keys[pygame.K_RIGHT]:
                if sound_height < 7:
                    sound_height += 1
                print(sound_height)
                pygame.time.delay(200)

            if keys[pygame.K_LEFT]:
                if sound_height > 1:
                    sound_height -= 1
                print(sound_height)
                pygame.time.delay(200)

        # MAPPA TASTI (da sostituire con mouse click)

            if key_just_pressed(pygame.K_q):
                note_name = f"C{sound_height}"
            elif key_just_pressed(pygame.K_2):
                note_name = f"Db{sound_height}"
            elif key_just_pressed(pygame.K_w):
                note_name = f"D{sound_height}"
            elif key_just_pressed(pygame.K_3):
                note_name = f"Eb{sound_height}"
            elif key_just_pressed(pygame.K_e):
                note_name = f"E{sound_height}"
            elif key_just_pressed(pygame.K_r):
                note_name = f"F{sound_height}"
            elif key_just_pressed(pygame.K_5):
                note_name = f"Gb{sound_height}"
            elif key_just_pressed(pygame.K_t):
                note_name = f"G{sound_height}"
            elif key_just_pressed(pygame.K_6):
                note_name = f"Ab{sound_height}"
            elif key_just_pressed(pygame.K_y):
                note_name = f"A{sound_height}"
            elif key_just_pressed(pygame.K_7):
                note_name = f"Bb{sound_height}"
            elif key_just_pressed(pygame.K_u):
                note_name = f"B{sound_height}"

            if note_name and note_name in self.sounds:
                self.sounds[note_name].play()

            # Always render the current note name (or blank if none)
            # Accumulate all played notes in a string
            if not hasattr(self, "played_notes"):
                self.played_notes = ""
            if note_name:
                self.played_notes += note_name + " "

            display_notes = self.played_notes.strip()

            title = font.render(display_notes, True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.width / 2, self.height / 2 - 225))
            self.screen.blit(title, title_rect)

            prev_keys = keys  # Update previous keys for next frame

            pygame.display.flip()
            
        #TRACKING MOUSE 

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                POS = pygame.mouse.get_pos()
                print(POS)
            pygame.display.update()

# LOOP MENU

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.bg)
            self.menu.mainloop(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    game = Game()
    game.run()