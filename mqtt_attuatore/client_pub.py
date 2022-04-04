from flask import Flask, render_template, redirect, request, url_for
import paho.mqtt.publish as publish
import sys

app = Flask(__name__)
TOPIC_DIREZIONE = "tps/motore/direzione"
TOPIC_VELOCITA = "tps/motore/velocità"
BROKER = sys.argv[1:][0]

print(f"[BROKER] {BROKER}")

@app.route("/")
def base():
    return redirect(url_for("attuatore"))

@app.route("/attuatore")
def attuatore():
    if request.args == []:
        velocità = request.args["velocità"]
        direzione = request.args["direzione"]
        publish.single(TOPIC_VELOCITA, velocità, hostname = BROKER)
        publish.single(TOPIC_DIREZIONE, direzione, hostname = BROKER)
    return render_template("attuatore.html")

app.run()