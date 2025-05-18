# Nmap and Dirb Enumeration Tool

This is a Python3-based enumeration tool that automates **Nmap** and **Dirb** scans with interactive prompts. It's built for pentesting practice, CTF competitions, or ethical hacking tasks where recon is the first step.

## Features

- Interactive CLI prompts for flexible configuration
- Supports custom port ranges and scan types with Nmap
- Runs Dirb with selectable wordlists and extensions
- Option to save scan results with timestamped filenames
- Validates tool installation and input formats

---

## Requirements

- Python 3.x
- Linux-based OS (uses `apt` and shell tools)
- Tools: `nmap`, `dirb`

## Usage
### Run the script directly:

python3 enum_tool.py

### You will be prompted to:

Choose whether to run Nmap and/or Dirb

Enter the target IP address (with validation)

Select port range (optional for Nmap and Dirb)

Choose wordlist (small, big, or common) for Dirb

Add file extensions to test (basic, intermediate, advanced, file, or custom)

Choose to save output to files
Wordlists and Extensions

### Wordlist options:

small → wordlists/small.txt

big → wordlists/big.txt

common → (default; you must add this manually)

Extension presets:

basic → php, txt, html

intermediate → php, html, js, txt, bak

advanced → php, html, js, txt, bak, sql, zip, json, xml, log

file → uses wordlists/extensions_common.txt (DirBuster style)

custom → enter your own extensions interactively

## Output

Scan results are saved as:

scan_nmap_<ip>_<timestamp>.txt

scan_dirb_<ip>_<timestamp>.txt

Timestamps are in HHMMSS format to avoid overwrites

## Legal Disclaimer

This tool is intended for educational and ethical use only.
Never run scans against systems you do not own or have explicit permission to test.

## Example Output

Do you want to run an nmap scan? (y/n): y
Enter the IP address: 192.168.1.10
Do you want to scan a specific port for nmap? (y/n): y
Enter lower port range (default to 0): 80
Enter higher port range (default to 65535): 100
Do you want to save the output to a file? (y/n): y


