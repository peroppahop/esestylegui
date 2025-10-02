import tkinter as tk

# ウィンドウ管理用辞書
_windows = {}
_colormode = "defoltcolor"

# ====================================
# colormode 設定
# ====================================
def colormode(mode="defoltcolor"):
    """
    色モードを設定
    - 'rgb': (R,G,B) タプル
    - 'hex': '#RRGGBB' 文字列
    - 'defoltcolor': Tk標準色文字列
    """
    global _colormode
    if mode in ["rgb", "hex", "defoltcolor"]:
        _colormode = mode
    else:
        raise ValueError("colormodeは 'rgb' / 'hex' / 'defoltcolor' のみ対応")

def _convert_color(color):
    if _colormode == "rgb" and isinstance(color, tuple):
        return "#%02x%02x%02x" % color
    elif _colormode == "hex" and isinstance(color, str):
        return color
    elif _colormode == "defoltcolor" and isinstance(color, str):
        return color
    else:
        return "#ffffff"

def _darker_color(rgb, ratio=15/16):
    """RGBを指定比率で暗くする"""
    r, g, b = rgb
    r = int(r * ratio)
    g = int(g * ratio)
    b = int(b * ratio)
    return "#%02x%02x%02x" % (r, g, b)

# ====================================
# ウィンドウ作成
# ====================================
def cw(wkey="window1", wtitle="新しいウィンドウ",
       basecolor=(255,255,255), ctrlbar="on", wicon=None, tml=None):
    """
    ウィンドウを作成
    """
    if wkey in _windows:
        raise ValueError(f"{wkey} はすでに存在します")

    # tml が on の場合
    if tml == "on":
        basecolor = (255,255,255)
        ctrlbar = "og"

    # 色変換
    if isinstance(basecolor, tuple):
        base_hex = _convert_color(basecolor)
    else:
        base_hex = basecolor

    # 最初のウィンドウか Toplevelか
    root = tk.Toplevel() if _windows else tk.Tk()
    root.configure(bg=base_hex)

    # ウィンドウタイトル
    if ctrlbar != "off":
        root.title(wtitle)

    # アイコン設定
    if wicon:
        try:
            root.iconbitmap(wicon)
        except Exception as e:
            print(f"アイコン設定失敗: {e}")

    # ====================================
    # ctrlbar 処理
    # ====================================
    if ctrlbar == "off":
        root.overrideredirect(True)

    elif ctrlbar == "og":
        root.overrideredirect(True)

        # basecolorがtupleの場合、そのまま使う
        if isinstance(basecolor, tuple):
            titlebar_color = _darker_color(basecolor)
        else:
            # hex → rgb に変換
            bc = basecolor.lstrip("#")
            rgb = tuple(int(bc[i:i+2],16) for i in (0,2,4))
            titlebar_color = _darker_color(rgb)

        # メインフレーム
        main_frame = tk.Frame(root, bg=base_hex)
        main_frame.pack(fill="both", expand=True)

        # タイトルバー
        titlebar = tk.Frame(main_frame, bg=titlebar_color, height=40)
        titlebar.pack(fill="x", side="top")

        # タイトルラベル
        title_label = tk.Label(titlebar, text=wtitle, fg="white", bg=titlebar_color,
                               font=("Arial",12,"bold"))
        title_label.pack(side="left", padx=10)

        # 移動用関数
        def start_move(event):
            root._x = event.x
            root._y = event.y
        def do_move(event):
            x = root.winfo_pointerx() - root._x
            y = root.winfo_pointery() - root._y
            root.geometry(f"+{x}+{y}")
        titlebar.bind("<Button-1>", start_move)
        titlebar.bind("<B1-Motion>", do_move)

        # ボタン機能
        def minimize(): root.iconify()
        def maximize(): root.state("zoomed")
        def fullscreen(): root.attributes("-fullscreen", not root.attributes("-fullscreen"))
        def close(): root.destroy()

        for txt, cmd in [("−", minimize), ("□", maximize), ("⛶", fullscreen), ("❌", close)]:
            b = tk.Button(titlebar, text=txt, command=cmd,
                          bg="#666", fg="white", relief="flat",
                          width=4, height=1, font=("Arial",12,"bold"))
            b.pack(side="right", padx=2)

        # 内容フレーム
        content = tk.Frame(main_frame, bg=base_hex)
        content.pack(fill="both", expand=True)

    _windows[wkey] = root
    return root

# ====================================
# ウィンドウ表示
# ====================================
def showwindow(wkey="window1"):
    if wkey not in _windows:
        raise ValueError(f"ウィンドウ '{wkey}' は存在しません")
    _windows[wkey].mainloop()
