from random import sample, randint

class WordJumbleGame:
    """
    Main class for the Word Jumble game.
    Handles game logic, scoring, and user interaction.
    7-letter words are loaded from a text file.
    100 points are awarded for each correct guess.
    0 points are awarded for incorrect guesses.
    3 modes: manual play, agent play, or quit.
    1 round per playthrough, with option to replay.
    """

    def __init__(self, word_file="seven_letter_words.txt"):
        """
        Initializes the game with a word file.

        Args:
            word_file (str):    Path to the text file with 7-letter words.
                                Defaults to "seven_letter_words.txt".
        """
        self.word_file = word_file
        self.words = self._load_words()
        self.anagrams = self._create_anagrams()
        self.score = 0

    def _load_words(self):
        """
        Loads words from the file and returns them as a list.

        Returns:
            list: List of words (str).
        """
        with open(self.word_file, "r") as file:
            return [line.strip().upper() for line in file.readlines()]

    def _create_anagrams(self) -> dict:
        """
        Dictionary mapping sorted letter strings to their anagrams.
        """
        anagrams = {}
        for word in self.words:
            sl = "".join(sorted(word))
            if sl not in anagrams:
                anagrams[sl] = []
            anagrams[sl].append(word)
        return anagrams

    def random_word(self):
        """
        Returns a random 7-letter word from the loaded list.

        Returns:
            str: Random word.
        """
        return self.words[randint(0, len(self.words) - 1)]

    def jumble_word(self, word):
        """
        Jumbles the letters of the given word.

        Args:
            word (str): Word to jumble.

        Returns:
            str: Jumbled word.
        """
        return ''.join(sample(word, len(word)))

    def play_round(self, player):
        """
        Plays one round of the game with the given player.

        Args:
            player (Player/Agent): Player object (either Player or Agent).
        """
        word = self.random_word()
        jumbled = self.jumble_word(word)
        print(f"\nUnjumble this word: {jumbled}")

        guess = player.make_guess(jumbled, self.anagrams)

        if guess == word:
            print(f"You entered: {guess}")
            print("That is correct! You gained 100 points.")
            self.score += 100
        else:
            print(f"You entered: {guess}")
            print(f"Oh no! That is incorrect. The correct answer is: {word}")
        print(f"Your point total is: {self.score}")

    def start(self):
        """
        Starts the game and handles user interaction.
        """
        print("Welcome to Word Jumble!")
        print("Below is a 7-letter word.")
        print("Unjumble the word to the best of your ability.")
        print("If you guess correctly, you will receive 100 points.")
        print("If you guess incorrectly, you will get 0 points.")
        mode = input("Type '0' to play manually, '1' to watch an agent play, or '2' to leave: ")
        if mode == '0':
            player = Player()
        elif mode == '1':
            player = Agent()
            print("Agent is playing. Watch the moves!")
        else:
            print("You quit the game. Bye!")
            return
        attempt = "Y"
        while attempt.upper() == "Y":
            self.play_round(player)
            attempt = input("Do you want to try again? Type 'Y' to continue or 'N' to quit: ")
        print(f"\nYour final score is: {self.score}")

class Player:
    """
    Class representing a human player.
    """
    def make_guess(self, jumbled_word, anagrams=None):
        """
        Asks the human player for a guess.
        """
        return input().upper()

class Agent:
    """
    Class representing an AI agent player.
    """
    def make_guess(self, jumbled_word, anagrams):
        """
        Logic for the agent to unjumble the word using the pre-computed map.
        """
        print(f"Agent sees: {jumbled_word}")
        
        sorted_jumble = "".join(sorted(jumbled_word))
        guesses = anagrams.get(sorted_jumble, [""])
        if len(guesses) > 1:
            print(f"Agent found multiple possible words: {guesses} \nPicking randomly.")
        guess = guesses[randint(0, len(guesses) - 1)] if guesses else ""
        return guess

# Run the game
if __name__ == "__main__":
    game = WordJumbleGame()
    game.start()