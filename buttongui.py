import tkinter as tk
from PIL import Image, ImageTk

# ボタンクラス
class ESGButton(tk.Canvas):
    def __init__(self, master, size=(100, 50), text="", PIC=None,
                 shape="sqr", color=(200, 200, 200), command=None, **kwargs):
        width, height = size
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)

        self.command = command
        self.text = text
        self.shape = shape
        self.color = "#%02x%02x%02x" % color
        self.img = None

        # 図形を描画
        self._draw_shape(width, height)

        # テキストを描画
        if text:
            self.create_text(width // 2, height // 2, text=text, font=("Arial", 12))

        # 画像を追加
        if PIC:
            img = Image.open(PIC).resize((width, height))
            self.img = ImageTk.PhotoImage(img)
            self.create_image(width // 2, height // 2, image=self.img)

        # クリック時イベント
        self.bind("<Button-1>", self._on_click)

    def _draw_shape(self, width, height):
        if self.shape == "sqr":
            self.create_rectangle(0, 0, width, height, fill=self.color, outline="")
        elif self.shape == "csq":
            self.create_rectangle(0, 0, width, height, fill=self.color, outline="", width=2)
            self.create_oval(0, 0, width, height, outline="", width=0)  # 疑似的に角丸
        elif self.shape == "oval":
            self.create_oval(0, 0, width, height, fill=self.color, outline="")
        elif self.shape == "trg":
            self.create_polygon(width//2, 0, width, height, 0, height, fill=self.color, outline="")
        elif self.shape == "dtrg":
            self.create_polygon(0, 0, width, 0, width//2, height, fill=self.color, outline="")
        else:
            self.create_rectangle(0, 0, width, height, fill=self.color, outline="")

    def _on_click(self, event):
        if self.command:
            self.command()


# esg.btn 関数として提供
def btn(sw, size=(100, 50), text="", PIC=None, shape="sqr", color=(200, 200, 200), program=None):
    """
    sw : 親ウィンドウ (mainloopを持つtk.Tkやtk.Frame)
    size : (幅, 高さ)
    text : ボタンに表示する文字
    PIC : ボタンに使う画像のファイルパス
    shape : sqr, csq, oval, trg, dtrg
    color : (R,G,B)
    program : クリック時に実行する関数
    """
    b = ESGButton(sw, size=size, text=text, PIC=PIC, shape=shape, color=color, command=program)
    b.pack(padx=5, pady=5)
    return b
