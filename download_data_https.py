import subprocess
import os

# DOWNLOAD via wget Bibliothek
# In dieser Anwendung werden alle Daten einer Url mit einer spezifischen Dateiendung heruntergeladen. 
# Dieses Script habe ich für den Download von der NSIDC Datenbank - Earthdata Datenbank geschrieben, für die man LogIn Daten braucht. 
# Der final genutze Datensatz braucht kein Log In daher einfach diese Terminal Anfragen mit der "Enter" Taste überspringen
# Die größten Teile dieser Anwendung stehen so auf der Website von NSIDC und in der Wget Bibliothek


def download_with_wget(url, username=None, password=None, cookies_file=None, output_folder=None, target_extension=None, visited_urls=set()):
    if cookies_file is None:
        cookies_file = os.path.expanduser("~/.urs_cookies")

    try:
        wget_args = [
            'wget', '--load-cookies', cookies_file, '--save-cookies', cookies_file,
            '--keep-session-cookies', '--no-check-certificate', '--auth-no-challenge=on',
            '-r', '-np', '-e', 'robots=off', '--no-parent'
        ]
        # Wget funktioniert so, dass es eine https Anfrage an den Server stellt. Die Angaben mit "--" sind Parameter, welche in die Serveranfrage eingebunden werden.
        # Die hier gegebenen sind standard und ohne wird die Anfrage vom Server nicht bearbeitet.
        
        # Wenn Passwort und Nutzername gegeben, https Anfrage mit diesen stellen

        if username and password:
            wget_args.extend(['--http-user=' + username, '--http-password=' + password])

        # Neuer Ordner für die neuen Dateien

        if output_folder:
            output_path = os.path.join(output_folder, 'downloaded_files')
            wget_args.extend(['-P', output_path])
        else:
            output_path = 'downloaded_files'

        # Nur herunterladen der Dateien mit der "target_extension"

        wget_args.extend(['-A', f'*.{target_extension}'])  # Only accept files with the specified extension

        # Der Wget Anfrage wird hier die gewünschte URL hinzugefügt.

        wget_args.append(url)

        # Hier wird die https Anfrage gestellt. Die Bibliothek subprocess ermöglicht uns, neue Prozesse zu erzeugen und die Ausgabe abzufangen. 
        # wget_args sind die Argumente/ Parameter die wir vorher defineirt haben

        subprocess.run(wget_args, check=True)

        # Angabe zum Ausgabeordner 

        print(f"Downloaded to folder: {output_path}")
        return output_path

        # Wenn subprocess ein Error hat, gibt Terminal einen Error aus. 
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {url}. Error: {e}")
        return None


## Funktionsaufruf ##
    
url_to_download = input("Enter the URL to download: ")
username = input("Enter your Login username: ")
password = input("Enter your Login password: ") if username else None

output_folder = input("Enter the folder where you want to download files (leave blank for default): ")
output_folder = output_folder.strip() if output_folder else None

format_ending = input("Type in the format you like to extract: ")

pathway = download_with_wget(url_to_download, username, password, target_extension=format_ending, output_folder=output_folder)

