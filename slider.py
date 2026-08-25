import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial=0.5, label=""):
        self.track_rect = pygame.Rect(x, y, width, 10)
        self.handle_radius = 12
        self.min = min_val
        self.max = max_val
        self.value = initial
        self.label = label
        self.dragging = False
        self.on_change = None

    def draw(self, screen, font):
        # 1. Малюємо смужку (трек)
        pygame.draw.rect(screen, (200, 200, 200), self.track_rect, border_radius=5)
        pygame.draw.rect(screen, (50, 50, 50), self.track_rect, 2, border_radius=5)

        # 2. Обчислюємо позицію кружечка (від 0.0 до 1.0)
        ratio = (self.value - self.min) / (self.max - self.min)
        handle_x = int(self.track_rect.left + ratio * self.track_rect.width)
        handle_y = self.track_rect.centery

        # 3. Малюємо кружечок (ручку)
        pygame.draw.circle(screen, (50, 50, 50), (handle_x, handle_y), self.handle_radius)

        # 4. Малюємо текст із назвою та значенням
        if font and self.label:
            val_text = f"{int(self.value * 100)}%" if self.max <= 1.0 else f"{int(self.value)}"
            text_surf = font.render(f"{self.label}: {val_text}", True, (0, 0, 0))
            screen.blit(text_surf, (self.track_rect.left, self.track_rect.top - 30))

    def handle_event(self, event):
        # Натиснули мишку на лінію — починаємо перетягування
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.track_rect.inflate(10, 20).collidepoint(event.pos):
                self.dragging = True
                self._update_val(event.pos[0])

        # Соваємо мишкою — оновлюємо значення
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_val(event.pos[0])

        # Відпустили мишку — зупиняємо перетягування
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def _update_val(self, mouse_x):
        # Обчислюємо нове значення залежно від того, де знаходиться мишка
        rel_x = mouse_x - self.track_rect.left
        ratio = max(0.0, min(1.0, rel_x / self.track_rect.width))
        self.value = self.min + ratio * (self.max - self.min)

        # Передаємо нове значення назовні
        if self.on_change:
            self.on_change(self.value)