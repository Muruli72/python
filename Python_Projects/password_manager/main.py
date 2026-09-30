from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']



    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(numbers) for _ in range(randint(2, 4))]
    password_numbers = [choice(symbols) for _ in range(randint(2, 4))]

    password_list= password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data={
         website:{
            "email": email,
            "password": password
         }
    }
    if website == "" or email == "" or password == "":
        messagebox.showerror("Error", "Please enter all fields")
    else:

        is_ok = messagebox.askokcancel(
            title="Confirm Details",
            message=(
                f"These are the details entered:\n\n"
                f"Website: {website}\n"
                f"Email: {email}\n"
                f"Password: {password}\n\n"
                f"Do you want to save them?"
)
        )
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.focus()
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas( width=200, height=200, bg="white")
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

#Lable
website_label=Label( text="Website", bg="white")
website_label.grid(row=1, column=0)
email_label=Label(text="Email", bg="white")
email_label.grid(row=2, column=0)
password_label=Label( text="Password", bg="white")
password_label.grid(row=3, column=0)

#entries
website_entry=Entry( width=35)
website_entry.grid(row=1, column=1,columnspan=2)
website_entry.focus()
email_entry=Entry( width=35)
email_entry.grid(row=2, column=1,columnspan=2)
email_entry.insert(0, "your_email@gmail.com")
password_entry=Entry( width=35)
password_entry.grid(row=3, column=1,columnspan=2)

#Buttons
generate_password_button=Button( text="Generate Password",command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add",command=save)
add_button.grid(row=4, column=1)

window.mainloop()
