# 🔥 Free Fire Ban API – API Guide
```
Author  : @iamnoobeco  
Repo    : https://github.com/iamdeveco/free-fire-ban-api
```

🚀 Features

✅ Free Fire Player Ban Checker API <br>
✅ JSON Response + HTML UI (Glassmorphic + Particle.js) <br>
✅ Auto User-Agent Rotation (Bypass basic protections) <br>
✅ Ban Period converted into Months <br>
✅ Clean Flask-based backend (Python 3.9+) <br>


⚡ Installation

```
# 1. Clone repo
git clone https://github.com/iamdeveco/free-fire-ban-api.git
cd free-fire-ban-api

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server
python app.py
```

👉 Server will start on **[http://0.0.0.0:8080](http://0.0.0.0:8080)**

---

🌍 API Endpoints

🔹 Root (UI Page)

```bash
GET /
```

👉 Shows Glassmorphic Web UI with particle background.
You can input a UID and check if a player is banned.

---

🔹 Check Ban (JSON API)

```bash
GET /bancheck?uid=PLAYER_UID
```

✅ Example:

```bash
curl "http://127.0.0.1:8080/bancheck?uid=123456789"
```

📦 Response:

```json
{
  "success": true,
  "meta": {
    "credits": "@iamnoobeco",
    "repo": "https://github.com/iamdeveco/free-fire-ban-api"
  },
  "player": {
    "uid": "123456789",
    "status": "BANNED",
    "is_banned": true,
    "ban_period": "5 months"
  }
}
```

---

🔹 Check Ban (HTML Page)

```bash
GET /bancheck_page?uid=PLAYER_UID
```

👉 Returns the same result but inside a **premium web UI**.

---
# IF YOU RUN IN VERCEL <br>

``` Install Command
pip3 install -r requirements.txt
```
``` Build  Command
python3 app.py
```
 

⚠️ Disclaimer

This project is made **for educational purposes only**.
We are not affiliated with **Garena / Free Fire**.
Use at your own risk.

---

⭐ Credits

Developer: @iamnoobeco
Repository: [Free Fire Ban API](https://github.com/iamdeveco/free-fire-ban-api) <br><br>
<img width="1439" height="818" alt="image" src="https://github.com/user-attachments/assets/60b2e8b1-6267-466e-afca-85c35f2f7baa" />
