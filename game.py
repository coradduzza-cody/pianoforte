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
                                    theme=pygame_menu.themes.THEME_DARK)
        
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

        self.active_note = None
        self.active_note_time = 0  # Store the time when the note was activated

    # CARICAMENTO IMMAGINE PIANO

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


        # MAPPATURA TASTI e CLICK

            cPoint = [(50, 550), (180, 550), (180, 420), (145, 420), (145, 250), (50, 250)]
            dbPoint = [(145, 420), (210, 420), (210, 250), (145, 250)]
            dPoint = [(180, 550), (180, 420), (210, 420), (210, 250), (275, 250), (275, 420), (305, 420), (305, 550)]
            ebPoint = [(275, 420), (340, 420), (340, 250), (275, 250)]
            ePoint = [(340, 250), (435, 250), (435, 550), (305, 550), (305, 420), (340, 420)]
            fPoint = [(435, 550), (565, 550), (565, 420), (530, 420), (530, 250), (435, 250)]
            gbPoint = [(530, 420), (595, 420), (595, 250), (530, 250)]
            gPoint = [(565, 550), (565, 420), (595, 420), (595, 250), (660, 250), (660, 420), (695, 420), (695, 550)]
            abPoint = [(660, 420), (725, 420), (725, 250), (660, 250)]
            aPoint = [(695, 550), (695, 420), (725, 420), (725, 250), (790, 250), (790, 420), (825, 420), (825, 550)]
            bbPoint = [(790, 420), (855, 420), (855, 250), (790, 250)]
            bPoint = [(855, 250), (950, 250), (950, 550), (825, 550), (825, 420), (855, 420)]

            cTile = pygame.draw.polygon(self.screen, (25, 120, 60), cPoint, 3)
            ddTile = pygame.draw.polygon(self.screen, (255, 0, 0), dbPoint, 3)
            dTile = pygame.draw.polygon(self.screen, (25, 120, 60), dPoint, 3)
            ebTile = pygame.draw.polygon(self.screen, (255, 0, 0), ebPoint, 3)
            eTile = pygame.draw.polygon(self.screen, (25, 120, 60), ePoint, 3)
            fTile = pygame.draw.polygon(self.screen, (25, 120, 60), fPoint, 3)
            gbTile = pygame.draw.polygon(self.screen, (255, 0, 0), gbPoint, 3)
            gTile = pygame.draw.polygon(self.screen, (25, 120, 60), gPoint, 3)
            abTile = pygame.draw.polygon(self.screen, (255, 0, 0), abPoint, 3)
            aTile = pygame.draw.polygon(self.screen, (25, 120, 60), aPoint, 3)
            bbTile = pygame.draw.polygon(self.screen, (255, 0, 0), bbPoint, 3)
            bTile = pygame.draw.polygon(self.screen, (25, 120, 60), bPoint, 3)

            tiles = [
                (cTile, cPoint, "C"),
                (ddTile, dbPoint, "Db"),
                (dTile, dPoint, "D"),
                (ebTile, ebPoint, "Eb"),
                (eTile, ePoint, "E"),
                (fTile, fPoint, "F"),
                (gbTile, gbPoint, "Gb"),
                (gTile, gPoint, "G"),
                (abTile, abPoint, "Ab"),
                (aTile, aPoint, "A"),
                (bbTile, bbPoint, "Bb"),
                (bTile, bPoint, "B"),
            ]

        
        # MAPPA TASTI

            if key_just_pressed(pygame.K_q):
                note_name = f"C{sound_height}"
                self.active_note = (tiles[0][1], tiles[0][2])  # Activate C note
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

        # TRACKING MOUSE 

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                print(pos)

        # GESTIONE PRESSIONE TASTI

            for tile, points, note in tiles:
                if tile.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0] and self.point_in_polygon(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], points):
                        note_name = f"{note}{sound_height}"
                        if note_name in self.sounds:
                            self.sounds[note_name].play()
                        print(note)
                        self.active_note = (points, note)
                        self.active_note_time = pygame.time.get_ticks()  # Record the activation time
                        pygame.time.delay(200)

            if self.active_note:
                
                if pygame.time.get_ticks() - self.active_note_time < 300:

                    if self.active_note[1] in ["Db", "Eb", "Gb", "Ab", "Bb"]:
                        pygame.gfxdraw.filled_polygon(self.screen, self.active_note[0], (50, 50, 50))
                    else:
                        pygame.gfxdraw.filled_polygon(self.screen, self.active_note[0], (240, 240, 240))
 
                else:
                    self.active_note = None


        # DISPLAY TASTI PREMUTI

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

            pygame.display.update()

# FUNZIONE PER CAPIRE SE UN PUNTO FA PARTE DELLA NOTA

    def point_in_polygon(self, x, y, poly):
        num = len(poly)
        j = num - 1
        c = False
        for i in range(num):
            if ((poly[i][1] > y) != (poly[j][1] > y)) and \
            (x < (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1] + 1e-10) + poly[i][0]):
                c = not c
            j = i
        return c

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