"""The game module is focused on the internal workings of the game, encapsulating the game's
rules, data structures, and logic. - ChatGPT"""

import pygame
from sys import exit
from enum import Enum
from random import choice

from .audio import AudioEngine
from .ui import UIManager
from .settings import FPS
from .room import Room, tomb, hell
from .player import Player
from .character import NPC, deck
from .parser import Parser
from .stack import Stack


pygame.init()


class GameState(Enum):
    """State machine for the game."""
    MENU = 1
    PLAYING = 2


class Game:
    """Game class.

    Attributes:
        running: Whether the game is running.
        game_state: The current game state: MENU, PLAYING, or PAUSED.
        clock: The game clock, used for keeping the FPS.
        ui: The rendering engine of the game.
        audio: The audio engine of the game.
        player: The object that represents the player.
        current_room: The room the player is currently in.
        parser: The parser is responsible for translating user input for the game to turn into
                game actions.
        current_text: All the text displayed by the system.
        command_stack: The stack of commands the player has entered.
        temp_stack: A temporary stack used for storing commands when the player is scrolling.
        combat: Whether the player is in combat.
    """
    # Attribute types
    running: bool
    game_state: GameState
    clock: pygame.time.Clock
    ui: UIManager
    audio: AudioEngine
    player: Player
    current_room = Room
    parser: Parser
    current_text: str
    active_npcs: list[NPC]
    command_stack: Stack
    temp_stack: Stack
    combat: bool

    def __init__(self) -> None:
        """Initialize a new game."""
        pygame.init()
        self.game_state = GameState.MENU
        self.running = True
        self.clock = pygame.time.Clock()
        self.ui = UIManager()
        self.audio = AudioEngine()
        self.parser = Parser()
        self.player = Player(self.current_room)
        self.active_npcs = []
        self.setup_npcs()
        self.set_room(tomb)
        self.current_text = self.current_room.desc
        self.command_stack = Stack()
        self.temp_stack = Stack()
        self.combat = False

    def setup_npcs(self) -> None:
        """Set up the NPCs."""
        self.active_npcs.append(deck)
        deck.setup_deck()

    def run(self) -> None:
        """The main game loop."""
        while self.running:
            self.handle_events()
            parsed_input = self.parser.parse_command(self.ui.user_input)
            if parsed_input is not None:
                self.handle_command(parsed_input[0], parsed_input[1])
            if self.ui.user_input != '':
                self.ui.user_input = ''
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        """Handle user input and update game state accordingly."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.game_state == GameState.MENU:
                # if not self.audio.playing:
                #     self.audio.play_track('title')
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_state = self.game_state.PLAYING
            elif self.game_state == GameState.PLAYING:
                # self.audio.stop_track()
                # if not self.audio.playing:
                #     self.audio.play_track(self.current_room.name)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.ui.user_text = self.ui.user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.ui.user_input = self.ui.user_text.strip('>')
                        self.add_text(self.ui.user_text)
                        self.ui.user_text = '> '
                        while not self.temp_stack.is_empty():
                            self.command_stack.push(self.temp_stack.pop())
                        self.command_stack.push(self.ui.user_input)
                        if self.combat:
                            self.handle_combat()
                    elif event.key == pygame.K_UP:
                        if not self.command_stack.is_empty():
                            command = self.command_stack.pop()
                            self.ui.user_text = '>' + command
                            self.temp_stack.push(command)
                    elif event.key == pygame.K_DOWN:
                        if not self.temp_stack.is_empty():
                            command = self.temp_stack.pop()
                            self.ui.user_text = '>' + command
                            self.command_stack.push(command)
                        else:
                            self.ui.user_text = '> '
                    elif event.key == pygame.K_PAGEUP:
                        if self.ui.scroll_position > 0:
                            self.ui.scroll_position -= 1
                    elif event.key == pygame.K_PAGEDOWN:
                        if self.ui.scroll_position < len(self.ui.lines) - 9:
                            self.ui.scroll_position += 1
                    else:
                        self.ui.user_text += event.unicode.upper()
                self.handle_mouse_scrolling(event)

    def handle_mouse_scrolling(self, event: pygame.event.Event) -> None:
        """Handle mouse scrolling."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if self.ui.scroll_position > 0:
                    self.ui.scroll_position -= 1
            elif event.button == 5:
                if self.ui.scroll_position < len(self.ui.lines) - 9:
                    self.ui.scroll_position += 1

    def render(self) -> None:
        """Use the UI module to render the game based on the current game state."""
        if self.game_state == GameState.MENU:
            hover = self.ui.render_main_menu()
            if hover and pygame.mouse.get_pressed()[0]:
                self.game_state = self.game_state.PLAYING
        elif self.game_state == GameState.PLAYING:
            self.ui.render_text(self.current_text)

        self.ui.update()

    def add_text(self, text: str) -> None:
        """Add the given string to a new line of self.current_text."""
        self.current_text += '                                           ' + text
        self.ui.scroll_position = max(0, len(self.ui.lines) - 7 + len(text) // 44)

    def handle_command(self, action: str | None, subject: str | None) -> None:
        """Handle the output of the parser and perform the appropriate action."""

        # Commands that did not have a valid action.
        if action is None:
            self.add_text("THAT'S NOT A VERB I RECOGNIZE.")
            return

        # Commands that did not have a valid subject. These can be one-word commands or invalid.
        if subject is None:
            if action not in {'LOOK', 'INVENTORY', 'I', 'WAIT', 'SIT', 'SLEEP', 'STAND'}:
                self.add_text(f'I UNDERSTOOD YOU AS FAR AS WANTING TO {action}.')
                return
            elif action == 'LOOK':
                self.add_text(self.current_room.desc)
                return
            elif action in ('INVENTORY', 'I'):
                self.add_text(str(self.player))
                self.audio.play_sound('open_inventory')
                return
            elif action == 'WAIT':
                self.add_text(choice(('YOU LOITER.',
                                      'YOU WAIT FOR THE GAME TO BEAT ITSELF.',
                                      '*WHISTLING*',
                                      "MAYBE IF YOU WAIT LONG ENOUGH, YOU'LL WIN. MAYBE.")))
                return
            elif action == 'SIT':
                if not self.player.sitting:
                    self.add_text('YOU SIT DOWN.')
                    self.player.sitting = True
                    return
                else:
                    self.add_text('YOU ARE ALREADY SITTING. ARE YOU TRYING TO PHASE THROUGH THE '
                                  'GROUND?')
                    return
            elif action == 'STAND':
                if self.player.sitting:
                    self.add_text('YOU STAND UP.')
                    self.player.sitting = False
                    return
                else:
                    if self.player.health >= 50:
                        self.add_text('YOU HAVE EXCELLENT POSTURE.')
                        return
                    else:
                        self.add_text('YOU FIGHT THE URGE TO HUNCH OVER IN PAIN.')
                        return
            elif action == 'SLEEP':
                self.add_text('NOW IS NOT THE TIME FOR A NAP.')
                return

        # Commands that had a valid subject.
        else:
            if action == 'EXAMINE':
                for item in self.current_room.items:
                    if item.name == subject:
                        self.add_text(item.desc)
                        return
                for item in self.player.inventory:
                    if item.name == subject:
                        self.add_text(item.desc)
                        return
                for npc in self.active_npcs:
                    if npc.name == subject:
                        self.add_text(npc.desc)
                        return
                self.add_text('YOU SEE NO SUCH THING.')
                return
            elif action == 'TAKE':
                for item in self.current_room.items:
                    if item.name == subject:
                        self.current_room.remove_item(item)
                        self.player.add_item(item)
                        self.add_text(f'YOU TAKE THE {item.name}.')
                        return
                for npc in self.active_npcs:
                    if any(item.name == subject for item in npc.inventory):
                        self.add_text('NO GRABSIES.')
                        return
                self.add_text("YOU CAN'T SEE ANY SUCH THING.")
                return
            elif action == 'EQUIP':
                for item in self.player.inventory:
                    if item.name == subject:
                        self.player.hold(item)
                        self.add_text(f'YOU ARE NOW HOLDING THE {item.name}.')
                        return
                self.add_text("YOU DON'T HAVE ANY SUCH THING IN YOUR INVENTORY, SO YOU CAN'T "
                              "EQUIP IT.")
                return
            elif action == 'ATTACK':
                for npc in self.active_npcs:
                    if npc.name == subject:
                        if not npc.hostile:
                            self.add_text(f'{npc.name} IS NOW HOSTILE.')
                            npc.hostile = True
                        self.add_text(self.player.attack(npc))
                        self.combat = True
                        return
                self.add_text('YOU SEE NO SUCH TARGET.')
                return
            elif action == 'DROP':
                if subject == 'ALL':
                    for item in self.player.inventory:
                        self.player.remove_item(item)
                        self.current_room.add_item(item)
                        self.add_text(f'YOU DROP THE {item.name}.')
                    return
                for item in self.player.inventory:
                    if item.name == subject:
                        self.player.remove_item(item)
                        self.add_text(f'YOU DROP THE {item.name}.')
                        return
                self.add_text("YOU AREN'T CARRYING ANY SUCH THING, SO YOU CAN'T DROP IT.")
                return

    def handle_combat(self) -> None:
        """Handle a round of combat."""
        for npc in self.active_npcs:
            if npc.hostile and npc.location == self.current_room:
                self.add_text(npc.spell_attack(self.player))
            if self.player.health <= 0:
                self.player.health = 1
                self.combat = False
                self.add_text('YOU ARE DEAD. SEE YOU IN HELL.')
                self.set_room(hell)
                return

    def set_room(self, room: Room) -> None:
        """Update the current room and update the parser nouns accordingly,
        as well as the player's location.
        """
        self.current_room = room
        self.player.location = self.current_room
        # self.add_text(self.current_room.desc)

        # Make a new parser to flush the last room's noun additions
        self.parser = Parser()
        for item in room.items:
            self.parser.nouns.append(item.name)
        for item in self.player.inventory:
            self.parser.nouns.append(item.name)
        for npc in self.active_npcs:
            self.parser.nouns.append(npc.name)
            for item in npc.inventory:
                self.parser.nouns.append(item.name)
