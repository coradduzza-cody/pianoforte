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
        pygame.mixer.set_num_channels(32)

        self.res = (1000, 900)
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption("Piano Simulator")
        self.clock = pygame.time.Clock()
        self.running = True

        self.bg = (89, 115, 158)    
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.onchange = 0.5
        self.prevChange = self.onchange

        # Preload all notes for all heights
        self.sounds = {}
        self.notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        for h in range(1, 8):
            for n in self.notes:
                path = f"piano-mp3/{n}{h}.mp3"
                self.sounds[f"{n}{h}"] = pygame.mixer.Sound(path)   
                self.sounds[f"{n}{h}"].set_volume(self.onchange)  # SET 50%

        self.meow_sound = pygame.mixer.Sound("cat_sounds/meow.mp3")
        self.meow_sound.set_volume(self.onchange)

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
        self.controlsMenu = pygame_menu.Menu('Controls', 900, 900,
                                    theme=self.theme)
        
        self.controlsMenu.add.label('Left click the mouse or use the keyboard:', font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
        
        self.controlsMenu.add.image('images\piano_keys.jpg', scale=(0.5, 0.5))
        self.controlsMenu.add.image('images\piano_keys2.jpg', scale=(0.5, 0.5))

        self.controlsMenu.add.label('Use left and right arrow to change the piano\'s octave', font_size=25, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
    
    #AUDIO MENU
        self.audioMenu = pygame_menu.Menu('Audio', 600, 600,
                                    theme=self.theme)
        
        def set_volume(value):
            self.onchange = value / 100
            for sound in self.sounds.values():
                sound.set_volume(self.onchange)
            self.meow_sound.set_volume(self.onchange)
            self.prevChange = self.onchange

        self.audioMenu.add.range_slider(
            'Volume: ',
            default=int(self.onchange * 100),
            range_values=(0, 100),
            increment=5,
            value_format=lambda x: str(int(x)) + '%',
            font_size=25,
            font_color=(0, 0, 0),
            background_color=(180, 191, 209),
            margin=(0, 20),
            padding=(10, 20),
            onchange=set_volume
        )

        self.audioMenu.add.button('Test audio', lambda: self.meow_sound.play(), font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))

    # SETTINGS MENU
        self.settingsMenu = pygame_menu.Menu('Settings', 600, 600,
                                    theme=self.theme)
        
        self.settingsMenu.add.button(self.audioMenu.get_title(), self.audioMenu, font_size=30, font_color=(0, 0, 0), 
                             background_color=(180, 191, 209)
                             ,margin=(0, 20)
                             ,padding=(10, 20))
        
        self.settingsMenu.add.button(self.controlsMenu.get_title(), self.controlsMenu, font_size=30, font_color=(0, 0, 0), 
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
        
        self.homeMenu.add.button(self.settingsMenu.get_title(), self.settingsMenu, font_size=30, font_color=(0, 0, 0), 
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
        sound_height = 4                    #primo pianoforte
        sound_height2 = sound_height + 1    #secondo pianoforte

        font = pygame.font.Font(None, 50)

        prev_keys = pygame.key.get_pressed()

        self.active_note = None
        self.active_note_time = 0

        self.catHitbox = pygame.draw.rect(self.screen, (0, 0, 0), (self.width - 250, 50, 200, 200), 2)

    # LOOP PRINCIPALE

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.bg)

        # GESTIONE e DISPLAY INPUT 

            keys = pygame.key.get_pressed()
            note_name = ""

            def key_just_pressed(key):
                return keys[key] and not prev_keys[key]

            if keys[pygame.K_ESCAPE]:
                self.homeMenu.reset(1)
                run = False

            # Octave change logic
            if keys[pygame.K_RIGHT]:
                if sound_height < 6: 
                    sound_height += 1
                    sound_height2 = sound_height + 1
                print(sound_height)
                pygame.time.delay(200)

            if keys[pygame.K_LEFT]:
                if sound_height > 1:
                    sound_height -= 1
                    sound_height2 = sound_height + 1
                print(sound_height)
                pygame.time.delay(200)


     # MAPPATURA TASTI e CLICK

        #SHIFT PIANO
            y_offset_1 = -150  
            y_offset_2 = 400

            def shift_points(points, y_offset):
                return [(x, y + y_offset) for (x, y) in points]

            # COORDINATE ORIGINALI
            cPoint_base = [(50, 550), (180, 550), (180, 420), (145, 420), (145, 250), (50, 250)]
            dbPoint_base = [(145, 420), (210, 420), (210, 250), (145, 250)]
            dPoint_base = [(180, 550), (180, 420), (210, 420), (210, 250), (275, 250), (275, 420), (305, 420), (305, 550)]
            ebPoint_base = [(275, 420), (340, 420), (340, 250), (275, 250)]
            ePoint_base = [(340, 250), (435, 250), (435, 550), (305, 550), (305, 420), (340, 420)]
            fPoint_base = [(435, 550), (565, 550), (565, 420), (530, 420), (530, 250), (435, 250)]
            gbPoint_base = [(530, 420), (595, 420), (595, 250), (530, 250)]
            gPoint_base = [(565, 550), (565, 420), (595, 420), (595, 250), (660, 250), (660, 420), (695, 420), (695, 550)]
            abPoint_base = [(660, 420), (725, 420), (725, 250), (660, 250)]
            aPoint_base = [(695, 550), (695, 420), (725, 420), (725, 250), (790, 250), (790, 420), (825, 420), (825, 550)]
            bbPoint_base = [(790, 420), (855, 420), (855, 250), (790, 250)]
            bPoint_base = [(855, 250), (950, 250), (950, 550), (825, 550), (825, 420), (855, 420)]

            # PRIMO PIANOFORTE
            cPoint = shift_points(cPoint_base, y_offset_1)
            dbPoint = shift_points(dbPoint_base, y_offset_1)
            dPoint = shift_points(dPoint_base, y_offset_1)
            ebPoint = shift_points(ebPoint_base, y_offset_1)
            ePoint = shift_points(ePoint_base, y_offset_1)
            fPoint = shift_points(fPoint_base, y_offset_1)
            gbPoint = shift_points(gbPoint_base, y_offset_1)
            gPoint = shift_points(gPoint_base, y_offset_1)
            abPoint = shift_points(abPoint_base, y_offset_1)
            aPoint = shift_points(aPoint_base, y_offset_1)
            bbPoint = shift_points(bbPoint_base, y_offset_1)
            bPoint = shift_points(bPoint_base, y_offset_1)

            # SECODNO PIANOFORTE
            cPoint2 = shift_points(cPoint_base, y_offset_1 + y_offset_2)
            dbPoint2 = shift_points(dbPoint_base, y_offset_1 + y_offset_2)
            dPoint2 = shift_points(dPoint_base, y_offset_1 + y_offset_2)
            ebPoint2 = shift_points(ebPoint_base, y_offset_1 + y_offset_2)
            ePoint2 = shift_points(ePoint_base, y_offset_1 + y_offset_2)
            fPoint2 = shift_points(fPoint_base, y_offset_1 + y_offset_2)
            gbPoint2 = shift_points(gbPoint_base, y_offset_1 + y_offset_2)
            gPoint2 = shift_points(gPoint_base, y_offset_1 + y_offset_2)
            abPoint2 = shift_points(abPoint_base, y_offset_1 + y_offset_2)
            aPoint2 = shift_points(aPoint_base, y_offset_1 + y_offset_2)
            bbPoint2 = shift_points(bbPoint_base, y_offset_1 + y_offset_2)
            bPoint2 = shift_points(bPoint_base, y_offset_1 + y_offset_2)

            # DISEGNO PRIMO
            cTile = pygame.draw.polygon(self.screen, (255, 255, 255), cPoint)
            pygame.draw.polygon(self.screen, (0, 0, 0), cPoint, 2)
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

            # DISEGNO SECONDO
            cTile2 = pygame.draw.polygon(self.screen, (255, 255, 255), cPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), cPoint2, 2)
            ddTile2 = pygame.draw.polygon(self.screen, (0, 0, 0), dbPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), dbPoint2, 2)
            dTile2 = pygame.draw.polygon(self.screen, (255, 255, 255), dPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), dPoint2, 2)
            ebTile2 = pygame.draw.polygon(self.screen, (0, 0, 0), ebPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), ebPoint2, 2)
            eTile2 = pygame.draw.polygon(self.screen, (255, 255, 255), ePoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), ePoint2, 2)
            fTile2 = pygame.draw.polygon(self.screen, (255, 255, 255), fPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), fPoint2, 2)
            gbTile2 = pygame.draw.polygon(self.screen, (0, 0, 0), gbPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), gbPoint2, 2)
            gTile2 = pygame.draw.polygon(self.screen, (255, 255, 255), gPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), gPoint2, 2)
            abTile2 = pygame.draw.polygon(self.screen, (0, 0, 0), abPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), abPoint2, 2)
            aTile2 = pygame.draw.polygon(self.screen, (255, 255, 255), aPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), aPoint2, 2)
            bbTile2 = pygame.draw.polygon(self.screen, (0, 0, 0), bbPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), bbPoint2, 2)
            bTile2 = pygame.draw.polygon(self.screen, (255, 255, 255), bPoint2)
            pygame.draw.polygon(self.screen, (0, 0, 0), bPoint2, 2)

            
            tiles = [
                (cTile, cPoint, "C"), (ddTile, dbPoint, "Db"), (dTile, dPoint, "D"), (ebTile, ebPoint, "Eb"),
                (eTile, ePoint, "E"), (fTile, fPoint, "F"), (gbTile, gbPoint, "Gb"), (gTile, gPoint, "G"),
                (abTile, abPoint, "Ab"), (aTile, aPoint, "A"), (bbTile, bbPoint, "Bb"), (bTile, bPoint, "B"),
                (cTile2, cPoint2, "C"), (ddTile2, dbPoint2, "Db"), (dTile2, dPoint2, "D"), (ebTile2, ebPoint2, "Eb"),
                (eTile2, ePoint2, "E"), (fTile2, fPoint2, "F"), (gbTile2, gbPoint2, "Gb"), (gTile2, gPoint2, "G"),
                (abTile2, abPoint2, "Ab"), (aTile2, aPoint2, "A"), (bbTile2, bbPoint2, "Bb"), (bTile2, bPoint2, "B"),
            ]

        
        # MAPPA TASTI
            
            if len(tiles) >= 24:
                key_note_map = [
                    (pygame.K_q, "C", 0, sound_height),
                    (pygame.K_2, "Db", 1, sound_height),
                    (pygame.K_w, "D", 2, sound_height),
                    (pygame.K_3, "Eb", 3, sound_height),
                    (pygame.K_e, "E", 4, sound_height),
                    (pygame.K_r, "F", 5, sound_height),
                    (pygame.K_5, "Gb", 6, sound_height),
                    (pygame.K_t, "G", 7, sound_height),
                    (pygame.K_6, "Ab", 8, sound_height),
                    (pygame.K_y, "A", 9, sound_height),
                    (pygame.K_7, "Bb", 10, sound_height),
                    (pygame.K_u, "B", 11, sound_height),

                    (pygame.K_z, "C", 12, sound_height2),
                    (pygame.K_s, "Db", 13, sound_height2),
                    (pygame.K_x, "D", 14, sound_height2),
                    (pygame.K_d, "Eb", 15, sound_height2),
                    (pygame.K_c, "E", 16, sound_height2),
                    (pygame.K_v, "F", 17, sound_height2),
                    (pygame.K_g, "Gb", 18, sound_height2),
                    (pygame.K_b, "G", 19, sound_height2),
                    (pygame.K_h, "Ab", 20, sound_height2),
                    (pygame.K_n, "A", 21, sound_height2),
                    (pygame.K_j, "Bb", 22, sound_height2),
                    (pygame.K_m, "B", 23, sound_height2),
                ]
                for key, note, idx, octave in key_note_map:
                    if key_just_pressed(key):
                        note_name = f"{note}{octave}"
                        self.active_note = (tiles[idx][1], tiles[idx][2])
                        self.active_note_time = pygame.time.get_ticks()
                        print(f"Key pressed: {note_name}")

            if note_name in self.sounds:
                self.sounds[note_name].play()

        # TRACKING MOUSE 

            """ if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                print(pos) """

        # GESTIONE PRESSIONE TASTI

            for idx, (tile, points, note) in enumerate(tiles):
                if tile.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0] and self.point_in_polygon(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], points):
                        # primo piano (tiles 0-11)
                        if idx < 12:
                            note_name = f"{note}{sound_height}"
                        # secondo piano (tiles 12-23)
                        else:
                            note_name = f"{note}{sound_height2}"
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
                self.played_notes = []

            current_time = pygame.time.get_ticks()

            if note_name:
                self.played_notes.append((note_name, current_time))


            self.played_notes = [
                (n, t) for (n, t) in self.played_notes if current_time - t < 2500
            ]

           
            display_notes = " ".join(n for (n, t) in self.played_notes)

            title = font.render(display_notes, True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.width / 2, self.height / 2))
            self.screen.blit(title, title_rect)

            prev_keys = keys


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
            octave_text = font.render(f"Octave: {sound_height} / {sound_height2}", True, (0, 0, 0))
            self.screen.blit(octave_text, (self.width/2-125, self.height/2+400))
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