import sqlite3 #communicating database
import random
db = sqlite3.connect("Yritystiedot_ja_sähköpostit")

db.isolation_level = None #Changes will take effect immediately

db.execute("CREATE TABLE IF NOT EXISTS yritysten_tiedot (id INTEGER PRIMARY KEY, nimi STRING, etunimi STRING, sukunimi STRING, titteli STRING)")  #Creating table if it doesn't exists

data = None

#companys info

yritys = ""
etunimi = ""
sukunimi = ""
titteli = ""
sposti = ""


def save(data): #Function for saving data
        try:
            id = "" + ''.join(["{}".format(random.randint(0,9)) for num in range (0,6)])  #Generate id for primary key
            
            result = db.execute("SELECT nimi, etunimi, sukunimi FROM yritysten_tiedot WHERE nimi = ? AND etunimi = ? AND sukunimi = ?", [data["yritys"], data["etunimi"], data["sukunimi"]]).fetchone()
            if result is not None:
                print("Henkilö on jo listalla! ")
                return False
            else:
                db.execute("INSERT INTO yritysten_tiedot (id, nimi, etunimi, sukunimi, titteli, sposti) VALUES (?,?,?,?,?,?)",[id, data["yritys"],data["etunimi"], data["sukunimi"], data["titteli"], data["sposti"]])
                return True
        except Exception as e:
            print("Virhe: ", e)
            return False
    
def collect_data():  #function for collecting data that has to be saved
    
    data = {
    "yritys" : input("Yrityksen nimi: "),
    "etunimi" : input("Yhteyshenkilön etunimi: "),
    "sukunimi" : input("Yhteyshenkilön sukunimi: "),
    "titteli" : input("Henkilön titteli yrityksessä: "),
    "sposti" : input("Yhteyshenkilön sähköposti: ")
    } #Data in dictionary

    print("Tallennettava tieto: ", data)
    confirm = input("\n" + "Vahvistan haluavani tallentaa yllä olevat tiedot ja vakuutan tietojen oikeellisuuden (K/E) ").upper() #Confirm for willingness to save the data
    if confirm.__eq__("K"):
        if(save(data)):
            print("Data tallennettu onnistuneesti!")
        else:
            print("Datan tallennus epäonnistui")
        return True  # If confirm is K, data will be saved
    if confirm.__eq__("E"):
        return None # If confirm E, data not saved
    
def look_info(): # Function for looking contacts
    company = input("Anna sen yrityksen nimi, jonka kontakteja etsit: ")
    result = db.execute("SELECT etunimi, sukunimi, titteli, sposti FROM yritysten_tiedot WHERE LOWER(nimi) LIKE LOWER(?)", [f"%{company}%"]).fetchall()
    print(result)

# main
def main(): 
    while True: 
        question = input("Etsitkö tietoja vai haluatko tallentaa niitä? Kirjoita T/E ").upper()  #defining task to execute
    
        if not question.__eq__("T") and not question.__eq__("E"):  #Checking if the answer is ok

            print("Anna vastauksena T tai E ")
            continue
    
        if question.__eq__("T"): #User wants to put data
            collect_data()
        elif question.__eq__("E"):  #User wants to look contact
            look_info()
        question2 = input("Haluatko lisätä muita tietoja tai lukea tietoja? Kirjoita K/E ").upper()

        if question2.__eq__("K"):
            continue  # Let's go back to line 64
        if question2.__eq__("E"):
            break  #Breaking main


print(main())