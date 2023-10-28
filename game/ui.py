"""UI handles the user interface."""

import pygame
from game.settings import WIDTH, HEIGHT
from textwrap import wrap


class TitleElements:
    """Title screen elements."""

    def __init__(self) -> None:
        """I will take ChatGPTs word for it."""
        self.title_bg = None
        self.title_bg_rect = None
        self.title_text_surf = None
        self.title_text_rect = None
        self.title_text_shadow = None
        self.title_text_shadow_rect = None
        self.sword_surf = None
        self.sword_rect = None
        self.press_enter_surf = None
        self.press_enter_rect = None
        self.press_enter_shadow = None
        self.press_enter_shadow_rect = None

    def initialize(self, font: pygame.font.Font, title_font: pygame.font.Font) -> None:
        """Initialize this stuff for some reason."""
        # Background
        self.title_bg = pygame.image.load('assets/images/fantasy_bg.png').convert_alpha()
        self.title_bg_rect = self.title_bg.get_rect(center=(WIDTH // 2 + 120, HEIGHT // 2 - 100))

        # Title text
        self.title_text_surf = title_font.render('FORGED', True, 'ivory')
        self.title_text_rect = self.title_text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.title_text_shadow = title_font.render('FORGED', True, 'black')
        self.title_text_shadow_rect = self.title_text_shadow.get_rect(
            center=(WIDTH // 2 - 4, HEIGHT // 4 + 4))

        # Sword
        self.sword_surf = pygame.image.load(
            'assets/images/fire_sword_transparent.png').convert_alpha()
        self.sword_rect = self.sword_surf.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))

        # Press enter
        self.press_enter_surf = font.render('PRESS ENTER TO START', True, 'ivory')
        self.press_enter_rect = self.press_enter_surf.get_rect(
            bottomright=(WIDTH - 18, HEIGHT - 18))
        self.press_enter_shadow = font.render('PRESS ENTER TO START', True, 'black')
        self.press_enter_shadow_rect = self.press_enter_shadow.get_rect(
            bottomright=(WIDTH - 20, HEIGHT - 16))


class UIManager:
    """The brains of the UI of Forged.

    Attributes:
        screen: The display surface.
        font: The main font of the game.
        title_font: The title screen sized font.
        user_text: The text typed by the user before input.
        user_input: The text input by the user.
        scroll_position: The current scroll position.
        lines: The lines of text to be rendered.
        bg_offset_x: The x-offset of the background image.
        bg_offset_y: The y-offset of the background image.
    """
    # Attribute types
    screen: pygame.Surface
    font: pygame.font.Font
    title_font: pygame.font.Font
    title_elements: TitleElements
    user_text: str
    user_input: str
    scroll_position: int
    lines: list[str]
    bg_offset_x: int
    bg_offset_y: int

    def __init__(self) -> None:
        """Initialize the UI manager."""
        pygame.display.set_icon(pygame.image.load('assets/images/F.png'))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Forged', 'assets/images/fire_sword_scaled.png')
        self.font = pygame.font.Font('assets/font/Commodore Pixelized v1.2.ttf', 36)
        self.title_font = pygame.font.Font('assets/font/Commodore Pixelized v1.2.ttf', 72)
        self.title_elements = TitleElements()
        self.user_text = '> '
        self.user_input = ''
        self.scroll_position = 0
        self.lines = []
        self.bg_offset_x = 0
        self.bg_offset_y = 0

    def render_text(self, display_text: str) -> None:
        """Render text when playing the game."""
        pairs = []
        line_spacing = 18
        self.lines = wrap(display_text, 44)

        # while len(self.lines) > 9:
        #     self.lines.pop(0)

        # Handling scrolling
        start_idx = self.scroll_position
        end_idx = self.scroll_position + 9
        if end_idx > len(self.lines):
            end_idx = len(self.lines)

        # Getting a text surf and rect for every line
        for line in self.lines[start_idx:end_idx]:
            text_surf = self.font.render(line, True, 'white')
            text_rect = text_surf.get_rect(topleft=(18, line_spacing))
            pairs.append((text_surf, text_rect))
            line_spacing += 67
        self.screen.fill('black')

        # Game text rendering
        for text_pair in pairs:
            self.screen.blit(text_pair[0], text_pair[1])

        # User text rendering at the bottom
        user_text_surf = self.font.render(self.user_text, True, 'white')
        user_text_rect = user_text_surf.get_rect(bottomleft=(18, HEIGHT - 18))
        self.screen.blit(user_text_surf, user_text_rect)

    def render_main_menu(self) -> bool:
        """Render the main menu. Returns whether the user is hovering over the start button."""

        # Background rect and offset
        title_bg_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        title_bg_rect.center = (WIDTH // 2 - 100 - self.bg_offset_x,
                                HEIGHT // 2 - 100 - self.bg_offset_y)

        # Background render
        self.screen.blit(self.title_elements.title_bg, title_bg_rect)

        # Sword
        self.screen.blit(self.title_elements.sword_surf, self.title_elements.sword_rect)

        # Game title text
        self.screen.blit(self.title_elements.title_text_shadow,
                         self.title_elements.title_text_shadow_rect)
        self.screen.blit(self.title_elements.title_text_surf, self.title_elements.title_text_rect)

        # Press enter button
        self.screen.blit(self.title_elements.press_enter_shadow,
                         self.title_elements.press_enter_shadow_rect)
        self.screen.blit(self.title_elements.press_enter_surf,
                         self.title_elements.press_enter_rect)

        # Press enter button hover visual
        mouse_pos = pygame.mouse.get_pos()
        self.bg_offset_x = mouse_pos[0] // 6
        self.bg_offset_y = mouse_pos[1] // 6
        if self.title_elements.press_enter_rect.collidepoint(mouse_pos):
            self.title_elements.press_enter_surf = self.font.render(
                'PRESS ENTER TO START', True, 'gold')
            self.title_elements.press_enter_shadow = self.font.render(
                'PRESS ENTER TO START', True, 'black')
            return True
        else:
            self.title_elements.press_enter_surf = self.font.render(
                'PRESS ENTER TO START', True, 'ivory')
            self.title_elements.press_enter_shadow = self.font.render(
                'PRESS ENTER TO START', True, 'black')
            return False

    def update(self) -> None:
        """Update the display surface."""
        pygame.display.update()
