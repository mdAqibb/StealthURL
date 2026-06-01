# 🔒 StealthURL

> Privacy-first URL shortener with password protection, one-time links, URL masking, and anti-screenshot mechanisms.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange?style=flat-square&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

## Overview

**StealthURL** is a security-focused URL shortening service built with Flask. Unlike standard shorteners, StealthURL is built around privacy and access control — giving you fine-grained control over who can access your links and under what conditions.

## Features

| Feature | Description |
|---|---|
| 🔑 **Password Protection** | Lock links behind a password — only intended recipients get through |
| 🎭 **URL Masking** | Hide the destination URL from preview tools and link scanners |
| 💣 **One-Time Links** | Links self-destruct after a single visit |
| 🛡️ **Anti-Screenshot** | Browser-level protection against screen capture (where supported) |
| 📊 **Analytics** *(coming soon)* | Clicks, geolocation, browser info, and access timestamps |

## Installation

```bash
git clone https://github.com/mdAqibb/StealthURL.git
cd StealthURL
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` in your browser.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Frontend | HTML5, CSS3, JavaScript |
| Database | SQLite (default) — extendable to PostgreSQL or MySQL |

## Project Structure

```
StealthURL/
├── app.py              # Main Flask application
├── templates/          # HTML templates
├── static/             # CSS & JS assets
├── requirements.txt    # Python dependencies
└── README.md
```

## Use Cases

- Sharing sensitive links with a specific person
- Time-limited or access-limited file sharing
- Hiding affiliate or redirect URLs
- Security research and red-team operations

## Author

**Mohammed Aqib**  
[LinkedIn](https://www.linkedin.com/in/88maqib/) • [GitHub](https://github.com/mdAqibb)

---

> ⚠️ For educational and personal use only. Do not use URL masking or one-time links for malicious purposes.
