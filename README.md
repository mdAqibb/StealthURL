# StealthURL 🔒  
**Advanced URL Shortener with Security and Privacy at its Core**

StealthURL is a powerful and secure URL shortening service built to protect user privacy and enhance link sharing. Unlike traditional shorteners, StealthURL offers advanced features such as password protection, one-time-use links, screenshot/video recording prevention, and URL masking — all designed with security-first principles.

---

## Features

- **Password-Protected Links**  
  Ensure only the intended recipient can access the link using a set password.

- **URL Masking**  
  Hide the destination URL to prevent phishing detection or URL preview tools from revealing the target.

- **One-Time Use Links**  
  Generate links that expire after a single visit — perfect for sensitive or temporary information.

- **Anti-Screenshot/Recording Mechanisms**  
  Basic protection to discourage users from capturing link content via screenshots or screen recording (browser-dependent).

- 🧾 **Detailed Link Analytics (coming soon)**  
  View insights like clicks, geolocation, browser info, and access time for each link.

---

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (default) / Extendable to PostgreSQL or MySQL




```bash
git clone https://github.com/yourusername/stealthurl.git
cd stealthurl
pip install -r requirements.txt
python app.py
