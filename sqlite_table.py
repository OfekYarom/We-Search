import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()

def print_method():
    for i in c:
        print "\n"
        for j in i:
            print j

def Create_table():
    c.execute('''CREATE TABLE searchr
             (name TEXT PRIMARY KEY, score1 REAL, number1 REAL, page1 TEXT, score2 REAL, number2 REAL, page2 TEXT)''')

def update_score(grade, name, which_one):
    cell = select(name)
    if which_one == 1:#check which of the pages to update         
        score = cell[1]
        number = cell[2]
    else:
        score = cell[4]
        number = cell[5]
    final_grade = (score*number + grade)/(number+1)
    c.execute('''UPDATE searchr SET score%s=%s WHERE name="%s"''' % (which_one,final_grade, name))
    
    
def select(pull):#select data from DB and orgnizing the data
    info = (conn.execute(('SELECT * FROM searchr WHERE name = "%s"') % (pull)))
    list_of_info =[]
    for i in info:# getting the info incoded from the temple
        for j in i: # decoding the info
            list_of_info.append(j)
    return list_of_info

def add_info (name, score2, number2, page2):
    try:# checks if the name exists
        c.execute('''UPDATE searchr SET score2=%s, number2=%s, page2="%s" WHERE name="%s"''' % (score2, number2, page2, name))
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
            if page1>page2:
                print "hey"
            else:
                print "bey"
        else:
            if ((page1) > 0.5):
                print "hey1"
            else:
                print "bey1"
                
    except Exception:
        print "eror"
    
            

    
Create_table()


create_name2 ("ofek", 0.75, 5, "www.ksksk", 0.73, 6, "www.kksk")



create_name1 ("omer", 90, 3, "www.kd/nnndnd")


conn.commit()



c.execute('select * from searchr')

print_method()
