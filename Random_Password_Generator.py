import random
import string
import pyperclip
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, Checkbutton, Frame, messagebox, LabelFrame

# Setting up the GUI
root = Tk()
root.title("Advanced Password Generator")
root.geometry("800x600")
root.state('zoomed')  # Fullscreen mode

# Set up colors
bg_color = "#6A0DAD"  # Purple color
btn_color = "#A95CBB"  # Lighter purple for buttons
text_color = "#FFFFFF"  # White for text
highlight_color = "#DDA0E5"  # Highlight color for buttons
option_bg_color = "#E3A6D2"  # Original background for checkboxes

# Variables
password_var = StringVar()
password_length = IntVar(value=12)
include_lowercase = IntVar(value=0)
include_uppercase = IntVar(value=0)
include_numbers = IntVar(value=0)
include_specials = IntVar(value=0)

def generate_password():
    length = password_length.get()
    if length < 8 or length > 20:
        messagebox.showerror("Invalid Length", "Password length must be between 8 and 20 characters.")
        return

    # Read the checkbox states
    include_lower = include_lowercase.get()
    include_upper = include_uppercase.get()
    include_digits = include_numbers.get()
    include_symbols = include_specials.get()

    # Construct the character pool based on checkbox states
    characters = ''
    if include_lower: characters += string.ascii_lowercase
    if include_upper: characters += string.ascii_uppercase
    if include_digits: characters += string.digits
    if include_symbols: characters += string.punctuation

    if not characters:
        password_var.set("Select at least one character type.")
        return

    # Generate password
    password = []
    if include_lower: password.append(random.choice(string.ascii_lowercase))
    if include_upper: password.append(random.choice(string.ascii_uppercase))
    if include_digits: password.append(random.choice(string.digits))
    if include_symbols: password.append(random.choice(string.punctuation))

    # Fill the rest of the password length
    password += random.choices(characters, k=length - len(password))

    # Shuffle the password list to ensure randomness
    random.shuffle(password)

    # Convert list to string
    password_var.set(''.join(password))

def copy_to_clipboard():
    pyperclip.copy(password_var.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Frame for UI components
main_frame = Frame(root, bg=bg_color)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Header
header_frame = Frame(main_frame, bg=bg_color)
header_frame.pack(pady=10)
Label(header_frame, text="Random Password Generator", font=("Arial", 26, "bold"), bg=bg_color, fg=text_color).pack()

# Password Options Frame
options_frame = LabelFrame(main_frame, text="Password Options", bg=bg_color, fg=text_color, font=("Arial", 14, "bold"))
options_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Password Length Input
length_frame = Frame(options_frame, bg=bg_color)
length_frame.pack(pady=10, padx=10)
Label(length_frame, text="Password Length (8-20):", font=("Arial", 14, "bold"), bg=bg_color, fg=text_color).grid(row=0, column=0, padx=5)
Entry(length_frame, textvariable=password_length, font=("Arial", 12), justify="center", width=5).grid(row=0, column=1, padx=5)

# Character Options - Centered Checkbuttons
checkbutton_frame = Frame(options_frame, bg=bg_color)
checkbutton_frame.pack(pady=10, padx=10)

Label(checkbutton_frame, text="Include:", font=("Arial", 14, "bold"), bg=bg_color, fg=text_color).pack(pady=5)

# Function to create checkbuttons with improved decoration
def create_checkbutton(text, variable):
    check = Checkbutton(checkbutton_frame, text=text, variable=variable, bg=option_bg_color, fg=text_color,
                         font=("Arial", 12), activebackground=highlight_color, selectcolor=bg_color,
                         padx=10, pady=5)  # indicatoron is set to 0 to mimic button
    check.pack(anchor='w', padx=10, pady=5, fill='x')  # Fill the x-axis for better spacing

    # Function to change color on click
    def update_bg_color(var, chk):
        if var.get() == 1:  # If checked
            chk.config(bg=highlight_color)  # Highlight color
        else:  # If unchecked
            chk.config(bg=option_bg_color)  # Original background color

    # Initialize the background color based on the current variable state
    update_bg_color(variable, check)  # Set initial color based on state

    # Bind the variable to update background color on click
    variable.trace("w", lambda *args: update_bg_color(variable, check))

# Create check buttons
create_checkbutton("Lowercase", include_lowercase)
create_checkbutton("Uppercase", include_uppercase)
create_checkbutton("Numbers", include_numbers)
create_checkbutton("Special Characters", include_specials)

# Buttons
button_frame = Frame(main_frame, bg=bg_color)
button_frame.pack(pady=20)

def on_enter(e):
    e.widget['background'] = highlight_color  # Lighter highlight on hover

def on_leave(e):
    e.widget['background'] = btn_color  # Original button color

generate_button = Button(button_frame, text="Generate Password", command=generate_password, bg=btn_color, fg=text_color, font=("Arial", 14), padx=20, pady=10)
generate_button.grid(row=0, column=0, padx=20)
generate_button.bind("<Enter>", on_enter)
generate_button.bind("<Leave>", on_leave)

copy_button = Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg=btn_color, fg=text_color, font=("Arial", 14), padx=20, pady=10)
copy_button.grid(row=0, column=1, padx=20)
copy_button.bind("<Enter>", on_enter)
copy_button.bind("<Leave>", on_leave)

# Password Display
password_display_frame = Frame(main_frame, bg=bg_color)
password_display_frame.pack(pady=20)
Label(password_display_frame, textvariable=password_var, font=("Arial", 18), bg=bg_color, fg=text_color).pack()

# Run the application
root.mainloop()
