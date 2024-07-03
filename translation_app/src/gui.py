import tkinter as tk
from tkinter import messagebox
from app import translate_text_backend, translate_text_sr_to_en

def translate_text():
    source_text = source_text_entry.get("1.0", tk.END).strip()
    direction = direction_var.get()

    if not source_text:
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return

    if direction == "en_to_sr":
        translated_text = translate_text_backend(source_text)
    else:
        translated_text = translate_text_sr_to_en(source_text)

    # Check if the translation contains unknown tokens
    if "<UNK>" in translated_text:
        messagebox.showinfo("Translation Warning", "Some words could not be translated.")

    target_text_entry.delete("1.0", tk.END)
    target_text_entry.insert(tk.END, translated_text)


# Main application window
app = tk.Tk()
app.title("Text Translation Application")
app.geometry("800x600")
app.configure(bg="#ffffff")


title_frame = tk.Frame(app, bg="#4CAF50", bd=2)
title_frame.pack(fill=tk.X)
title_label = tk.Label(title_frame, text="Text Translation Application", font=("Helvetica", 24, "bold"), bg="#4CAF50", fg="#ffffff", pady=10)
title_label.pack()


input_frame = tk.Frame(app, bg="#e0e0e0", pady=20)
input_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

direction_var = tk.StringVar(value="en_to_sr")

direction_label = tk.Label(input_frame, text="Translation Direction", font=("Helvetica", 14), bg="#e0e0e0")
direction_label.grid(row=0, column=0, sticky="e", padx=(20, 10), pady=(10, 10))

direction_menu = tk.OptionMenu(input_frame, direction_var, "en_to_sr", "sr_to_en")
direction_menu.config(font=("Helvetica", 12))
direction_menu.grid(row=0, column=1, padx=(10, 20), pady=(10, 10))

source_label = tk.Label(input_frame, text="Source Text", font=("Helvetica", 14), bg="#e0e0e0")
source_label.grid(row=1, column=0, sticky="ne", padx=(20, 10), pady=(10, 10))

source_text_entry = tk.Text(input_frame, height=10, width=50, font=("Helvetica", 12), wrap=tk.WORD, padx=10, pady=10, bd=2, relief=tk.SUNKEN)
source_text_entry.grid(row=1, column=1, padx=(10, 20), pady=(10, 10))

translate_button = tk.Button(input_frame, text="Translate", command=translate_text, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", padx=20, pady=10)
translate_button.grid(row=2, column=0, columnspan=2, pady=20)

target_label = tk.Label(input_frame, text="Translated Text", font=("Helvetica", 14), bg="#e0e0e0")
target_label.grid(row=3, column=0, sticky="ne", padx=(20, 10), pady=(10, 10))

target_text_entry = tk.Text(input_frame, height=10, width=50, font=("Helvetica", 12), wrap=tk.WORD, padx=10, pady=10, bd=2, relief=tk.SUNKEN)
target_text_entry.grid(row=3, column=1, padx=(10, 20), pady=(10, 10))

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(3, weight=1)

app.mainloop()
