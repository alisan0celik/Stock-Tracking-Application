# This code created by Alişan Çelik
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pytz

from datetime import datetime
import time as t
import http.client
import json

import threading
from tkinter import PhotoImage
import matplotlib.pyplot as plt

hisseler = []
sembol_comboboxes = []
adet_entries = []
adetler = []
sembol_listesi = []
secilen_hisseler = []

hisseler_verileri = {}


conn = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 2SJZNSOth9GYznj2wPB2Yp:31V2L183PuARI9EW2g4cuS"
}

conn.request("GET", "/economy/hisseSenedi", headers=headers)

res = conn.getresponse()
data = res.read()

# Decode the response data
decoded_data = data.decode("utf-8")

# Parse the JSON data
json_data = json.loads(decoded_data)

# Extract symbols from the JSON data
symbols = [item.get("code") for item in json_data.get("result", [])]

# Sort symbols alphabetically
sembollar = sorted(symbols)

# Print the sorted symbols


# Close the connection
conn.close()

ilk_fiyat = {sembol: None for sembol in sembollar}
maaliyetler = {sembol: 0 for sembol in sembollar}
def update_hisse_symbols(event, index):
    filter_text = sembol_comboboxes[index].get().lower()
    filtered_symbols = [symbol for symbol in sembollar if filter_text in symbol.lower()]
    sembol_comboboxes[index]["values"] = filtered_symbols
def update_symbols(*args):
    filter_text = ekle_sembol_combobox.get().lower()
    filtered_symbols = [symbol for symbol in sembollar if filter_text in symbol.lower()]
    ekle_sembol_combobox["values"] = filtered_symbols


def clear_table(table):
    for item in table.get_children():
        table.delete(item)

def kapat_uygulama():
    window.destroy()


def show_summary_window(table):
    summary_window = tk.Toplevel()
    summary_window.title("Total Amount and Profit/Loss")
    summary_window.geometry("600x400")

    total_tutar = sum(float(table.item(item, 'values')[4]) for item in table.get_children())  # Assuming 'Tutar' column is at index 4
    total_kar_zarar = sum(float(table.item(item, 'values')[3]) for item in table.get_children())  # Assuming 'Kar ve Zarar' column is at index 3

    summary_label = tk.Label(summary_window, text=f"Total Amount: {total_tutar:.2f} TL\nTotal Profit/Loss: {total_kar_zarar:.2f} TL")
    summary_label.pack()

    # Display the pie chart
    labels = [table.item(item, 'values')[0] for item in table.get_children()]  # Assuming 'Hisse Adı' column is at index 0
    sizes = [float(table.item(item, 'values')[4]) for item in table.get_children()]  # Assuming 'Tutar' column is at index 4

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.

    plt.title("Total Amount")

    plt.show()

# Function that initializes the created table
def create_table_window():
    if hasattr(create_table_window, 'table_window') and create_table_window.table_window:
        # If there is a window named table_window, close it
        create_table_window.table_window.destroy()

    table_window = tk.Toplevel()
    table_window.title("Stock Trader")
    table_window.geometry("1000x400")

    table_frame = ttk.LabelFrame(table_window, text="Stock Chart")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Stock Name", "Price", "Quantity", "Profit and loss ", "Amount")
    table = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        table.heading(col, text=col, command=lambda _col=col: sort_table(table, _col))
        table.column(col, width=100, anchor="center")

    table.tag_configure('positive', background='green')
    table.tag_configure('negative', background='red')
    table.tag_configure('zero', background='black', foreground='white')

    create_table_window.sort_column = None
    create_table_window.sort_direction = None

    table.pack(fill="both", expand=True)

    create_table_window.table_window = table_window
    toplam_button = tk.Button(table_frame, text="Total amount and Profit/Loss", command=lambda: show_summary_window(table))
    toplam_button.pack()
    return table

def update_table_row_colors(table):
    for item in table.get_children():
        kar_zarar_value = float(table.item(item, 'values')[3])  # Assuming 'Kar ve Zarar' column is at index 3

        # Clear existing tags
        table.item(item, tags=())

        # Set new tags based on the value of 'Kar ve Zarar'
        if kar_zarar_value > 0:
            table.item(item, tags=('positive',))
        elif kar_zarar_value < 0:
            table.item(item, tags=('negative',))
        else:
            table.item(item, tags=('zero',))
