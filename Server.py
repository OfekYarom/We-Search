###############################   Import   ##################################################################################################
from flask import Flask
import string
import math
import urllib
import wikipedia
import sqlite3
import uuid
###############################    TF - IDF   #################################################################################################
conn = sqlite3.connect('dbe.db', check_same_thread=False) # Contacting the DataBase
c = conn.cursor()



def Create_table(): #Creates the table if the database is empty
    try:
        c.execute('''CREATE TABLE Searches
                         (ID TEXT PRIMARY KEY,SearchName TEXT, Score REAL, Number REAL, Page TEXT, Place REAL)''')
    except Exception:
        pass

def select_all(pull):# Selects data from DB and orgnizing the data
    info = (conn.execute(('SELECT * FROM Searches WHERE SearchName = "%s"') % (pull)))
    list_of_info =[]
    for i in info:# Getting the info from SearchesDB Table
        for j in i: # Getting the info from the list
            list_of_info.append(j)
    return list_of_info

def select_one(ID):# Selects data from DB and orgnizing the data
    info = (conn.execute(('SELECT * FROM Searches WHERE ID = "%s"') % (ID)))
    list_of_info =[]
    for i in info:# Getting the info from SearchesDB Table
        for j in i: # Getting the info from the list
            list_of_info.append(j)
    return list_of_info

def CREATE_ID():  #function that create an uniqe id for each item in DB
    ID=str(uuid.uuid4()).replace('-','')
    try:
        select_one(ID)
        ID=str(uuid.uuid4()).replace('-','')
    except Exception:
        pass
    return ID

def create_name(ID, SearchName , Score, Page, Place):  #function that gets called whenever a New info is added to DB for an New Search
    c.execute('''INSERT INTO Searches (ID, SearchName , Score, Number, Page, Place) VALUES (?, ?, ?, ?, ?, ?)''',(ID, SearchName , Score, 1, Page, Place))
    conn.commit()

def update_score(Score, ID):#function that gets called whenever the client gave a feedback
    cell = select_one(ID) # Gets the info about the Search Name the user is trying to update
    the_grade = Score
    if the_grade == 1:
        the_grade = 0.12
    NewScore = (cell[2]*cell[3] + Score)/(cell[3]+1)
    c.execute('''UPDATE Searches SET score=%s,  number=%s WHERE ID="%s"''' % (NewScore, (cell[3]+1), ID))# Updating the database with the new score
    conn.commit()
    
def choose (SearchName): #Choose the best option for an info request or trying to find new info
    try:
        cell = select_all(SearchName)
        amount_of_info = len(cell)/6
        size = len(cell)/6
        score = 0
        deffult = 0
        while(amount_of_info != 0):
            if (score < cell[(amount_of_info*6-4)]):
                score = cell[(amount_of_info*6-4)]
                PAGE = cell[(amount_of_info*6-2)]
                ID = cell[(amount_of_info*6-6)]
                if (PAGE.lower() == SearchName):
                    deffult = 1
            
            amount_of_info = amount_of_info - 1
            
            choice =[PAGE, (len(cell)/6), deffult, ID]
            if (score < 0.06):
                choice =["RE", (len(cell)/6), deffult, 0]
        return choice
    except Exception:
        choice = ["EROR",0, 0, 0]
        return choice
    
            
def documents (doc_0, chance, deffult):
    
    # get the text from wikipedia according to the user input
    # the function is getting the text for each word and for the all input
    error = 0
    title =[]
    tokenize = lambda doc: doc.lower().split(" ") # organizing the text
    all_documents = [doc_0]    
    try:# checks if web page is working without any errors
        #gets the info from the web page
        if deffult == 0:
            Page = (wikipedia.page(("%s") % (doc_0)))
            title.append(Page.title)
            doc_one = Page.content
            doc_two = Page.summary
            all_documents.append (doc_one)
            all_documents.append (doc_two)
            error = error + 1
    except Exception:
        pass
    try:# checks if web page is working without any errors
        amount_results = (wikipedia.search(("%s") % (doc_0)))
        amount_results = amount_results[1:]
        amount_results = amount_results[(2*chance):]
        last = 0
        for i in amount_results:
            if last == 0:
                try:# checks if web page is working without any errors
                    Page = (wikipedia.page(("%s") % (i)))
                    title.append(Page.title)
                    doc_one = Page.content
                    doc_two = (Page.summary)
                    all_documents.append (doc_one)
                    all_documents.append (doc_two)
                    error = error + 1
                    last = last + 1
                except Exception:
                    pass
    except Exception:
        pass

    splited = doc_0.split()
    if ((len(splited))>1):
        #if the input is built from more than one word
        # the program gets the info for each word separately
        count = 1
        while (((len(splited))>= count)):
            word = splited[count-1]
            try:# checks if web page is working without any errors
                    amount_results = (wikipedia.search(("%s") % (word)))
                    amount_results = amount_results[(2*chance):]
                    last = 0
                    for i in amount_results:
                        if last == 0:
                            try:# checks if web page is working without any errors
                                Page = (wikipedia.page(("%s") % (i)))
                                title.append(Page.title)
                                doc_one = Page.content
                                doc_two = (Page.summary)
                                all_documents.append (doc_one)
                                all_documents.append (doc_two)
                                error = error + 1
                                last = last + 1
                            except Exception:
                                pass
            except Exception:
                pass

            count = count + 1
            if (((len(splited)) < count)):
                out_put_fun =[all_documents, error, tokenize, title]
                return out_put_fun
    else:
        out_put_fun =[all_documents, error, tokenize, title] 
        return out_put_fun

def sublinear_term_frequency(term, tokenized_document): # getting the term and the docs # calling the function (getting it all togheter)
   count = tokenized_document.count(term) # counting how many times the term is shown in the doucement
   if count == 0:
       return 0 # if doesnt shown once returning 0
   else:
      return 1 + math.log(count) 
