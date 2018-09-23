###############################   Import   ##################################################################################################
from flask import Flask
import string
import math
import urllib
import urllib2
import wikipedia
import sqlite3
###############################    TF - IDF   #################################################################################################
conn = sqlite3.connect(':memory:')
c = conn.cursor()

def print_method():
    for i in c:
        print "\n"
        for j in i:
            print j

def Create_table():
    c.execute('''CREATE TABLE searchr
             (name TEXT PRIMARY KEY, score1 REAL, number1 REAL, page1 TEXT, score2 REAL, number2 REAL, page2 TEXT, score3 REAL, number3 REAL, page3 TEXT)''')

def update_score(grade, name, which_one):
    cell = select(name)
    if which_one == 1:#check which of the pages to update         
        score = cell[1]
        number = cell[2]
    else:
        if which_one == 2:
            score = cell[4]
            number = cell[5]
        else:
            score = cell[7]
            number = cell[8]
    final_grade = (score*number + grade)/(number+1)
    c.execute('''UPDATE searchr SET score%s=%s WHERE name="%s"''' % (which_one,final_grade, name))
    
    
def select(pull):#select data from DB and orgnizing the data
    info = (conn.execute(('SELECT * FROM searchr WHERE name = "%s"') % (pull)))
    list_of_info =[]
    for i in info:# getting the info incoded from the temple
        for j in i: # decoding the info
            list_of_info.append(j)
    return list_of_info

def add_info (name, score2, number2, page2, which):
    try:# checks if the name exists
        c.execute('''UPDATE searchr SET score%s=%s, number%s=%s, page%s="%s" WHERE name="%s"''' % (which, score2, which, number2, which, page2, name))
        conn.commit()
    except Exception:
        pass
     
def create_name1(name, score1, number1, page1):
    try:# checks if the name exists
        c.execute('''INSERT INTO searchr (name, score1, number1, page1) VALUES (?, ?, ?, ?)''',(name, score1, number1, page1))
        conn.commit()
    except Exception:
        pass

def create_name2(name, score1, number1, page1, score2, number2, page2):
    try:# checks if the name exists
        c.execute('''INSERT INTO searchr (name, score1, number1, page1, score2, number2, page2) VALUES (?, ?, ?, ?, ?, ?, ?)''',(name, score1, number1, page1, score2, number2, page2))
        conn.commit()
    except Exception:
        pass
def choose (name):
    try:
        info  = select(name)
        page1 = info[1]*info[2]
        if info[6] != None:
            page2= info[4]*info[5]
            if info[8] != None:
                page3= info[7]*info[8]
                if page1>page2:
                    if page1>page3:
                        PAGE= info[3]
                    else:
                        PAGE= info[9]
                else:
                    if page2>page3:
                        PAGE= info[6]
                    else:
                        PAGE= info[9]
            else:
                if page1>page2:
                    PAGE= info[3]
                else:
                    PAGE= info[6]
        else:     
            if ((info[1]) > 0.5):
                PAGE= info[3]
            else:
                PAGE= "RE"
        return PAGE
                
    except Exception:
        PAGE = "EROR"
        return PAGE
    
            
