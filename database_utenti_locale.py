import keyring

class DatabaseUtentiLocale(): 
    # Salvataggio dell'username in locale in forma di token
    @staticmethod
    def salva_email(email): 
        # Definizione del token
        id = "last_user_username"
        token = email
        # Salvataggio del token
        keyring.set_password("FlipAndLearn", id, token)

    @staticmethod
    def salva_password(password): 
        # Definizione del token
        id = "last_user_password"
        token = password
        # Salvataggio del token
        keyring.set_password("FlipAndLearn", id, token)

    # Ottenimento delle credenziali
    @staticmethod
    def get_credentials():
        # Recupero dell'username
        id_username = "last_user_username"
        username = keyring.get_password("FlipAndLearn", id_username)
        # Recupero della password
        id_password = "last_user_password"
        password = keyring.get_password("FlipAndLearn", id_password)
        return username, password

    # Rimozione delle credenziali 
    # @staticmethod   
    def remove_credentials(username):
        keyring.delete_password("myapp", username)