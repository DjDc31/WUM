import psutil
import curses
import os

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

def display_network_usage(stdscr):
    # Effacer l'écran
    stdscr.clear()

    # Afficher le titre et le sous-titre
    stdscr.addstr(0, 0, "WUM")
    stdscr.addstr(1, 0, "Welcome to WebUsageMonitor")

    # Afficher la consommation internet
    bytes_sent, bytes_received = get_network_usage()
    gb_sent = bytes_sent / (1024**3)
    gb_received = bytes_received / (1024**3)
    stdscr.addstr(3, 0, "Data sent since Wi-Fi activation: {:.2f} GB".format(gb_sent))
    stdscr.addstr(4, 0, "Data received since Wi-Fi activation: {:.2f} GB".format(gb_received))

    # Afficher le bouton de réinitialisation
    stdscr.addstr(6, 0, "Press 'R' to reset usage to 0")

    # Rafraîchir l'écran
    stdscr.refresh()

    # Attendre la saisie de l'utilisateur
    while True:
        key = stdscr.getch()
        if key == ord('R') or key == ord('r'):
            # L'utilisateur a appuyé sur 'R' ou 'r', réinitialiser les valeurs et mettre à jour l'affichage
            reset_values()
            display_network_usage(stdscr)
            break

def main(stdscr):
    # Initialiser l'interface utilisateur
    curses.curs_set(0)
    stdscr.nodelay(1)

    # Appeler la fonction pour afficher la consommation internet
    display_network_usage(stdscr)

    # Attendre la saisie de l'utilisateur pour quitter
    stdscr.getch()

# Lancer l'interface utilisateur
curses.wrapper(main)
