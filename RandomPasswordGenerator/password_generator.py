
import tkinter as tk
from tkinter import messagebox
import random
import string
import re
import platform


C = {
    "bg":         "#0A0E1A",
    "surface":    "#111827",
    "surface2":   "#1A2235",
    "border":     "#1E2D45",
    "border2":    "#2A3F5F",
    "violet":     "#7C3AED",
    "violet_lt":  "#A855F7",
    "violet_dim": "#2D1B69",
    "mint":       "#10D9A0",
    "amber":      "#F59E0B",
    "rose":       "#F43F5E",
    "sky":        "#38BDF8",
    "text":       "#F1F5F9",
    "text2":      "#94A3B8",
    "text3":      "#475569",
    "white":      "#FFFFFF",
}


_OS = platform.system()


if _OS == "Windows":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

if _OS == "Windows":
    F_DISPLAY  = ("Trebuchet MS", 22, "bold")
    F_TITLE    = ("Trebuchet MS", 13, "bold")
    F_SUBTITLE = ("Trebuchet MS", 9)
    F_LABEL    = ("Trebuchet MS", 10, "bold")
    F_SUBLABEL = ("Trebuchet MS", 9)
    F_MONO     = ("Consolas",     15, "bold")
    F_MONO_SM  = ("Consolas",     10)
    F_BTN      = ("Trebuchet MS", 11, "bold")
    F_BADGE    = ("Consolas",     13, "bold")
elif _OS == "Darwin":
    F_DISPLAY  = ("Helvetica Neue", 22, "bold")
    F_TITLE    = ("Helvetica Neue", 13, "bold")
    F_SUBTITLE = ("Helvetica Neue", 9)
    F_LABEL    = ("Helvetica Neue", 10, "bold")
    F_SUBLABEL = ("Helvetica Neue", 9)
    F_MONO     = ("Menlo",          15, "bold")
    F_MONO_SM  = ("Menlo",          10)
    F_BTN      = ("Helvetica Neue", 11, "bold")
    F_BADGE    = ("Menlo",          13, "bold")
else:
    F_DISPLAY  = ("DejaVu Sans",       21, "bold")
    F_TITLE    = ("DejaVu Sans",       12, "bold")
    F_SUBTITLE = ("DejaVu Sans",       9)
    F_LABEL    = ("DejaVu Sans",       10, "bold")
    F_SUBLABEL = ("DejaVu Sans",       9)
    F_MONO     = ("DejaVu Sans Mono",  14, "bold")
    F_MONO_SM  = ("DejaVu Sans Mono",  10)
    F_BTN      = ("DejaVu Sans",       11, "bold")
    F_BADGE    = ("DejaVu Sans Mono",  13, "bold")



class ToggleSwitch(tk.Canvas):
    W, H, PAD = 46, 24, 3

    def __init__(self, parent, variable, command=None, **kw):
        super().__init__(parent, width=self.W, height=self.H,
                         bg=C["surface"], highlightthickness=0, bd=0, **kw)
        self._var  = variable
        self._cmd  = command
        self._busy = False
        self._tx   = self._off_x()
        self.bind("<Button-1>", self._click)
        self._draw()

    def _off_x(self): return self.PAD + (self.H - 2*self.PAD)//2
    def _on_x(self):  return self.W - self.PAD - (self.H - 2*self.PAD)//2

    def _draw(self):
        self.delete("all")
        on  = self._var.get()
        clr = C["violet"] if on else C["border2"]
        r   = self.H // 2
        self.create_oval(0, 0, r*2, self.H, fill=clr, outline="")
        self.create_oval(self.W-r*2, 0, self.W, self.H, fill=clr, outline="")
        self.create_rectangle(r, 0, self.W-r, self.H, fill=clr, outline="")
        tr = r - self.PAD
        tx = self._tx
        self.create_oval(tx-tr, self.PAD, tx+tr, self.H-self.PAD,
                         fill=C["white"], outline="")

    def _click(self, _=None):
        if self._busy: return
        self._var.set(not self._var.get())
        tgt = self._on_x() if self._var.get() else self._off_x()
        self._anim(tgt)
        if self._cmd: self._cmd()

    def _anim(self, tgt):
        self._busy = True
        step = 3 if tgt > self._tx else -3
        self._tx += step
        self._draw()
        if abs(self._tx - tgt) > abs(step):
            self.after(12, lambda: self._anim(tgt))
        else:
            self._tx = tgt; self._draw(); self._busy = False



