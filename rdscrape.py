import requests
import csv
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image


path = "rd.jpg" # image file name for logo to be displayed in root window (must be in same directory as running script)

details = []
accountdetailsdisplay = []

file_path = 'token.txt'
try:
    with open ("token.txt", "r") as myfile:
            apitoken=myfile.read()
except:
            fp = open(file_path, 'w+')

def gui_input(prompt):

    root = tk.Toplevel()
    # this will contain the entered string, and will
    # still exist after the window is destroyed
    var = tk.StringVar()

    # create the GUI
    label = tk.Label(root, text=prompt)
    entry = tk.Entry(root, textvariable=var)
    label.pack(side="left", padx=(20, 0), pady=20)
    entry.pack(side="right", fill="x", padx=(0, 20), pady=20, expand=True)

    # Let the user press the return key to destroy the gui 
    entry.bind("<Return>", lambda event: root.destroy())

    # this will block until the window is destroyed
    root.wait_window()

    # after the window has been destroyed, we can't access
    # the entry widget, but we _can_ access the associated
    # variable
    value = var.get()
    return value


def deletelist():
    details.clear()

    
def savefile():
    # asks user to input filename to save as CSV file, this is prompted when user clicks Output to CSV file once Download Links button has been pressed and links have been scraped.
    filename = gui_input("Insert filename to Save:")
    with open (filename + '.csv','w') as file:
       writer=csv.writer(file)
       writer.writerow(['ID','Filename','Source Link', 'Real Debrid Link'])
       for row in details:
          writer.writerow(row)
    messagebox.showinfo("Save to CSV",  "Successfully created CSV File")

def checktoken():
    # If API token in token.txt is not of correct length, then user is prompted to enter the correct API token
    messagebox.showinfo("API Token",  "Your current API Token is\n" + apitoken)
    if len(apitoken) < 26 :
        messagebox.showinfo("API Token",  "Your current API Token is not correct, please enter the correct token when prompted below")
        inputtoken()
        sys.exit()

def incorrecttoken():
    # messagebox displayed informing user of incorrect API token, and prompted user to input correct length token, by calling inputtoken function
    messagebox.showinfo("API Token",  "Your current API Token is not correct, please enter the correct token when prompted below")
    inputtoken()
    quit()

def account():
    # checks API token, if not correct user is prompted to input correct api token, if correct, users account details are displayed in message box
    checktoken()
    url = "https://api.real-debrid.com/rest/1.0/user?auth_token=" + apitoken
    page = requests.get(url)
    if page.status_code == 401:
        incorrecttoken()
    else:
        print (url)
        data = page.json()
        accountdetails ="ID of User" ,  data ['id'] ,  "\nUsername:", data['username'], "\nEmail:", data['email'], "\nPremium Status:", data['type'], "\nExpiration Date:", data['expiration']
        messagebox.showinfo("Hello There",  accountdetails)

def history():
     # checks API token, if not correct user is prompted to input correct api token, if correct, users download links history is scraped
    checktoken()
    deletelist()
    for p in range(1, 10):
        try:
            url = "https://api.real-debrid.com/rest/1.0/downloads?auth_token="+apitoken+"&page="+str(p)
            print (url)
            page = requests.get(url)
            if page.status_code == 401:
                incorrecttoken()
            
            data = page.json()

            for i in range(0,50):
                datascrape = data[i]['id'],  data[i]['filename'], data[i]['link'], data[i]['download']
                details.append(datascrape)
                
        except:
            break
            
    messagebox.showinfo("Important Message", "Links have been gathered, please click Output to CSV to save file!") 


def inputtoken():
     apitoken = gui_input("Insert Correct API Token:")
     with open('token.txt', 'w') as file:
        if len(apitoken) == 26 :
            messagebox.showinfo("API Token",  apitoken + "has been set as your API Token")
            messagebox.showinfo("API Token",  "Script will now Close \nPlease rerun script and New API Token will be set")
            file.write(apitoken)
        elif len(apitoken) < 26:
            messagebox.showinfo("API Token",  "No API Token found in token.txt file,  please add API Token to this file to use script")
                    
               


def quit():
    root.quit()


root = tk.Tk()
root.geometry("450x450")
root.wm_title("Real Debird - Downloaded Links to CSV")
# Code to add widgets will go here...
Label = tk.Label(root, text = 'Real Debrid\n Downloaded Links to CSV', font = ('Comic Sans MS',18))
button = tk.Button(root, text="Account Details", command=account)
button2 = tk.Button(root, text="Downloads List", command=history)
button3 = tk.Button(root,  text = "Output to CSV File", command=savefile)
button4 = tk.Button(root,  text = "Quit Program", command=quit)
Label.pack()
button.pack()
button2.pack()
button3.pack()
button4.pack()
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()

        
