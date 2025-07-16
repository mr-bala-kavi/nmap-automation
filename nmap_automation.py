import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime


attack_map = {
    "ftp": {
        "vuln": ["Anonymous login", "FTP bounce", "CVE-1999-0497"],
        "attack": ["Hydra brute-force", "Metasploit: auxiliary/scanner/ftp/ftp_login"]
    },
    "ssh": {
        "vuln": ["Weak credentials", "Shellshock (older versions)"],
        "attack": ["Hydra SSH login", "SSH key cracking", "Brute-force"]
    },
    "http": {
        "vuln": ["Directory listing", "Outdated CMS", "Insecure headers"],
        "attack": ["Nikto scan", "dirb/gobuster", "Burp Suite mapping", "Searchsploit"]
    },
    "https": {
        "vuln": ["SSL misconfig", "Self-signed certs"],
        "attack": ["sslscan", "testssl.sh", "Burp Suite (HTTPS)"]
    },
    "smb": {
        "vuln": ["Null sessions", "MS17-010 (EternalBlue)", "Open shares"],
        "attack": ["enum4linux", "Metasploit smb exploits", "smbclient"]
    },
    "mysql": {
        "vuln": ["Default creds", "Remote access without firewall"],
        "attack": ["Hydra", "sqlmap", "mysql command line"]
    },
    "rdp": {
        "vuln": ["BlueKeep (CVE-2019-0708)"],
        "attack": ["rdp brute-force", "Metasploit: exploit/windows/rdp/bluekeep"]
    }
}

def run_nmap(target, output):
    print(f"[+] Running Nmap scan on: {target}")
    xml_out = f"{output}.xml"
    nmap_command = [
        "nmap", "-sC", "-sV", "-O", "-T4", "--script", "vuln",
        "-oX", xml_out, target
    ]
    subprocess.run(nmap_command, check=True)
    return xml_out

def parse_nmap(xml_file):
    results = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for host in root.findall("host"):
        addr_elem = host.find("address")
        addr = addr_elem.attrib.get("addr", "Unknown")
        ports_info = []
        for port in host.findall(".//port"):
            port_id = port.attrib.get("portid")
            protocol = port.attrib.get("protocol")
            state = port.find("state").attrib.get("state")
            service_elem = port.find("service")
            service = service_elem.attrib.get("name", "unknown") if service_elem is not None else "unknown"
            port_dict = {
                "port": f"{protocol}/{port_id}",
                "state": state,
                "service": service,
                "vuln": attack_map.get(service, {}).get("vuln", ["Unknown / manual investigation"]),
                "attack": attack_map.get(service, {}).get("attack", ["Manual recon recommended"])
            }
            ports_info.append(port_dict)
        results.append((addr, ports_info))
    return results

def generate_html_report(scan_data, output_file):
    print(f"[+] Generating HTML report: {output_file}")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<html><head><title>Advanced Nmap Recon Report</title>
<style>body{{font-family:Arial}} li{{margin-bottom:10px}}</style>
</head><body>
<h1>Nmap Recon Report</h1>
<p><b>Generated:</b> {timestamp}</p><hr>"""

    for host, ports in scan_data:
        html += f"<h2>Host: {host}</h2><ul>"
        for p in ports:
            html += f"<li><b>Port:</b> {p['port']} - {p['state']} - {p['service']}"
            html += "<ul>"
            html += "<li><b>Possible Vulnerabilities:</b><ul>" + "".join(f"<li>{v}</li>" for v in p['vuln']) + "</ul></li>"
            html += "<li><b>Suggested Attacks:</b><ul>" + "".join(f"<li>{a}</li>" for a in p['attack']) + "</ul></li>"
            html += "</ul></li>"
        html += "</ul><hr>"

    html += "</body></html>"

    with open(output_file, "w") as f:
        f.write(html)

def main():
    print("== Auto Recon + Attack Suggestion Tool ==")
    target = input("Enter target IP or subnet (e.g., 192.168.1.0/24): ").strip()
    if not target:
        print("[-] No target specified. Exiting.")
        return
    output = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        xml_result = run_nmap(target, output)
        scan_data = parse_nmap(xml_result)
        generate_html_report(scan_data, f"{output}.html")
        print(f"[+] Scan complete. Open your report: {output}.html")
    except subprocess.CalledProcessError:
        print("[-] Nmap scan failed. Check network or permissions.")
    except Exception as e:
        print(f"[-] Unexpected error: {e}")

if __name__ == "__main__":
    main()
