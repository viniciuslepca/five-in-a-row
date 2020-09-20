def initialize_board_data(height, width):
    return [[{
        'x': i,
        'y': j,
        'value': None
    } for j in range(width)] for i in range(height)]


class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board_data = initialize_board_data(height, width)

    def __repr__(self):
        return f'<Game: height {self.height}, width {self.width}>'

    def make_play(self, x, y, val):
        if x > len(self.board_data) or y > len(self.board_data[0]):
            return False

        if val != 'b' and val != 'w':
            return False

        if self.board_data[x][y] is None:
            self.board_data[x][y] = val
            return True

        return False