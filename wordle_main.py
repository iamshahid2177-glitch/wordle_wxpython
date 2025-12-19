import wx
import random

WORD_LIST = [
    "apple", "mango", "grape", "peach", "berry",
    "lemon", "melon", "plumb", "plaza", "charm",
    "flame", "brave", "crown", "sword", "ghost",
    "light", "storm", "cloud", "river", "stone",
    "metal", "eagle", "tiger", "shark", "whale",
    "zebra", "horse", "snake", "otter", "panda",
    "koala", "anger", "pride", "trust", "faith",
    "mercy", "glory", "honor", "peace", "smile",
    "grace"
]

ROWS = 6
COLS = 5

BG_DEFAULT = wx.Colour(211, 211, 211)
BG_CORRECT = wx.Colour(0, 160, 0)
BG_PRESENT = wx.Colour(218, 165, 32)
BG_ABSENT = wx.Colour(128, 128, 128)

#---------------------------------------------------------------------------------

class WordleFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Wordle - wxPython", size=(420, 520))

        self.word = random.choice(WORD_LIST)
        self.current_row = 0
        self.cells = []

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="WORDLE")
        title.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour("purple")
        main_sizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        grid_sizer = wx.GridSizer(ROWS, COLS, 10, 10)

        for r in range(ROWS):
            row = []
            for c in range(COLS):
                cell = wx.StaticText(
                    panel,
                    label="",
                    size=(55, 55),
                    style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE
                )
                cell.SetBackgroundColour(BG_DEFAULT)
                cell.SetFont(wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                row.append(cell)
                grid_sizer.Add(cell, 0, wx.EXPAND)
            self.cells.append(row)

        main_sizer.Add(grid_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 15)

        self.entry = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER | wx.TE_CENTER)
        self.entry.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.entry.Bind(wx.EVT_TEXT_ENTER, self.check_guess)
        main_sizer.Add(self.entry, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 40)

        self.status = wx.StaticText(panel, label="Enter a 5-letter word")
        main_sizer.Add(self.status, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        reset_btn = wx.Button(panel, label="Reset")
        reset_btn.Bind(wx.EVT_BUTTON, self.reset_game)
        btn_sizer.Add(reset_btn, 0, wx.RIGHT, 10)

        help_btn = wx.Button(panel, label="Help")
        help_btn.Bind(wx.EVT_BUTTON, self.show_help)
        btn_sizer.Add(help_btn, 0)

        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        panel.SetSizer(main_sizer)
        self.entry.SetFocus()
        self.Show()

    def check_guess(self, event):
        guess = self.entry.GetValue().lower()
        self.entry.Clear()

        if len(guess) != COLS or not guess.isalpha():
            self.status.SetLabel("Invalid input! Enter 5 letters.")
            return

        if self.current_row >= ROWS:
            return

#------------------------------------------------------------------------------

        for i in range(COLS):
            cell = self.cells[self.current_row][i]
            cell.SetLabel(guess[i].upper())

            if guess[i] == self.word[i]:
                cell.SetBackgroundColour(BG_CORRECT)
                cell.SetForegroundColour(wx.WHITE)
            elif guess[i] in self.word:
                cell.SetBackgroundColour(BG_PRESENT)
                cell.SetForegroundColour(wx.BLACK)
            else:
                cell.SetBackgroundColour(BG_ABSENT)
                cell.SetForegroundColour(wx.WHITE)

            cell.Refresh()

        if guess == self.word:
            self.status.SetLabel("🎉 You Win!")
            self.entry.Disable()
        else:
            self.current_row += 1
            if self.current_row == ROWS:
                self.status.SetLabel(f"Game Over! Word was {self.word.upper()}")
                self.entry.Disable()
            else:
                self.status.SetLabel("Try again!")

    def reset_game(self, event):
        self.word = random.choice(WORD_LIST)
        self.current_row = 0

        for r in range(ROWS):
            for c in range(COLS):
                cell = self.cells[r][c]
                cell.SetLabel("")
                cell.SetBackgroundColour(BG_DEFAULT)
                cell.SetForegroundColour(wx.BLACK)
                cell.Refresh()

        self.entry.Enable()
        self.entry.Clear()
        self.entry.SetFocus()
        self.status.SetLabel("New game! Enter a 5-letter word")

#-------------------------------------------------------------------------------------------

    def show_help(self, event):
        msg = (
            "Guess the hidden 5-letter word within 6 tries.\n\n"
            "Green  = correct letter, correct spot\n"
            "Gold   = letter in word, wrong spot\n"
            "Gray   = letter not in word\n\n"
            "Type your guess and press Enter."
        )
        wx.MessageBox(msg, "How to Play", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App(False)
    frame = WordleFrame()
    app.MainLoop()


#----------------------------------------------------------------------------------------------