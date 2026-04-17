from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "skelem_secret_key"

PASSWORD = "THATOM2026"

DM_SCRIPTS = {
    "How did you do that?": "Hey! Yeah, that’s something a lot of people get stuck on. What specifically have you tried so far?",
    "Where can I learn more?": "I can definitely give you the breakdown. Just so I make sure I'm giving you the right info, what's your main goal with this?",
    "I’ve been struggling with this too": "I hear you—it’s a frustrating spot to be in. How long has this been a challenge for you?",
    "Send me the link": "I'll drop that for you now! Are you planning to use it for your business or something else?",
    "🔥 Fire / This is exactly what I needed": "Appreciate that! Are you currently trying to improve this area?"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("scriptor"))

    return '''
    <div style="text-align:center; margin-top:120px; font-family:Arial;">
        <h2>DM Scriptor Access</h2>
        <form method="post">
            <input type="password" name="password" placeholder="Enter Access Code">
            <button type="submit">Unlock</button>
        </form>
    </div>
    '''

@app.route("/scriptor")
def scriptor():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("index.html", scripts=DM_SCRIPTS)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))