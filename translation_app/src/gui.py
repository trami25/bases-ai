import tkinter as tk
from tkinter import messagebox
from app import translate_text_backend

def translate_text():
    source_text = source_text_entry.get("1.0", tk.END).strip()
    if not source_text:
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return

    translated_text = translate_text_backend(source_text)

    # Check if the translation contains unknown tokens
    if "<UNK>" in translated_text:
        messagebox.showinfo("Translation Warning", "Some words could not be translated.")

    target_text_entry.delete("1.0", tk.END)
    target_text_entry.insert(tk.END, translated_text)


app = tk.Tk()
app.title("Text Translation Application")
app.geometry("600x400")
app.configure(bg="#f0f0f0")

title_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 10)

title_label = tk.Label(app, text="Text Translation Application", font=title_font, bg="#f0f0f0", pady=10)
title_label.grid(row=0, column=0, columnspan=2)

source_label = tk.Label(app, text="Source Text", font=label_font, bg="#f0f0f0")
source_label.grid(row=1, column=0, sticky="e", padx=(20, 10), pady=(10, 5))

source_text_entry = tk.Text(app, height=10, width=50, font=entry_font)
source_text_entry.grid(row=1, column=1, padx=(10, 20), pady=(10, 5))

translate_button = tk.Button(app, text="Translate", command=translate_text, font=label_font, bg="#4CAF50", fg="white",
                             padx=20, pady=5)
translate_button.grid(row=2, column=0, columnspan=2, pady=10)

target_label = tk.Label(app, text="Translated Text", font=label_font, bg="#f0f0f0")
target_label.grid(row=3, column=0, sticky="e", padx=(20, 10), pady=(5, 10))

target_text_entry = tk.Text(app, height=10, width=50, font=entry_font)
target_text_entry.grid(row=3, column=1, padx=(10, 20), pady=(5, 10))

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=3)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(3, weight=1)

app.mainloop()
