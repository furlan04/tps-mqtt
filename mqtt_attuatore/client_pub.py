from flask import Flask, render_template, redirect, request, url_for
import paho.mqtt.publish as publish
import json
import sys

app = Flask(__name__)
TOPIC_DIREZIONE = "tps/motore/direzione"
TOPIC_VELOCITA = "tps/motore/velocità"
BROKER = sys.argv[1:][0]

print(f"[BROKER] {BROKER}")

@app.route("/")
def base():
    return render_template("attuatore.html")

@app.route("/attuatore")
def attuatore():
    velocità = { "velocita": request.args["velocità"] }
    direzione = { "direzione": request.args["direzione"] }
    print(f"[{TOPIC_VELOCITA}] {velocità}")
    print(f"[{TOPIC_DIREZIONE}] {direzione}")
    publish.single(TOPIC_VELOCITA, json.dumps(velocità), hostname = BROKER)
    publish.single(TOPIC_DIREZIONE, json.dumps(direzione), hostname = BROKER)
    return redirect("/")

app.run()