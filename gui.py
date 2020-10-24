import boardgame
import tkinter as tk


class GUI:
    selected_piece = None
    focused = None
    images = {}
    color1 = "#DDB88C"
    color2 = "#A66D4F"
    highlightcolor = "khaki"
    rows = 20
    columns = 20
    dim_square = 32

    def __init__(self, parent, chessboard):
        self.chessboard = chessboard
        self.parent = parent
        # Adding Top Menu
        self.menubar = tk.Menu(parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Game", command=self.new_game)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.parent.config(menu=self.menubar)

        # Adding Frame
        self.btmfrm = tk.Frame(parent, height=64)
        self.info_label = tk.Label(self.btmfrm,
                                text="   Black to Start the Game  ",
                                fg=self.color2)
        self.info_label.pack(side=tk.RIGHT, padx=8, pady=5)
        self.btmfrm.pack(fill="x", side=tk.BOTTOM)

        canvas_width = self.columns * self.dim_square
        canvas_height = self.rows * self.dim_square
        self.canvas = tk.Canvas(parent, width=canvas_width,
                               height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.canvas.bind("<Button-1>", self.square_clicked)

    def new_game(self):
        self.chessboard.init_board()
        self.draw_board()
        self.draw_pieces()
        self.info_label.config(text="   Black to Start the Game  ", fg='red')

    def square_clicked(self, event):
        if self.chessboard.get_game_state() in ['BLACK_WON','WHITE_WON']:
            return

        col_size = row_size = self.dim_square
        selected_column = int(event.x / col_size)
        selected_row = int(event.y / row_size)

        if self.selected_piece:
            if self.selected_piece != (selected_row, selected_column):
                self.move(self.selected_piece, (selected_row, selected_column))
            self.selected_piece = None
            self.focused = None
            self.draw_board()
            self.draw_pieces()
        else:
            self.focus(selected_row, selected_column)
            self.draw_board()

    def move(self, p1, p2):
        move_result = self.chessboard.make_move(p1, p2, 1)
        turn = 'Black' if self.chessboard.get_turn() == 'x' else 'White'
        color = 'White' if self.chessboard.get_turn() == 'x' else 'Black'
        pos1 = chr(p1[1]+65) + str(20-p1[0])
        pos2 = chr(p2[1]+65) + str(20-p2[0])

        if self.chessboard.get_game_state() == 'WHITE_WON':
            self.info_label['text'] = f'{color} : {pos1}->{pos2}    White won!'
            self.info_label['fg'] = 'black'
        elif self.chessboard.get_game_state() == 'BLACK_WON':
            self.info_label['text'] = f'{color} : {pos1}->{pos2}    Black won!'
            self.info_label['fg'] = 'black'
        elif move_result:
            self.info_label['text'] = f'{color} : {pos1}->{pos2}    {turn}\'s turn'

    def focus(self, row, col):
        board = self.chessboard.get_board()
        piece = board[row][col]
        footprint, footprint_none = self.chessboard.make_footprint(board, row, col)
        if (footprint, footprint_none) != ([-1], [-1]) and len(footprint) > 0:
            self.selected_piece = (row, col)
            # import pdb; pdb.set_trace()
            self.focused = self.chessboard.moves_available(row, col)

    def draw_board(self):
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.dim_square)
                y1 = ((19 - row) * self.dim_square)
                x2 = x1 + self.dim_square
                y2 = y1 + self.dim_square
                if (self.focused is not None and (19-row, col) in self.focused):
                    self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=self.highlightcolor,
                                                 tags="area")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color1 if row*col*(row-19)*(col-19) == 0 else self.color2,
                                                 tags="area")
        self.canvas.tag_raise("occupied")
        self.canvas.tag_lower("area")

    def draw_pieces(self):
        self.canvas.delete("occupied")
        board = self.chessboard.get_board()
        for y, row in enumerate(board):
            for x, piece in enumerate(row):
                if piece == 'x':
                    filename = 'pieces_image/black.png'
                elif piece == 'o':
                    filename = 'pieces_image/white.png'
                else:
                    continue
                piecename = "%s%s%s" % (piece, str(x).zfill(2), str(y).zfill(2))
                if filename not in self.images:
                    self.images[filename] = tk.PhotoImage(file=filename)
                self.canvas.create_image(0, 0, image=self.images[filename],
                                         tags=(piecename, "occupied"),
                                         anchor="c")
                y0 = (y * self.dim_square) + int(self.dim_square / 2)
                x0 = (x * self.dim_square) + int(self.dim_square / 2)
                self.canvas.coords(piecename, x0, y0)


def main(chessboard):
    root = tk.Tk()
    root.title("Chess")
    gui = GUI(root, chessboard)
    gui.draw_board()
    gui.draw_pieces()
    root.mainloop()


if __name__ == "__main__":
    game = boardgame.GessGame()
    main(game)
