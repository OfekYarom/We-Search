###############################   Import   ##################################################################################################
from __future__ import division
import string
import math
import urllib2
###############################   Web Download   #############################################################################################
get_html = urllib2.urlopen("http://google.de")
page_source = get_html.read()

###############################   Strip Html Tags   ###########################################################################################
def strip_html_tags(html_and_txt):
   
   converted_list = list(html_and_txt)#הופך הכל לרשימה
   i,j = 0,0
	
   while i < len(converted_list):
      if converted_list[i] == '<':# כשטאג נפתח
         while converted_list[i] != '>':#מוחק הכל עד שהוא נסגר
            converted_list.pop(i)
         converted_list.pop(i)# מוחק גם את סוף הטאג
      else:
         i=i+1 # אם לא נפתח טאג ממשיך הלאה
		
   spaces='' 
   return spaces.join(converted_list) # מוסיף רווחים
print strip_html_tags (page_source)
###############################    TF - IDF   #################################################################################################
tokenize = lambda doc: doc.lower().split(" ") # מסדר את הטקסטים בפורמט

document_0 = "the create pillow."
document_1 = "the the the."
document_2 = "the pillow."
document_3 = "create pillow."
document_4 = "the create"
document_5 = "soft pillow."
document_6 = "the create"

all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]

def sublinear_term_frequency(term, tokenized_document): # מקבל מונח ומסמך
   count = tokenized_document.count(term) # סופר כמה פעמים מופיע המונח במסמך
   if count == 0:
       return 0 # אם לא קיים - מחזיר 0
   else:
      return 1 + math.log(count) # אם קיים מחזיר את כמות הפעמים אחרי לוג
#  מחזיר את כמות הפעמים שמונח מופיע בטקסט אחרי נורמליזציה (לוג)

def inverse_document_frequencies(tokenized_documents): # מקבל מסמך
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist]) # יוצר סט של כל המונחים שמופיעים בכל המסמכים
    for tkn in all_tokens_set: # לכל מונח ברשימה
        contains_token = map(lambda doc: tkn in doc, tokenized_documents) #  מעביר את כל הנתונים לרשימה ומעביר אותם לפורמט אחר
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token))) # שם במילון את ההערך של כל מילה בכך שמחלק את כמות הפעמים שמופיעה המילה בסהכ המילים
    return idf_values

# מחזיר את הערך של כל מונח על פי כמות הפעמים שהוא מופיע במסמכים האחרים

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]# הופך את המסמכים לפורמט הרלוונטי
    idf = inverse_document_frequencies(tokenized_documents) #מכניס את הערך של כל מילה על פי אידיף למשתנה
    tfidf_documents = []
    for document in tokenized_documents: #לכל מסמך
        doc_tfidf = []
        for term in idf.keys(): #מסמך  - לכל מונח בתוך קטגוריה במילון
            tf = sublinear_term_frequency(term, document)#  מציב בטי אף
            doc_tfidf.append(tf * idf[term])#  מחשב את מכפלת טי אף ואידיאף ובכך מגיע לערך הסופי של המושג
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents
# מתניע את התהליך - מקבל את הערך של כל מסמך עבור צירוף כלשהו




def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))# סוכם את הסכום של מכפלת האברים של TF ו IDF
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2])) # מציב את הנתוונים בנוסחא
    if not magnitude:
        return 0
    return dot_product/magnitude
#מנרמל את הנתונים
   
tfidf_representation = tfidf(all_documents)
our_tfidf_comparisons = []
for count_0, doc_0 in enumerate(tfidf_representation):
   for count_1, doc_1 in enumerate(tfidf_representation):
      our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
      
# מבצע את התהליך עבור כל מסמך עבור כל מסמך אחר
def orgnize_info():
   final_match = " "
   best_match = 0
   second_match = 0
   for z in zip(sorted(our_tfidf_comparisons, reverse = True)):
      
      for one_result in z: # מקבל את הערך של כל התאמה ואת המסמכים הרלוונטים להתאמה
         
         if one_result [2] == 0 or one_result[1] == 0: # מסנן את המסמכים הלא רלוונטים
            
            for solo in one_result: # מקבל את כל הערכים בתצורה בודדת
               
               if (solo < 0.999999 and solo != 0): # מסנן את כל מה שהוא לא ערך ההתאמה
                  
                  if solo > best_match: # בודק מה ההתאמה הטובה ביותר ומאחסן אותה 
                     best_match = solo
         if best_match == one_result [0]: # בודק לאיזה מסמך שהוא לא אפס ההתאמה רלוונטית ומאחסן את התוצאה ב סידור מידע
            
            if one_result[1] != 0:
               
               final_match = all_documents[one_result[1]]
            if one_result[2] != 0:
               
               final_match =  all_documents[one_result[2]]
   return final_match
   
#מבודד את המשפט בעל הניקוד הגבוהה ביותר ביחס למשפט 0 ומאחסן אותו
print orgnize_info()





























