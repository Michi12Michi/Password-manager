from tkinter import *
from tkinter import messagebox
from random import randint, sample, shuffle
import json

# ------------------------------------- UTILITY ---------------------------------------- #
def clear_fields():
    ent_website.delete(0, END)
    ent_username.delete(0, END)
    ent_username.insert(0, "@")
    ent_password.delete(0, END)
    ent_website.focus()
    
def search_website():
    try:
        with open("data.json", "r") as filedata:
            data = json.load(filedata)
    except FileNotFoundError:
        messagebox.showerror(title="File not found", message="File not found. Sorry for the inconvenience.")
    else:
        try:
            data_username = data[ent_website.get()]["username"]
            data_password = data[ent_website.get()]["password"]
        except KeyError:
            messagebox.showerror(title="Key not found", message = "Key not found.")
        else:
            messagebox.showinfo(title="Data request", message=f"username: {data_username}\npassword: {data_password}")
    finally:
        clear_fields()
    
    
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVNM"
numbers = "0123456789"
spec_chars = "!$%&()=^_*-+"

def generate_pass():
    if ent_password.get():
        ent_password.delete(0, END)
    n_letters = randint(8, 10)
    n_spec = randint(2, 4)
    n_num = randint(2, 4)
    gen_pass = []
    gen_pass.extend(sample(letters, n_letters))
    gen_pass.extend(sample(spec_chars, n_spec))
    gen_pass.extend(sample(numbers, n_num))
    shuffle(gen_pass)
    ent_password.insert(0, "".join(gen_pass))

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    if ent_website.get() and ent_username.get() and ent_password.get():
        if messagebox.askokcancel(title="Validate data", message="Are you sure?") == True:
            new_data = {
                ent_website.get(): {
                    "username": ent_username.get(),
                    "password": ent_password.get()
                    }
                }
            data = {}
            try:
                with open("data.json", "r") as filedata:        
                    data = json.load(filedata)
            except FileNotFoundError:
                messagebox.showinfo(title = "File not found!", message="File will be created.")
                with open("data.json", "w") as filedata:
                    json.dump(new_data, filedata, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as filedata:
                    json.dump(data, filedata, indent=4)
            finally:
                clear_fields()
    else:
        messagebox.showinfo(title="Ooops!", message="Don't feed blank fields, please...")

# ---------------------------- UI SETUP ------------------------------- #
main_window = Tk() 
main_window.title("Password Manager") 
main_window.config(background="#FFFFFF", padx = 50, pady = 50)
img_logo = PhotoImage(file="logo.png") 
canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.config(background = "#FFFFFF") 
canvas.create_image(100, 100, image=img_logo) 

lab_website = Label(text = "Website", bg = "#FFFFFF", pady = 10)
lab_username = Label(text = "Email/Username", bg = "#FFFFFF", pady = 10)
lab_password = Label(text = "Password", bg = "#FFFFFF", pady = 10)

ent_website = Entry(width = 25)
ent_website.focus()
ent_username = Entry(width = 35)
ent_username.insert(0, "@")
ent_password = Entry(width = 25)

btn_search = Button(text = "Search", width = 4, pady = 0, command=search_website)
btn_genpassword = Button(text = "Gen!", width = 4, pady = 0, command=generate_pass)
btn_add = Button(text = "Add", width = 33, pady = 0, command=save_data)
canvas.grid(row = 0, column = 1)
lab_website.grid(row = 1, column = 0)
lab_username.grid(row = 2, column = 0)
lab_password.grid(row = 3, column = 0)
ent_website.grid(row = 1, column = 1)
ent_username.grid(row = 2, column = 1, columnspan = 2)
ent_password.grid(row = 3, column = 1)
btn_search.grid(row = 1, column=2)
btn_genpassword.grid(row = 3, column = 2)
btn_add.grid(row = 4, column = 1, columnspan = 2)
main_window.mainloop()
