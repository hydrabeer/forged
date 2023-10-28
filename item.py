"""The item class models the items in the game."""


class Item:
    """Item class.

    Attributes:
        name: The name of this item.
        desc: The description of this item.
        in_inventory: Whether this item is in a character's inventory.
    """
    # Attribute types
    name: str
    desc: str
    in_inventory: bool

    def __init__(self, name: str, desc: str) -> None:
        """Initialize a new item."""
        self.name = name
        self.desc = desc
        self.in_inventory = False

    def action(self, action: str) -> None:
        """This method is called when this item appears as the subject of a player
        command. The action parameter is the verb of the command."""
        ...


class Weapon(Item):
    """Weapon class. Inherits from Item.

    Attributes:
        damage: The damage this weapon does.
    """
    # Attribute types
    damage: int

    def __init__(self, name: str, desc: str, damage: int) -> None:
        """Initialize a new weapon."""
        Item.__init__(self, name, desc)
        self.damage = damage


class Armor(Item):
    """A class for armor. Inherits from Item.

    Attributes:
        rating: The rating of this armor determines its effectiveness.
    """
    # Attribute types
    rating: int

    def __init__(self, name: str, desc: str, rating: int) -> None:
        """Initialize a new armor."""
        Item.__init__(self, name, desc)
        self.rating = rating


class Magic(Item):
    """A class for inexhaustible spells. Inherits from Item.

    Attributes:
        damage: The damage this spell does.
    """
    # Attribute types
    damage: int

    def __init__(self, name: str, desc: str, damage: int) -> None:
        """Initialize a new spell."""
        Item.__init__(self, name, desc)
        self.damage = damage
