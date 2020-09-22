def initialize_board_data(height, width):
    return [[{
        'x': i,
        'y': j,
        'cellState': None
    } for j in range(width)] for i in range(height)]


class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board_data = initialize_board_data(height, width)
        self.winner = None
        self.win_length = 5
        self.BLACK = '⚫'
        self.WHITE = '⚪'
        self.players = []
        self.first_player_turn = True

    def __repr__(self):
        return f'<Game: height {self.height}, width {self.width}>'

    def reset_game(self):
        self.board_data = initialize_board_data(self.height, self.width)
        self.winner = None
        self.first_player_turn = True

    def add_player(self, player_id):
        if len(self.players) < 2:
            self.players.append(player_id)
            return True
        return False

    def remove_player(self, player_id):
        self.players.remove(player_id)

    # Adds a stone of value "val" to position (x, y),
    # assuming it is empty and valid
    def make_play(self, x, y, player_id):
        # Only allow play if game isn't over
        if self.winner is not None:
            return False

        # Only allow plays within the bounds of the board
        if x >= len(self.board_data) or y >= len(self.board_data[0]):
            return False

        # Check that the player is connected and playing at their turn
        if player_id not in self.players:
            return False

        player_index = self.players.index(player_id)
        if (self.first_player_turn and player_index == 1) or (
                not self.first_player_turn and player_index == 0):
            return False

        val = self.BLACK if self.first_player_turn else self.WHITE

        if self.board_data[x][y]['cellState'] is None:
            self.board_data[x][y]['cellState'] = val
            self.check_game_over(x, y, val, player_id)
            self.first_player_turn = not self.first_player_turn
            return True

        # Don't do anything if the desired position already has a played value
        return False

    # Checks if the game is over after a stone is played at position (x, y)
    def check_game_over(self, x, y, val, player_id):
        # Check for bounds
        if x > len(self.board_data) or y > len(self.board_data[x]):
            return

        if self.check_vertical(x, y, val):
            self.winner = player_id
            return

        if self.check_horizontal(x, y, val):
            self.winner = player_id
            return

        if self.check_diagonal(x, y, val):
            self.winner = player_id
            return

    # Checks for a vertical line of 5 stones
    def check_vertical(self, x, y, val):
        data = self.board_data
        win_length = self.win_length
        # Iterate through possible "beginning" options
        for outer_offset in range(win_length):
            i = x - outer_offset
            num_hits = 0
            for inner_offset in range(win_length):
                i_off = i + inner_offset
                if i_off < len(data) and data[i_off][y]['cellState'] == val:
                    num_hits += 1
            if num_hits == win_length:
                return True

        return False

    # Checks for a vertical line of 5 stones
    def check_horizontal(self, x, y, val):
        data = self.board_data
        win_length = self.win_length
        # Iterate through possible "beginning" options
        for outer_offset in range(win_length):
            j = y - outer_offset
            num_hits = 0
            for inner_offset in range(win_length):
                j_off = j + inner_offset
                if j_off < len(data[x]) and data[x][j_off]['cellState'] == val:
                    num_hits += 1
            if num_hits == win_length:
                return True

        return False

    # Checks for a diagonal line of 5 stones
    def check_diagonal(self, x, y, val):
        data = self.board_data
        win_length = self.win_length
        # Check diagonal from NW to SE
        for outer_offset in range(win_length):
            i = x - outer_offset
            j = y - outer_offset
            num_hits = 0
            for inner_offset in range(win_length):
                i_off = i + inner_offset
                j_off = j + inner_offset
                if i_off < len(data) and j_off < len(data[i_off]) and \
                        data[i_off][j_off]['cellState'] == val:
                    num_hits += 1
            if num_hits == win_length:
                return True

        # Check diagonal from SW to NE
        for outer_offset in range(win_length):
            i = x + outer_offset
            j = y - outer_offset
            num_hits = 0
            for inner_offset in range(win_length):
                i_off = i - inner_offset
                j_off = j + inner_offset
                if i_off < len(data) and j_off < len(data[i_off]) and \
                        data[i_off][j_off]['cellState'] == val:
                    num_hits += 1
            if num_hits == win_length:
                return True

        return False