# if shown returning the number of times after normalization (log)

def inverse_document_frequencies(tokenized_documents): # getting a document
    idf = {}
    all_tokens = set([item for sublist in tokenized_documents for item in sublist]) # creating a set of all the terms in all the documents
    for tkn in all_tokens: # for every word
        token = map(lambda doc: tkn in doc, tokenized_documents) #  nurmlizing all words inside the doc
        idf[tkn] = 1 + math.log(len(tokenized_documents)/(sum(token))) # puts in dictionary the value of each word by dividing the number of times the word appears by the total words
    return idf

# returning this value

def tfidf(documents, tokenize):
    tokenized_documents = [tokenize(d) for d in documents]# converting the documents to a different format
    idf = inverse_document_frequencies(tokenized_documents) #putting the value of each word in a varbile
    tfidf_documents = []
    for document in tokenized_documents: # for each doc
        doc_tfidf = []
        for term in idf.keys(): #for each catgory in the dictionary
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])#  Calculates the product of the idf and tf
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents
# getting all the functions to work togheter



def cosine_similarity(grades1, grades2):
    dot = sum(p*q for p,q in zip(grades1, grades2))# Calculates the sum of the idf and tf
    magnitude = math.sqrt(sum([grade**2 for grade in grades1])) * math.sqrt(sum([grade**2 for grade in grades2])) # put the results in the Tf Idf Formula
    if not magnitude:
        return 0
    return dot/magnitude
# normalization

def orgnize_info(our_tfidf_comparisons, all_documents):
    final_match = " "
    best_match = 0
    number = 0
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
                    number = one_result[1]
                if one_result[2] != 0:
                    final_match =  all_documents[one_result[2]]
                    number = one_result[2]
    number = number - 1
    final = [final_match, best_match, number]
    return final

def algo (all_documents,tokenize):# combining all the functions to get the formula and the result
   tfidf_representation = tfidf(all_documents, tokenize)
   our_tfidf_comparisons = []
   for count_0, doc_0 in enumerate(tfidf_representation):
       for count_1, doc_1 in enumerate(tfidf_representation):
           our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
   return orgnize_info(our_tfidf_comparisons, all_documents)
# doing this process for each doc

###############################   FLASK   #############################################################################################

app = Flask(__name__)

@app.route('/SearchEngine/api/v1.0/<string:KEYWORD>', methods=['GET']) # Handling an info request from the client
def index(KEYWORD):
    Create_table()
    textInput=KEYWORD # get the word from the user
    PAGE = choose(textInput) # Checking the DB and deciding which work pattern is the best for every request
    size = PAGE[1]
    deffult = PAGE[2]
    iza = PAGE[3]
    PAGE = PAGE[0]
    if PAGE == "EROR": # If No info is exists about the search
        in_put_fun = documents(textInput,0, 0)# Getting info and preparing for the TF IDF
        all_documents = in_put_fun[0]
        error = in_put_fun[1]
        tokenize = in_put_fun[2]
        title = in_put_fun[3]
        textOutPut= algo(all_documents, tokenize) # Starts the tf idf
        textOut = textOutPut[1]
        ID= CREATE_ID()
        if (len(textOutPut[0].split())) < 330:
            i=0
        else:
            i=1
        if (len(textOutPut[0].split()))  > 2:
            title = title[((textOutPut[2]-1)/2)]
            where = (textOutPut[2]%2) #  Gets info about the text
            create_name(ID ,textInput, textOut, title, where) #updating the DB 
        textOutPut = textOutPut[0].replace("\n", "")
        textOutPut = textOutPut.replace("\'", "")
        out_put_client = [textOutPut, ID, i, error]
        return "%s" %(out_put_client) # Returns it to the client
    if PAGE == "RE": # if the info existing in the DB isn't good enough
        in_put_fun = documents(textInput,size, deffult)# Getting info and preparing for the TF IDF
        all_documents = in_put_fun[0]
        error = in_put_fun[1]
        tokenize = in_put_fun[2]
        title = in_put_fun[3]
        textOutPut= algo(all_documents, tokenize) # starts the tf idf
        textOut = textOutPut[1]
        ID = CREATE_ID()
        if (len(textOutPut[0].split())) < 330:
            i=0
        else:
            i=1
        if (len(textOutPut[0].split()))  > 2:
            title = title[((textOutPut[2]-1)/2)]# Gets info about the text
            where = (textOutPut[2]%2)
            create_name(ID ,textInput, textOut, title, where) #updating the DB 
        textOutPut = textOutPut[0].replace("\n", "")
        textOutPut = textOutPut.replace("\'", "")
        out_put_client = [textOutPut, ID, i, error]
        return "%s" %(out_put_client) # Returns it to the client
    else: # If great info existing in DB
        list_of_info = select_one(iza)
        Page = (wikipedia.page(("%s") % (list_of_info[4]))) # Gets the full info from the web
        where = list_of_info[5]
        if where == 1:
            textOutPut = Page.summary
        else:
            textOutPut = Page.content
        textOutPut = textOutPut.replace("\n", "")
        textOutPut = textOutPut.replace("\'", "")
        if (len(textOutPut.split())) < 330:
            i=0
        else:
            i=1
        out_put_client = [textOutPut, iza, i, 1]
        return "%s" %(out_put_client) # Returns it to the client
@app.route('/SearchEngine/feedback/v1.1/<string:ID>/<int:THESCORE>', methods=['GET'])
def feedback(ID, THESCORE): # Getting the client feedback about the info
    update_score(THESCORE, ID) # Updating the score of the search info
    

        
        

if __name__ == '__main__':
    app.run(debug=True)
