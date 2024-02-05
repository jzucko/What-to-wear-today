import tkinter as tk 
from PIL import Image, ImageTk
import requests
import urllib.parse
import json
import os
import sqlite3

connect=sqlite3.connect('wheater_data.db')
c=connect.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS w_data (
          date TEXT,
          temperature INTEGER,
          humidity INTEGER,
          pressure INTEGER
)""")

root=tk.Tk()
root.title('Wheater')
root.geometry('400x200')

coat_image_tk=None
jacket_image_tk=None
tshirt_image_tk=None

date=None
temp_max=None
hum=None
pres=None

def submit_db():
    global date, temp_max, hum, pres 
    connect=sqlite3.connect('wheater_data.db')
    c=connect.cursor()
    
    #insert into table
    c.execute('INSERT INTO w_data (date, temperature, humidity, pressure) VALUES (?, ?, ?, ?)', 
              (date, temp_max, hum, pres))
           
    connect.commit()
    connect.close() 
    
def view_data():
    view_window = tk.Toplevel()
    view_window.title('Spremljeni podaci')
    
    text_widget = tk.Text(view_window, width=40, height=10)
    text_widget.pack()
    
    try:
        c.execute('SELECT * FROM w_data')
        rows = c.fetchall()
        records=''
        
        for r in rows:
            records += str(r[0]) + ' '+ '\t' + str(r[1]) + ' ' + '\t'+ str(r[2]) + ' ' + '\t'+ str(r[3])+ '\n'
    
    except sqlite3.Error as e:
        print(f'Error view data {e}')
        
    record_lbl=tk.Label(root, text=records)
    record_lbl.pack()
    
    c.close()
    connect.close()
    
def coat_display():
    global coat_image_tk
    try:
        coat_image=Image.open(r'C:\JelenaZ\Python\PY_VS_code\IoT\Parcijalni IoT\coat.png')
        coat_image = coat_image.resize((60, 50))
        coat_image_tk=ImageTk.PhotoImage(coat_image)
        
        coat_label=tk.Label(root, image=coat_image_tk)
        coat_label.pack()
    except Exception as e:
        print(f' Error: {e} ')
        
def jacket_display():
    global jacket_image_tk
    try:
        jacket_image=Image.open(r'C:\JelenaZ\Python\PY_VS_code\IoT\Parcijalni IoT\jacket.png')
        jacket_image = jacket_image.resize((60, 50))
        jacket_image_tk=ImageTk.PhotoImage(jacket_image)
        
        jacket_label=tk.Label(root, image=jacket_image_tk)
        jacket_label.pack()
    except Exception as e:
        print(f' Error: {e} ')
        
def tshirt_display():
    global tshirt_image_tk
    try:
        tshirt_image=Image.open(r'C:\JelenaZ\Python\PY_VS_code\IoT\Parcijalni IoT\tshirt.png')
        tshirt_image = tshirt_image.resize((60, 50))
        tshirt_image_tk=ImageTk.PhotoImage(tshirt_image)
        
        tshirt_label=tk.Label(root, image=tshirt_image_tk)
        tshirt_label.pack()
    except Exception as e:
        print(f' Error: {e} ')

def destroy():
    root.destroy()

def wheater_api():#api_lbl
    global date, temp_max, hum, pres
    try:
        api_request=requests.get("https://api.tutiempo.net/json/?lan=en&apid=XwGaz4zza4at15z&lid=72153")
        print(api_request.status_code)  # Check the HTTP status code
        print(api_request.text)  # Print the response content
        api=json.loads(api_request.content)
        print(api)# Print the entire parsed JSON
        location=api["locality"]['name']
        date=api["day1"]['date']
        temp_max=api["day1"]['temperature_max']
        hum=api["day1"]['humidity']
        pres=api["hour_hour"]["hour1"]["pressure"]
        
        if temp_max <=10:
            wheater_colour='blue'
            coat_display()
            
        elif temp_max >=11 and temp_max <=29:
            wheater_colour= 'green'
            jacket_display()
            
        elif temp_max >=30:
            wheater_colour ='red'
            tshirt_display()
            
        api_lbl=tk.Label(root, text=f'Grad{location}, datum: {date}, temperatura: {temp_max}, vlažnost: {hum}, tlak: {pres}', background=wheater_colour)
        api_lbl.pack()
    except Exception as e:
        api=f'Error {e}'



wheater_api()
submit_db()

#view_data_btn= tk.Button(root, text='Vidi spremljene podatke', command=view_data).pack()
btn_close=tk.Button(text='Exit', command=destroy).pack()

root.mainloop()
connect.close()
