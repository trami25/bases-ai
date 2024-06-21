import tkinter as tk
from tkinter import messagebox
from app import translate_text_backend

def translate_text():
    source_text = source_text_entry.get("1.0", tk.END).strip()
    if not source_text:
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return


    translated_text = translate_text_backend(source_text)

    target_text_entry.delete("1.0", tk.END)
    target_text_entry.insert(tk.END, translated_text)

app = tk.Tk()
app.title("Text Translation Application")

tk.Label(app, text="Source Text").pack()
source_text_entry = tk.Text(app, height=10, width=50)
source_text_entry.pack()

tk.Button(app, text="Translate", command=translate_text).pack()

tk.Label(app, text="Translated Text").pack()
target_text_entry = tk.Text(app, height=10, width=50)
target_text_entry.pack()

app.mainloop()
