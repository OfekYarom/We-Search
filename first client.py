import json
import requests
import Tkinter as tk
from Tkinter import *
###############################   UI   #############################################################################################
def raise_frame(frame): # function for raising pages
    frame.tkraise()
def Search(): # set up and start the procses of the TF IDF
    textInput=txt.get()
    api_url = 'http://127.0.0.1:5000/SearchEngine/api/v1.1/%s' % (textInput)
    response = requests.get(api_url)
    textOutPut= response.text
    textOutPut = textOutPutClient [0]
    error = textOutPutClient [1]
    i = textOutPutClient [2]
    lbl_10["text"] = textOutPut # bring the output to the user
    if error > 0:
        if i==0:
            raise_frame(f2)# opens the next page to show the output
        else:
            raise_frame(f2)# opens the next page to show the output
            lbl_10.config(font=("Arial Bold", alot_of_txt))
            # depends on the amount of text is changing the length of a line and the size of the text.
    else:
        txt.delete(0, 'end')
        raise_frame(f4)# if no output have found
    # what to do when Search button clicked
    
def Send(): # the algorithem for the radio buttons
    X = var.get()
    if (X == 1 or X == 3):
        raise_frame(f3)
    if (X == 2):
        raise_frame(f3)
    if (X == 4):
        txt.delete(0, 'end')
        raise_frame(f1)
    # what to do when review button clicked

root = Tk() # creating tk window
#creats the components of the pages & the pages
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)
# setting the pages size acording to the screen size
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size_labels = (screenwidth*screenheight)/26200
size_smalllabels = size_labels/2
size_of_txt = size_labels/5
alot_of_txt = size_labels/10
size_of_entry = size_labels*1.5
x_cordnite = ((screenwidth/2)-(screenwidth/2.6))
y_cordnite = ((screenheight/2)-screenheight/2.6)
root.geometry(("%dx%d+%d+%d") %((screenwidth/1.3),(screenheight/1.3),x_cordnite,y_cordnite))
root.resizable(0, 0)
root.title("Search Engine") # giving the window a name

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

#page one - get Search Word
lbl_0 = Label(f1, text = "Search Engine", font = ("Arial Bold",size_labels))
lbl_0.grid(column=1, row = 1, sticky=(W, E))
lbl_1 = Label(f1, text = "Looking for info? Type it here and we will find it for you!", font = ("Arial Bold",size_smalllabels))
lbl_1.grid(column=1, row = 2, sticky=(W, E))
txt = Entry(f1, width=int((size_of_entry)))
txt.grid(column = 1, row = 3, pady = size_smalllabels)
txt.focus()
btn = Button(f1, text="Search", command=Search)
btn.grid(column=1, row=4)

#page two - get Feedback
var = IntVar()
lbl_4 = Label(f2, text = "Search Engine", font = ("Arial Bold",size_labels))
lbl_4.grid(column=1, row = 1, sticky=(W, E))
lbl_10 = Label(f2, text = "txt", font = ("Arial Bold",size_of_txt))
lbl_10.grid(column=1, row = 2, sticky=(W, E))
lbl_2 = Label(f2, text = "Is this was helpful? Do you want something better?", font = ("Arial Bold",int(size_smalllabels*1.127)))
lbl_2.grid(column=1, row = 5, sticky=(W, E))
rad1 = Radiobutton(f2,text='Helpful',  variable=var, value=1)
rad2 = Radiobutton(f2,text='Not Helpful',  variable=var, value=2)
rad3 = Radiobutton(f2,text='I Dont Know',  variable=var, value=3)
rad4 = Radiobutton(f2,text='I Want to Search Agin',  variable=var, value=4)
rad1.grid(column=1, row=6)
rad2.grid(column=1, row=7)
rad3.grid(column=1, row=8)
rad4.grid(column=1, row=9)
btn = Button(f2, text="Send", command=Send)
btn.grid(column=1, row=10)

#page three - Last Messege
lbl_5 = Label(f3, text = "Search Engine", font = ("Arial Bold",size_labels))
lbl_5.grid(column=1, row = 1, sticky=(W, E))
lbl_6 = Label(f3, text = "Thank You For Helping Us Improve!", font = ("Arial Bold",int(size_labels/1.26)))
lbl_6.grid(column=1, row = 2, sticky=(W, E))
lbl_7 = Label(f3, text = "Please Come Back Agin For Better Answer", font = ("Arial Bold",int(size_smalllabels*1.2)))
lbl_7.grid(column=1, row = 3, sticky=(W, E))
btn_11 = Button(f3, text="Try Agin", command=(lambda:raise_frame(f1)))
btn_11.grid(column=1, row=10)

#page Four - Last Messege
lbl_12 = Label(f4, text = "Search Engine", font = ("Arial Bold",size_labels))
lbl_12.grid(column=1, row = 1, sticky=(W, E))
lbl_13 = Label(f4, text = "Error Occurred", font = ("Arial Bold",size_labels))
lbl_13.grid(column=1, row = 2, sticky=(W, E))
lbl_14 = Label(f4, text = "Please Check Your Spelling Or Be More Specific And Try Agin", font = ("Arial Bold",int(size_smalllabels/1.07)))
lbl_14.grid(column=1, row = 3, sticky=(W, E))
btn_15 = Button(f4, text="Try Agin", command=(lambda:raise_frame(f1)))
btn_15.grid(column=1, row=10)




raise_frame(f1)# opening the first page - starts UI

root.mainloop() # making it to run until closed by user
