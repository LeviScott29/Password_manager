from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json

letters = []
numbers = []
punctuations = ["#", "%", "!", "$"]

for i in string.digits:
    numbers.append(i)
for i in string.ascii_letters:
    letters.append(i)

# ---------------------------- SEARCH FUNCTION------------------------------- #
def search():
    entry = text_web.get()
    try:
        with open("database.json", "r") as file:
            read = json.load(file)
            if entry in read:
                email = read[entry]["email"]
                password = read[entry]["password"]
                messagebox.showinfo(title=entry, message=f"Email: {email} \n \nPassword: {password}")
            else:
                messagebox.showerror(title="error", message=f"{entry} does not exist")
    except FileNotFoundError:
        print("file not found")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generator():
    password = []
    for _ in range(3):
        letter_choice = random.choice(letters)
        number_choice = random.choice(numbers)
        punc_choice = random.choice(punctuations)
        password.append(letter_choice)
        password.append(number_choice)
        password.append(punc_choice)
    random.shuffle(password)
    pass_string = ''.join(password)

    text_pass.insert(0, pass_string)
    pyperclip.copy(pass_string)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_entry():
    website = text_web.get()
    user = text_user.get()
    password = text_pass.get()
    new_data = {
        website: {
            "email": user,
            "password": password,
        }
    }
    if len(password) == 0 or len(user) == 0:
        if len(password) == 0:
            messagebox.showerror(title=website, message="password box is empty")
        elif len(user) == 0:
            messagebox.showerror(title=website, message="username/email box is empty")
    else:
        try:
            with open("database.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("database.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)

            with open("database.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            text_web.delete(0, END)
            text_user.delete(0, END)
            text_pass.delete(0, END)
            pass_added.config(text="information added")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

#labels
label_user = Label()
label_web = Label()
label_pass = Label()
label_user.config(text="Email/Username:")
label_user.grid(column=0, row=2)
label_web.config(text="Website:")
label_web.grid(column=0, row=1)
label_pass.config(text="Password:")
label_pass.grid(column=0, row=3)
pass_added = Label()
pass_added.grid(column=1, row=5)

#buttons
button_pass = Button(text="Generate Password", command=generator)
button_add = Button(text="Add", width=45, command=save_entry)
button_pass.grid(column=2, row=3, sticky="w")
button_add.grid(column=1, row=4, columnspan=2, sticky="w")
button_search = Button(text="search", width=14, command=search)
button_search.grid(column=2, row=1)


#text boxes
text_web = Entry(width=34)
text_web.grid(column=1, row=1, columnspan=2, sticky="w")
text_web.focus()
text_user = Entry(width=53)
text_user.grid(column=1, row=2, columnspan=2, sticky="w")
text_user.insert(0, "somebody@gmail.com")
text_pass = Entry(width=33)
text_pass.grid(column=1, row=3)


window.mainloop()
