import firebase_admin
from firebase_admin import db, credentials, firestore
import bcrypt
import random
import os

# Struttura del database
# utenti
#   |--> username
#   |       |--> email
#   |       |--> lingua_da_tradurre
#   |       |--> numero_vocaboli
#   |       |--> password (Nonlasapraimai001!)
#   |       |--> vocaboli
#   |               |--> ID vocabolo
#   |                         |--> eng
#   |                         |--> esempio
#   |                         |--> ita
#   |                         |--> priority
#   |                         |--> uso
#   |               |--> vocaboli_priorities

# Inizializzazione - Connessione al/creazione di un database
path_credenziali = os.path.abspath(os.path.dirname(__file__)) + "/CredenzialiDatabase/credentials.json"
cred = credentials.Certificate(path_credenziali) 
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://flipandlearn-28204-default-rtdb.europe-west1.firebasedatabase.app/"
})

class Database: 

    # Inizializzazione delle informazioni sull'utente loggato
    logged_email = None
    logged_username = None
    logged_lingua_da_tradurre = None
    vocabolo_da_mostrare = None
    vocabolo_mostrato_id = None
    lista_vocaboli_aggiornata = 1

    # PARAMETRI
    VOCABOLO_PRIORITY_MAX = 3

    @staticmethod
    def estrai_username(email): 
        # Estrai l'username dalla email
        username = email.split('@')[0]
        username = username.replace('.', '_')
        # Return
        return username


    # Signup - Verifica se c'è già un utente il cui username (derivato dalla mail) è uguale
    @staticmethod # Metodo utilizzabile anche senza definire un'istanza della classe
    def is_emailValid(email):
        # Estrazione dell'usernamea a partire dalla mail
        username = Database.estrai_username(email)
        # Riferimento degli utenti esistenti
        utenti = db.reference('utenti')
        # Verifica se è presente un utente con un username uguale a quello appena ottenuto
        if utenti.child(username).get():
            return False  # Email non valida, esiste già
        else:
            return True  # Email valida, non esiste
    
    # Signup - Creazione di un nuovo utente
    @staticmethod
    def create_new_user(email, password): 
        # Estrazione dell'username a partire dalla mail
        username = Database.estrai_username(email)
        # Codifica della password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Struttura del nuovo utente
        nuovo_utente = {
            "email": email, 
            "password": hashed_password.decode('utf-8'), 
            "vocaboli": [], 
            "numero_vocaboli": 0,
            "lingua_da_tradurre": "ita",
        }
        # Creazione del nuovo utente
        try: 
            # Riferimento degli utenti esistenti
            utenti = db.reference("utenti")
            # Creazione di nuovo figlio chiamato "username" e con la struttura di "nuovo_utente"
            utenti.child(username).set(nuovo_utente)
            return True
        except: 
            return False
    
    # Cancellazione di un utente
    @staticmethod
    def delete_user(email): 
        # Estrazione dell'username a partire dalla mail
        username = Database.estrai_username(email)
        # Riferimento dell'utente da cancellare
        utente_da_cancellare = db.reference(f"utenti/{username}")
        # Controlla se l'utente esiste
        if utente_da_cancellare.get() is not None: 
            # Elimina l'utente
            utente_da_cancellare.delete()
        else: 
            pass
    
    # Cancellazione di tutti gli utenti
    @staticmethod
    def delete_all_users():
        # Riferimento alla root degli utenti
        utenti = db.reference("utenti")
        try:
            # Elimina tutti gli utenti
            utenti.delete()
        except:
            pass
    
    # Login - Verifica che esista un utente con la mail (e quidni l'username) e la password uguali a quelle indicate dall'utnete
    @staticmethod
    def is_userValid(email_inserita, password_inserita): 
        # Estrazione dello username a partire dalla password
        username = Database.estrai_username(email_inserita)

        # Riferimento al nodo dell'utente specifico
        utente_trovato_ref = db.reference(f"utenti/{username}")
        utente_trovato = utente_trovato_ref.get()

        # Estrazione dell'email
        email_trovata_ref = db.reference(f"utenti/{username}/email")
        email_trovata = email_trovata_ref.get()

        # Verifica che l'utente esista all'interno del database
        if (utente_trovato is None) or (email_trovata != email_inserita):
            return False
    
        # Recupero della password dell'utente identificato
        hashed_password_trovata = utente_trovato['password']

        # Verifica la password fornita con l'hash salvato nel database
        if bcrypt.checkpw(password_inserita.encode('utf-8'), hashed_password_trovata.encode('utf-8')):
            # Aggiornamento delle informazioni sull'utente loggato
            Database.logged_email = email_inserita
            Database.logged_username = username
            # Aggiornamento della lingua da tradurre
            lingua_da_tradurre_ref = db.reference(f"utenti/{Database.logged_username}/lingua_da_tradurre")
            Database.logged_lingua_da_tradurre = lingua_da_tradurre_ref.get()
            # Creazione del dizionario delle priorità
            Database.download_priority_vector()

            return True
        else:
            return False
        
    # Aggiunta di un nuovo vocabolo
    @staticmethod
    def aggiungi_vocabolo(vocabolo_ita, vocabolo_eng, vocabolo_uso, vocabolo_es): 
        if vocabolo_ita: 
            vocabolo_ita = vocabolo_ita[0].upper() + vocabolo_ita[1:]
        if vocabolo_eng: 
            vocabolo_eng = vocabolo_eng[0].upper() + vocabolo_eng[1:]
        if vocabolo_uso: 
            vocabolo_uso = vocabolo_uso[0].upper() + vocabolo_uso[1:]
        if vocabolo_es: 
            vocabolo_es = vocabolo_es[0].upper() + vocabolo_es[1:]
        # Definizione del nuovo vocabolo
        nuovo_vocabolo = {
            "ita": vocabolo_ita,
            "eng": vocabolo_eng, 
            "uso": vocabolo_uso, 
            "esempio": vocabolo_es,
        }
        try: 
            ### Salvataggio del nuovo vocabolo
            # Riferimento del numero di vocaboli
            numero_vocaboli_utente_ref = db.reference(f"utenti/{Database.logged_username}/numero_vocaboli")
            # Lettura del numero di vocaboli
            numero_vocaboli_utente = numero_vocaboli_utente_ref.get()
            # Incremento del numero di vocaboli
            numero_vocaboli_utente = numero_vocaboli_utente + 1
            # Riferimento in cui salvare i vocaboli
            vocaboli_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli/")
            # Salvataggio del nuovo vocabolo
            vocaboli_ref.child(str(numero_vocaboli_utente)).set(nuovo_vocabolo)
            # Incremento del numero di vocaboli dell'utente
            numero_vocaboli_utente_ref.set(numero_vocaboli_utente)

            ### Salvataggio della nuova priorità
            nuova_priority = {
                "id": numero_vocaboli_utente,
                "priority": Database.VOCABOLO_PRIORITY_MAX,
            }
            # Salvataggio della priorità del nuovo vocabolo
            vocaboli_priorities_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli_priorities/")
            # Salvataggio della priorità del vocabolo
            vocaboli_priorities_ref.child(str(numero_vocaboli_utente)).set(nuova_priority)
            # Scarica nuovamente il dizionario delle priorità
            Database.download_priority_vector()
            # Flag - Database da aggiornare
            Database.lista_vocaboli_aggiornata = 1
            # Return 
            return True
        except Exception as e:
            # Return
            return False

    # Cambia la lingua da tradurre in italiano
    @staticmethod
    def switch_to_italian(): 
        # Modifica del database
        try:
            # Riferimento della lingua da tradurre all'interno del database
            lingua_da_tradurre_ref = db.reference(f"utenti/{Database.logged_username}/lingua_da_tradurre")
            # Modifica del database
            lingua_da_tradurre_ref.set("ita")
            # Modifica del database locale
            Database.logged_lingua_da_tradurre = "ita"
            # Return 
            return True
        except Exception as e: 
            # Return
            return False
            
    # Cambia la lingua da tradurre in inglese
    @staticmethod
    def switch_to_english(): 
        # Modifica del database
        try:
            # Riferimento della lingua da tradurre all'interno del database
            lingua_da_tradurre_ref = db.reference(f"utenti/{Database.logged_username}/lingua_da_tradurre")
            # Modifica del database
            lingua_da_tradurre_ref.set("eng")
            # Modifica del database locale
            Database.logged_lingua_da_tradurre = "eng"
            # Return 
            return True
        except Exception as e: 
            # Return
            return False

    @staticmethod  
    def download_priority_vector(): 
        # Riferimento del vettore delle priorità
        priority_dictionary_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli_priorities/")
        # Download della priority vector
        Database.dizionario_priority = priority_dictionary_ref.get()
        
        Database.almeno_un_vocabolo = 0
        if Database.dizionario_priority is not None: 
            # Cancellazione degli elementi pari a None (se ne genera sempre uno)
            Database.dizionario_priority = [item for item in Database.dizionario_priority if item is not None]
            # Verifica se c'è almeno un vocabolo visualizzabile
            for vocabolo in Database.dizionario_priority: 
                if vocabolo is not None: 
                    if vocabolo.get("cancellato") is None: 
                        Database.almeno_un_vocabolo = 1
                        break

    
    # Ottenimento dell'ID del vocabolo da visualizzare
    @staticmethod
    def cambia_vocabolo():
        # Definizione di un vettore contenente i numeri compresi tra 1 e Database.VOCABOLO_PRIORITY_MAX
        possible_priorities = list(range(1, Database.VOCABOLO_PRIORITY_MAX + 1))

        # Verifica che ci siano vocaboli
        if Database.dizionario_priority is not None and Database.almeno_un_vocabolo == 1: 
            # Riordino casuale del dizionario delle priorità
            random.shuffle(Database.dizionario_priority)

            # Ottieni il primo vocabolo con priorità pari a priority
            id_trovato = 0
            while id_trovato == 0: 
                # Identificazione di una priorità creando un numero randomico tra 1 e VOCABOLO_PRIORITY_MAX. 
                priority = random.choices(possible_priorities, possible_priorities)[0]
                for vocabolo in Database.dizionario_priority: 
                    if vocabolo.get("priority") == priority: 
                        if vocabolo.get("cancellato") is None: 
                            id_trovato = 1
                            vocabolo_id = vocabolo["id"]
                            Database.vocabolo_mostrato_id = vocabolo_id
            
            # Ottenimento del vocabolo selezionato
            vocabolo_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli/{vocabolo_id}/")
            vocabolo = vocabolo_ref.get()
            # Return del vocabolo
            Database.vocabolo_da_mostrare = vocabolo
        else: 
            Database.vocabolo_da_mostrare = None

    # Aumenta priorità vocabolo
    @staticmethod
    def aumenta_priority(): 
        if Database.vocabolo_da_mostrare is not None: 
            # Modifica il database locale
            for vocabolo in Database.dizionario_priority: 
                if vocabolo["id"] == Database.vocabolo_mostrato_id: 
                    # Calcolo della nuova priorità
                    old_priority = vocabolo["priority"]
                    new_priority = min(old_priority + 1, Database.VOCABOLO_PRIORITY_MAX)
                    # Modifica del database locale
                    vocabolo["priority"] = new_priority
                    # Modifica la priorità nel database Firebase
                    priority_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli_priorities/{Database.vocabolo_mostrato_id}/priority")
                    priority_ref.set(new_priority)
                    break

    # Diminuisci la priroità del vocabolo
    @staticmethod
    def diminuisci_priority():
        if Database.vocabolo_da_mostrare is not None: 
            # Modifica il database locale
            for vocabolo in Database.dizionario_priority: 
                if vocabolo["id"] == Database.vocabolo_mostrato_id: 
                    # Calcolo della nuova priorità
                    old_priority = vocabolo["priority"]
                    new_priority = max(old_priority - 1, 1)
                    # Modifica del database locale
                    vocabolo["priority"] = new_priority
                    # Modifica la priorità nel database Firebase
                    priority_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli_priorities/{Database.vocabolo_mostrato_id}/priority")
                    priority_ref.set(new_priority)
                    break
    
    # Cancella vocabolo
    @staticmethod
    def cancella_vocabolo(id): 
        # Riferimento del vocabolo da cancellare
        vocabolo_da_cancellare_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli/{id}/cancellato")
        vocabolo_da_cancellare_ref.set(1)

        # Cancellazione dalla tabella delle priorità
        vocabolo_da_cancellare_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli_priorities/{id}/cancellato")
        vocabolo_da_cancellare_ref.set(1)

        # Scarica la priority vector aggiornata
        Database.download_priority_vector()

        # Aggiornamento lista vocaboli
        Database.lista_vocaboli_aggiornata = 1

    # Aggiorna vocabolo
    @staticmethod
    def aggiorna_vocabolo(id, eng, ita, uso, esempio): 
        # eng
        eng_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli/{id}/eng")
        eng_ref.set(eng)
        # ita
        ita_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli/{id}/ita")
        ita_ref.set(ita)
        # uso
        uso_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli/{id}/uso")
        uso_ref.set(uso)
        # esempio
        esempio_ref = db.reference(f"utenti/{Database.logged_username}/vocaboli/{id}/esempio")
        esempio_ref.set(esempio)

        # Aggiornamento lista vocaboli
        Database.lista_vocaboli_aggiornata = 1