def sort_table(tree, col):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    def try_numeric(value):
        try:
            return float(value)
        except ValueError:
            return value

    if create_table_window.sort_column == col and create_table_window.sort_direction == "ascending":
        data.sort(key=lambda x: try_numeric(x[0]), reverse=True)
        create_table_window.sort_direction = "descending"
    else:
        data.sort(key=lambda x: try_numeric(x[0]), reverse=False)
        create_table_window.sort_direction = "ascending"

    create_table_window.sort_column = col

    for index, item in enumerate(data):
        tree.move(item[1], '', index)

def hisse_senedi_takip():
    table = create_table_window()
    fiyatlar = [0] * 30
    ilk_fiyat_kaydedildi = [False] * 30

    for i in range(30):
        sembol = sembol_comboboxes[i].get()
        adet = adet_entries[i].get()
        if sembol and adet:
            if sembol not in sembol_listesi:
                secilen_hisseler.append(sembol)
                sembol_listesi.append(sembol)
            adetler.append(int(adet))

    if not secilen_hisseler:
        messagebox.showerror("Hata", "Please select at least one stock.")

    turkey_tz = pytz.timezone('Europe/Istanbul')
    alim_mesaji = f"Your transactions have been completed successfully"
    messagebox.showinfo("basarili islem", alim_mesaji)

    while True:
        conn = http.client.HTTPSConnection("api.collectapi.com")
        headers = {
            'content-type': "application/json",
            'authorization': "apikey 2SJZNSOth9GYznj2wPB2Yp:31V2L183PuARI9EW2g4cuS"
        }

        conn.request("GET", "/economy/liveBorsa", headers=headers)
        res = conn.getresponse()
        data = res.read()

        response_data = json.loads(data.decode("utf-8"))
        conn.close()

        turkey_time = datetime.now(tz=turkey_tz)
        saat_dakika = turkey_time.strftime("%H:%M")

        clear_table(table)

        for i, (sembol, adet) in enumerate(zip(secilen_hisseler, adetler)):
            hisse_senedi_adi = sembol
            fiyat = None

            for result in response_data.get("result", []):
                if result.get("name") == hisse_senedi_adi:
                    fiyat = result.get("price")
                    if ilk_fiyat[hisse_senedi_adi] is None:
                        ilk_fiyat[hisse_senedi_adi] = fiyat  # Save first price
                        if maaliyetler[hisse_senedi_adi] == 0:
                            maaliyetler[hisse_senedi_adi] = ilk_fiyat[hisse_senedi_adi]
                        break

                    break


            if fiyat is not None:
                tutar = fiyat * adet
                fiyat_degisimi = fiyat - ilk_fiyat[hisse_senedi_adi]
                kar_veya_zarar = fiyat_degisimi * adet

                if (fiyat_degisimi / ilk_fiyat[hisse_senedi_adi]) * 100 >= 3:  # If the profit is more than 3%
                    satim_mesaji = f"{hisse_senedi_adi} Stock sold at {fiyat} price. Profit: {kar_veya_zarar} TL (%{fiyat_degisimi:.2f})"
                    messagebox.showwarning("Satış İşlemi", satim_mesaji)
                elif (fiyat_degisimi / ilk_fiyat[hisse_senedi_adi]) * 100 <= -5:  # If the damage is more than 5%
                    satim_mesaji = f"{hisse_senedi_adi} stock sold at {fiyat} price. Loss: {kar_veya_zarar} TL (%{fiyat_degisimi:.2f})"
                    messagebox.showwarning("Satış İşlemi", satim_mesaji)

            else:
                print(f"{hisse_senedi_adi} stock not found.")

            yeni_veri = (hisse_senedi_adi, fiyat, adet, kar_veya_zarar, tutar)
            table.insert("", "end", values=yeni_veri)

        turkey_time = datetime.now(tz=turkey_tz)
        saat_dakika = turkey_time.strftime("%H:%M")
        update_table_row_colors(table)
        if saat_dakika >= "17:00":
            satim_mesaji = f"Sell all the stocks because it's the end of the day"
            messagebox.showwarning("Satış İşlemi", satim_mesaji)
            break

        t.sleep(30)


