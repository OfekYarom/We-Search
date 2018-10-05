###############################   Import   ##################################################################################################
from flask import Flask
import string
import math
import urllib
import wikipedia
import sqlite3
###############################    TF - IDF   #################################################################################################
conn = sqlite3.connect('example.db', check_same_thread=False) # Contacting the DataBase
c = conn.cursor()


def Create_table(): #Creates the table if the database is empty
    try:
        c.execute('''CREATE TABLE searchr
                 (name TEXT PRIMARY KEY, score1 REAL, number1 REAL, page1 TEXT,where1 REAL, score2 REAL, number2 REAL, page2 TEXT,where2 REAL, score3 REAL, number3 REAL, page3 TEXT, where3 REAL)''')
    except Exception:
        pass

def update_score(grade, name, which_one):#function that gets called whenever the client gave a feedback
    cell = select(name) # Gets the info about the Search Name the user is trying to update
    the_grade = grade
    if the_grade == 1:
        the_grade = 0.24
    if which_one == 1:# Check which of the pages of this search to update         
        score = cell[1]
        number = cell[2]
    else:
        if which_one == 2:
            score = cell[5]
            number = cell[6]
        else:
            score = cell[9]
            number = cell[10]
    final_grade = (score*number + the_grade)/(number+1)
    number = number + 1 # Preparing the stats for the update
    c.execute('''UPDATE searchr SET score%s=%s,  number%s=%s WHERE name="%s"''' % (which_one,final_grade,which_one,number, name))# Updating the database with the new score
    
    
def select(pull):# Selects data from DB and orgnizing the data
    info = (conn.execute(('SELECT * FROM searchr WHERE name = "%s"') % (pull)))
    list_of_info =[]
    for i in info:# Getting the info from DB Table
        for j in i: # Getting the info from the list
            list_of_info.append(j)
    return list_of_info

def add_info (name, score2, number2, page2, where2):    #function that gets called whenever a New info is added to DB for an existing Search
    try: # Checks if the name exists
        info  = select(name)
        if info[3] != page2 and info[7] != page2:
            if info[7] != None:
                c.execute('''UPDATE searchr SET score%s=%s, number%s=%s, page%s="%s", where%s=%s WHERE name="%s"''' % (3, score2, 3, number2, 3, page2, 3, where2, name))
            else:
                c.execute('''UPDATE searchr SET score%s=%s, number%s=%s, page%s="%s", where%s=%s WHERE name="%s"''' % (2, score2, 2, number2, 2, page2, 2, where2, name))
            conn.commit()
    except Exception:
        pass
def create_name(name, score1, number1, page1, where1):  #function that gets called whenever a New info is added to DB for an New Search
    c.execute('''INSERT INTO searchr (name, score1, number1, page1, where1) VALUES (?, ?, ?, ?, ?)''',(name, score1, number1, page1, where1))
    conn.commit()

def choose (name): #Choose the best option for an info request or trying to find new info
    try:
        info  = select(name)
        page1 = info[1]
        size = 1
        deffult = 0
        if info[3].lower() == name:
            deffult = 1
        if info[6] != None:
            size = 2
            if info[7].lower() == name:
                deffult = 1
            page2= info[5]
            if info[9] != None:
                if info[11].lower() == name:
                    deffult = 1
                page3= info[9]
                if page1>page2:
                    if page1>page3:
                        best = page1
                        PAGE= info[3]
                        iza = 1
                    else:
                        iza = 3
                        best = page3
                        PAGE= info[11]
                else:
                    if page2>page3:
                        best = page2
                        iza = 2
                        PAGE= info[7]
                    else:
                        best = page3
                        iza = 3
                        PAGE= info[11]
            else:
                if page1>page2:
                    iza = 1
                    best = page1
                    PAGE= info[3]
                else:
                    iza = 2
                    best = page2
                    PAGE= info[7]
        else:
            PAGE = info[3]
            iza = 1
            best = page1
        if (best < 0.12 and info[11] == None):
            PAGE= "RE"
            iza = 3
            if info[7] != None:
                iza = 2
            
        choice =[PAGE, size, deffult, iza, info]
        return choice
                
    except Exception:
        PAGE = "EROR"
        choice = [PAGE,0, 0, 1]
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
        if chance == 1:
            amount_results = amount_results[2:]
        if chance == 2:
            amount_results = amount_results[4:]
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
                    if chance == 1:
                        amount_results = amount_results[2:]
                    if chance == 2:
                        amount_results = amount_results[4:]
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
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist]) # creating a set of all the terms in all the documents
    for tkn in all_tokens_set: # for every word
        contains_token = map(lambda doc: tkn in doc, tokenized_documents) #  nurmlizing all words inside the doc
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token))) # puts in dictionary the value of each word by dividing the number of times the word appears by the total words
    return idf_values

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



def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))# Calculates the sum of the idf and tf
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2])) # put the results in the Tf Idf Formula
    if not magnitude:
        return 0
    return dot_product/magnitude
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
        if (len(textOutPut[0].split())) < 330:
            i=0
        else:
            i=1
        if (len(textOutPut[0].split()))  > 2:
            title = title[((textOutPut[2]-1)/2)]
            where = (textOutPut[2]%2) #  Gets info about the text
            create_name(textInput, textOut, 1, title, where) #updating the DB 
        textOutPut = textOutPut[0].replace("\n", "")
        textOutPut = textOutPut.replace("\'", "")
        out_put_client = [textOutPut, 1, i, error]
        return "%s" %(out_put_client) # Returns it to the client
    if PAGE == "RE": # if the info existing in the DB isn't good enough
        in_put_fun = documents(textInput,size, deffult)# Getting info and preparing for the TF IDF
        all_documents = in_put_fun[0]
        error = in_put_fun[1]
        tokenize = in_put_fun[2]
        title = in_put_fun[3]
        textOutPut= algo(all_documents, tokenize) # starts the tf idf
        textOut = textOutPut[1]
        if (len(textOutPut[0].split())) < 330:
            i=0
        else:
            i=1
        if (len(textOutPut[0].split()))  > 2:
            title = title[((textOutPut[2]-1)/2)]# Gets info about the text
            where = (textOutPut[2]%2)
            add_info (textInput, textOut, 1, title, where)# updating the DB 
        textOutPut = textOutPut[0].replace("\n", "")
        textOutPut = textOutPut.replace("\'", "")
        out_put_client = [textOutPut, iza, i, error]
        return "%s" %(out_put_client) # Returns it to the client
    else: # If great info existing in DB
        list_of_info = select(textInput) 
        if PAGE == list_of_info[3]:
            where = list_of_info[4]
            list_of_info = list_of_info[3]
        else:
            if PAGE == list_of_info[7]:
                where = list_of_info[8]
                list_of_info = list_of_info[7]
            else:
                where = list_of_info[12]
                list_of_info = list_of_info[11]
        Page = (wikipedia.page(("%s") % (list_of_info))) # Gets the full info from the web
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
@app.route('/SearchEngine/feedback/v1.1/<string:THEWORD>/<int:THESCORE>/<int:WHICH>', methods=['GET'])
def feedback(THEWORD, THESCORE, WHICH): # Getting the client feedback about the info
    update_score(THESCORE, THEWORD, WHICH) # Updating the score of the search info
    

        
        

if __name__ == '__main__':
    app.run(debug=True)
