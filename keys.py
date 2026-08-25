import pygame
from effects import update_and_draw_flying_notes

KEY_UNPRESSED = pygame.transform.scale(
    pygame.image.load('assets/images/key_unpressed.png'), (100, 250)
)

NOTE_BY_INDEX = {0: 'C', 1: 'D', 2: 'E'}


def create_key_rects(num_keys, start_x=50, start_y=100, key_width=100, key_height=250):
    return [pygame.Rect(start_x + i * key_width, start_y, key_width, key_height) for i in range(num_keys)]


def draw_keys(screen, key_rects):
    for rect in key_rects:
        screen.blit(KEY_UNPRESSED, (rect.x, rect.y))

    # Малюємо та оновлюємо анімацію нот
    update_and_draw_flying_notes(screen)