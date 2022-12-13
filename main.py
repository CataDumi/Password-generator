from tkinter import *
from tkinter import messagebox
import pyperclip
import json
from encode import Encode
from decode import Decode
import random
from encode import ALPHABET

shift = random.randint(80, 160)
# print(shift)
if shift > len(ALPHABET):
    shift = shift % len(ALPHABET)
# print(shift)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    entry_password.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    char = [(random.choice(letters)) for i in range(nr_letters)]
    # print(char)

    symb = [(random.choice(symbols)) for i in range(nr_symbols)]
    # print(symb)

    num = [(random.choice(numbers)) for i in range(nr_numbers)]
    # print(num)

    password_list = char + num + symb
    random.shuffle(password_list)

    password = "".join(password_list)

    # print(f"Your password is: {password}")
    entry_password.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    website = entry_website.get()
    # print(website)

    email = entry_email.get()
    # print(email)

    password = entry_password.get()
    # print(password)

    ###aici vreau sa se faca criptarea

    encoded_website = Encode(start_text=website, shift=shift).end_text
    encoded_mail = Encode(start_text=email, shift=shift).end_text

    encoded_site_text = Encode(start_text='site', shift=shift).end_text
    encoded_email_text = Encode(start_text='email', shift=shift).end_text
    encoded_password_text = Encode(start_text='password', shift=shift).end_text

    new_data = {
        encoded_site_text: encoded_website,
        encoded_email_text: encoded_mail,
        encoded_password_text: password,
        'k': shift,
    }

    # print(new_data)

    if len(website) == 0 or len(password) == 0:
        if len(website) == 0:
            messagebox.askretrycancel(message=f"Website entry is empty")
        else:
            messagebox.askretrycancel(message=f"Password entry is empty")


    else:
        try:
            listObj = []
            # Read JSON file
            with open('test.json') as fp:
                listObj = json.load(fp)
            # Verify existing list
            listObj.append(new_data)

            # Verify updated list
            # print(listObj)
            with open('test.json', 'w') as json_file:
                json.dump(listObj, json_file,
                          indent=4,
                          separators=(',', ': '))

            with open('test.json', 'w') as json_file:
                json.dump(listObj, json_file,
                          indent=4,
                          separators=(',', ': '))
            # print('Successfully appended to the JSON file')
            print(listObj)
            print(type(listObj))



        except FileNotFoundError:  #### daca nu gasesti json ul respectiv ... creeaza unul
            with open("test.json", mode="w") as file:
                json.dump(new_data, file, indent=4)

        entry_password.delete(0, END)
        entry_website.delete(0, END)


####aici e functia de cautare

DICT=None

def search():
    global DICT
    flag_not_found=False
    wanted_site = entry_website.get()

    if len(wanted_site) == 0:
        messagebox.askretrycancel(message=f"Website entry is empty")
    else:
        ### asa deschide json file ul si incep sa ma uit in el
        with open('test.json', 'r') as file:
            list = json.load(file)
            # print(list, type(list))

        for dict in list:
            ###asa vad fiecare dict
            # print(dict)
            decode_key = dict['k']
            # print(decode_key)
            for item in dict:
                ###asa vad key urile din fiecare dict
                # print(item)
                ###asa vad valorile din fiecare dict
                # print(dict[item])
                target=Decode(str(dict[item]),decode_key).end_text
                # print(target)
                if target==wanted_site:
                    match=dict
                    # print(dict) #### aici gasesc dictionarul cautat
                    ### aici decodez respeectivul dictionar:
                    # print(match) ### aici vad dict codat care contine site ul cautat
                    match_key=match['k']
                    # print(match_key) ### aici vad key ul pt decriptare
                    new_dict={ Decode(str(item),match_key).end_text:Decode(str(match[item]),match_key).end_text for item in match}
                    # print(new_dict) #### totul e stas pana aici functioneaza perfect
                    DICT=new_dict

        # print(DICT) ### e ok ..primesti noul dictionar

        if DICT==None:
            messagebox.showinfo(title="Error", message="Website not saved")
            entry_website.delete(0, END)
        else:
            messagebox.showinfo(title="Search",message= f"Email: {DICT['email']}\n Password: {DICT['password']}")
            DICT=None

window = Tk()
window.title("Password")
window.config(pady=50, padx=50)

image = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

label_website = Label(text="Website")
label_website.config(justify=RIGHT)
label_website.grid(column=0, row=1)

label_email = Label(text="Email/Username")
label_email.grid(column=0, row=2)

label_password = Label(text="Password")
label_password.grid(column=0, row=3)

entry_website = Entry(width=25)
entry_website.focus()
entry_website.grid(row=1, column=1)

entry_email = Entry(width=25)
entry_email.insert(END, "email@gmail.com")
entry_email.grid(row=2, column=1)

entry_password = Entry(width=25)
entry_password.grid(column=1, row=3)

generate_password_botton = Button(text="Generate Password", command=generate_password)
generate_password_botton.grid(column=2, row=3)

add_button = Button(text="Add", width=25, command=add)
add_button.grid(row=4, column=1, )

search_button = Button(text="Search", command=search, width=14)
search_button.grid(column=2, row=1)

window.mainloop()
