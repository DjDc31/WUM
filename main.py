import psutil
import curses
import os
import json
import time
from datetime import datetime, timedelta
from art import *
from pyfiglet import Figlet

# Variables pour stocker les valeurs initiales
initial_bytes_sent = 0
initial_bytes_received = 0

# Charger les valeurs initiales à partir du fichier
try:
    with open("initial_values.txt", "r") as file:
        values = file.readline().split(",")
        initial_bytes_sent = int(values[0])
        initial_bytes_received = int(values[1])
except FileNotFoundError:
    pass

def get_network_usage():
    global initial_bytes_sent, initial_bytes_received

    network_stats = psutil.net_io_counters()

    # Stocker les valeurs initiales si elles sont nulles
    if initial_bytes_sent == 0 and initial_bytes_received == 0:
        initial_bytes_sent = network_stats.bytes_sent
        initial_bytes_received = network_stats.bytes_recv

        # Écrire les valeurs initiales dans le fichier
        with open("initial_values.txt", "w") as file:
            file.write("{},{}".format(initial_bytes_sent, initial_bytes_received))

    bytes_sent = network_stats.bytes_sent - initial_bytes_sent
    bytes_received = network_stats.bytes_recv - initial_bytes_received

    return bytes_sent, bytes_received

def reset_values():
    # Réinitialiser les valeurs initiales à zéro
    global initial_bytes_sent, initial_bytes_received
    initial_bytes_sent = 0
    initial_bytes_received = 0

    # Supprimer le fichier initial_values.txt s'il existe
    if os.path.exists("initial_values.txt"):
        os.remove("initial_values.txt")

import os
import json
from datetime import datetime, timedelta

def get_consumption_history():
    # Récupérer la date d'aujourd'hui
    today = datetime.now().date()

    # Récupérer les données des 7 derniers jours à partir du fichier
    history_file = "consumption_history.json"

    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            try:
                history_data = json.load(file)
            except json.JSONDecodeError:
                history_data = {}
    else:
        # Créer un dictionnaire vide si le fichier n'existe pas
        history_data = {}

    # Vérifier si les données d'aujourd'hui existent déjà dans l'historique
    if str(today) in history_data:
        data_sent = history_data[str(today)]["sent"]
        data_received = history_data[str(today)]["received"]
    else:
        # Exemple de données de consommation fictives pour les 7 derniers jours
        data_sent = [2.3, 1.8, 3.2, 2.6, 1.5, 2.1, 1.9]
        data_received = [1.5, 1.2, 2.8, 2.1, 1.4, 1.9, 1.7]

        # Mettre à jour les données d'aujourd'hui dans l'historique
        history_data[str(today)] = {"sent": data_sent[-1], "received": data_received[-1]}

    # Enregistrer les données mises à jour dans le fichier
    with open(history_file, "w") as file:
        json.dump(history_data, file)

    return data_sent, data_received


def display_network_usage(stdscr):
    # Effacer l'écran
    stdscr.clear()

    # Utiliser la bibliothèque `art` pour générer le titre en ASCII
    title_art = text2art("WUM", font='block')
    stdscr.addstr(0, 10, title_art)

    # Afficher le sous-titre
    stdscr.addstr(13, 15, "Welcome to WebUsageMonitor")

    # Afficher la consommation internet
    bytes_sent, bytes_received = get_network_usage()
    gb_sent = bytes_sent / (1024**3)
    gb_received = bytes_received / (1024**3)
    stdscr.addstr(17, 3, "Data sent since Wi-Fi activation: {:.2f} GB".format(gb_sent))
    stdscr.addstr(18, 3, "Data received since Wi-Fi activation: {:.2f} GB".format(gb_received))

    # Afficher le total consommé
    total_gb = gb_sent + gb_received
    stdscr.addstr(15, 0, "Total data consumed: {:.2f} GB".format(total_gb))

    # Afficher le bouton de réinitialisation
    stdscr.addstr(20, 0, "Press 'R' to reset usage to 0")
    stdscr.addstr(21, 0, "Press 'X' to exit")
    stdscr.addstr(22, 0, "Press 'H' to view consumption history")

    # Afficher l'indication de mise à jour des données
    stdscr.addstr(24, 0, "Data updates every minute")

    # Afficher le copyright
    stdscr.addstr(26, 15, "© Cyrille Varin 2023")

    # Rafraîchir l'écran
    stdscr.refresh()

def display_consumption_history(stdscr):
    # Effacer l'écran
    stdscr.clear()

    # Récupérer les données de consommation du jour actuel
    today_sent, today_received = get_consumption_history()

    # Afficher le titre de l'historique
    stdscr.addstr(0, 10, "Consumption History")

    # Afficher les données de consommation du jour actuel
    date = datetime.now().strftime("%Y-%m-%d")
    total = today_sent + today_received
    stdscr.addstr(2, 0, "{}: {:.2f} GB sent, {:.2f} GB received (Total conso.: {:.2f} GB)".format(date, today_sent, today_received, total))

    # Afficher l'instruction pour revenir à l'affichage en direct
    stdscr.addstr(4, 0, "Press any key to go back to live display")


def main(stdscr):
    # Initialiser l'interface utilisateur
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(-1)  # Désactiver la temporisation pour éviter la fermeture automatique

    # Afficher la consommation initiale
    display_network_usage(stdscr)

    # Initialiser la variable last_refresh_time
    last_refresh_time = time.time()

    # Boucle principale pour gérer les entrées de l'utilisateur
    while True:
        key = stdscr.getch()

        # Vérifier si l'utilisateur a appuyé sur 'R' ou 'r' pour réinitialiser les valeurs
        if key == ord('R') or key == ord('r'):
            reset_values()
            display_network_usage(stdscr)

        # Vérifier si l'utilisateur a appuyé sur 'X' ou 'x' pour quitter
        elif key == ord('X') or key == ord('x'):
            break

        # Vérifier si l'utilisateur a appuyé sur 'H' ou 'h' pour afficher l'historique
        elif key == ord('H') or key == ord('h'):
            display_consumption_history(stdscr)

        else:
            # Afficher la consommation en direct
            display_network_usage(stdscr)

        # Vérifier si le délai d'actualisation est atteint
        current_time = time.time()
        if current_time - last_refresh_time > 60:
            # Mettre à jour les données et afficher la consommation en direct
            display_network_usage(stdscr)
            last_refresh_time = current_time

    # Fermer la fenêtre
    curses.endwin()

# Exécution du programme
curses.wrapper(main)
