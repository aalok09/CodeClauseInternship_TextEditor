import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap="word", undo=True)
        self.text_area.pack(fill="both", expand=True)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Insert Image", command=self.insert_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_editor)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.edit_menu.add_command(label="Clear All", command=self.clear_all)

        self.theme_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Theme", menu=self.theme_menu)
        self.theme_menu.add_command(label="Day", command=self.set_day_theme)
        self.theme_menu.add_command(label="Night", command=self.set_night_theme)

        self.status_bar = tk.Label(self.root, text="Word Count: 0")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.text_area.bind("<KeyRelease>", self.update_word_count)

        self.set_day_theme()

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)

    def save_file(self):
        if not hasattr(self, 'file_path'):
            self.save_file_as()
        else:
            content = self.text_area.get(1.0, tk.END)
            with open(self.file_path, "w") as file:
                file.write(content)

    def save_file_as(self):
        content = self.text_area.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            self.file_path = file_path

    def exit_editor(self):
        self.root.destroy()

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def select_all(self):
        self.text_area.tag_add("sel", "1.0", "end")

    def clear_all(self):
        self.text_area.delete(1.0, tk.END)

    def update_word_count(self, event=None):
        content = self.text_area.get(1.0, tk.END)
        words = content.split()
        word_count = len(words)
        self.status_bar.config(text=f"Word Count: {word_count}")

    def set_day_theme(self):
        self.root.configure(bg="white")
        self.text_area.configure(bg="white", fg="black")
        self.status_bar.configure(bg="white", fg="black")

    def set_night_theme(self):
        self.root.configure(bg="black")
        self.text_area.configure(bg="black", fg="white")
        self.status_bar.configure(bg="black", fg="white")

    def insert_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            image = tk.PhotoImage(file=file_path)
            self.text_area.image_create(tk.END, image=image)
            self.text_area.insert(tk.END, "\n")  # Add a newline after the image

def main():
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
