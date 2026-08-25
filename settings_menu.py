import pygame
from buttons import Button
from ui.slider import Slider

class SettingsMenu:
    def __init__(self, screen_rect, initial_volume, initial_keys, min_keys, max_keys, on_change, on_back):
        self.screen_rect = screen_rect
        self.on_change = on_change
        self.on_back = on_back

        cx = screen_rect.centerx

        # Кнопка «Вихід / Назад»
        back_idle = pygame.image.load('assets/images/buttons/exit_unhover.png')
        back_hover = pygame.image.load('assets/images/buttons/exit_hover.png')
        self.back_btn = Button(40, 30, 48, 48, action=self.on_back, img_idle=back_idle, img_hover=back_hover)

        # Слайдер гучності
        self.volume_slider = Slider(
            cx - 150, 150, 300,
            min_val=0.0, max_val=1.0, initial=initial_volume,
            label="Гучність"
        )
        self.volume_slider.on_change = self._update

        # Слайдер кількості клавіш
        self.keys_slider = Slider(
            cx - 150, 260, 300,
            min_val=min_keys, max_val=max_keys, initial=initial_keys,
            label="Кількість клавіш"
        )
        self.keys_slider.on_change = self._update

    def _update(self, _=None):
        # Викликаємо зовнішню функцію зміни налаштувань
        if self.on_change:
            self.on_change(self.volume_slider.value, int(self.keys_slider.value))

    def draw(self, screen, font):
        # Малюємо заголовок
        title = font.render("Налаштування", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(self.screen_rect.centerx, 70)))

        # Малюємо всі елементи UI
        self.back_btn.draw(screen)
        self.volume_slider.draw(screen, font)
        self.keys_slider.draw(screen, font)

    def handle_event(self, event):
        self.back_btn.handle_event(event)
        self.volume_slider.handle_event(event)
        self.keys_slider.handle_event(event)