from flask import Flask, request, jsonify, render_template_string
import requests
import random

app = Flask(__name__)

# ==========================
# Config
# ==========================
CREDITS = "@iamnoobeco"
REPO = "https://github.com/iamdeveco/free-fire-ban-api"
# User agents (rotate for safety)
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118 Safari/537.36",
]


def check_banned(player_id: str):
    """Check if Free Fire player is banned"""
    url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={player_id}"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://ff.garena.com/en/support/",
        "x-requested-with": "B6FksShzIgjfrYImLpTsadjS86sddhFH"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json().get("data", {})
            is_banned = bool(data.get("is_banned", 0))
            period = data.get("period", 0)

            # Convert period into months
            ban_period = f"{period} month{'s' if period != 1 else ''}" if is_banned else "0 months"

            return {
                "success": True,
                "meta": {"credits": CREDITS, "repo": REPO},
                "player": {
                    "uid": player_id,
                    "status": "BANNED" if is_banned else "NOT BANNED",
                    "is_banned": is_banned,
                    "ban_period": ban_period
                }
            }, 200
        else:
            return {
                "success": False,
                "meta": {"credits": CREDITS},
                "error": {
                    "message": "Failed to fetch data from Garena server",
                    "status_code": response.status_code,
                    "uid": player_id
                }
            }, response.status_code

    except requests.exceptions.Timeout:
        return {"success": False, "error": {"message": "Request timed out"}}, 504
    except Exception as e:
        return {"success": False, "error": {"message": str(e)}}, 500


# ==========================
# HTML TEMPLATE
# ==========================
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Free Fire Ban Checker</title>
  <style>
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      background: #0a0a0f;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      overflow: hidden;
    }

    /* Particle Background */
    #particles-js {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      z-index: -1;
    }

    /* Glassmorphic Container */
    .container {
      max-width: 500px;
      width: 90%;
      padding: 40px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.04);
      backdrop-filter: blur(18px);
      border: 1px solid rgba(0, 229, 255, 0.2);
      box-shadow: 0 0 25px rgba(0, 229, 255, 0.15);
      text-align: center;
      animation: fadeIn 0.8s ease;
      z-index: 1;
    }

    /* 🔥 Glow Title Animation */
    h1 {
      font-size: 2rem;
      margin-bottom: 25px;
      background: linear-gradient(
        90deg,
        #111 0%,
        #00e5ff 25%,
        #8a2be2 50%,
        #00ffcc 75%,
        #111 100%
      );
      background-size: 200% auto;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: glowSlide 4s linear infinite;
    }

    @keyframes glowSlide {
      0%   { background-position: 200% center; }
      100% { background-position: -200% center; }
    }

    /* Input Styling */
    input {
      width: 80%;
      padding: 12px;
      margin-bottom: 20px;
      border: none;
      border-radius: 10px;
      font-size: 1rem;
      color: #fff;
      background: rgba(255, 255, 255, 0.07);
      outline: none;
      transition: all 0.3s ease;
    }
    input:focus {
      border: 1px solid #00e5ff;
      box-shadow: 0 0 12px rgba(0, 229, 255, 0.4);
    }

    /* Button Styling */
    button {
      padding: 12px 28px;
      border: none;
      border-radius: 12px;
      font-size: 1rem;
      font-weight: bold;
      color: #0a0a0f;
      background: linear-gradient(90deg, #00e5ff, #8a2be2, #00ffcc);
      cursor: pointer;
      transition: all 0.3s ease;
    }
    button:hover {
      transform: translateY(-2px);
      box-shadow: 0 0 18px rgba(0, 229, 255, 0.5);
    }

    /* Result Card */
    .result {
      margin-top: 25px;
      padding: 20px;
      border-radius: 15px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(0, 229, 255, 0.2);
      box-shadow: inset 0 0 12px rgba(0, 229, 255, 0.2);
      animation: fadeIn 0.6s ease;
    }
    .result h2 {
      font-size: 1.2rem;
      margin-bottom: 10px;
      color: #00e5ff;
    }
    .result p {
      margin: 6px 0;
      font-size: 1rem;
    }

    /* Fade Animation */
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(15px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <!-- Particle.js Background -->
  <div id="particles-js"></div>

  <!-- Main Content -->
  <div class="container">
    <h1>Free Fire Ban Checker</h1>
    <form method="get" action="/bancheck_page">
      <input type="text" name="uid" placeholder="Enter Player UID" required>
      <br>
      <button type="submit">Check Status</button>
    </form>

    {% if result %}
      <div class="result">
        <h2>Result for UID: {{ result.player.uid }}</h2>
        <p>Status: 
          <strong style="color:{{ 'red' if result.player.is_banned else 'lime' }}">
            {{ result.player.status }}
          </strong>
        </p>
        <p>Banned: {{ result.player.is_banned }}</p>
        <p>Ban Period: {{ result.player.ban_period }}</p>
        <small>Credits: {{ result.meta.credits }}</small>
      </div>
    {% endif %}
  </div>

  <!-- Particles.js CDN -->
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": ["#00e5ff", "#8a2be2", "#00ffcc"] },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.5, "random": true },
        "size": { "value": 3, "random": true },
        "line_linked": {
          "enable": true,
          "distance": 150,
          "color": "#00e5ff",
          "opacity": 0.2,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 1.8,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": false
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": { "enable": true, "mode": "grab" },
          "onclick": { "enable": true, "mode": "push" },
          "resize": true
        },
        "modes": {
          "grab": { "distance": 150, "line_linked": { "opacity": 0.5 } },
          "push": { "particles_nb": 4 }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>

"""


@app.route("/")
def home():
    return render_template_string(INDEX_HTML)


@app.route("/bancheck", methods=["GET"])
def bancheck():
    """Return JSON result only"""
    player_id = request.args.get("uid", "").strip()
    if not player_id:
        return jsonify({"success": False, "error": {"message": "Player ID is required"}}), 400

    result, code = check_banned(player_id)
    return jsonify(result), code


@app.route("/bancheck_page", methods=["GET"])
def bancheck_page():
    """Return HTML + Result"""
    player_id = request.args.get("uid", "").strip()
    if not player_id:
        return render_template_string(INDEX_HTML, result=None)

    result, code = check_banned(player_id)
    return render_template_string(INDEX_HTML, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
