import subprocess
from datetime import datetime
import ipaddress

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"

def nmap_scan(ip, port_select, low_port, high_port, save):
    current_time = datetime.now().strftime("%H%M%S")
    filename = f"nmap_scan_{ip}_{current_time}.txt"
    command = "nmap"

    if port_select == "y":
        command += f" -p {low_port}-{high_port} -sV {ip}"
    elif port_select == "n" or port_select == "":
        command += f" -sV {ip}"

    if save == "y" or save == "":
        command += f" -oN {filename}"

    return command

if __name__ == "__main__":
    while True:
        ip_address = input("Enter the IP address: ")
        if not ip_address:
            print("Please provide an IP address")
            continue
        try:
            ipaddress.ip_address(ip_address)
            break
        except ValueError:
            print("Please provide a valid IP address")

    while True:
        port_select = input("Do you want to scan a specific port? (y/n) Blank will use default port: ")
        if port_select in ["y", "n", ""]:
            break
        else:
            print("Please enter 'y' or 'n'")

    if port_select == "y":
        while True:
            low_port_range = input("Enter lower port range (default to 0): ")
            if not low_port_range:
                low_port_range = 0
            try:
                low_port_range = int(low_port_range)
                break
            except ValueError:
                print("Please provide a valid port number")

        while True:
            high_port_range = input("Enter higher port range (default to 65535): ")
            if not high_port_range:
                high_port_range = 65535
            try:
                high_port_range = int(high_port_range)
                if high_port_range >= low_port_range:
                    break
                else:
                    print("High port range must be greater than or equal to low port range")
            except ValueError:
                print("Please provide a valid port number")
    else:
        low_port_range = 0
        high_port_range = 65535

    while True:
        save_output = input("Do you want to save the output to a file? (y/n) Blank will default to y: ")
        if save_output in ["y", "n", ""]:
            break
        else:
            print("Please enter 'y' or 'n' or leave blank for default to y")

    nmap_command = nmap_scan(ip_address, port_select, low_port_range, high_port_range, save_output)
    print(f"Running command: {nmap_command}")
    output = run_command(nmap_command)
    print(output)