"""The character module contains the Character and NPC classes."""

from __future__ import annotations
from game.room import Room, tomb
from game.item import Item, Weapon, Magic
from random import randint


class Character():
    """The character class. Superclass of NPC and Player.
    This is an abstract class and should not be instantiated directly.

    Attributes:
        health: The hit points of this character.
        inventory: The items that this character has.
        location: The room that this character is in.
        holding: The item that this character is holding, or None if this character is holding
                 nothing.
        ac: The armor class of this character.
    """
    # Attribute types
    health: int
    inventory: list[Item]
    location: Room
    holding: Item | Weapon | None
    ac: int

    def __init__(self, location: Room) -> None:
        """Initialize a new character."""
        self.health = 100
        self.inventory = []
        self.location = location
        self.holding = None
        self.ac = 10

    def add_item(self, item: Item) -> None:
        """Add the specified item to the inventory of this character."""
        self.inventory.append(item)
        item.in_inventory = True
        if item == self.holding:
            self.holding = None

    def hold(self, item: Item) -> None:
        """Remove the given item from the inventory of this character and update self.holding.

        Preconditions:
            item in self.inventory
            self.holding is None
        """
        self.inventory.remove(item)
        item.in_inventory = False
        self.holding = item

    def remove_item(self, item: Item) -> None:
        """If the given item is in the inventory of this character, remove it. If the given item
        is being held, change self.holding to None. In both cases, add the item to
        self.location.items.

        Preconditions:
            item in self.inventory or self.holding == item
        """
        if item in self.inventory:
            self.inventory.remove(item)
            item.in_inventory = False
        else:  # item == self.holding
            self.holding = None

        self.location.add_item(item)

    def attack(self, target: Character) -> str:
        """Attack the target."""
        raise NotImplementedError


class NPC(Character):
    """NPC class. Inherits from Character.

    Attributes:
        name: The name of this NPC.
        desc: The description of this NPC.
        hostile: Whether this NPC is hostile toward the player.
    """
    # Attribute types
    name: str
    desc: str
    hostile: bool

    def __init__(self, location: Room, name: str, desc: str) -> None:
        """Initialize a new NPC."""
        Character.__init__(self, location)
        self.name = name
        self.desc = desc
        self.hostile = False

    def attack(self, target: Character) -> str:
        """Attack the target."""
        if self.holding is Weapon:
            crit_damage = self.holding.damage * 2
            hit = False
            crit = False
            roll = randint(1, 20)
            if roll == 20:
                target.health -= crit_damage
                crit = True
                hit = True
            elif roll >= target.ac:
                target.health -= self.holding.damage
                hit = True
            if target is not NPC:
                if hit and crit:
                    return f"{self.name} CRIT YOU FOR {crit_damage} DAMAGE!"
                elif hit:
                    return f"{self.name} HIT YOU FOR {self.holding.damage} DAMAGE!"
                else:
                    return f"{self.name}'S ATTACK MISSED YOU!"
            else:  # target is NPC
                if hit and crit:
                    return f"{self.name} CRIT {target.name} FOR {crit_damage} DAMAGE!"
                elif hit:
                    return f"{self.name} HIT {target.name} FOR {self.holding.damage} DAMAGE!"
                else:
                    return f"{self.name}'S ATTACK MISSED {target.name}!"
        else:
            return f"{self.name} TRIED TO ATTACK BUT ISN'T HOLDING A WEAPON."

    def spell_attack(self, target: Character) -> str:
        """Attack the target with a spell."""
        if type(self.holding) is Magic:
            target.health -= self.holding.damage
            if target is not NPC:
                return (f"{self.name} HIT YOU WITH A {self.holding.name} "
                        f"SPELL FOR {self.holding.damage} DAMAGE!")
            else:  # target is NPC
                return f"{self.name} HIT {target.name} FOR {self.holding.damage} DAMAGE!"
        else:
            return f"{self.name} TRIED TO MAKE A SPELL ATTACK BUT FORGOT HOW."

    def setup_deck(self) -> None:
        """Set up Deck."""
        self.add_item(Magic('FIREBALL', 'A BALL OF FIRE', 100))
        self.holding = deck.inventory[0]
        self.add_item(Item('TORCH', "A RAMSHACKLE TORCH. IT GIVES OFF A DIM LIGHT."))


deck = NPC(tomb, 'DECK', 'DECK IS A TALL, SLENDER, ELF WITH DARK EYES, WITH A SHOCK OF '
                         'DARK EMERALD HAIR AND A RESTING WORRY FACE. HE HAS BEEN '
                         'TRAVELLING WITH YOU IN SEARCH OF TREASURE AND GLORY. ONE '
                         'OF THE GOOD GUYS.')
