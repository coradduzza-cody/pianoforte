import pygame
import pygame_menu
from pygame.locals import *
import sys
import os
import random

class Game:

# INIZIALIZZAZIONE GIOCO

    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(32)  # Allow up to 32 overlapping sounds

        self.res = (1000, 900)
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Piano Simulator")
        self.clock = pygame.time.Clock()
        self.running = True

        self.bg = (89, 115, 158)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # Preload all notes for all heights
        self.sounds = {}
        self.notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        for h in range(1, 8):
            for n in self.notes:
                path = f"piano-mp3/{n}{h}.mp3"
                self.sounds[f"{n}{h}"] = pygame.mixer.Sound(path)   

        self.meow_sound = pygame.mixer.Sound("cat_sounds/meow.mp3")
        self.meow_sound.set_volume(0.3)    

    # MENU' SETUP
        
        self.theme = pygame_menu.themes.Theme(
            title_background_color=(115, 143, 189),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE,
            title_font_shadow=False,
            widget_font=pygame_menu.font.FONT_MUNRO,
            widget_font_color=(0, 0, 0),
            background_color=(89, 115, 158),
            )

    # CREDITS MENU

        self.creditsMenu = pygame_menu.Menu('Credits', 600, 600,
                                    theme=self.theme)
        
        self.creditsMenu.add.label('Developed by Elio and Giovanni', font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
    
    # CONTROLS MENU
        self.controlsMenu = pygame_menu.Menu('Controls', 600, 600,
                                    theme=self.theme)
        
        self.controlsMenu.add.label('Left click the mouse or use the keyboard:', font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
        
        self.controlsMenu.add.image('images\piano_keys.jpg', scale=(0.5, 0.5))

        self.controlsMenu.add.label('Use left and right arrow to change the piano\'s octave', font_size=25, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
        

    # HOME MENU
        self.homeMenu = pygame_menu.Menu('PIANO SIMULATOR', 600, 600,
                                    theme=self.theme)
        
        self.homeMenu.add.button('Play', self.play, font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
        self.homeMenu.add.button(self.controlsMenu.get_title(), self.controlsMenu, font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
        self.homeMenu.add.button(self.creditsMenu.get_title(), self.creditsMenu, font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
        self.homeMenu.add.button('Quit', pygame_menu.events.EXIT, font_size=30, font_color=(0, 0, 0), 
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

        self.catHitbox = pygame.draw.rect(self.screen, (0, 0, 0), (self.width - 250, 50, 200, 200), 2)

    # LOOP PRINCIPALE

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.bg)

            # Always draw the piano image every frame
            # self.screen.blit(pianoImg, (50, 250))

        # GESTIONE e DISPLAY INPUT 

            keys = pygame.key.get_pressed()
            note_name = ""

            # Only play sound on key DOWN event (not while held)
            def key_just_pressed(key):
                return keys[key] and not prev_keys[key]

            if keys[pygame.K_ESCAPE]:
                self.homeMenu.reset(1)
                run = False

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

            cTile = pygame.draw.polygon(self.screen, (255, 255, 255), cPoint)  # Fill color
            pygame.draw.polygon(self.screen, (0, 0, 0), cPoint, 2)  # Border color
            ddTile = pygame.draw.polygon(self.screen, (0, 0, 0), dbPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), dbPoint, 2)
            dTile = pygame.draw.polygon(self.screen, (255, 255, 255), dPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), dPoint, 2)
            ebTile = pygame.draw.polygon(self.screen, (0, 0, 0), ebPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), ebPoint, 2)
            eTile = pygame.draw.polygon(self.screen, (255, 255, 255), ePoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), ePoint, 2)
            fTile = pygame.draw.polygon(self.screen, (255, 255, 255), fPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), fPoint, 2)
            gbTile = pygame.draw.polygon(self.screen, (0, 0, 0), gbPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), gbPoint, 2)
            gTile = pygame.draw.polygon(self.screen, (255, 255, 255), gPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), gPoint, 2)
            abTile = pygame.draw.polygon(self.screen, (0, 0, 0), abPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), abPoint, 2)
            aTile = pygame.draw.polygon(self.screen, (255, 255, 255), aPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), aPoint, 2)
            bbTile = pygame.draw.polygon(self.screen, (0, 0, 0), bbPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), bbPoint, 2)
            bTile = pygame.draw.polygon(self.screen, (255, 255, 255), bPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), bPoint, 2)

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
            
            if len(tiles) >= 12:
                key_note_map = [
                    (pygame.K_q, "C", 0),
                    (pygame.K_2, "Db", 1),
                    (pygame.K_w, "D", 2),
                    (pygame.K_3, "Eb", 3),
                    (pygame.K_e, "E", 4),
                    (pygame.K_r, "F", 5),
                    (pygame.K_5, "Gb", 6),
                    (pygame.K_t, "G", 7),
                    (pygame.K_6, "Ab", 8),
                    (pygame.K_y, "A", 9),
                    (pygame.K_7, "Bb", 10),
                    (pygame.K_u, "B", 11),
                ]
                for key, note, idx in key_note_map:
                    if key_just_pressed(key):
                        note_name = f"{note}{sound_height}"
                        self.active_note = (tiles[idx][1], tiles[idx][2])
                        self.active_note_time = pygame.time.get_ticks()
                        print(f"Key pressed: {note_name}")

            if note_name in self.sounds:
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
                        self.active_note_time = pygame.time.get_ticks()
                        pygame.time.delay(200)

            if self.active_note:
                
                if pygame.time.get_ticks() - self.active_note_time < 300:

                    if self.active_note[1] in ["Db", "Eb", "Gb", "Ab", "Bb"]:
                        pygame.draw.polygon(self.screen, (50, 50, 50), self.active_note[0])
                        pygame.draw.polygon(self.screen, (0, 0, 0), self.active_note[0], 2)
                        # pygame.gfxdraw.filled_polygon(self.screen, self.active_note[0], (50, 50, 50))
                    else:
                        pygame.draw.polygon(self.screen, (240, 240, 240), self.active_note[0])
                        pygame.draw.polygon(self.screen, (0, 0, 0), self.active_note[0], 2)
                        # pygame.gfxdraw.filled_polygon(self.screen, self.active_note[0], (240, 240, 240))
 
                else:
                    self.active_note = None


        # DISPLAY TASTI PREMUTI

            if not hasattr(self, "played_notes"):
                self.played_notes = []  # List of (note_name, timestamp) tuples

            current_time = pygame.time.get_ticks()

            if note_name:
                self.played_notes.append((note_name, current_time))


            self.played_notes = [
                (n, t) for (n, t) in self.played_notes if current_time - t < 2500
            ]

            # Build display string from remaining notes
            display_notes = " ".join(n for (n, t) in self.played_notes)

            title = font.render(display_notes, True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.width / 2, self.height / 2 - 225))
            self.screen.blit(title, title_rect)

            prev_keys = keys  # Update previous keys for next frame


        # CRAZY CAT SECTION WOHOO

            """ if not hasattr(self, "cat_image"):
                cats = len([name for name in os.listdir('cat_images') if name.endswith('.png') and os.path.isfile(os.path.join('cat_images', name))])  # number of .png files in the cat_images folder
                selected_cat = random.randint(1, cats)
                self.cat_image = pygame.image.load(f"cat_images/cat{selected_cat}.png")
                self.cat_image = pygame.transform.scale(self.cat_image, (200, 200))
            
            self.screen.blit(self.cat_image, (self.width - 250, 50))

            title = font.render("Press C to meow!", True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.width - 150, 50))
            self.screen.blit(title, title_rect)
            
            if keys[pygame.K_c]:
                self.meow_sound.stop()
                self.meow_sound.play()
                pygame.time.delay(300)

            if pygame.mouse.get_pressed()[0] and self.catHitbox.collidepoint(pygame.mouse.get_pos()):
                self.meow_sound.stop()
                self.meow_sound.play()
                pygame.time.delay(300) """

        # PULSANTE MENU
            menu_button_rect = pygame.Rect(10, 10, 120, 40)
            pygame.draw.rect(self.screen, (180, 191, 209), menu_button_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), menu_button_rect, 2, border_radius=10)
            button_font = pygame.font.Font(None, 36)
            button_text = button_font.render("Menu", True, (0, 0, 0))
            text_rect = button_text.get_rect(center=menu_button_rect.center)
            self.screen.blit(button_text, text_rect)

            
            if pygame.mouse.get_pressed()[0] and menu_button_rect.collidepoint(pygame.mouse.get_pos()):
                self.homeMenu.reset(1)
                return

        # PULSANTE OTTAVA
            octave_text = font.render(f"Octave: {sound_height}", True, (0, 0, 0))
            self.screen.blit(octave_text, (self.width - 200, self.height - 300))
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
            self.homeMenu.mainloop(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    game = Game()
    game.run()