class PillButton(tk.Canvas):
    def __init__(self, parent, text, cmd, bg, fg, hover,
                 w=130, h=42, font=None, **kw):
        super().__init__(parent, width=w, height=h,
                         bg=parent["bg"], highlightthickness=0, bd=0, **kw)
        self._t=text; self._cmd=cmd; self._bg=bg
        self._fg=fg; self._hv=hover; self._width=w; self._height=h
        self._font=font or F_BTN
        self._paint(bg)
        self.bind("<Enter>",    lambda _: self._paint(self._hv))
        self.bind("<Leave>",    lambda _: self._paint(self._bg))
        self.bind("<Button-1>", lambda _: self._cmd())

    def _paint(self, bg):
        self.delete("all")
        r = self._height // 2
        self.create_oval(0, 0, r*2, self._height, fill=bg, outline="")
        self.create_oval(self._width-r*2, 0, self._width, self._height, fill=bg, outline="")
        self.create_rectangle(r, 0, self._width-r, self._height, fill=bg, outline="")
        self.create_text(self._width//2, self._height//2,
                         text=self._t, fill=self._fg, font=self._font)



class StrengthBar(tk.Canvas):
    N=4; GAP=6; H=10

    def __init__(self, parent, **kw):
        super().__init__(parent, height=self.H,
                         bg=C["surface"], highlightthickness=0, bd=0, **kw)
        self._score = 0
        self._COLS  = [C["rose"], C["amber"], C["violet_lt"], C["mint"]]
        self.bind("<Configure>", lambda _: self._draw())

    def set(self, score):
        self._score = score
        self._draw()

    def _draw(self):
        self.update_idletasks()
        self.delete("all")
        W = self.winfo_width()
        if W < 10: return
        sw = (W - (self.N-1)*self.GAP) // self.N
        filled = int(self._score / 25)
        for i in range(self.N):
            x1 = i*(sw+self.GAP); x2 = x1+sw
            clr = self._COLS[min(i,3)] if i < filled else C["border"]
            r = self.H//2
            self.create_oval(x1, 0, x1+r*2, self.H, fill=clr, outline="")
            self.create_oval(x2-r*2, 0, x2, self.H, fill=clr, outline="")
            self.create_rectangle(x1+r, 0, x2-r, self.H, fill=clr, outline="")



def generate_password(length, upper, lower, digits, symbols, exclude=""):
    cs = ""
    if upper:   cs += string.ascii_uppercase
    if lower:   cs += string.ascii_lowercase
    if digits:  cs += string.digits
    if symbols: cs += string.punctuation
    for ch in exclude: cs = cs.replace(ch, "")

    if not cs:       return None, "Select at least one character type."
    if length < 4:   return None, "Minimum password length is 4."
    if length > 128: return None, "Maximum password length is 128."

    sure = []
    for pool_src, active in [
        (string.ascii_uppercase, upper),
        (string.ascii_lowercase, lower),
        (string.digits,          digits),
        (string.punctuation,     symbols)
    ]:
        if active:
            p = "".join(c for c in pool_src if c not in exclude)
            if p: sure.append(random.choice(p))

    rest = [random.choice(cs) for _ in range(length - len(sure))]
    pw = sure + rest
    random.shuffle(pw)
    return "".join(pw), None


def score_password(pw):
    if not pw: return 0, "", C["text3"]
    s, n = 0, len(pw)
    if n >= 8:  s += 20
    if n >= 12: s += 15
    if n >= 16: s += 15
    if re.search(r'[A-Z]', pw):        s += 10
    if re.search(r'[a-z]', pw):        s += 10
    if re.search(r'\d',    pw):        s += 10
    if re.search(r'[^A-Za-z0-9]', pw): s += 15
    s += int(len(set(pw))/n * 5)
    s = min(s, 100)
    if s < 25: return s, "Weak",        C["rose"]
    if s < 50: return s, "Fair",        C["amber"]
    if s < 75: return s, "Strong",      C["violet_lt"]
    return s,   "Very Strong",          C["mint"]



