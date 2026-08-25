
import pygame

# Картинки нот
NOTE_IMAGES = {
    'C': pygame.transform.scale(pygame.image.load('assets/images/notes/c.png'), (50, 50)),
    'D': pygame.transform.scale(pygame.image.load('assets/images/notes/d.png'), (50, 50)),
    'E': pygame.transform.scale(pygame.image.load('assets/images/notes/e.png'), (50, 50)),
}

flying_notes = []


def spawn_flying_note(rect, note_name):
    if note_name in NOTE_IMAGES:
        img = NOTE_IMAGES[note_name]
        x = rect.centerx - img.get_width() // 2
        y = rect.y - img.get_height()
        flying_notes.append({'img': img, 'x': x, 'y': y})


def update_and_draw_flying_notes(screen):
    for note in flying_notes[:]:
        note['y'] -= 2  # Рух вгору
        screen.blit(note['img'], (note['x'], note['y']))

        # Видаляємо ноту, якщо вона вилетіла за екран
        if note['y'] < -50:
            flying_notes.remove(note)