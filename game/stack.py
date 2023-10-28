"""The stack module contains a stack data structure for the game."""

from typing import Any


class Stack:
    """A stack is a data structure that is first in last out.

    Attributes:
        _items: The items in the stack.
    """
    # Attribute types
    _items: list[Any]

    def __init__(self) -> None:
        """Initialize a new stack."""
        self._items = []

    def push(self, item: Any) -> None:
        """Push an item onto the top of the stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Pop an item off the top of the stack."""
        return self._items.pop()

    def peek(self) -> Any:
        """Peek at the top item of the stack."""
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return whether the stack is empty."""
        return self._items == []

    def size(self) -> int:
        """Return the size of the stack."""
        return len(self._items)

    def __str__(self) -> str:
        """Return a string representation of the stack."""
        return str(self._items)

    def __contains__(self, item: Any) -> bool:
        """Return whether the stack contains the specified item."""
        return item in self._items
