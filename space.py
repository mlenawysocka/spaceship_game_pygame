import pygame
pygame.font.init()  # zaimportowanie czcionek

WIDTH, HEIGHT = 800, 450  # szerokość i wysokość okna gry
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # definicja okna gry
pygame.display.set_caption("Spaceship War")  # dodanie opisu w oknie gry

# definicje kolorów
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# definicja ramki na środku okna
BORDER = pygame.Rect(WIDTH/2 - 2, 0, 4, HEIGHT)

# definicje czcionek
HEALTH_FONT = pygame.font.SysFont('arial', 24)
WINNER_FONT = pygame.font.SysFont('arial', 72)

FPS = 60  # frames per second
STEP = 5   # liczba pikseli do poruszania dla rakiet
BULLET_SPEED = 8    # liczba pikseli do poruszania dla strzałów

# rozmiary rakiet
SPACESHIP_WIDTH = 40  # szerokość
SPACESHIP_HEIGHT = 60  # wysokość

# definicja nowych zdarzeń, potrzebna do obsługi uderzenie rakiety
WHITE_HIT = pygame.USEREVENT + 1  # traktujemy to jako kolejny 'proces', czyli po prostu liczbę
YELLOW_HIT = pygame.USEREVENT + 2  # traktujemy to jako kolejny 'proces', czyli po prostu liczbę, ale następną po porzedniej

