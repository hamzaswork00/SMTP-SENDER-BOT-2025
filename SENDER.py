import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import base64
import os

# Mot de passe chiffré
ENCRYPTED_PASSWORD = b'ZXJyb3JfNDA0X3Nk'

def decrypt_password():
    return base64.b64decode(ENCRYPTED_PASSWORD).decode()

def afficher_titre():
    print("""
    ███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗  ██████╗ ███████╗██████╗ 
    ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔════╝ ██╔════╝██╔══██╗
    ███████╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝██║  ███╗█████╗  ██████╔╝
    ╚════██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔═══╝ ██║   ██║██╔══╝  ██╔═══╝ 
    ███████║███████╗██║ ╚████║██████╔╝███████╗██║     ╚██████╔╝███████╗██║     
    ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝      ╚═════╝ ╚══════╝╚═╝     
    PRESTIGE BUILT by : @error_404_ma
    """)

def charger_configuration(fichier_config):
    config = {}
    with open(fichier_config, "r") as f:
        for line in f:
            key, value = line.strip().split('|')
            config[key.strip()] = value.strip()
    return config

def charger_letter(fichier_letter, format_html):
    with open(fichier_letter, "r") as f:
        contenu = f.read()
    if format_html.lower() == "html":
        return contenu
    else:
        return MIMEText(contenu, "plain")

def envoyer_email(smtp_info, letter, liste_emails):
    try:
        # Connexion au serveur SMTP
        context = ssl.create_default_context()
        if smtp_info["SSL"].lower() == "tls":
            server = smtplib.SMTP(smtp_info["HOST"], int(smtp_info["PORT"]))
            server.starttls(context=context)
        else:
            server = smtplib.SMTP_SSL(smtp_info["HOST"], int(smtp_info["PORT"]), context=context)
        
        # Authentification
        server.login(smtp_info["USER"], smtp_info["PASSWORD"])
        
        # Préparation et envoi des emails
        for email in liste_emails:
            msg = MIMEMultipart()
            msg['From'] = smtp_info["NameSender"]
            msg['To'] = email
            msg['Subject'] = Header(input("Entrez l'objet de l'email : "), 'utf-8')
            
            # Ajout du contenu (HTML ou texte brut)
            msg.attach(MIMEText(letter, 'html' if smtp_info["LetterType"] == "html" else 'plain'))
            
            # Envoi
            server.sendmail(smtp_info["EmailSender"], email, msg.as_string())
            print(f"Email envoyé à {email}")
        
        server.quit()
        print("Tous les emails ont été envoyés avec succès.")
    
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")

def main():
    afficher_titre()
    password = input("Entrez le mot de passe : ")
    if password != decrypt_password():
        print("Mot de passe incorrect !")
        return
    
    # Chargement des fichiers nécessaires
    fichier_config = input("Entrez le chemin du fichier Config.txt : ")
    fichier_letter = input("Entrez le chemin du fichier Letter.txt : ")
    fichier_maillist = input("Entrez le chemin du fichier maillist.txt : ")

    smtp_info = charger_configuration(fichier_config)
    format_html = input("La lettre est-elle en format HTML ou TXT ? (html/txt) : ")
    smtp_info["LetterType"] = format_html
    letter = charger_letter(fichier_letter, format_html)
    
    # Chargement des emails
    with open(fichier_maillist, "r") as f:
        liste_emails = [email.strip() for email in f.readlines()]
    
    envoyer_email(smtp_info, letter, liste_emails)

if __name__ == "__main__":
    main()
