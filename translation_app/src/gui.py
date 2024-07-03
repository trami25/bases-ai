import tkinter as tk
from tkinter import messagebox
from app import translate_text_backend, translate_text_sr_to_en


def translate_text():
    source_text = source_text_entry.get("1.0", tk.END).strip()
    direction = direction_var.get()

    if not source_text:
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return
    if direction_var.get() == "en_to_sr":
        translated_text = translate_text_backend(source_text)
    else:
        translated_text = translate_text_sr_to_en(source_text)

    # Check if the translation contains unknown tokens
    if "<UNK>" in translated_text:
        messagebox.showinfo("Translation Warning", "Some words could not be translated.")

    target_text_entry.delete("1.0", tk.END)
    target_text_entry.insert(tk.END, translated_text)


app = tk.Tk()
app.title("Text Translation Application")
app.geometry("600x400")
app.configure(bg="#f0f0f0")

direction_var = tk.StringVar(value="en_to_sr")

title_label = tk.Label(app, text="Text Translation Application", font=("Helvetica", 16, "bold"), bg="#f0f0f0", pady=10)
title_label.grid(row=0, column=0, columnspan=3)

direction_label = tk.Label(app, text="Translation Direction", font=("Helvetica", 12), bg="#f0f0f0")
direction_label.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=(10, 5))

direction_menu = tk.OptionMenu(app, direction_var, "en_to_sr", "sr_to_en")
direction_menu.grid(row=1, column=1, padx=(10, 20), pady=(10, 5))

source_label = tk.Label(app, text="Source Text", font=("Helvetica", 12), bg="#f0f0f0")
source_label.grid(row=2, column=0, sticky="e", padx=(20, 10), pady=(10, 5))

source_text_entry = tk.Text(app, height=10, width=50, font=("Helvetica", 10))
source_text_entry.grid(row=2, column=1, padx=(10, 20), pady=(10, 5))

translate_button = tk.Button(app, text="Translate", command=translate_text, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
translate_button.grid(row=3, column=0, columnspan=3, pady=10)

target_label = tk.Label(app, text="Translated Text", font=("Helvetica", 12), bg="#f0f0f0")
target_label.grid(row=4, column=0, sticky="e", padx=(20, 10), pady=(5, 10))

target_text_entry = tk.Text(app, height=10, width=50, font=("Helvetica", 10))
target_text_entry.grid(row=4, column=1, padx=(10, 20), pady=(5, 10))

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=3)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(3, weight=1)

app.mainloop()