# Battleship Game in Python
Quick game project for my university

# Battleship - Game Specifications

## Game Objective
- Sink all of the opponent's (computer's) ships by guessing their positions on the board
- Accomplish this before the computer sinks all of your ships

## Game Rules
- The game is played on two 10x10 boards (one for the player and one for the computer)
- Each player has a fleet consisting of:
  * 1 battleship (occupies 4 squares)
  * 2 cruisers (each occupies 3 squares)
  * 3 destroyers (each occupies 2 squares)
  * 4 submarines (each occupies 1 square)
- Ships must be placed horizontally or vertically (not diagonally)
- Ships cannot touch each other on any side or corner
- Players take turns firing shots, trying to hit the opponent's ships
- After hitting an opponent's ship, the player gets an additional move
- The game ends when all ships of one player are sunk

## Game Mechanics
- **Two 10x10 boards** - one for the player's ships, one for the computer's ships
- **Turn-based system** - players make moves alternately, with a bonus for hitting
- **Ship visibility** - the player only sees their own ships and hit areas on the opponent's board
- **Hit system** - marking hits and misses on the board
- **Sinking verification** - checking if an entire ship has been sunk
- **Computer strategy** - random shot selection (in the simple version) or intelligent targeting system after the first hit
- **Game history recording** - saving all moves, hits, and sinks to a file

## Program Structure
- **Object-oriented programming** - using classes to represent game elements
- **Basic classes**:
  * `Board` - representation of the game board
  * `Ship` - class storing information about a ship (position, length, status)
  * `Player` - abstract base class for players
- **Inheritance**:
  * `HumanPlayer` - derived class handling human player moves
  * `ComputerPlayer` - derived class implementing computer AI
- **Encapsulation** - hiding internal class data and providing access through methods
- **Polymorphism** - different implementations of methods (e.g., `make_move()`) in derived classes
- **Game history** - `GameHistory` class for recording and saving game progress

## Game History Functionality
- Saving the entire game progress to a text file
- Recording all moves made (coordinates, shot result)
- Saving game duration and final result
- Option to browse historical games and statistics (e.g., hit percentage)
- Ability to continue a saved game

## Python Elements Used
- Two-dimensional (nested) lists for board representation
- Dictionaries for storing ship information
- Functions for organizing code and game logic
- `while` loop for game flow control
- Conditional statements `if/elif/else`
- Random selection (`random.randint()`, `random.choice()`)
- User input handling (`input()`)
- Input data validation
- String manipulation and text formatting
- List operations (adding, checking contents)
- File operations (opening, writing, reading)
- Classes and inheritance (object-oriented programming)
- Exception handling (`try/except`)
- `datetime` module for time recording

## Interface
- Text-based, relying on console messages
- Two boards displayed side by side or one below the other
- Board markings:
  * `~` - water (empty field)
  * `O` - player's ship
  * `X` - hit
  * `.` - miss (shot in water)
  * `#` - sunk ship
- Coordinates marked with numbers and letters for easy field selection
- Messages about hits, misses, and sinkings
- Game result information
- Menu with options for new game, loading a saved game, and viewing statistics
