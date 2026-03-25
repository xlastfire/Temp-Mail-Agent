# 📧 Temp-Mail-Agent

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/xlastfire/Temp-Mail-Agent)](https://github.com/xlastfire/Temp-Mail-Agent/issues)
[![GitHub stars](https://img.shields.io/github/stars/xlastfire/Temp-Mail-Agent)](https://github.com/xlastfire/Temp-Mail-Agent/stargazers)

**Temp-Mail-Agent** is a complete, beautifully colored Command Line Interface (CLI) tool for generating and managing temporary email addresses directly from your terminal. Powered by the [tempmail123.com](https://tempmail123.com) API.

## ✨ Features

* **⚡ Instant Setup:** Generate a secure, 10-minute temporary email address with a single keystroke.
* **📬 Live Inbox:** Receive, view, and read full emails (subject, sender, and body) directly in the terminal.
* **🔄 Auto-Refresh:** Built-in auto-refresh settings to keep your inbox up to date without manual polling.
* **🎨 Beautiful UI:** Fully colored terminal interface with clean ASCII borders and menus.
* **🗑️ Mailbox Management:** Easily delete your temporary mailbox and spin up a new one.

## 🚀 Installation

**1. Clone the repository:**
```bash
git clone https://github.com/xlastfire/Temp-Mail-Agent.git
cd Temp-Mail-Agent
```

**2. Install required dependencies:**
This script requires the `requests` library. You can install it via pip:
```bash
pip install requests
```
*(Alternatively, if you create a `requirements.txt`, run `pip install -r requirements.txt`)*

## 💻 Usage

Run the script using Python 3:

```bash
python3 temp_mail_agent.py
```

### Main Menu Overview

Once started, you will be greeted by the main dashboard:

```text
╔════════════════════════════════════════════════════════════════════╗
║                   📧 TempMail123 Terminal Agent                    ║
║                          By @xlastfire                             ║
╚════════════════════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────────────────────
📊 MAILBOX STATUS
──────────────────────────────────────────────────────────────────────
  ❌ No active mailbox
  💡 Create one with option 1

══════════════════════════════════════════════════════════════════════
  MAIN MENU
══════════════════════════════════════════════════════════════════════

  [1] 🆕 Create New Mailbox
  [2] 📬 View Inbox
  [3] ⚙️  Settings
  [4] 🔄 Quick Refresh
  [5] 🗑️  Delete Mailbox
  [6] ℹ️  About
  [0] 🚪 Exit

  Select option: 
```

## ⚙️ Settings
You can tweak the agent's behavior from the **Settings (Option 3)** menu:
* **Toggle Auto-Refresh:** Turn automatic inbox refreshing `ON` or `OFF`.
* **Change Refresh Interval:** Set how often the agent checks for new emails (default is `5` seconds, can be set between `1-60` seconds).

## 🛠️ Built With

* [Python 3](https://www.python.org/) - The main programming language.
* [Requests](https://pypi.org/project/requests/) - For handling HTTP requests to the API.
* [TempMail123 API](https://tempmail123.com) - The backend temporary email provider.

## 👨‍💻 Author

**xlastfire**
* GitHub: [@xlastfire](https://github.com/xlastfire)
* Repository:[Temp-Mail-Agent](https://github.com/xlastfire/Temp-Mail-Agent)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check out the [issues page](https://github.com/xlastfire/Temp-Mail-Agent/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
