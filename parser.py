"""The parser translates user input into actions and subjects."""

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class Parser:
    """Command parser class for Forged.

    Attributes:
        stop_words: A set of words that convey little meaning and can be removed from inputs.
        verbs: A set of accepted verbs.
        nouns: A list of accepted nouns. These change based on the room, but always include
               cardinal directions.
    """
    stop_words: set
    verbs: set
    nouns: list[str]

    def __init__(self) -> None:
        """Initialize the parser."""
        self.stop_words = set(stopwords.words('english'))
        self.verbs = {'LOOK', 'TAKE', 'DROP', 'EXAMINE', 'SEARCH', 'INVENTORY', 'I', 'OPEN',
                      'CLOSE', 'LOCK', 'UNLOCK', 'ASK', 'TELL', 'SAY', 'GIVE', 'SHOW', 'WAIT',
                      'AGAIN', 'ATTACK', 'BUY', 'COVER', 'DRINK', 'EAT', 'FILL', 'JUMP', 'KISS',
                      'KNOCK', 'LISTEN', 'MOVE', 'PULL', 'PUSH', 'REMOVE', 'READ', 'SIT', 'SLEEP',
                      'STAND', 'THROW', 'TIE', 'TOUCH', 'TURN', 'UNTIE', 'WEAR', 'EQUIP'}
        self.nouns = ['NORTH', 'N' 'EAST', 'E' 'SOUTH', 'S' 'WEST', 'W', 'ALL']

    # noinspection PyTypeChecker
    def parse_command(self, user_input: str) -> tuple[str | None] | None:
        """Accept a user input string and returns the action and the subject in a tuple if they
        are found. An action or subject that is not found will be returned as None in the tuple.
        """
        if user_input == '':
            return
        tokens = word_tokenize(user_input)
        words = [word for word in tokens if word.isalpha() and word not in self.stop_words]

        action = None
        subject = None

        for index, word in enumerate(words):
            if word in self.verbs:
                action = word
            elif word in self.nouns:
                subject = word
            elif index < len(words) - 1:
                two_word = word + ' ' + words[index + 1]
                if two_word in self.nouns:
                    subject = two_word

        return (action, subject)
