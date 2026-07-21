import tkinter as tk
from tkinter import messagebox
import getpass
import sqlite3

from db import get_conn, setup_db, create_password, get_password, update_password, delete_password
from crypto_utils import init_master, unlock_vault
from generator import generate_password


class PasswordManagerApp(tk.Tk):
    # Design Tokens
    BG        = "#1C1C2E"
    SURFACE   = "#2A2A40"
    ACCENT    = "#7C5CBF"
    ACCENT_LT = "#9B7FD4"
    TEXT      = "#E8E6F0"
    TEXT_DIM  = "#8A88A0"
    DANGER    = "#E05A5A"
    SUCCESS   = "#5ABE8A"
    FONT_BODY  = ("Segoe UI", 10)
    FONT_HEAD  = ("Segoe UI Semibold", 11)
    FONT_TITLE = ("Segoe UI Light", 22)
    FONT_MONO  = ("Consolas", 10)

    def __init__(self):
        super().__init__()
        self.conn = get_conn()
        setup_db(self.conn)
        self.fernet = None

        self.title("Password Manager")
        self.geometry("860x580")
        self.resizable(True, True)
        self.configure(bg=self.BG)

        vault_exists = self.conn.execute("SELECT COUNT(*) FROM master").fetchone()[0] > 0
        if vault_exists:
            self._show_unlock()
        else:
            self._show_setup

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _label(self, parebt, text, font=None, color=None, **kwargs):
        return tk.Label(parebt, text=text,
            font=font or self.FONT_BODY,
            fg=color or self.TEXT, bg=self.BG, **kwargs)

    def _entry(self, parent, show="", width=30):
        return tk.Entry(parent, show=show, width=width,
            font=self.FONT_BODY,
            bg=self.SURFACE, fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat", bd=6)

    def _btn(self, parent, text, cmd, color=None, **kwargs):
        c = color or self.ACCENT
        return tk.Button(parent, text=text, command=cmd,
            font=self.FONT_HEAD,
            bg=c, fg=self.TEXT,
            activebackground=self.ACCENT_LT, activeforeground=self.TEXT,
            relief="flat", padx=14, pady=6, cursor="hand2", **kwargs)

    def _show_setup(self):
        self._clear()
        frame = tk.Frame(self, bg=self.BG)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self._label(frame, "🔐 Password Manager", font=self.FONT_TITLE).pack(pady=(0, 4))
        self._label(frame, "Create your master password to get started.",
                    color=self.TEXT_DIM).pack(pady=(0, 24))

        self._label(frame, "Master Password").pack(anchor="w")
        pw1 = self._entry(frame, show="●", width=36)
        pw1.pack(pady=(2, 12))
        pw1.focus()

        self._label(frame, "Confirm Password").pack(anchor="w")
        pw2 = self._entry(frame, show="●", width=36)
        pw2.pack(pady=(2, 20))

        def create():
            p1, p2 = pw1.get(), pw2.get()
            if not p1:
                messagebox.showwarning("Required", "Please enter a master password.")
                return
            if p1 != p2:
                messagebox.showerror("Mismatch", "Passwords do not match.")
                return
            if len(p1) < 8:
                messagebox.showwarning("Too short", "Master password must be at least 8 characters.")
                return
            self.fernet = init_master(self.conn, p1)
            self._show_vault()

        pw2.bind("<Return>", lambda _: create())
        self._btn(frame, "Create Vault", create, width=34).pack()

    def _show_unlock(self):
        self._clear()
        frame = tk.Frame(self, bg=self.BG)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self._label(frame, "🔐 Password Manager", font=self.FONT_TITLE).pack(pady=(0, 4))
        self._label(frame, "Enter your master password to unlock.",
                    color=self.TEXT_DIM).pack(pady=(0, 24))

        self._label(frame, "Master Password").pack(anchor="w")
        pw = self._entry(frame, show="●", width=36)
        pw.pack(pady=(2, 20))
        pw.focus()

        err_var = tk.StringVar()
        tk.Label(frame, textvariable=err_var, fg=self.DANGER,
                 bg=self.BG, font=self.FONT_BODY).pack(pady=(0, 8))

        def unlock(event=None):
            try:
                self.fernet = unlock_vault(self.conn, pw.get())
                self._show_vault()
            except RuntimeError as e:
                err_var.set(str(e))
                pw.delete(0, tk.END)

        pw.bind("<Return>", unlock)
        self._btn(frame, "Unlock", unlock, width=34).pack()

    def _show_vault(self):
        self._clear()
        self._label(self, "Vault — coming next!", font=self.FONT_TITLE).pack(pady=40)

    def on_close(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()