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
        self.BLACK = '⚫'
        self.WHITE = '⚪'
        self.winner = None
        self.win_length = 5

    def __repr__(self):
        return f'<Game: height {self.height}, width {self.width}>'

    # Adds a stone of value "val" to position (x, y),
    # assuming it is empty and valid
    def make_play(self, x, y, val):
        # Only allow play if game isn't over
        if self.winner is not None:
            return False

        # Only allow plays within the bounds of the board
        if x >= len(self.board_data) or y >= len(self.board_data[0]):
            return False

        # Only allow black or white values to be played
        if val != self.BLACK and val != self.WHITE:
            return False

        if self.board_data[x][y]['cellState'] is None:
            self.board_data[x][y]['cellState'] = val
            self.check_game_over(x, y, val)
            return True

        # Don't do anything if the desired position already has a played value
        return False

    # Checks if the game is over after a stone is played at position (x, y)
    def check_game_over(self, x, y, val):
        # Check for bounds
        if x > len(self.board_data) or y > len(self.board_data[0]):
            return

        if self.check_vertical(x, y, val):
            self.winner = val
            return

        if self.check_horizontal(x, y, val):
            self.winner = val
            return

        if self.check_diagonal(x, y, val):
            self.winner = val
            return

    # Checks for a vertical line of 5 stones
    def check_vertical(self, x, y, val):
        data = self.board_data
        win_length = self.win_length
        # Iterate through possible "beginning" options
        for outer_offset in range(win_length):
            i = x - outer_offset
            num_hits = 0
            print('i', i)
            for inner_offset in range(win_length):
                i_off = i + inner_offset
                print('i off', i_off)
                print('data', data[i_off][y])
                if i_off < len(data) and data[i_off][y]['cellState'] == val:
                    print(i_off, y, data[i_off][y])
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
        win_length  = self.win_length
        # Check diagonal from NW to SE
        for outer_offset in range(win_length):
            i = x - outer_offset
            j = y - outer_offset
            num_hits = 0
            for inner_offset in range(win_length):
                i_off = i + inner_offset
                j_off = j + inner_offset
                if i_off < len(data) and j_off < len(data[i_off]) and data[i_off][j_off]['cellState'] == val:
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
                if i_off < len(data) and j_off < len(data[i_off]) and data[i_off][j_off]['cellState'] == val:
                    num_hits += 1
            if num_hits == win_length:
                return True

        return False