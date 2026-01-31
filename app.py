from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

def calculate_risk(d):
    score = 0

    if d["insulin"] < 2 or d["insulin"] > 25:
        score += 2
    if d["bmi"] >= 25:
        score += 2
    if d["bp"] >= 140:
        score += 2
    if d["cholesterol"] >= 5.2:
        score += 1
    if d["ldl"] >= 3.0:
        score += 1
    if d["hdl"] < 1.0:
        score += 1
    if d["triglycerides"] >= 1.7:
        score += 1

    return min(score * 10, 100)


@app.route("/", methods=["GET", "POST"])
def index():
    risk = None
    graph = None

    if request.method == "POST":
        data = {k: float(request.form[k]) for k in request.form}
        risk = calculate_risk(data)

        plt.figure(figsize=(6,4))
        plt.bar(["Sog‘lom", "Diabet xavfi"],
                [100-risk, risk],
                color=["#2ecc71", "#e74c3c" if risk >= 50 else "#f39c12"])
        plt.title("🩺 Diabet xavf darajasi")
        plt.ylabel("Foiz (%)")
        plt.ylim(0, 100)

        for i, v in enumerate([100-risk, risk]):
            plt.text(i, v + 2, f"{v:.1f}%", ha="center", fontsize=12)

        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format="png")
        img.seek(0)
        graph = base64.b64encode(img.getvalue()).decode()
        plt.close()

    return render_template("index.html", risk=risk, graph=graph)


if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


