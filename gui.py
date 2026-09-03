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
            self._show_setup()

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _label(self, parent, text, font=None, color=None, **kwargs):
        return tk.Label(parent, text=text,
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
        self.configure(bg=self.BG)

        # ---- sidebar
        sidebar = tk.Frame(self, bg=self.SURFACE, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🔐", font=("Segoe UI", 28),
                 bg=self.SURFACE, fg=self.ACCENT).pack(pady=(28, 4))
        tk.Label(sidebar, text="Vault", font=("Segoe UI Semibold", 16),
                 bg=self.SURFACE, fg=self.TEXT).pack(pady=(0, 28))

        def nav_btn(text, cmd):
            b = tk.Button(sidebar, text=text, command=cmd,
                          font=self.FONT_BODY, bg=self.SURFACE, fg=self.TEXT,
                          activebackground=self.ACCENT, activeforeground=self.TEXT,
                          relief="flat", padx=16, pady=10, anchor="w",
                          cursor="hand2", width=18)
            b.pack(fill="x", padx=8, pady=2)
            return b

        nav_btn("＋  Add Entry", self._show_add_dialog)
        nav_btn("🔑  Generator", self._show_generator)
        nav_btn("🔒  Lock Vault", self._lock)

        # ---- main area
        main = tk.Frame(self, bg=self.BG)
        main.pack(side="right", fill="both", expand=True)

        # search bar
        top = tk.Frame(main, bg=self.BG)
        top.pack(fill="x", padx=20, pady=(20, 8))
        tk.Label(top, text="Search:", font=self.FONT_BODY,
                 fg=self.TEXT_DIM, bg=self.BG).pack(side="left", padx=(0, 8))
        self._search_var = tk.StringVar()
        search = tk.Entry(top, textvariable=self._search_var, width=30,
                          font=self.FONT_BODY, bg=self.SURFACE, fg=self.TEXT,
                          insertbackground=self.TEXT, relief="flat", bd=6)
        search.pack(side="left")
        self._search_var.trace_add("write", lambda *_: self._refresh_table())

        # treeview table
        from tkinter import ttk
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=self.SURFACE, fieldbackground=self.SURFACE,
                        foreground=self.TEXT, rowheight=30, font=self.FONT_BODY,
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background=self.BG, foreground=self.TEXT_DIM,
                        font=self.FONT_HEAD, relief="flat")
        style.map("Treeview",
                  background=[("selected", self.ACCENT)],
                  foreground=[("selected", self.TEXT)])

        cols = ("Title", "Username")
        self._tree = ttk.Treeview(main, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=280)

        sb = ttk.Scrollbar(main, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 8))
        sb.pack(side="left", fill="y", pady=(0, 8), padx=(0, 20))
        self._tree.bind("<Double-1>", lambda _: self._show_detail())

        # action bar
        bar = tk.Frame(main, bg=self.BG)
        bar.pack(fill="x", padx=20, pady=(0, 16))
        self._btn(bar, "View / Edit", self._show_detail).pack(side="left", padx=(0, 8))
        self._btn(bar, "Copy Password", self._copy_password).pack(side="left", padx=(0, 8))
        self._btn(bar, "Delete", self._delete_entry, color=self.DANGER).pack(side="left")

        self._refresh_table()

    def _refresh_table(self):
        q = self._search_var.get().strip()
        all_entries = get_password(self.conn, self.fernet, None)
        if q:
            all_entries = [e for e in all_entries if q.lower() in e[1].lower()]
        self._tree.delete(*self._tree.get_children())
        for entry in all_entries:
            self._tree.insert("", "end", iid=str(entry[0]), values=(entry[1], entry[2]))

    def _selected_id(self):
        sel = self._tree.selection()
        return int(sel[0]) if sel else None

    def _copy_password(self):
        entry_id = self._selected_id()
        if not entry_id:
            messagebox.showinfo("Select entry", "Please select an entry first.")
            return
        entries = get_password(self.conn, self.fernet, None)
        for e in entries:
            if e[0] == entry_id:
                self.clipboard_clear()
                self.clipboard_append(e[3])
                messagebox.showinfo("Copied", "Password copied to clipboard!")
                return

    def _delete_entry(self):
        entry_id = self._selected_id()
        if not entry_id:
            messagebox.showinfo("Select entry", "Please select an entry first.")
            return
        if messagebox.askyesno("Delete", "Delete this entry permanently?"):
            delete_password(self.conn, self._tree.item(str(entry_id))["values"][0])
            self._refresh_table()

    def _show_detail(self):
        entry_id = self._selected_id()
        if not entry_id:
            messagebox.showinfo("Select entry", "Please select an entry first.")
            return
        self._show_add_dialog(entry_id)

    def _show_add_dialog(self, entry_id=None):
        existing = None
        if entry_id:
            entries = get_password(self.conn, self.fernet, None)
            for e in entries:
                if e[0] == entry_id:
                    existing = e
                    break

        dlg = tk.Toplevel(self)
        dlg.title("Edit Entry" if entry_id else "Add Entry")
        dlg.configure(bg=self.BG)
        dlg.geometry("420x340")
        dlg.resizable(False, False)
        dlg.grab_set()

        pad = dict(padx=24, pady=6)

        def row_label(text):
            tk.Label(dlg, text=text, font=self.FONT_BODY,
                     fg=self.TEXT_DIM, bg=self.BG, anchor="w").pack(fill="x", **pad)

        def row_entry(show=""):
            e = self._entry(dlg, show=show, width=40)
            e.pack(fill="x", **pad)
            return e

        row_label("Site / App")
        site_e = row_entry()

        row_label("Username / Email")
        user_e = row_entry()

        pw_frame = tk.Frame(dlg, bg=self.BG)
        pw_frame.pack(fill="x", padx=24, pady=6)
        tk.Label(pw_frame, text="Password", font=self.FONT_BODY,
                 fg=self.TEXT_DIM, bg=self.BG).pack(anchor="w")

        pw_inner = tk.Frame(pw_frame, bg=self.BG)
        pw_inner.pack(fill="x")
        pw_e = self._entry(pw_inner, show="●", width=30)
        pw_e.pack(side="left", fill="x", expand=True)

        def gen_pw():
            pw_e.config(show="")
            pw_e.delete(0, tk.END)
            pw_e.insert(0, generate_password(20))

        self._btn(pw_inner, "⟳", gen_pw, width=3).pack(side="left", padx=(6, 0))

        show_var = tk.BooleanVar(value=False)

        def toggle_show():
            pw_e.config(show="" if show_var.get() else "●")

        tk.Checkbutton(pw_inner, text="Show", variable=show_var, command=toggle_show,
                       bg=self.BG, fg=self.TEXT_DIM, selectcolor=self.SURFACE,
                       activebackground=self.BG, font=self.FONT_BODY).pack(side="left", padx=6)

        # pre-fill if editing
        if existing:
            site_e.insert(0, existing[1])
            user_e.insert(0, existing[2])
            pw_e.insert(0, existing[3])

        def save():
            site = site_e.get().strip()
            user = user_e.get().strip()
            pw = pw_e.get()

            if not site or not user or not pw:
                messagebox.showwarning("Missing fields", "Site, username and password are required.")
                return

            if entry_id:
                update_password(self.conn, self.fernet, entry_id, site, user, pw)
            else:
                try:
                    create_password(self.conn, self.fernet, site, user, pw)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    return

            self._refresh_table()
            dlg.destroy()

        self._btn(dlg, "Save Entry", save).pack(pady=(8, 0))

    def _show_generator(self):
        messagebox.showinfo("Coming soon", "Generator coming next!")

    def _lock(self):
        self.fernet = None
        self._show_unlock()

    def on_close(self):
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()