def baslat_hisse_takibi():
    t = threading.Thread(target=hisse_senedi_takip)
    t.start()

def ekle_hisse():
    secilen_hisse = ekle_sembol_combobox.get()
    adet = ekle_adet_entry.get()

    if secilen_hisse and adet:
        adet = int(adet)
        if secilen_hisse in secilen_hisseler:
            # The stock is already listed, increase its quantity
            index = secilen_hisseler.index(secilen_hisse)
            adetler[index] += adet
        else:
            # Share is not listed, add new share
            secilen_hisseler.append(secilen_hisse)
            adetler.append(adet)


        baslat_hisse_takibi()  # Start tracking after adding shares
    else:
        messagebox.showerror("Hata", "Please enter a valid share and quantity.")


def update_canvas_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
# Create Tkinter window
window = tk.Tk()
window.title("Stock Tracking Application")
window.geometry("1200x800")

icon_image = PhotoImage(file="simge2c.png")

# Set the window icon
window.iconphoto(True, icon_image)

# Create Main Frame
main_frame = tk.Frame(window, bg="#ADD8E6")
main_frame.pack(fill="both", expand=True)


kapat_button = tk.Button(main_frame, text="Shut Down", command=kapat_uygulama)
kapat_button.pack()

# Create a Frame for Scrollbar
scrollbar_frame = tk.Frame(main_frame)
scrollbar_frame.pack(side="right", fill="y")

# Create canvas component
canvas = tk.Canvas(main_frame, bg="#ADD8E6")
canvas.pack(side="left", fill="both", expand="yes")

# Create scrollbar component
vertical_scrollbar = tk.Scrollbar(scrollbar_frame, orient="vertical", command=canvas.yview)
vertical_scrollbar.pack(fill="y")

# Connect Canvas and Scrollbar
canvas.configure(yscrollcommand=vertical_scrollbar.set)

# Create a Frame for the content
content_frame = tk.Frame(canvas, bg="#ADD8E6")
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Create the add button and bind the function
ekle_button = tk.Button(content_frame, text="Add", command=ekle_hisse)
ekle_button.pack()

# Stock selection box
ekle_sembol_label = tk.Label(content_frame, text="Stock Symbol:")
ekle_sembol_label.pack()
ekle_sembol_combobox = ttk.Combobox(content_frame, values=sembollar)
ekle_sembol_combobox.pack()
ekle_sembol_combobox.bind("<<ComboboxSelected>>", update_symbols)
ekle_sembol_combobox.bind("<KeyRelease>", update_symbols)

# Quantity input box
ekle_adet_label = tk.Label(content_frame, text="Quantity:")
ekle_adet_label.pack()
ekle_adet_entry = tk.Entry(content_frame)
ekle_adet_entry.pack()

# Add "Start" button
baslat_button = tk.Button(content_frame, text="Start", command=baslat_hisse_takibi)
baslat_button.pack()

# Set scrollregion
content_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Update the canvas scroll region when the content changes
content_frame.bind("<Configure>", update_canvas_scrollregion)

# Mousewheel binding
canvas.bind_all("<MouseWheel>", on_mousewheel)

for i in range(30):
    hisse_frame = ttk.LabelFrame(content_frame, text=f"Stock {i + 1}")
    hisse_frame.pack(fill="x", padx=10, pady=5)

    sembol_label = tk.Label(hisse_frame, text="Stock Symbol:")
    sembol_label.pack()
    sembol_combobox = ttk.Combobox(hisse_frame, values=sembollar, postcommand=lambda i: update_hisse_symbols(None, i))
    sembol_combobox.pack()
    sembol_comboboxes.append(sembol_combobox)



    adet_label = tk.Label(hisse_frame, text="Quantity:")
    adet_label.pack()
    adet_entry = tk.Entry(hisse_frame)
    adet_entry.pack()
    adet_entries.append(adet_entry)

created_by_label = tk.Label(window, text="created by Alisan Celik", bg="#ADD8E6", font=("Arial", 10))
created_by_label.place(relx=1.0, rely=1.0, anchor='se')

window.mainloop()

# This code created by Alişan Çelik