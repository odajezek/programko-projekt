import pygame
import sys

# Inicializace Pygame
pygame.init()

# Konstanty
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 200, 0)

# Nastavení obrazovky
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ježkův bar :)")
clock = pygame.time.Clock()

# Načtení pozadí
background = pygame.image.load("wall.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Načtení obrázku zákazníka
customer_img = pygame.image.load("customer.png")
customer_img = pygame.transform.scale(customer_img, (200, 200)) 

# Fonty
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 30)

# Hlasitost
volume = 0.5
pygame.mixer.init()
pygame.mixer.music.set_volume(volume)

# Fullscreen stav
fullscreen = False

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        color = LIGHT_GRAY if self.is_hovered else GRAY
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surf = small_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    return self.action
        return None

class Slider:
    def __init__(self, x, y, width, min_val=0.0, max_val=1.0, start_val=0.5):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.handle_x = x + width * ((start_val - min_val) / (max_val - min_val))
        self.dragging = False

    def draw(self, surface):
        # Čára slideru
        pygame.draw.rect(surface, GRAY, self.rect)
        # Kolečka posuvníku
        handle_rect = pygame.Rect(self.handle_x - 8, self.rect.centery - 8, 16, 16)
        pygame.draw.circle(surface, GREEN if self.dragging else BLACK, handle_rect.center, 8)
        # Text hlasitosti
        vol_text = small_font.render(f"Hlasitost: {int(self.value * 100)}%", True, BLACK)
        surface.blit(vol_text, (self.rect.x, self.rect.y - 40))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) < 15 and abs(event.pos[1] - self.rect.centery) < 15:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.value = self.min_val + (self.max_val - self.min_val) * ((self.handle_x - self.rect.x) / self.rect.width)
            pygame.mixer.music.set_volume(self.value)

def settings_scene():
    global fullscreen, screen

    back_button = Button(300, 500, 200, 50, "Zpět do menu", "main_menu")
    fullscreen_button = Button(300, 400, 200, 50, "Přepnout fullscreen", "toggle_fullscreen")
    slider = Slider(250, 300, 300, 0.0, 1.0, pygame.mixer.music.get_volume())

    while True:
        mouse_pos = pygame.mouse.get_pos()
        current_state = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                back_button.check_hover(mouse_pos)
                fullscreen_button.check_hover(mouse_pos)

            result = back_button.handle_event(event)
            if result:
                current_state = result

            result = fullscreen_button.handle_event(event)
            if result == "toggle_fullscreen":
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            slider.handle_event(event)

        if current_state:
            return current_state

        screen.fill(WHITE)
        title = font.render("Nastavení", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        slider.draw(screen)
        fullscreen_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

def main_menu():
    buttons = [
        Button(300, 150, 200, 50, "hrát", "hra :)"),
        Button(300, 250, 200, 50, "nastavení", "nastavení"),
        Button(300, 350, 200, 50, "skóre", "skóre"),
        Button(300, 450, 200, 50, "Konec", "quit")
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        current_state = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for button in buttons:
                if event.type == pygame.MOUSEMOTION:
                    button.check_hover(mouse_pos)
                result = button.handle_event(event)
                if result:
                    current_state = result

        if current_state:
            return current_state

        # === vykreslení pozadí ===
        screen.blit(background, (0, 0))

        # Nápis a tlačítka
        title = font.render("ježkův bar", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)


def scene(scene_name):
    back_button = Button(300, 500, 200, 50, "Zpět do menu", "main_menu")
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        current_state = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                back_button.check_hover(mouse_pos)
            
            result = back_button.handle_event(event)
            if result:
                current_state = result

        if current_state:
            return current_state

        # === Vykreslení pozadí ===
        screen.fill(WHITE)
        
        # Nadpis
        #title = font.render(f"Toto je {scene_name}", True, BLACK)
        #screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        if scene_name == "hra :)":
            # Posunutí obrázku výš
            customer_rect = customer_img.get_rect(center=(SCREEN_WIDTH//2, 200))
            screen.blit(customer_img, customer_rect)

            # Zalomený text
            text_lines = [
                "Hra bude spočívat v tom, že hráč bude obsluhovat zákazníky.",
                "Za to dostane body, které budou zapsané do databáze",
                "a zobrazeny v 'skóre'."
            ]

            # Posun textu výš 
            start_y = customer_rect.bottom + 20
            for i, line in enumerate(text_lines):
                example_text = small_font.render(line, True, BLACK)
                text_x = SCREEN_WIDTH//2 - example_text.get_width()//2
                text_y = start_y + i * 35
                screen.blit(example_text, (text_x, text_y))

        # Tlačítko zpět
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

def main():
    current_state = "main_menu"
    
    while True:
        if current_state == "main_menu":
            current_state = main_menu()
        elif current_state == "nastavení":
            current_state = settings_scene()
        elif current_state == "quit":
            pygame.quit()
            sys.exit()
        else:
            current_state = scene(current_state)

if __name__ == "__main__":
    main()
