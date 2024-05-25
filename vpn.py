import os
import pyfiglet
from stem import Signal
from stem.control import Controller
import requests
import subprocess

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    ascii_banner = pyfiglet.figlet_format("SAFETY")
    print("\033[34m" + ascii_banner + "\033[0m")  # 34 is the ANSI code for blue

def print_options():
    options = [
        "1. Normal VPN",
        "2. Tor Browser",
        "3. MAC Address Changer"
    ]
    for option in options:
        print("\033[31m" + option + "\033[0m")  # 31 is the ANSI code for red

def get_user_choice():
    choice = input("\033[32mSelect one of the options (1-3): \033[0m")  # 32 is the ANSI code for green
    return choice

def start_vpn():
    print("\033[33mYou have selected Normal VPN. Starting VPN...\033[0m")  # 33 is the ANSI code for yellow
    # VPN yapılandırma dosyanızın yolunu burada belirtin
    vpn_config_path = "/storage/emulated/0/Download/us-free-421049.protonvpn.udp.ovpn"
    try:
        subprocess.call(f"sudo openvpn --config {vpn_config_path}", shell=True)
        print("\033[33mVPN connection established!\033[0m")
    except Exception as e:
        print(f"\033[31mAn error occurred while starting the VPN: {e}\033[0m")

def install_tor():
    print("\033[33mInstalling Tor...\033[0m")  # 33 is the ANSI code for yellow
    os.system("pkg update -y && pkg install tor -y")

def start_tor():
    print("\033[33mYou have selected Tor Browser. Connecting to Tor network...\033[0m")  # 33 is the ANSI code for yellow
    install_tor()
    
    os.system("tor &")
    
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()  # Authenticates using CookieAuthentication
            controller.signal(Signal.NEWNYM)  # Creates a new Tor circuit
            
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            response = requests.get('https://check.torproject.org/', proxies=proxies)
            if 'Congratulations. This browser is configured to use Tor.' in response.text:
                print("\033[33mSuccessfully connected to the Tor network!\033[0m")
            else:
                print("\033[31mUnable to connect to the Tor network.\033[0m")
    except Exception as e:
        print(f"\033[31mUnable to connect to the Tor control port: {e}\033[0m")

def change_mac_address():
    print("\033[33mYou have selected MAC Address Changer. Changing MAC address...\033[0m")  # 33 is the ANSI code for yellow
    
    # Enter the new MAC address here (e.g., "00:11:22:33:44:55")
    new_mac = input("\033[32mEnter the new MAC address: \033[0m")

    # Enter the name of the relevant interface here (e.g., "eth0", "wlan0" etc.)
    interface = input("\033[32mEnter the name of the network interface you want to change the MAC address for: \033[0m")

    # Create the command to change the MAC address
    command = f"sudo ip link set dev {interface} down && sudo ip link set dev {interface} address {new_mac} && sudo ip link set dev {interface} up"
    
    # Execute the command
    try:
        subprocess.call(command, shell=True)
        print("\033[33mMAC address successfully changed!\033[0m")
    except Exception as e:
        print("\033[31mAn error occurred while changing the MAC address:", str(e) + "\033[0m")

def handle_choice(choice):
    if choice == "1":
        start_vpn()
    elif choice == "2":
        start_tor()
    elif choice == "3":
        change_mac_address()
    else:
        print("\033[33mInvalid option!\033[0m")

if __name__ == "__main__":
    clear_screen()
    print_banner()
    print_options()
    choice = get_user_choice()
    handle_choice(choice)
