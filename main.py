import tkinter as tk
from MainWindow import MainWindow


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.pack()
    root.title("Партнёры ВостНИИ")
    root.geometry("1515x785")
    root.resizable(False, False)
    root.mainloop()
