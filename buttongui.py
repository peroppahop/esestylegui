import tkinter as tk
from PIL import Image, ImageTk

_buttons = {}

def btn(sw="window1", size=(80,30), text="ボタン", PIC=None,
        shape="sqr", color=(200,200,200), command=None):
    """
    カスタムボタンを作成する
    sw      : 親ウィンドウのキー
    size    : (幅, 高さ)
    text    : 表示文字列
    PIC     : 画像ファイルパス
    shape   : sqr, csq, oval, trg, dtrg
    color   : (R,G,B)
    command : クリック時に呼び出す関数
    """
    from .maingui import _windows  # maingui のウィンドウ辞書を利用

    if sw not in _windows:
        raise ValueError(f"ウィンドウ '{sw}' が存在しません")

    root = _windows[sw]
    w, h = size
    hexcolor = "#%02x%02x%02x" % color

    canvas = tk.Canvas(root, width=w, height=h, bg=root["bg"], highlightthickness=0)
    canvas.pack(pady=5)

    # ボタン形状を描画
    if shape == "sqr":
        shape_id = canvas.create_rectangle(0, 0, w, h, fill=hexcolor, outline="")
    elif shape == "csq":
        shape_id = canvas.create_rectangle(2, 2, w-2, h-2, fill=hexcolor, outline="", width=3)
    elif shape == "oval":
        shape_id = canvas.create_oval(0, 0, w, h, fill=hexcolor, outline="")
    elif shape == "trg":
        shape_id = canvas.create_polygon(w/2, 0, w, h, 0, h, fill=hexcolor, outline="")
    elif shape == "dtrg":
        shape_id = canvas.create_polygon(0, 0, w, 0, w/2, h, fill=hexcolor, outline="")
    else:
        shape_id = canvas.create_rectangle(0, 0, w, h, fill=hexcolor, outline="")

    # 画像 or テキスト
    if PIC:
        try:
            img = Image.open(PIC).resize((w, h))
            img_tk = ImageTk.PhotoImage(img)
            canvas.image = img_tk
            canvas.create_image(w/2, h/2, image=img_tk)
        except Exception as e:
            print(f"画像読み込み失敗: {e}")
    else:
        canvas.create_text(w/2, h/2, text=text, fill="black", font=("Arial", 12))

    # クリックイベント
    def on_click(event=None):
        if command:
            command()

    canvas.tag_bind(shape_id, "<Button-1>", on_click)
    canvas.bind("<Button-1>", on_click)

    _buttons[text] = canvas
    return canvas
