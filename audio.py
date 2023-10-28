"""The audio module is responsible for playing audio in Forged."""

import pygame


class AudioEngine:
    """The audio engine of Forged.

    Attributes:
        tracks: The music tracks of the game.
        sound_effects: The sound effects of the game.
        playing: Whether the audio engine is playing music.
    """
    # Attribute types
    tracks: dict[str, str]
    sound_effects: dict[str, pygame.mixer.Sound]
    playing: bool

    def __init__(self) -> None:
        """Initialize the audio engine."""
        self.tracks = {'title': 'assets/music/grassy_world.mp3',
                       'tomb': 'assets/music/forgotten_tombs.mp3',
                       'forest': 'assets/music/forest_ambience.mp3',
                       'rain': 'assets/music/rain_ambience.ogg'}
        self.sound_effects = {'open_inventory': pygame.mixer.Sound(file='assets/sounds/inventory'
                                                                        '/leather_inventory.wav')}
        self.playing = False

    def play_track(self, track_name: str) -> None:
        """Play the specified track."""
        track = self.tracks[track_name]
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)
        self.playing = True

    def stop_track(self) -> None:
        """Stop the currently playing track."""
        pygame.mixer.music.fadeout(300)
        self.playing = False

    def play_sound(self, sound_name: str) -> None:
        """Play the specified sound."""
        sound = self.sound_effects[sound_name]
        sound.play()