def documents (doc_0):
    
    # get the text from wikipedia according to the user input
    # the function is getting the text for each word and for the all input
    error = 0
    tokenize = lambda doc: doc.lower().split(" ") # organizing the text
    document_0 = doc_0
    all_documents = [document_0]
    check_url = ((('https://en.wikipedia.org/wiki/%s') %(doc_0)))
    check_url = check_url.replace(" ", "_")
    try:# checks if web page is working without getting errors
        urllib.urlopen(check_url)
    except urllib2.HTTPError, e:
        pass
    except urllib2.URLError, e:
        pass
    else: # if no eror acourded the program keep runing the web page
        stat1 = (urllib.urlopen(check_url)).getcode()
        if stat1 == 200:
            # if the web page contians info its keep runing.
            response = (urllib2.urlopen(check_url))
            page_source = response.read()
            if "usually refers to:" not in page_source:
                #gets the info from the web page
                Page = (wikipedia.page(("%s") % (doc_0)))
                doc_one = Page.content
                doc_two = (Page.summary)
                all_documents.append (doc_one)
                all_documents.append (doc_two)
                error = error + 1
    splited = doc_0.split()
    if ((len(splited))>1):
        #if the input is built from more than one word
        # the program gets the info for each word separately
        count = 1
        while (((len(splited))>= count)):
            word = splited[count-1]
            try:# checks if web page is working without getting errors
                (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(word))))
            except urllib2.HTTPError, e:
                pass
            except urllib2.URLError, e:
                pass
            else: # if no eror acourding its keep runing the web page
                stat = (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(word)))).getcode()
                # if the web page contians info its keep runing.
                if stat == 200:
                    amount_results = (wikipedia.search(("%s") % (word)))
                    last = 0
                    for i in amount_results:
                        if last == 0:
                            try:# checks if web page is working without getting errors
                                (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(i))))
                            except urllib2.HTTPError, e:
                                pass
                            except urllib2.URLError, e:
                                pass
                            else: # if no eror acourding its keep runing the web page
                                stat1 = (urllib.urlopen((('https://en.wikipedia.org/wiki/%s') %(i)))).getcode()
                                # if the web page contian info its keep runing.
                                if stat1 == 200:
                                    response = (urllib2.urlopen((('https://en.wikipedia.org/wiki/%s') %(i))))
                                    page_source = response.read()
                                    if "usually refers to:" not in page_source:
                                        #gets the info from the web page
                                        Page = (wikipedia.page(("%s") % (i)))
                                        doc_one = Page.content
                                        doc_two = (Page.summary)
                                        all_documents.append (doc_one)
                                        all_documents.append (doc_two)
                                        error = error + 1
                                        last = last + 1
            count = count + 1
            if (((len(splited)) < count)):
                out_put_fun =[all_documents, error, tokenize]
                return out_put_fun
    else:
        out_put_fun =[all_documents, error, tokenize]
        return out_put_fun

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
    for tkn in all_tokens_set: # for every word
        contains_token = map(lambda doc: tkn in doc, tokenized_documents) #  moving the terms into a map
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token))) # puts in dictionary the value of each word by dividing the number of times the word appears by the total words
    return idf_values

# returning this value

def tfidf(documents, tokenize):
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

def orgnize_info(our_tfidf_comparisons, all_documents):
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

@app.route('/SearchEngine/api/v1.1/<string:KEYWORD>', methods=['GET'])
def index(KEYWORD):
    textInput=KEYWORD # get the word from the user
    PAGE = choose(textInput)
    if PAGE == "EROR":
        in_put_fun = documents(textInput)# get it inside the tfidf
        all_documents = in_put_fun[0]
        error = in_put_fun[1]
        tokenize = in_put_fun[2]
        textOutPut= algo(all_documents, tokenize) # starts the tf idf
        textOutPut = textOutPut.replace("\n", "")
        textOutPut = textOutPut.replace("\'", "")
        if (len(textOutPut.split())) < 330:
            i=0
        else:
            i=1
        out_put_client = [textOutPut, i, error]
        return "%s" %(out_put_client)
    if PAGE == "RE":
        in_put_fun = documents(textInput)# get it inside the tfidf
        all_documents = in_put_fun[0]
        error = in_put_fun[1]
        tokenize = in_put_fun[2]
        textOutPut= algo(all_documents, tokenize) # starts the tf idf
        textOutPut = textOutPut.replace("\n", "")
        textOutPut = textOutPut.replace("\'", "")
        if (len(textOutPut.split())) < 330:
            i=0
        else:
            i=1
        out_put_client = [textOutPut, i, error]
        
    else:
        pass
        
        

if __name__ == '__main__':
    app.run(debug=True)
