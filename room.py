"""The room class is instantiated to represent the different locations in the game."""

from __future__ import annotations
from game.item import Item


class Room:
    """Room class.

    Attributes:
        name: The name of this room. Currently only used to play music.
        desc: A description of this room.
        items: The items in this room that can be picked up.
        exits: The rooms connected to this room.
    """
    # Attribute types
    name: str
    desc: str
    items: list[Item]
    exits: dict[str, Room]

    def __init__(self, name: str, desc: str, items=None, exits=None) -> None:
        """Initialize a new room."""
        self.name = name
        self.desc = desc
        self.items = items if items else []
        self.exits = exits if exits else {}

    def get_exit(self, direction: str) -> Room:
        """Return the room in the specified direction."""
        return self.exits.get(direction)

    def add_item(self, item: Item) -> None:
        """Add the specified item to this room."""
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        """Remove the specified item from this room."""
        self.items.remove(item)


tomb = Room('tomb', "YOU ARE IN A DARK CHAMBER WITH ROUGH WALLS. YOUR COMPANION, DECK, HOLDS A "
                    "SPUTTERING TORCH THAT PROVIDES THE ONLY LIGHT HERE. THE AIR IS STILL, "
                    "SMELLS OF DEATH, AND EACH INHALE FEELS AS THOUGH IT ADDS A LAYER OF DUST IN "
                    "YOUR LUNGS. YOU SEE A PASSAGE TO THE NORTH, AND TWO SMALLER CREVICES TO THE "
                    "EAST AND WEST THAT YOU THINK YOU COULD FIT THROUGH. ")

hell = Room('hell', "YOU WAKE UP IN A PILE OF BONES. YOU ARE IN A LARGE, BLOOD-RED CAVERN WITH A "
                    "CEILING SO FAR AWAY THAT IT'S CONCEALED BY FOG. IT SMELLS OF SULFUR AND "
                    "BURNING FLESH. THERE IS A SMALL PASSAGE TO THE NORTH AND A LARGE "
                    "EBONY DOOR TO THE EAST.")
