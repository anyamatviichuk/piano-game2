import pygame


class Button:
    def __init__(self, x, y, width, height, action=None, img_idle=None, img_hover=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.img_idle = pygame.transform.scale(img_idle, (width, height)) if img_idle else None
        self.img_hover = pygame.transform.scale(img_hover, (width, height)) if img_hover else None

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        img = self.img_hover if (hovered and self.img_hover) else self.img_idle
        if img:
            screen.blit(img, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()