import sys
import pygame
from pygame import mixer

from setting import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, KEYS
from sounds import load_sounds
from keys import create_key_rects, draw_keys, NOTE_BY_INDEX
from effects import spawn_flying_note
from buttons import Button
from ui.settings_menu import SettingsMenu


def main():
    pygame.init()
    mixer.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Piano Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    sounds = load_sounds(KEYS)
    current_state = "PIANO"
    volume = 0.7
    num_keys = 3

    for sound in sounds.values():
        sound.set_volume(volume)

    key_rects = create_key_rects(num_keys)

    keyboard_map = {
        pygame.K_a: 0,
        pygame.K_s: 1,
        pygame.K_d: 2,
    }
    note_keys_order = ["c", "d", "e", "f", "g", "a", "b"]

    settings_icon_idle = pygame.image.load("assets/images/buttons/exit_unhover.png")
    settings_icon_hover = pygame.image.load("assets/images/buttons/exit_hover.png")

    def open_settings():
        nonlocal current_state
        current_state = "SETTINGS"

    btn_settings = Button(
        WINDOW_WIDTH - 50, 10, 40, 40,
        action=open_settings,
        img_idle=settings_icon_idle,
        img_hover=settings_icon_hover
    )

    def play_note(idx):
        if idx < num_keys:
            note_name = note_keys_order[idx]
            if note_name in sounds:
                sounds[note_name].play()

            # Спавнимо нотку прямо під час натискання
            note_char = NOTE_BY_INDEX.get(idx)
            spawn_flying_note(key_rects[idx], note_char)

    def on_settings_change(new_vol, new_keys_count):
        nonlocal volume, num_keys, key_rects
        volume = new_vol
        for snd in sounds.values():
            snd.set_volume(volume)

        if new_keys_count != num_keys:
            num_keys = new_keys_count
            key_rects = create_key_rects(num_keys)

    settings_menu = SettingsMenu(
        screen_rect=screen.get_rect(),
        initial_volume=volume,
        initial_keys=num_keys,
        min_keys=1,
        max_keys=len(KEYS),
        on_change=on_settings_change,
        on_back=lambda: set_state("PIANO")
    )

    def set_state(state):
        nonlocal current_state
        current_state = state

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_state == "PIANO":
                btn_settings.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key in keyboard_map:
                        play_note(keyboard_map[event.key])

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for idx, rect in enumerate(key_rects):
                        if rect.collidepoint(event.pos):
                            play_note(idx)

            elif current_state == "SETTINGS":
                settings_menu.handle_event(event)

        screen.fill(WHITE)

        if current_state == "PIANO":
            draw_keys(screen, key_rects)
            btn_settings.draw(screen)

        elif current_state == "SETTINGS":
            settings_menu.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()