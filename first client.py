import requests
import Tkinter as tk
from Tkinter import *
from PIL import ImageTk, Image
###############################   Nurmlzition for text   #############################################################################################
def text_normal(the_out, the_size):
    # orgnaizing the text for containing not too much words a line
    # depends on the amount of text is changing the length of a line and the size of the text.
    i = 0
    full =[]
    for word in (the_out.split()):
        full.append(word)
        i+= 1
        if i == int(the_size):
            i = 0
            full.append ("\n")
    complite = (' '.join(full))
    return complite
###############################   UI   #############################################################################################

def raise_frame(frame): # function for raising pages
    frame.tkraise()
def on_click(event):
    #function that gets called whenever entry is clicked
    if txt.cget('fg') == 'grey':
       txt.delete(0, "end") # delete all the text in the entry
       txt.insert(0, '') #Insert blank for user input
       txt.config(fg = 'black')
def focusout(event):
    if txt.get() == '':
        txt.insert(0, 'Looking for info? Type it here and we will find it for you!')
        txt.config(fg = 'grey')

def Search(): # set up and start the procses of the TF IDF
    global textInput
    global which
    textInput=txt.get()
    api_url = 'http://127.0.0.1:5000/SearchEngine/api/v1.0/%s' % (textInput)
    response = requests.get(api_url)
    textOutPut= response.text
    error = int(textOutPut [-2])
    i = int(textOutPut [-5])
    which = int(textOutPut [-8])
    textOutPut = textOutPut[:-11]
    textOutPut = textOutPut[3:]
    if i == 0:
        the_size = 15
    else:
        the_size = 38
    textOutPut = text_normal (textOutPut,the_size)
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
    if (X == 1):
        raise_frame(f3)
        txt.delete(0, 'end')
        feedback_url = 'http://127.0.0.1:5000/SearchEngine/feedback/v1.1/%s/%s/%s' % (textInput,"1",which)
        response = requests.get(feedback_url)
    if (X == 2):
        txt.delete(0, 'end')
        raise_frame(f3)
        feedback_url = 'http://127.0.0.1:5000/SearchEngine/feedback/v1.1/%s/%s/%s' % (textInput,"0",which)
        response = requests.get(feedback_url)
    if (X == 3):
        txt.delete(0, 'end')
        raise_frame(f3)
    if (X == 4):
        txt.delete(0, 'end')
        raise_frame(f1)
    # what to do when review button clicked

root = Tk() # creating tk window
root.configure(background='white')
#creats the components of the pages & the pages
f1 = Frame(root)
f1.configure(background='white')
f2 = Frame(root)
f2.configure(background='white')
f3 = Frame(root)
f3.configure(background='white')
f4 = Frame(root)
f4.configure(background='white')
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
symbol=PhotoImage(file="WeSearch.png")
lbl_0 = Label(f1, image=symbol)
lbl_0.grid(column=1, row = 1, sticky=(W, E, S))
lbl_0.configure(background='white')
lbl_1 = Label(f1, text = "Looking for info? Type it here and we will find it for you!", font = ("Arial Bold",size_smalllabels))
lbl_1.grid(column=1, row = 4, sticky=(W, E, N))
lbl_1.configure(background='white',foreground="white")
txt = Entry(f1, width=int((size_of_entry)))
txt.grid(column = 1, row = 2, pady = size_smalllabels)
txt.insert(0, 'Looking for info? Type it here and we will find it for you!')
txt.bind('<FocusIn>', on_click)
txt.bind('<FocusOut>', focusout)
txt.config(fg = 'grey')
btn = Button(f1, text = "Search", command=Search)
btn.grid(column=1, row=4)
btn.configure(background='white')

#page two - get Feedback
var = IntVar()
lbl_4 = Label(f2, image=symbol)
lbl_4.grid(column=1, row = 1, sticky=(W, E, S))
lbl_4.configure(background='white')
lbl_10 = Label(f2, text = "txt", font = ("Arial Bold",size_of_txt))
lbl_10.grid(column=1, row = 2, sticky=(W, E))
lbl_10.configure(background='white')
lbl_2 = Label(f2, text = "Is this was helpful? Do you want something better?", font = ("Arial Bold",int(size_smalllabels*0.5)))
lbl_2.grid(column=1, row = 5, sticky=(W, E))
lbl_2.configure(background='white')
rad1 = Radiobutton(f2,text='Helpful',  variable=var, value=1)
rad2 = Radiobutton(f2,text='Not Helpful',  variable=var, value=2)
rad3 = Radiobutton(f2,text='I Dont Know',  variable=var, value=3)
rad4 = Radiobutton(f2,text='I Want to Search Agin',  variable=var, value=4)
rad1.grid(column=1, row=6)
rad1.configure(background='white')
rad2.grid(column=1, row=7)
rad2.configure(background='white')
rad3.grid(column=1, row=8)
rad3.configure(background='white')
rad4.grid(column=1, row=9)
rad4.configure(background='white')
btn = Button(f2, text="Send", command=Send)
btn.grid(column=1, row=10)
btn.configure(background='white')

#page three - Last Messege
lbl_5 = Label(f3, image=symbol)
lbl_5.grid(column=1, row = 1, sticky=(W, E, S))
lbl_5.configure(background='white')
lbl_6 = Label(f3, text = "Thank You For Helping Us Improve!", font = ("Arial Bold",int(size_labels/1.26)))
lbl_6.grid(column=1, row = 2, sticky=(W, E))
lbl_6.configure(background='white')
lbl_7 = Label(f3, text = "Please Come Back Agin For Better Answer", font = ("Arial Bold",int(size_smalllabels*1.2)))
lbl_7.grid(column=1, row = 3, sticky=(W, E))
lbl_7.configure(background='white')
btn_11 = Button(f3, text="Try Agin", command=(lambda:raise_frame(f1)))
btn_11.grid(column=1, row=10)
btn_11.configure(background='white')
#page Four - Last Messege
lbl_12 = Label(f4, image=symbol)
lbl_12.grid(column=1, row = 1, sticky=(W, E, S))
lbl_12.configure(background='white')
lbl_13 = Label(f4, text = "Error Occurred", font = ("Arial Bold",size_labels))
lbl_13.grid(column=1, row = 2, sticky=(W, E))
lbl_13.configure(background='white')
lbl_14 = Label(f4, text = "Please Check Your Spelling Or Be More Specific And Try Agin", font = ("Arial Bold",int(size_smalllabels/1.07)))
lbl_14.grid(column=1, row = 3, sticky=(W, E))
lbl_14.configure(background='white')
btn_15 = Button(f4, text="Try Agin", command=(lambda:raise_frame(f1)))
btn_15.grid(column=1, row=10)
btn_15.configure(background='white')




raise_frame(f1)# opening the first page - starts UI
root.mainloop() # making it to run until closed by user
