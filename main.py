import customtkinter as ctk
from tkinter import messagebox, Listbox
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Contact Book")
app.geometry("950x650")

file_name = "contacts.json"

if os.path.exists(file_name):
    with open(file_name, "r") as file:
        contacts = json.load(file)
else:
    contacts = []

selected_index = None


# save contacts
def save_contacts():
    with open(file_name, "w") as file:
        json.dump(contacts, file, indent=4)


# show all contacts
def show_contacts():

    contact_list.delete(0, "end")

    for contact in contacts:
        contact_list.insert(
            "end",
            f"{contact['name']} - {contact['phone']}"
        )


# clear input fields
def clear_fields():
    name_entry.delete(0, "end")
    phone_entry.delete(0, "end")
    email_entry.delete(0, "end")
    address_entry.delete(0, "end")


# add contact
def add_contact():

    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if name == "" or phone == "":
        messagebox.showerror(
            "Error",
            "Name and Phone Number are required"
        )
        return

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    })

    save_contacts()
    show_contacts()
    clear_fields()

    messagebox.showinfo(
        "Success",
        "Contact Added"
    )


# search contact
def search_contact():

    keyword = search_entry.get().lower()

    contact_list.delete(0, "end")

    for contact in contacts:

        if (
            keyword in contact["name"].lower()
            or
            keyword in contact["phone"]
        ):
            contact_list.insert(
                "end",
                f"{contact['name']} - {contact['phone']}"
            )


# when user clicks a contact
def select_contact(event):

    global selected_index

    selected = contact_list.curselection()

    if not selected:
        return

    selected_index = selected[0]

    contact = contacts[selected_index]

    clear_fields()

    name_entry.insert(0, contact["name"])
    phone_entry.insert(0, contact["phone"])
    email_entry.insert(0, contact["email"])
    address_entry.insert(0, contact["address"])


# update contact
def update_contact():

    global selected_index

    if selected_index is None:
        messagebox.showerror(
            "Error",
            "Select a contact first"
        )
        return

    contacts[selected_index]["name"] = name_entry.get()
    contacts[selected_index]["phone"] = phone_entry.get()
    contacts[selected_index]["email"] = email_entry.get()
    contacts[selected_index]["address"] = address_entry.get()

    save_contacts()
    show_contacts()

    messagebox.showinfo(
        "Updated",
        "Contact Updated"
    )


# delete contact
def delete_contact():

    global selected_index

    if selected_index is None:
        messagebox.showerror(
            "Error",
            "Select a contact first"
        )
        return

    contacts.pop(selected_index)

    save_contacts()
    show_contacts()
    clear_fields()

    selected_index = None

    messagebox.showinfo(
        "Deleted",
        "Contact Deleted"
    )


title = ctk.CTkLabel(
    app,
    text="Contact Book",
    font=("Arial", 28, "bold")
)
title.pack(pady=15)

search_frame = ctk.CTkFrame(app)
search_frame.pack(pady=10)

search_entry = ctk.CTkEntry(
    search_frame,
    width=250,
    placeholder_text="Search Contact"
)
search_entry.pack(side="left", padx=10, pady=10)

search_button = ctk.CTkButton(
    search_frame,
    text="Search",
    command=search_contact
)
search_button.pack(side="left", padx=10)

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

left_frame = ctk.CTkFrame(main_frame)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

contact_label = ctk.CTkLabel(
    left_frame,
    text="Contact List",
    font=("Arial", 20, "bold")
)
contact_label.pack(pady=10)

contact_list = Listbox(
    left_frame,
    width=35,
    height=20,
    font=("Arial", 12)
)
contact_list.pack(padx=10, pady=10)

contact_list.bind(
    "<<ListboxSelect>>",
    select_contact
)

right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

name_entry = ctk.CTkEntry(
    right_frame,
    width=320,
    placeholder_text="Name"
)
name_entry.pack(pady=10)

phone_entry = ctk.CTkEntry(
    right_frame,
    width=320,
    placeholder_text="Phone Number"
)
phone_entry.pack(pady=10)

email_entry = ctk.CTkEntry(
    right_frame,
    width=320,
    placeholder_text="Email"
)
email_entry.pack(pady=10)

address_entry = ctk.CTkEntry(
    right_frame,
    width=320,
    placeholder_text="Address"
)
address_entry.pack(pady=10)

add_button = ctk.CTkButton(
    right_frame,
    text="Add Contact",
    command=add_contact
)
add_button.pack(pady=10)

update_button = ctk.CTkButton(
    right_frame,
    text="Update Contact",
    command=update_contact
)
update_button.pack(pady=10)

delete_button = ctk.CTkButton(
    right_frame,
    text="Delete Contact",
    command=delete_contact
)
delete_button.pack(pady=10)

footer = ctk.CTkLabel(
    app,
    text="Developed by Jashanpreet",
    font=("Arial", 12)
)
footer.pack(pady=10)

show_contacts()

app.mainloop()

