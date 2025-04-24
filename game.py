import random
import time
import json
from abc import ABC, abstractmethod
from datetime import datetime


class Ship:
    def __init__(self, name, length, orientation, start_coord):
        self._name = name
        self._length = length
        self._orientation = orientation
        self._start_coord = start_coord
        self._hits = set()

    @property
    def coordinates(self):
        row, col = self._start_coord
        return [(row + i, col) if self._orientation == 'V' else (row, col + i) for i in range(self._length)]

    def is_hit(self, coord):
        if coord in self.coordinates:
            self._hits.add(coord)
            return True
        return False

    def is_sunk(self):
        return set(self.coordinates) == self._hits


class Board:
    def __init__(self, hide_ships=False):
        self._grid = [['~'] * 10 for _ in range(10)]
        self._ships = []
        self._hide_ships = hide_ships

    def is_valid_position(self, ship):
        for r, c in ship.coordinates:
            if not (0 <= r < 10 and 0 <= c < 10):
                return False
            if self._grid[r][c] != '~':
                return False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 10 and 0 <= nc < 10:
                        if self._grid[nr][nc] != '~':
                            return False
        return True

    def place_ship(self, ship):
        if self.is_valid_position(ship):
            for r, c in ship.coordinates:
                self._grid[r][c] = 'O'
            self._ships.append(ship)
            return True
        return False

    def receive_shot(self, coord):
        row, col = coord
        for ship in self._ships:
            if ship.is_hit(coord):
                self._grid[row][col] = 'X'
                if ship.is_sunk():
                    for r, c in ship.coordinates:
                        self._grid[r][c] = '#'
                    return "Sunk"
                return "Hit"
        self._grid[row][col] = '.'
        return "Miss"

    def display(self):
        print("  " + " ".join("ABCDEFGHIJ"))
        for i, row in enumerate(self._grid):
            display_row = []
            for cell in row:
                if self._hide_ships and cell == 'O':
                    display_row.append('~')
                else:
                    display_row.append(cell)
            print(f"{i} " + " ".join(display_row))

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self._ships)


class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.opponent_board = Board(hide_ships=True)

    @abstractmethod
    def make_move(self, opponent):
        pass

    def place_all_ships(self):
        ship_data = [
            ("Battleship", 4, 1),
            ("Cruiser", 3, 2),
            ("Destroyer", 2, 3),
            ("Submarine", 1, 4),
        ]
        for name, size, count in ship_data:
            for _ in range(count):
                placed = False
                while not placed:
                    orientation = random.choice(['H', 'V'])
                    row = random.randint(0, 9)
                    col = random.randint(0, 9)
                    ship = Ship(name, size, orientation, (row, col))
                    if self.board.place_ship(ship):
                        placed = True


class HumanPlayer(Player):
    def make_move(self, opponent):
        while True:
            try:
                user_input = input(
                    f"{self.name}, enter your move (e.g., A5): ").upper()
                if len(user_input) < 2 or user_input[0] not in "ABCDEFGHIJ":
                    raise ValueError("Invalid format.")
                col = ord(user_input[0]) - ord('A')
                row = int(user_input[1:])
                if not (0 <= row < 10 and 0 <= col < 10):
                    raise ValueError("Out of bounds.")
                if self.opponent_board._grid[row][col] in ('X', '.', '#'):
                    raise ValueError("You already shot there.")
                result = opponent.board.receive_shot((row, col))
                self.opponent_board._grid[row][col] = opponent.board._grid[row][col]
                print(f"Result of your shot: {result}")
                return (row, col, result)
            except Exception as e:
                print(f"Error: {e}. Try again.")


class ComputerPlayer(Player):
    def __init__(self, name="Computer"):
        super().__init__(name)
        self._shots_fired = set()

    def make_move(self, opponent):
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if (row, col) not in self._shots_fired:
                self._shots_fired.add((row, col))
                result = opponent.board.receive_shot((row, col))
                self.opponent_board._grid[row][col] = opponent.board._grid[row][col]
                print(f"{self.name} fires at {chr(col + 65)}{row}: {result}")
                return (row, col, result)


class GameHistory:
    def __init__(self):
        self.moves = []
        self.start_time = datetime.now()
        self.end_time = None
        self.winner = None

    def record_move(self, player_name, coord, result):
        row, col = coord
        move_entry = {
            "player": player_name,
            "coord": f"{chr(col + 65)}{row}",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.moves.append(move_entry)

    def end_game(self, winner_name):
        self.end_time = datetime.now()
        self.winner = winner_name

    def save_to_file(self, filename="game_history.json"):
        game_data = {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "winner": self.winner,
            "moves": self.moves
        }
        try:
            with open(filename, 'a') as f:
                f.write(json.dumps(game_data) + "\n")
            print("Game saved to history.")
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def show_stats(filename="game_history.json"):
        try:
            with open(filename, 'r') as f:
                games = [json.loads(line.strip()) for line in f]
                for i, game in enumerate(games):
                    print(f"\nGame {i+1}:")
                    print(f"  Start: {game['start_time']}")
                    print(f"  End: {game['end_time']}")
                    print(f"  Winner: {game['winner']}")
                    total_moves = len(game['moves'])
                    hits = sum(1 for m in game['moves']
                               if m['result'] in ("Hit", "Sunk"))
                    hit_pct = (hits / total_moves) * 100 if total_moves else 0
                    print(f"  Moves: {total_moves}, Hit Rate: {hit_pct:.1f}%")
        except FileNotFoundError:
            print("No history found.")


class Game:
    def __init__(self):
        self.player = HumanPlayer("You")
        self.computer = ComputerPlayer()
        self.history = GameHistory()

    def setup_game(self):
        print("Placing your ships...")
        self.player.place_all_ships()
        print("Placing computer ships...")
        self.computer.place_all_ships()

    def play(self):
        current_player = self.player
        opponent = self.computer

        while True:
            print("\n" * 5)
            print("Your Board:")
            self.player.board.display()
            print("\nEnemy Board:")
            self.player.opponent_board.display()

            row, col, result = current_player.make_move(opponent)
            self.history.record_move(current_player.name, (row, col), result)

            if opponent.board.all_ships_sunk():
                print(f"\n{current_player.name} wins!")
                self.history.end_game(current_player.name)
                self.history.save_to_file()
                break

            if result in ("Miss",):
                current_player, opponent = opponent, current_player
                time.sleep(2)
            else:
                print(f"{current_player.name} gets another turn!")
                time.sleep(2)


def main():
    while True:
        print("\n--- Battleship Menu ---")
        print("1. New Game")
        print("2. View Game Stats")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            game = Game()
            game.setup_game()
            game.play()
        elif choice == '2':
            GameHistory.show_stats()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
