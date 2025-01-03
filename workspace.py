from tkinter import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Function to render LaTeX
def render_latex(event=None):
    latex_text = entry.get()
    latex_text = f"${latex_text}$"
    
    fig.clear()
    ax = fig.add_subplot(111)
    try:
        ax.text(0.5, 0.5, latex_text, fontsize=20, ha='center', va='center')
        ax.axis('off')
        canvas.draw()
        error_label.config(text="")
    except Exception as e:
        error_label.config(text="Invalid LaTeX!", fg="red")

# Function to insert clicked LaTeX with placeholders
def insert_latex(text, event=None):
    entry.insert(tk.END, text[1:-1])
    render_latex(event)

# Function to dynamically create canvases that render LaTeX
def create_latex_buttons(event=None):
    a, b = "a", "b"
    # This can be expanded upon by adding more groups of symbols and functions
    symbolset = [
        [f"$\\sqrt{{{a}}}$",
         f"$\\sqrt[{{{a}}}]{{{b}}}$",
         f"${{{a}}}^{{{b}}}$"],
        [f"$\\frac{{{a}}}{{{b}}}$",
         f"$\\sum_{{{b}}}^{{{a}}}$",
         f"$\\int_{{{b}}}^{{{a}}}$"],
        [f"$\\alpha$",
         f"$\\beta$",
         f"$\\gamma$"]
        ]
    row = 0
    for symbols in symbolset:
        col = 0
        for symbol in symbols:
            f = plt.figure(figsize=(0.5, 0.5))
            c = FigureCanvasTkAgg(f, master=button_frame)
            a = f.add_subplot(111)
            a.text(0.5, 0.5, symbol, fontsize=10, ha='center', va='center')
            a.axis('off')
            c.draw()
            c.get_tk_widget().bind("<Button-1>", lambda event, s=symbol: insert_latex(s, event))
            c.get_tk_widget().grid(row=row, column=col, padx=5, pady=5)
            col += 1
        row += 1

# Create the main window
root = Tk()
root.title("LaTeX in Tkinter")
root.geometry("700x700")

# Create a frame for the input
frame = Frame(root)
frame.pack(pady=20)

# Entry widget for LaTeX input
entry = Entry(frame, width=50)
entry.pack(side=LEFT, padx=10)
entry.bind("<KeyRelease>", render_latex)

# Label to display errors
error_label = Label(frame, text="", fg="red")
error_label.pack(side=LEFT, padx=10)

# Create a figure for displaying LaTeX
fig = plt.figure(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Create a frame for the buttons
button_frame = Frame(root)
button_frame.pack(padx=10, pady=10)

# Create buttons
create_latex_buttons()

# Start the Tkinter main loop
root.mainloop()