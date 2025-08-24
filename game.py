import pygame
from pygame.locals import *
import sys

class Game:
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
                

    def menu(self):
        mouse = pygame.mouse.get_pos()
        self.screen.fill((30, 30, 30))
        pygame.draw.rect(self.screen, (10,10,10), [self.width/2-250, self.height/2-300, 500, 150])

        # Play button
        play_rect = pygame.Rect(self.width/2-80, self.height/2-80, 140, 40)
        # Quit button
        quit_rect = pygame.Rect(self.width/2-80, self.height/2-20, 140, 40)

        play_hover = play_rect.collidepoint(mouse)
        quit_hover = quit_rect.collidepoint(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_hover:
                    self.play()
                if quit_hover:
                    pygame.quit()
                    sys.exit()

        if play_hover:
            pygame.draw.rect(self.screen, (255, 255, 255), play_rect)
        else:
            pygame.draw.rect(self.screen, (200, 200, 200), play_rect)

        if quit_hover:
            pygame.draw.rect(self.screen, (255, 255, 255), quit_rect)
        else:
            pygame.draw.rect(self.screen, (200, 200, 200), quit_rect)

        font = pygame.font.Font(None, 36)
        title = font.render("Piano Simulator", True, (255, 255, 255))
        text1 = font.render("Play", True, (255, 0, 0))
        text2 = font.render("Quit", True, (255, 0, 0))

        # Center the text within the rectangles
        title_rect = title.get_rect(center=(self.width / 2, self.height / 2 - 225))
        text1_rect = text1.get_rect(center=(self.width/2 - 80 + 140/2, self.height/2 - 80 + 40/2))
        text2_rect = text2.get_rect(center=(self.width/2 - 80 + 140/2, self.height/2 - 20 + 40/2))

        self.screen.blit(title, title_rect)
        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect) 
       
        pygame.display.flip()

    def play(self):
        run = True
        sound_hight = 4

        font = pygame.font.Font(None, 50)

        # Track which keys were pressed last frame
        prev_keys = pygame.key.get_pressed()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.bg)

            keys = pygame.key.get_pressed()
            note_name = ""

            # Only play sound on key DOWN event (not while held)
            def key_just_pressed(key):
                return keys[key] and not prev_keys[key]

            if keys[pygame.K_RIGHT]:
                if sound_hight < 7:
                    sound_hight += 1
                print(sound_hight)
                pygame.time.delay(200)

            if keys[pygame.K_LEFT]:
                if sound_hight > 1:
                    sound_hight -= 1
                print(sound_hight)
                pygame.time.delay(200)

            if key_just_pressed(pygame.K_q):
                note_name = f"C{sound_hight}"
            elif key_just_pressed(pygame.K_2):
                note_name = f"Db{sound_hight}"
            elif key_just_pressed(pygame.K_w):
                note_name = f"D{sound_hight}"
            elif key_just_pressed(pygame.K_3):
                note_name = f"Eb{sound_hight}"
            elif key_just_pressed(pygame.K_e):
                note_name = f"E{sound_hight}"
            elif key_just_pressed(pygame.K_r):
                note_name = f"F{sound_hight}"
            elif key_just_pressed(pygame.K_5):
                note_name = f"Gb{sound_hight}"
            elif key_just_pressed(pygame.K_t):
                note_name = f"G{sound_hight}"
            elif key_just_pressed(pygame.K_6):
                note_name = f"Ab{sound_hight}"
            elif key_just_pressed(pygame.K_y):
                note_name = f"A{sound_hight}"
            elif key_just_pressed(pygame.K_7):
                note_name = f"Bb{sound_hight}"
            elif key_just_pressed(pygame.K_u):
                note_name = f"B{sound_hight}"

            if note_name and note_name in self.sounds:
                self.sounds[note_name].play()

            # Clear the area where the note name is displayed
            pygame.draw.rect(self.screen, self.bg, (self.width / 2 - 100, self.height / 2 - 250, 200, 50))

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

            pygame.display.flip()
            prev_keys = keys  # Update previous keys for next frame

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.bg)
            self.menu()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    game = Game()
    game.run()

    print("meow meow")