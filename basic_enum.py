import subprocess
from datetime import datetime
import ipaddress
import sys

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"

def check_and_install(packages):
    missing_packages = []
    for package in packages:
        try:
            subprocess.run(['which', package], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError:
            missing_packages.append(package)
    
    if missing_packages:
        print("The following packages are not installed. Please install them using the following commands:")
        for package in missing_packages:
            print(f"sudo apt install -y {package}")
        sys.exit(1)

def nmap_scan(ip, port_select, low_port, high_port, save, current_time):
    filename = f"scan_nmap_{ip}_{current_time}.txt"
    command = "nmap"

    if port_select == "y":
        command += f" -p {low_port}-{high_port} -sV {ip}"
    elif port_select == "n" or port_select == "":
        command += f" -sV {ip}"

    if save == "y" or save == "":
        command += f" -oN {filename}"
    return command

def dirb_scan(ip, port, dirb_url, use_extensions, extensions, wordlist_input, save_output, current_time):
    command = "dirb"
    filename = f"scan_dirb_{ip}_{current_time}.txt"
    if port:
        if dirb_url == "http":
            command += f" http://{ip}:{port}"
        elif dirb_url == "https":
            command += f" https://{ip}:{port}"
    if not port:
        if dirb_url == "http":
            command += f" http://{ip}"
        elif dirb_url == "https":
            command += f" https://{ip}"
    if wordlist_input == "big":
        command += " wordlists/big.txt"
    elif wordlist_input == "small":
        command += " wordlists/small.txt"

    if use_extensions == "y":
        if extensions == "file":
            command += " -x wordlists/extensions_common.txt"
        else:
            command += f" -X {','.join(extensions)}"
        
    elif use_extensions == "n" or use_extensions == "":
        pass

    if save_output == "y" or save_output == "":
        command += f" -o {filename}"
    return command

#main block#
if __name__ == "__main__":

    #check if nmap and dirb are installed#
    check_and_install(['nmap', 'dirb'])

    #create current time var#
    current_time = datetime.now().strftime("%H%M%S")

    while True:
        use_nmap = input("Do you want to run an nmap scan? (y/n) Blank will default to y: ")
        if use_nmap == "":
            use_nmap = "y"
        if use_nmap in ["y", "n"]:
            break
        else:
            print("Please enter 'y' or 'n' or leave blank for default to y")

    while True:
        use_dirb = input("Do you want to run a dirb scan? (y/n) Blank will default to y: ")
        if use_dirb == "":
            use_dirb = "y"
        if use_dirb in ["y", "n"]:
            break
        else:
            print("Please enter 'y' or 'n' or leave blank for default to y")

    #check if ip is valid#
    if use_nmap == "y" or use_dirb == "y":
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

    #check if port is valid#
    if use_nmap == "y":
        while True:
            port_select = input("Do you want to scan a specific port for nmap? (y/n) Blank will use default port: ")
            if port_select == "":
                port_select = "n"
            if port_select in ["y", "n"]:
                break
            else:
                print("Please enter 'y' or 'n'")
        #check if port range is valid#
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

    #check if user wants to save output#
    if use_nmap == "y" or use_dirb == "y":
        while True:
            save_output = input("Do you want to save the output to a file? (y/n) Blank will default to y: ")
            if save_output == "":
                save_output = "y"
            if save_output in ["y", "n"]:
                break
            else:
                print("Please enter 'y' or 'n' or leave blank for default to y")

    if use_dirb == "y":
        while True:
            dirb_url = input("http or https? blank will default to http: ")
            if dirb_url == "":
                dirb_url = "http"
            if dirb_url in ["http", "https"]:
                break
            else:
                print("Please enter 'http' or 'https'")

        #check if user wants to use big or small wordlist#
        while True:
            wordlist_input = input("Which word list would you like to use, big or small? blank will default to common: ")
            if wordlist_input == "":
                wordlist_input = "common"
            if wordlist_input in ["big", "small", "common"]:
                break
            else:
                print("Please enter 'big' 'small' or 'common'")

        #check if you want to add extensions#
        while True:
            use_extensions = input("Do you want to specify extensions? (y/n) Blank will default to n: ")
            if use_extensions == "":
                use_extensions = "n"
            if use_extensions in ["y", "n"]:
                break
            else:
                print("Please enter 'y' or 'n'")

        if use_extensions == "y":
            #pick extension#
            basic = ["/","php", "txt", "html"]
            intermediate = ["/","php", "html", "js", "txt", "bak"]
            advanced = ["/","php", "html", "js", "txt", "bak", "sql", "zip", "json", "xml", "log"]
            file = ["file"]
            custom = []
            while True:
                print ("_________________________________________________________")
                print ("Basic: php, txt, html")
                print ("Intermediate: php, html, js, txt, bak")
                print ("Advanced: php, html, js, txt, bak, sql, zip, json, xml, log")
                print ("File: is DirBusters extensions_common.txt")
                print ("_________________________________________________________")
                extension = input("Enter the extension you want to use (basic, intermediate, advanced, file, custom): ")
                if extension == "basic":
                    extensions = basic
                    break
                elif extension == "intermediate":
                    extensions = intermediate
                    break
                elif extension == "advanced":
                    extensions = advanced
                    break
                elif extension == "file":
                    extensions = file
                    break
                elif extension == "custom":
                    while True:
                        entry = input("Enter extensions one at a time, enter blank to exit: ").strip().replace(".", "")
                        if entry == "":
                            break
                        else:
                            custom.append(entry)
                            print(f"Extensions so far: {custom}")
                    extensions = custom
                    break
                else:
                    print("Please enter a valid extension type")
        else:
            extensions = []

    if use_nmap == "y":
        nmap_command = nmap_scan(ip_address, port_select, low_port_range, high_port_range, save_output, current_time)
        print(f"Running command: {nmap_command}")
        output = run_command(nmap_command)
        print(output)
        print ("_________________________________________________________")

    while True:
        port_choice = input("Would you like to scan a specific port for dirb? (y/n) Blank will default to n: ")
        if port_choice == "":
            port_choice = "n"
        if port_choice == "y":
            port_input = input("Input port for dirb scan (0-65535): ")
            try:
                port_input = int(port_input)
                if 0 <= port_input <= 65535:
                    port = port_input
                    break
                else:
                    print("Please enter a valid port number between 0 and 65535")
            except ValueError:
                print("Please enter a valid port number between 0 and 65535")
        elif port_choice == "n":
            port = ""
            break
        else:
            print("Please enter 'y' or 'n' or leave blank for default to n")
            
    if use_dirb == "y":
        print ("_________________________________________________________")
        dirb_command = dirb_scan(ip_address, port, dirb_url, use_extensions, extensions, wordlist_input, save_output, current_time)
        print(f"Running command: {dirb_command}")
        output = run_command(dirb_command)
        print(output)
        print ("_________________________________________________________")