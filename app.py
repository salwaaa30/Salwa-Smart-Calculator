import re
import tkinter as tk

from calculator import CalculationError, evaluate_expression, format_result


THEMES = {
    "dark": {
        "background": "#111820",
        "panel": "#19232d",
        "display": "#202d38",
        "text": "#f3f6f7",
        "muted": "#91a2ad",
        "button": "#293743",
        "operator": "#344957",
        "utility": "#26323b",
        "accent": "#87d7c3",
        "accent_text": "#10251f",
        "border": "#2b3943",
        "error": "#ff9c8d",
    },
    "light": {
        "background": "#edf2ef",
        "panel": "#ffffff",
        "display": "#f4f8f6",
        "text": "#1b2826",
        "muted": "#687a76",
        "button": "#e7eeea",
        "operator": "#dce9e4",
        "utility": "#e9eeeb",
        "accent": "#176e59",
        "accent_text": "#ffffff",
        "border": "#d5e0db",
        "error": "#b33d31",
    },
}


class SmartCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Salwa Smart Calculator")
        self.root.geometry("830x690")
        self.root.minsize(650, 590)
        self.root.configure(bg=THEMES["dark"]["background"])
        self.root.option_add("*Font", ("Segoe UI", 11))

        self.expression = tk.StringVar()
        self.preview = tk.StringVar(value="0")
        self.theme_name = "dark"
        self.history = []
        self.error_visible = False
        self.themed_widgets = []
        self.widget_roles = {}

        self._build_header()
        self._build_content()
        self._apply_theme()
        self.root.bind_all("<Key>", self._on_key)

    def _register(self, widget, role):
        self.themed_widgets.append((widget, role))
        self.widget_roles[widget] = role
        return widget

    def _build_header(self):
        header = self._register(tk.Frame(self.root, padx=26, pady=18), "background")
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        title = self._register(
            tk.Label(header, text="SALWA  /  CALCULATOR", font=("Segoe UI Semibold", 12)),
            "text",
        )
        title.grid(row=0, column=0, sticky="w")
        subtitle = self._register(
            tk.Label(header, text="Perhitungan harian, dibuat lebih sederhana", font=("Segoe UI", 9)),
            "muted",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(3, 0))

        self.theme_button = self._make_button(header, "Terang", "utility", self._toggle_theme)
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=(12, 0))

    def _build_content(self):
        content = self._register(tk.Frame(self.root, padx=22, pady=0), "background")
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=3, minsize=390)
        content.columnconfigure(1, weight=1, minsize=190)
        content.rowconfigure(0, weight=1)

        calculator = self._register(tk.Frame(content, padx=16, pady=16), "panel")
        calculator.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        calculator.columnconfigure(0, weight=1)
        calculator.rowconfigure(1, weight=1)

        display = self._register(tk.Frame(calculator, padx=18, pady=14), "display")
        display.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        display.columnconfigure(0, weight=1)
        expression_label = self._register(
            tk.Label(
                display,
                textvariable=self.expression,
                font=("Segoe UI", 13),
                anchor="e",
                height=1,
            ),
            "muted",
        )
        expression_label.grid(row=0, column=0, sticky="ew")
        self.preview_label = self._register(
            tk.Label(
                display,
                textvariable=self.preview,
                font=("Segoe UI Light", 34),
                anchor="e",
                height=1,
            ),
            "text",
        )
        self.preview_label.grid(row=1, column=0, sticky="ew", pady=(3, 0))

        keypad = self._register(tk.Frame(calculator), "panel")
        keypad.grid(row=1, column=0, sticky="nsew")
        for column in range(4):
            keypad.columnconfigure(column, weight=1, uniform="key")
        for row in range(6):
            keypad.rowconfigure(row, weight=1, uniform="key")

        keys = [
            (("C", "utility", self.clear_all), ("CE", "utility", self.clear_entry),
             ("⌫", "utility", self.backspace), ("÷", "operator", lambda: self.input("÷"))),
            (("√x", "operator", self.square_root), ("%", "operator", self.percent),
             ("xʸ", "operator", lambda: self.input("^")), ("×", "operator", lambda: self.input("×"))),
            (("7", "button", lambda: self.input("7")), ("8", "button", lambda: self.input("8")),
             ("9", "button", lambda: self.input("9")), ("−", "operator", lambda: self.input("-"))),
            (("4", "button", lambda: self.input("4")), ("5", "button", lambda: self.input("5")),
             ("6", "button", lambda: self.input("6")), ("+", "operator", lambda: self.input("+"))),
            (("1", "button", lambda: self.input("1")), ("2", "button", lambda: self.input("2")),
             ("3", "button", lambda: self.input("3")), ("(", "utility", self.parenthesis)),
            (("+/−", "utility", self.toggle_sign), ("0", "button", lambda: self.input("0")),
             (".", "button", lambda: self.input(".")), ("=", "accent", self.calculate)),
        ]
        for row_index, row in enumerate(keys):
            for column_index, (label, role, command) in enumerate(row):
                button = self._make_button(keypad, label, role, command)
                button.grid(row=row_index, column=column_index, sticky="nsew", padx=4, pady=4)

        history_panel = self._register(tk.Frame(content, padx=14, pady=16), "panel")
        history_panel.grid(row=0, column=1, sticky="nsew")
        history_panel.columnconfigure(0, weight=1)
        history_panel.rowconfigure(1, weight=1)

        history_heading = self._register(
            tk.Label(history_panel, text="RIWAYAT", font=("Segoe UI Semibold", 10)),
            "text",
        )
        history_heading.grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.history_list = self._register(
            tk.Listbox(
                history_panel,
                borderwidth=0,
                highlightthickness=0,
                activestyle="none",
                font=("Segoe UI", 10),
                selectmode=tk.SINGLE,
                exportselection=False,
            ),
            "listbox",
        )
        self.history_list.grid(row=1, column=0, sticky="nsew")
        self.history_list.bind("<<ListboxSelect>>", self._select_history)
        self.history_hint = self._register(
            tk.Label(history_panel, text="Hitungan terbaru tersimpan di sini", font=("Segoe UI", 8)),
            "muted",
        )
        self.history_hint.grid(row=2, column=0, sticky="w", pady=(10, 0))
        clear_history = self._make_button(history_panel, "Hapus riwayat", "utility", self.clear_history)
        clear_history.grid(row=3, column=0, sticky="ew", pady=(12, 0))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def _make_button(self, parent, label, role, command):
        button = self._register(
            tk.Button(
                parent,
                text=label,
                command=command,
                cursor="hand2",
                relief="flat",
                borderwidth=0,
                padx=8,
                pady=10,
                font=("Segoe UI Semibold", 11),
                takefocus=False,
            ),
            role,
        )
        return button

    def _apply_theme(self):
        colors = THEMES[self.theme_name]
        for widget, role in self.themed_widgets:
            if role == "listbox":
                widget.configure(
                    bg=colors["panel"],
                    fg=colors["text"],
                    selectbackground=colors["operator"],
                    selectforeground=colors["text"],
                )
                continue
            if role in ("text", "muted"):
                parent_role = self.widget_roles.get(widget.master, "background")
                background = colors.get(parent_role, colors["background"])
                foreground = colors[role]
            elif role == "accent":
                foreground = colors["accent_text"]
                background = colors["accent"]
            else:
                background = colors.get(role, colors["panel"])
                foreground = colors["text"]
            options = {"bg": background}
            if isinstance(widget, (tk.Label, tk.Button)):
                options["fg"] = foreground
            if isinstance(widget, tk.Button):
                options["activebackground"] = colors["accent"] if role == "accent" else colors["operator"]
                options["activeforeground"] = colors["accent_text"] if role == "accent" else colors["text"]
            widget.configure(**options)

        self.theme_button.configure(text="Gelap" if self.theme_name == "light" else "Terang")

    def _toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self._apply_theme()

    def _update_preview(self):
        expression = self.expression.get()
        self.error_visible = False
        if not expression:
            self.preview.set("0")
            self.preview_label.configure(fg=THEMES[self.theme_name]["text"])
            return
        try:
            value = evaluate_expression(expression)
            self.preview.set(format_result(value))
            self.preview_label.configure(fg=THEMES[self.theme_name]["text"])
        except CalculationError:
            self.preview.set("")

    def input(self, value):
        if self.error_visible:
            self.expression.set("")
            self.error_visible = False
        current = self.expression.get()
        if value in ("+", "-", "×", "÷", "^"):
            if not current and value not in ("-",):
                return
            if current.endswith(("+", "-", "×", "÷", "^")):
                current = current[:-1]
        if value == ".":
            token = re.search(r"(?:\d+\.?\d*|\.\d+)$", current)
            if token and "." in token.group(0):
                return
            if not current or current.endswith(("+", "-", "×", "÷", "^", "(")):
                value = "0."
        self.expression.set(current + value)
        self._update_preview()

    def clear_all(self):
        self.expression.set("")
        self.preview.set("0")
        self.error_visible = False
        self.preview_label.configure(fg=THEMES[self.theme_name]["text"])

    def clear_entry(self):
        current = self.expression.get()
        if not current:
            return
        if current.endswith(")"):
            depth = 0
            for index in range(len(current) - 1, -1, -1):
                if current[index] == ")":
                    depth += 1
                elif current[index] == "(":
                    depth -= 1
                    if depth == 0:
                        prefix = current[:index]
                        if prefix.endswith("sqrt"):
                            index -= 4
                        current = current[:index]
                        break
        else:
            match = re.search(r"(?:\d+\.?\d*|\.\d+)$", current)
            if match:
                current = current[:match.start()]
        self.expression.set(current)
        self._update_preview()

    def backspace(self):
        current = self.expression.get()
        if current.endswith("**"):
            current = current[:-2]
        else:
            current = current[:-1]
        self.expression.set(current)
        self._update_preview()

    def square_root(self):
        current = self.expression.get()
        if current and not current.endswith(("+", "-", "×", "÷", "^", ".")):
            self.expression.set("sqrt(" + current + ")")
            self._update_preview()

    def percent(self):
        current = self.expression.get()
        if not current:
            return
        match = re.search(r"(?:\d+\.?\d*|\.\d+)$", current)
        if match:
            try:
                value = float(match.group(0)) / 100
                replacement = format_result(value)
                self.expression.set(current[:match.start()] + replacement)
                self._update_preview()
            except ValueError:
                return
        elif not current.endswith(("+", "-", "×", "÷", "^")):
            try:
                value = evaluate_expression(current) / 100
                self.expression.set(format_result(value))
                self._update_preview()
            except CalculationError:
                return

    def toggle_sign(self):
        current = self.expression.get()
        if not current:
            self.expression.set("-")
        elif current.startswith("-") and current.count("(") == current.count(")"):
            self.expression.set(current[1:])
        else:
            self.expression.set("-({})".format(current))
        self._update_preview()

    def parenthesis(self):
        current = self.expression.get()
        if current.count("(") > current.count(")") and current and not current.endswith(("+", "-", "×", "÷", "^", "(")):
            self.expression.set(current + ")")
        else:
            prefix = "×" if current and (current[-1].isdigit() or current.endswith(")")) else ""
            self.expression.set(current + prefix + "(")
        self._update_preview()

    def calculate(self):
        current = self.expression.get()
        if not current:
            return
        try:
            result = format_result(evaluate_expression(current))
            self._add_history(current, result)
            self.expression.set(result)
            self.preview.set(result)
            self.preview_label.configure(fg=THEMES[self.theme_name]["text"])
            self.error_visible = False
        except CalculationError as error:
            self.preview.set(str(error))
            self.preview_label.configure(fg=THEMES[self.theme_name]["error"])
            self.error_visible = True

    def _add_history(self, expression, result):
        self.history.insert(0, (expression, result))
        self.history = self.history[:10]
        self._render_history()

    def _render_history(self):
        self.history_list.delete(0, tk.END)
        for expression, result in self.history:
            self.history_list.insert(tk.END, "{} = {}".format(expression, result))

    def _select_history(self, _event):
        selection = self.history_list.curselection()
        if selection:
            expression, result = self.history[selection[0]]
            self.expression.set(expression)
            self.preview.set(result)
            self.error_visible = False
            self.preview_label.configure(fg=THEMES[self.theme_name]["text"])

    def clear_history(self):
        self.history = []
        self._render_history()

    def _on_key(self, event):
        if event.keysym in ("Return", "KP_Enter", "equal"):
            self.calculate()
            return "break"
        if event.keysym == "BackSpace":
            self.backspace()
            return "break"
        if event.keysym == "Escape":
            self.clear_all()
            return "break"
        if event.char and event.char in "0123456789.+-*/%^()":
            translated = {"*": "×", "/": "÷"}.get(event.char, event.char)
            self.input(translated)
            return "break"
        return None


def main():
    root = tk.Tk()
    SmartCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()