# załadowanie obrazów rakiet
# przekształcenia obrazków: obrót, skalowanie
# żółta rakieta
YELLOW_SPACESHIP_IMAGE = pygame.image.load('spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
# biała rakieta
WHITE_SPACESHIP_IMAGE = pygame.image.load('spaceship_white.png')
WHITE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(WHITE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
# tło
SPACE = pygame.transform.scale(pygame.image.load('ribbon-light-space.jpg'), (WIDTH, HEIGHT))


# funkcja odpowiedzialna za rysowanie okna
# przekazujemy do niej
# 1. obiekt prosotkąt będący rakietę (białą i żółtą)
# 2. listę strzałów rakiet
# 3. wartość zdrowia rakiet
def draw_window(white, yellow, white_bullets, yellow_bullets,  white_health, yellow_health):
    WIN.blit(SPACE, (0, 0))  # wypełnienie ekranu grafiką
    pygame.draw.rect(WIN, BLACK, BORDER)  # narysoawnie linii piionowej na środku ekranu

    # Tekst z warością zdrowia poszczególnych rakiet
    white_health_text = HEALTH_FONT.render("Health: " + str(white_health), 1, WHITE)  # ta 1 jest po prostu zawsze
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)  # ta 1 jest po prostu zawsze

    # wyświetlenie testu w lewym i prawym górnym narożniku
    WIN.blit(white_health_text, (WIDTH - white_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # wyświetlenie rakiet
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(WHITE_SPACESHIP, (white.x, white.y))

    # wyświtalnie strzałów dla każdej rakiety
    for bullet in white_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    # odświeżenie ekranu
    pygame.display.update()

# funkcja obsługująca ruch buałej rakiety
# rakieta sterowana jest klawiszami ADWS
# ruch jest ograniczony przez ramkę okna oraz jej środek (BORDER)
def white_handle_movement(keys_pressed, white):
    if keys_pressed[pygame.K_a] and white.x - STEP > 0:  # left
        white.x -= STEP
    if keys_pressed[pygame.K_d] and white.x + STEP + white.width + 20 < BORDER.x:  # right
        white.x += STEP
    if keys_pressed[pygame.K_w] and white.y - STEP > 0:  # up
        white.y -= STEP
    if keys_pressed[pygame.K_s] and white.y + STEP + white.height - 25 < HEIGHT:  # down
        white.y += STEP

# funkcja obsługująca ruch żółtej rakiety
# rakieta sterowana jest srzałkami
# ruch jest ograniczony przez ramkę okna oraz jej środek (BORDER)
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - STEP > BORDER.x + BORDER.width:   # left
        yellow.x -= STEP
    if keys_pressed[pygame.K_RIGHT] and yellow.x + STEP + yellow.width + 20 < WIDTH:  # right
        yellow.x += STEP
    if keys_pressed[pygame.K_UP] and yellow.y - STEP > 0:  # up
        yellow.y -= STEP
    if keys_pressed[pygame.K_DOWN] and yellow.y + STEP + yellow.height - 25 < HEIGHT:  # down
        yellow.y += STEP


def handle_bullets(white_bullets, yellow_bullets, white, yellow):
    for bullet in white_bullets:
        bullet.x += BULLET_SPEED
        # metoda colliderect zadziała tylko z prosokątami
        # sprawdza, czy doszło do zderzenia dwóch prostokątów
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            white_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_SPEED
        # metoda colliderect zadziała tylko z prosokątami
        # sprawdza, czy doszło do zderzenia dwóch prostokątów
        if white.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WHITE_HIT))
            yellow_bullets.remove(bullet)


# funkcja do wypisania na ekran zwycięzcy
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    # drukowanie na środek ekranu uwzględniające długość i szerokość okna i napisu
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()

    # 5 sekund na wyswietlenie napisu
    pygame.time.delay(5000)


# główna funkcja programu, logika gry
def main():
    # zamknięcie statków w obiekt typu prostokąt
    white = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(600, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # listy do przechowywania strzałów
    white_bullets = []
    yellow_bullets = []

    # zmienne do przechowywania wartości zdrowia
    white_health = 3
    yellow_health = 3

    # zmianna odpowiedzialna za późniejsze odświeżanie gry - FPS
    clock = pygame.time.Clock()

    run = True
    # główna pętla programu
    while run:
        # taktowanie zegara
        clock.tick(FPS)

        # zawsze zaczynamy od tej petli
        for event in pygame.event.get():
            # sprawdzamy, czy czlowiek zamkna oknął
            if event.type == pygame.QUIT:
                run = False
                # zamkniecie gry
                pygame.quit()

            # sprawdzamy, czy oddano strzał - pojedyncze nacisniecie klawisz
            if event.type == pygame.KEYDOWN:
                # jesli wcisnieto lewy SHIFT
                if event.key == pygame.K_LSHIFT:
                    # to stwórz nową kulę do strzału
                    bullet = pygame.Rect(white.x + white.width, white.y + white.height//2 - 2, 10, 5)
                    # i dodają ją do listy (by wyświetlić)
                    white_bullets.append(bullet)
                # analogicznie dla prawego SHIFT
                if event.key == pygame.K_RSHIFT:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

            # obsługa nowych zdarzeń - udrzenia
            #jeśli biała rakieta dostała, to zmniejsz jej zdrowie
            if event.type == WHITE_HIT:
                yellow_health -= 1
            # jeśli żółta rakieta dostała, to zmniejsz jej zdrowie
            if event.type == YELLOW_HIT:
                white_health -= 1

        # ustawienie odpowiedniego tekstu dla wygranego
        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Yellow wins"

        if white_health <= 0:
            winner_text = "White wins"

        # UWAGA
        # jeśli tekst nie jest pusty (czyli zaszło jedno ze zdarzeń wyżej),
        # to zakończ program
        if winner_text != "":
            draw_winner(winner_text)
            break

        # obsługa wszystkich wciśnietych klawiszy, by umożliwyć jednoczesne sterowanie 2 graczą
        keys_pressed = pygame.key.get_pressed()

        # obsługa poruszania się rakiet
        white_handle_movement(keys_pressed, white)
        yellow_handle_movement(keys_pressed, yellow)

        # obsługa poruszania się kul
        handle_bullets(white_bullets, yellow_bullets, white, yellow)

        # wyrysowanie okna
        draw_window(white, yellow, white_bullets, yellow_bullets, white_health, yellow_health)

    # restart gry
    main()


if __name__ == "__main__":
    main()