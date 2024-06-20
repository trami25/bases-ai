import tkinter as tk
from tkinter import messagebox
import requests

def translate_text():
    source_text = source_text_entry.get("1.0", tk.END).strip()
    if not source_text:
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return

    response = requests.post('http://127.0.0.1:5000/translate', json={'text': source_text})
    if response.status_code == 200:
        translated_text = response.json().get('translated_text', 'Translation failed.')
        target_text_entry.delete("1.0", tk.END)
        target_text_entry.insert(tk.END, translated_text)
    else:
        messagebox.showerror("Translation Error", "Failed to get translation.")

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