class App(tk.Tk):
    PAD = 24

    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.configure(bg=C["bg"])

        self.len_var    = tk.IntVar(value=16)
        self.upper_var  = tk.BooleanVar(value=True)
        self.lower_var  = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.sym_var    = tk.BooleanVar(value=False)
        self.excl_var   = tk.StringVar(value="")
        self.pass_var   = tk.StringVar(value="")
        self._raw       = ""
        self._show      = True

        self._build_ui()
        self._generate()

        self.update_idletasks()
        W = self.winfo_reqwidth()
        H = self.winfo_reqheight()
        SW = self.winfo_screenwidth()
        SH = self.winfo_screenheight()
        
        
        x = max(0, (SW - W) // 2)
        y = max(0, (SH - H) // 2)
        
        self.geometry(f"{W}x{H}+{x}+{y}")
        self.resizable(False, False)

    
    def _build_ui(self):
        self._mk_header()
        self._mk_pw_card()
        self._mk_controls()
        self._mk_buttons()
        self._mk_statusbar()

    
    def _mk_header(self):
        hf = tk.Frame(self, bg=C["bg"])
        hf.pack(fill="x", padx=self.PAD, pady=(20, 0))

        
        badge = tk.Frame(hf, bg=C["violet_dim"], width=52, height=52)
        badge.pack_propagate(False)
        badge.pack(side="left")
        tk.Label(badge, text="🔐", font=("Segoe UI Emoji", 22),
                 bg=C["violet_dim"]).place(relx=0.5, rely=0.5, anchor="center")

        right = tk.Frame(hf, bg=C["bg"])
        right.pack(side="left", padx=(14, 0))
        tk.Label(right, text="Password Generator",
                 font=F_DISPLAY, bg=C["bg"], fg=C["text"]).pack(anchor="w")
        tk.Label(right, text="Secure  ·  Customisable  ·  Instant",
                 font=F_SUBTITLE, bg=C["bg"], fg=C["text3"]).pack(anchor="w")

        
        tk.Frame(self, bg=C["violet"], height=2).pack(
            fill="x", padx=self.PAD, pady=(10, 0))

    
    def _mk_pw_card(self):
        wrap = tk.Frame(self, bg=C["border2"], padx=1, pady=1)
        wrap.pack(fill="x", padx=self.PAD, pady=(15, 0))

        card = tk.Frame(wrap, bg=C["surface"], padx=20, pady=20)
        card.pack(fill="x")

        
        top = tk.Frame(card, bg=C["surface"])
        top.pack(fill="x")
        tk.Label(top, text="GENERATED PASSWORD", font=F_SUBLABEL,
                 bg=C["surface"], fg=C["text3"]).pack(side="left")

        self._eye = tk.Label(top, text="  👁  Show", font=F_SUBLABEL,
                             bg=C["surface"], fg=C["text3"], cursor="hand2")
        self._eye.pack(side="right")
        self._eye.bind("<Button-1>", self._toggle_vis)

        
        box = tk.Frame(card, bg=C["surface2"],
                       highlightthickness=1, highlightbackground=C["border2"])
        box.pack(fill="x", pady=(10, 0))

        self._pw_disp = tk.Label(
            box, textvariable=self.pass_var,
            font=F_MONO, bg=C["surface2"], fg=C["violet_lt"],
            anchor="w", wraplength=360, justify="left",
            padx=16, pady=16
        )
        self._pw_disp.pack(fill="x")

        
        srow = tk.Frame(card, bg=C["surface"])
        srow.pack(fill="x", pady=(14, 0))

        self._str_lbl   = tk.Label(srow, text="", font=F_LABEL,
                                   bg=C["surface"], fg=C["text3"])
        self._str_lbl.pack(side="left")

        self._score_lbl = tk.Label(srow, text="", font=F_SUBLABEL,
                                   bg=C["surface"], fg=C["text3"])
        self._score_lbl.pack(side="right")

        self._bar = StrengthBar(card)
        self._bar.pack(fill="x", pady=(6, 0))

    
    def _mk_controls(self):
        wrap = tk.Frame(self, bg=C["border"], padx=1, pady=1)
        wrap.pack(fill="x", padx=self.PAD, pady=(15, 0))

        card = tk.Frame(wrap, bg=C["surface"], padx=20, pady=22)
        card.pack(fill="x")

        
        self._sec(card, "PASSWORD LENGTH")

        len_row = tk.Frame(card, bg=C["surface"])
        len_row.pack(fill="x", pady=(10, 0))

        self._badge = tk.Label(len_row, text=str(self.len_var.get()),
                               font=F_BADGE, bg=C["violet"],
                               fg=C["white"], width=4, pady=5)
        self._badge.pack(side="right")

        sf = tk.Frame(len_row, bg=C["surface"])
        sf.pack(side="left", fill="x", expand=True, padx=(0, 12))

        tk.Scale(sf, from_=4, to=64, orient="horizontal",
                 variable=self.len_var,
                 bg=C["surface"], fg=C["violet_lt"],
                 troughcolor=C["border2"], activebackground=C["violet"],
                 highlightthickness=0, bd=0, sliderrelief="flat",
                 showvalue=False, command=self._on_len, length=290
                 ).pack(fill="x")

        
        pr = tk.Frame(card, bg=C["surface"])
        pr.pack(fill="x", pady=(10, 18))
        tk.Label(pr, text="Quick:", font=F_SUBLABEL,
                 bg=C["surface"], fg=C["text3"]).pack(side="left", padx=(0, 8))
        for v in (8, 12, 16, 24, 32):
            tk.Button(pr, text=str(v), font=F_SUBLABEL,
                      bg=C["surface2"], fg=C["text2"],
                      activebackground=C["violet"], activeforeground=C["white"],
                      relief="flat", cursor="hand2", width=4, pady=5,
                      command=lambda x=v: self._set_len(x)
                      ).pack(side="left", padx=3)

        
        tk.Frame(card, bg=C["border"], height=1).pack(fill="x", pady=(0, 15))

        
        self._sec(card, "CHARACTER TYPES")

        for label, var in [
            ("Uppercase  A–Z",  self.upper_var),
            ("Lowercase  a–z",  self.lower_var),
            ("Digits      0–9", self.digits_var),
            ("Symbols  !@#$",   self.sym_var),
        ]:
            row = tk.Frame(card, bg=C["surface"])
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label, font=F_LABEL,
                     bg=C["surface"], fg=C["text2"]).pack(side="left")
            ToggleSwitch(row, variable=var, command=self._generate
                         ).pack(side="right")

        
        tk.Frame(card, bg=C["border"], height=1).pack(fill="x", pady=(12, 12))

        
        self._sec(card, "EXCLUDE CHARACTERS  (optional)")
        excl_wrap = tk.Frame(card, bg=C["surface2"],
                             highlightthickness=1, highlightbackground=C["border2"])
        excl_wrap.pack(fill="x", pady=(8, 0))
        tk.Entry(excl_wrap, textvariable=self.excl_var,
                 font=F_MONO_SM, bg=C["surface2"], fg=C["text"],
                 insertbackground=C["violet_lt"],
                 relief="flat", bd=10).pack(fill="x")

    
    def _mk_buttons(self):
        bf = tk.Frame(self, bg=C["bg"])
        bf.pack(fill="x", padx=self.PAD, pady=(15, 0))

        PillButton(bf, "⚡  GENERATE", self._generate,
                   C["violet"], C["white"], C["violet_lt"],
                   w=168, h=44).pack(side="left", padx=(0, 10))

        PillButton(bf, "📋  COPY", self._copy,
                   C["surface2"], C["text"], C["border2"],
                   w=124, h=44).pack(side="left", padx=(0, 10))

        PillButton(bf, "🗑  CLEAR", self._clear,
                   C["surface2"], C["text3"], "#2A1020",
                   w=118, h=44).pack(side="left")

    
    def _mk_statusbar(self):
        self._sv = tk.StringVar(value="Ready — press Generate to begin")
        bar = tk.Frame(self, bg=C["surface"])
        bar.pack(fill="x", pady=(15, 0), side="bottom")

        self._dot = tk.Frame(bar, bg=C["violet"], width=4)
        self._dot.pack(side="left", fill="y", padx=(0, 14))

        tk.Label(bar, textvariable=self._sv, font=F_SUBLABEL,
                 bg=C["surface"], fg=C["text2"],
                 anchor="w", pady=10).pack(side="left", fill="x")

    def _sec(self, parent, text):
        tk.Label(parent, text=text, font=F_SUBLABEL,
                 bg=C["surface"], fg=C["text3"]).pack(anchor="w")

      
    def _on_len(self, val):
        self._badge.config(text=str(int(float(val))))
        self._generate()

    def _set_len(self, v):
        self.len_var.set(v)
        self._badge.config(text=str(v))
        self._generate()

    def _generate(self, *_):
        pw, err = generate_password(
            self.len_var.get(),
            self.upper_var.get(), self.lower_var.get(),
            self.digits_var.get(), self.sym_var.get(),
            self.excl_var.get()
        )
        if err:
            messagebox.showwarning("Input Error", err, parent=self)
            return
        self._raw = pw
        self.pass_var.set(pw if self._show else "●" * len(pw))
        sc, lbl, clr = score_password(pw)
        self._bar.set(sc)
        self._str_lbl.config(text=lbl, fg=clr)
        self._score_lbl.config(text=f"{sc} / 100", fg=clr)
        self._status(f"✔  Generated  ·  {len(pw)} characters", C["mint"])

    def _toggle_vis(self, _=None):
        self._show = not self._show
        self.pass_var.set(self._raw if self._show else "●"*len(self._raw))
        self._eye.config(
            text="  👁  Show" if self._show else "  🙈 Hide",
            fg=C["text3"] if self._show else C["violet_lt"]
        )

    def _copy(self):
        if not self._raw:
            self._status("⚠  Nothing to copy yet", C["amber"]); return
        try:
            import pyperclip; pyperclip.copy(self._raw)
        except Exception:
            self.clipboard_clear(); self.clipboard_append(self._raw)
        self._status("📋  Copied to clipboard!", C["sky"])

    def _clear(self):
        self._raw = ""
        self.pass_var.set("")
        self._bar.set(0)
        self._str_lbl.config(text="", fg=C["text3"])
        self._score_lbl.config(text="", fg=C["text3"])
        self._status("Cleared.", C["text3"])

    def _status(self, msg, clr=None):
        self._sv.set(msg)
        if clr: self._dot.config(bg=clr)


if __name__ == "__main__":
    App().mainloop()
