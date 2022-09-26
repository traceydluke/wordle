# wordle.py
# Usage: python3 wordle.py

import json
import os.path
import random
from string import ascii_uppercase

from possible_answers import ANSWERS

with open(os.path.join(os.path.dirname(__file__), "words_dictionary.json"), "r") as f:
    VALID_WORDS = json.loads(f.read())
for word in ANSWERS:
    if word not in VALID_WORDS:
        VALID_WORDS[word] = 1


class ANSI:
    # ANSI escape codes (https://en.m.wikipedia.org/wiki/ANSI_escape_code#Colors)
    # 97 = "bright white" text, second number controls background color
    gray = "\033[97;100m"
    black = "\033[97;40m"
    yellow = "\033[97;43m"
    green = "\033[97;42m"
    reset = "\033[0m"


class Color:
    Gray = 0  # letter not yet guessed
    Black = 1  # letter not in the word
    Yellow = 2  # letter in the word but in the wrong position
    Green = 3  # letter in the right position

    ANSI_Map = {
        Gray: ANSI.gray,
        Black: ANSI.black,
        Yellow: ANSI.yellow,
        Green: ANSI.green,
    }


class Game:
    def __init__(self):
        self.solution = random.choice(ANSWERS)
        self.guesses = []
        self.guessColors = []
        self.allLetters = [Color.Gray for letter in ascii_uppercase]

    def isSolved(self):
        return len(self.guesses) > 0 and self.solution == self.guesses[-1].lower()

    def addGuess(self, guess):
        """
        Add a guess & update game state
        """
        # calculate colors & save
        self.guesses.append(guess)
        colorList = compareWords(self.solution, guess)
        self.guessColors.append(colorList)
        # update available letters
        for i, color in enumerate(colorList):
            letterIndex = ord(guess[i]) - ord("a")
            if self.allLetters[letterIndex] < color:
                self.allLetters[letterIndex] = color

    def show(self):
        """
        Print out game board (guess history + available letters)
        """
        for i, guess in enumerate(self.guesses):
            print(mapColors(guess.upper(), self.guessColors[i]))
        print()
        print(mapColors(ascii_uppercase, self.allLetters))
        print()

    def play(self):
        """
        Run the game!
        """
        self.show()
        for i in range(6):
            # get the user's guess
            validGuess = False
            while not validGuess:
                guess = input("Your guess: ").lower()
                if len(guess) != 5:
                    print("Guess must be 5 letters long, please try again")
                elif guess not in VALID_WORDS:
                    print("Word not in dictionary, please try again")
                else:
                    validGuess = True
            self.addGuess(guess)
            self.show()
            if self.solution == guess:
                break

        if self.isSolved():
            print(f"Correct! The word was {self.solution.upper()}\n")
        else:
            print(f"Sorry, the word was {self.solution.upper()}\n")


class Stats:
    def __init__(self):
        self.history = []
        self.numWins = 0
        self.currentStreak = 0
        self.maxStreak = 0
        self.histogram = {}
        for i in range(1, 7):
            self.histogram.setdefault(i, 0)

    def show(self):
        print(f"Played: {len(self.history)}")
        print("Win %: {:.1f}".format(100 * self.numWins / len(self.history)))
        print(f"Current streak: {self.currentStreak}")
        print(f"Max streak: {self.maxStreak}")
        print("Guess distribution:")
        for key, value in sorted(self.histogram.items()):
            print("{}: {}{}".format(key, "*" * value, value))

    def addGame(self, game):
        self.history.append(game)
        if game.isSolved():
            self.numWins += 1
            self.currentStreak += 1
            if self.currentStreak > self.maxStreak:
                self.maxStreak = self.currentStreak
            self.histogram[len(game.guesses)] += 1
        else:
            self.currentStreak = 0


def compareWords(solution, guess):
    """
    Compare arbitrary strings Wordle-style
    input: str solution, str guess
    output: list of ints (Color enums) indicating whether letters in guess are in solution
    """
    if len(solution) != len(guess):
        raise Exception("[compareWords] solution and guess have different lengths")
    output = [Color.Gray for chr in solution]
    # check for exact matches first since this can affect color choice for letters in the wrong spot
    remaining = ""
    for i in range(len(solution)):
        if solution[i] == guess[i]:
            output[i] = Color.Green
        else:
            remaining += solution[i]
    # determine yellow vs black color
    for i in range(len(solution)):
        if output[i] == Color.Gray:
            if guess[i] in remaining:
                output[i] = Color.Yellow
                remaining = remaining.replace(guess[i], "", 1)
            else:
                output[i] = Color.Black
    return output


def colorStr(text, colorEnum):
    """
    input: str text, Color/int colorEnum
    output: text with ANSI escape strings added for colored text
    """
    return Color.ANSI_Map[colorEnum] + text + ANSI.reset


def mapColors(text, colorList):
    """
    Map a list of colors onto characters in a string
    input: str text, array of Color enums/ints colorList
    output: str with colors applied to each character in the text string
    """
    return "".join([colorStr(text[i], color) for i, color in enumerate(colorList)])


def playGame():
    running = True
    stats = Stats()
    print("Welcome to PyWordle! Guess the secret 5-letter word!")
    while running:
        game = Game()
        game.play()
        stats.addGame(game)
        stats.show()
        running = input("Play again? Y/n: ").lower() in ["y", "yes"]
    print("Thanks for playing!")


if __name__ == "__main__":
    playGame()
