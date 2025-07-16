# 🛡️ Nmap Recon & Attack Suggestions

`nmap_automation.py` is a Python-based reconnaissance tool designed for offensive security assessments. It automates `nmap` scanning, parses the results, and generates an actionable **HTML report** including:

* Open, closed, and filtered ports
* Detected services and versions
* Potential vulnerabilities per service
* Suggested attacks per port/service

---

## 📌 Features

* 🔍 Deep Nmap scan (`-sC -sV -O --script vuln`)
* 🧠 Port-specific vulnerability mapping
* ⚔️ Attack recommendations (e.g., Metasploit, Hydra, enum4linux)
* 📝 Clean HTML reporting format
* 🛆 Self-contained script (no external Python dependencies)

---

## 🚀 Usage

### ✅ Prerequisites

* Kali Linux or any system with:

  * Python 3.6+
  * Nmap installed (`sudo apt install nmap`)

### 🐍 Run the Tool

```bash
sudo python3 nmap_automation.py
```

You’ll be prompted to enter a **target IP** or **subnet**, like:

```
Enter target IP or subnet (e.g., 192.168.1.0/24):
```

### 📁 Output

* `report_YYYYMMDD_HHMMSS.html`: A full HTML report of recon results.
* `report_YYYYMMDD_HHMMSS.xml`: Raw Nmap scan output for advanced users.

---

## 💡 Example Report Snippet

```html
Port: tcp/21 - open - ftp
➔ Vulnerabilities:
  - Anonymous login
  - FTP bounce
  - CVE-1999-0497
➔ Suggested Attacks:
  - Hydra brute-force
  - Metasploit: auxiliary/scanner/ftp/ftp_login
```

---

## 📌 Roadmap

* [ ] `searchsploit` CVE integration
* [ ] PDF export for offline reports
* [ ] Markdown / CSV export options
* [ ] Web-based interface (Flask)

---

## ⚠️ Disclaimer

This tool is intended **only for authorized security testing and educational purposes**. Unauthorized use against systems you don’t own is illegal and unethical.

---

## ✍️ Author

**Kali GPT**
Master Kali Linux. Excel in Offensive Security.
Built with ❤️ by [Balakavi](https://www.instagram.com/kavi.s_network)

---
