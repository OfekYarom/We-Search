###############################   Import   ##################################################################################################
import urllib
from __future__ import division
import string
import math
import urllib
import urllib2
import Tkinter as tk
from Tkinter import *
import wikipedia
from HTMLParser import HTMLParser
###############################    TF - IDF   #################################################################################################
global all_documents
global tokenize
def documents (doc_0):
    # get the text from wikipedia according to the user input
    # the function is getting the text for each word and for the all input
    global tokenize
    global all_documents
    tokenize = lambda doc: doc.lower().split(" ") # organizing the text
    document_0 = doc_0
    document_1 = (wikipedia.summary(("%s") % (doc_0)))
    document_2 = (wikipedia.page(("%s") % (doc_0)))
    document_2 = document_2.content
    all_documents = [document_0, document_1, document_2]
    splited = doc_0.split()
    if ((len(splited))>1): # checks if the web pages exists
        count = 1
        while (((len(splited))>= count)):
            word = splited[count-1]
            try:
                urllib2.urlopen
            except urllib2.HTTPError, e:
                pass
            except urllib2.URLError, e:
                pass
            else:
                stat = (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(word)).getcode()))
                if stat == 200:
                    Page = (wikipedia.page(("%s") % (word)))
                    doc_one = Page.content
                    doc_two = (wikipedia.summary(("%s") % (word)))
                    all_documents.append (doc_one)
                    all_documents.append (doc_two)
            count = count + 1


def sublinear_term_frequency(term, tokenized_document): # getting the term and the docs # calling the function (getting it all togheter)
   count = tokenized_document.count(term) # counting how many times the term is shown in the doucement
   if count == 0:
       return 0 # if doesnt shown once returning 0
   else:
      return 1 + math.log(count) 
# if shown retrning the number of times after normalization (log)

def inverse_document_frequencies(tokenized_documents): # getting a document
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist]) # creatung a set of all the terms in all the documents
    for tkn in all_tokens_set: # for each input
        contains_token = map(lambda doc: tkn in doc, tokenized_documents) #  moving the terms into a map
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token))) # puts in dictionary the value of each word by dividing the number of times the word appears by the total words
    return idf_values

# returning this value

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]# converting the documents to a different format
    idf = inverse_document_frequencies(tokenized_documents) #putting the value of each word in a varbile by idf
    tfidf_documents = []
    for document in tokenized_documents: # for each doc
        doc_tfidf = []
        for term in idf.keys(): #for each catgory in the dictionary
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])#  Calculates the product of the idf and tf
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents
# getting all the functions to work togheter




def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))# Calculates the sum of the idf and tf
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2])) # put the results in the formula
    if not magnitude:
        return 0
    return dot_product/magnitude
#normalization

def orgnize_info(our_tfidf_comparisons):
   final_match = " "
   best_match = 0
   second_match = 0
   for z in zip(sorted(our_tfidf_comparisons, reverse = True)):
      
      for one_result in z: #Receives the value of each adjustment and the relevant documents for the adjustment
         
         if one_result [2] == 0 or one_result[1] == 0: # Filters the irrelevant documents
            
            for solo in one_result: # Receives all entries in a single configuration
               
               if (solo < 0.999999 and solo != 0): # Filtering everything that is not the matching value
                  
                  if solo > best_match: # Checks what is the best match and stores it
                     best_match = solo
         if best_match == one_result [0]: #Checking which document that is not zero The match is relevant and stores the result
            
            if one_result[1] != 0:
               
               final_match = all_documents[one_result[1]]
            if one_result[2] != 0:
               
               final_match =  all_documents[one_result[2]]
   return final_match
def algo (all_documents):# combining all the functions to get the formula and the result
   tfidf_representation = tfidf(all_documents)
   our_tfidf_comparisons = []
   for count_0, doc_0 in enumerate(tfidf_representation):
       for count_1, doc_1 in enumerate(tfidf_representation):
           our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
   return orgnize_info(our_tfidf_comparisons)
# doing this process for each doc
###############################   UI   #############################################################################################
global textInput
def raise_frame(frame): # function for raising pages
    frame.tkraise()
def Search(): # set up and start the procses of the TF IDF
    global textInput
    textInput=txt.get() # get the word from the user
    documents(textInput)# get it inside the tfidf
    textOutPut= algo(all_documents) # starts the tf idf
    lbl_10["text"] = textOutPut # bring the output to the user
    raise_frame(f2)# opens the next page to show the output
    # what to do when Search button clicked    
    
def Send(): # the algorithem for the radio buttons
    X = var.get()
    if (X == 1 or X == 3):
       raise_frame(f3)
    if (X == 2):
       raise_frame(f3)
    if (X == 4):
       raise_frame(f1)
    # what to do when review button clicked

root = Tk() # creating tk window
#creats the components of the pages & the pages
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
# setting the pages size acording to the screen size
x_cordnite = ((root.winfo_screenwidth()/2) - 500)
y_cordnite = ((root.winfo_screenheight()/2) - 325)
root.geometry(("%dx%d+%d+%d") %(1000,650,x_cordnite,y_cordnite))
root.resizable(0, 0)
root.title("Search Engine") # giving the window a name

for frame in (f1, f2, f3):
    frame.grid(row=0, column=0, sticky='news')

#page one - get Search Word
lbl_0 = Label(f1, text = "Search Engine", font = ("Arial Bold",50))
lbl_0.grid(column=1, row = 1, sticky=(W, E))
lbl_1 = Label(f1, text = "Looking for info? Type it here and we will find it for you!", font = ("Arial Bold",28))
lbl_1.grid(column=1, row = 2, sticky=(W, E))
txt = Entry(f1, width=70)
txt.grid(column = 1, row = 3, pady = 40)
txt.focus()
btn = Button(f1, text="Search", command=Search)
btn.grid(column=1, row=4)

#page two - get Feedback
var = IntVar()
lbl_4 = Label(f2, text = "Search Engine", font = ("Arial Bold",50))
lbl_4.grid(column=1, row = 1, sticky=(W, E))
lbl_10 = Label(f2, text = "txt", font = ("Arial Bold",1))
lbl_10.grid(column=1, row = 2, sticky=(W, E))
lbl_2 = Label(f2, text = "Is this was helpful? do you want something better?", font = ("Arial Bold",31))
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

#page three - L
lbl_5 = Label(f3, text = "Search Engine", font = ("Arial Bold",50))
lbl_5.grid(column=1, row = 1, sticky=(W, E))
lbl_6 = Label(f3, text = "Thank You For Helping Us Improve!", font = ("Arial Bold",44))
lbl_6.grid(column=1, row = 2, sticky=(W, E))
lbl_7 = Label(f3, text = "Please Come Back Agin For Better Answer", font = ("Arial Bold",20))
lbl_7.grid(column=1, row = 3, sticky=(W, E))
btn_11 = Button(f3, text="Try Agin", command=(lambda:raise_frame(f1)))
btn_11.grid(column=1, row=10)


###############################   Strip Html Tags   ###########################################################################################
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset() # cleans the buffer and setting up
        self.fed = []
    def handle_data(self, l): # gets word and uppend it to a list
        self.fed.append(l)
    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)#using regex to clean the html out
    def get_data(self): # getting all to words togheter
        return ''.join(self.fed)

def html_to_text(html): # building an object and activiting the class
    s = MLStripper()
    s.feed(html) # 'feeding' the class each word
    return s.get_data()

raise_frame(f1)# opening the first page - starts UI
root.mainloop() # making it to run until closed by user
