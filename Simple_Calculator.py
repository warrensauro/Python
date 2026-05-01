import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("320x480")

entry = tk.Entry(root, font=24, justify="right")
entry.grid(row=0,column=0, columnspan=4, sticky="nsew", padx=10,pady=20)

def on_click(button_text):
    current = entry.get()
    if button_text == "=":
        try:
            entry.delete(0, tk.END)
            entry.insert(tk.END, eval(current))
        except Exception:
            messagebox.showerror("Error", "Invalid Input")
            entry.delete(0, tk.END)
    elif button_text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, button_text)

buttons = [
    'C', '(', ')', '/',
     '7', '8', '9', '*',
     '4', '5', '6', '-',
     '1', '2', '3', '+',
     '0', '.', '='
]

for i in range(5): root.grid_rowconfigure(i, weight=1)
for i in range(4): root.grid_columnconfigure(i, weight=1)

row, col = 1, 0
for btn in buttons:
    if btn == "=":
        tk.Button(root, font=14,text=btn, command=lambda x=btn: on_click(x)).grid(row=row, column=col, columnspan=2,sticky="nsew", padx=2, pady=2)
        col += 2
    else:
        tk.Button(root, font=14,text=btn, command=lambda x=btn: on_click(x)).grid(row=row, column=col,sticky="nsew", padx=2, pady=2)
        col += 1
    if col > 3:
        col = 0
        row +=1
root.mainloop()