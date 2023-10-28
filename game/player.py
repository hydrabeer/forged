"""The Player class tracks various attributes of the player, like their inventory and location."""

from game.room import Room
from game.item import Item, Weapon, Armor
from game.character import Character, NPC
from random import randint


class Player(Character):
    """Player class. Inherits from Character.

    Attributes:
        sitting: Whether the player is sitting.
    """
    # Attribute types
    sitting: bool

    def __init__(self, location: Room) -> None:
        """Initialize a new player."""
        Character.__init__(self, location)
        self.inventory = [Weapon('RUSTY DAGGER', 'A SHODDILY CRAFTED DAGGER. SLIGHTLY MORE IMPOSING'
                                                 ' THAN A FINGERNAIL.', 3),
                          Armor('SHABBY JERKIN', 'A TATTERED AND DIRTY '
                                                 'JERKIN. IT PROVIDES LITTLE PROTECTION.', 1)]
        self.sitting = False

    def __str__(self) -> str:
        """Return the contents of this player's inventory as a string."""
        output = 'YOU ARE CARRYING: '
        for index, item in enumerate(self.inventory):
            if index != len(self.inventory) - 1:
                output += f"{item.name}, "
            else:
                output += f"{item.name}"
        return output

    def move(self, direction: str) -> str:
        """Move the player to the room in the specified direction."""
        new_room = self.location.get_exit(direction)
        if new_room:
            self.location = new_room
        else:
            return 'YOU WALK INTO A WALL.'

    def attack(self, target: NPC) -> str:
        """The player attacks the specified target NPC."""
        if type(self.holding) is Weapon:
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
            if hit and crit:
                return f"YOU CRIT {target.name} FOR {crit_damage} DAMAGE!"
            elif hit:
                return f"YOU HIT {target.name} FOR {self.holding.damage} DAMAGE!"
            else:
                return f"YOUR ATTACK MISSED {target.name}!"
        else:
            return f"YOU AREN'T HOLDING A WEAPON."
