from flask import Flask, redirect, url_for, request, render_template
import os
from aiomcrcon import Client
import asyncio

#ajout pour https
#from flask_sslify import SSLify

app = Flask(__name__) # sauf ça
#sslify = SSLify(app)

# fin ajout pour https---

# ajout pour bot
import requests

WEBHOOK = "https://discord.com/api/webhooks/1170699996459442297/PkfJI9BdyWPmKsa60K02XPSNYkHZ2Xcnlv7h0iOfw_oFfPs7aJcCXCyfTfIeF0dEkEpN"

def output_discord(text):
    message = {"content": text}

    response = requests.post(WEBHOOK, json=message)

    if response.status_code == 204:
        print("Message envoyé avec succès")
    else:
        print(f"Erreur lors de l'envoi du message : {response.status_code} {response.reason}")
#fin ajout pour bot--


@app.route("/")
def home():
    return render_template("minecraft.html")

@app.route("/startserver", methods=['POST'])
def startserver():
    try:
        os.system("systemctl start servminecraft")
        output_discord("Quelqu'un a demandé le démarrage du serveur") #bot discord
        return '{"output": "Serveur lancé, veuillez patienter 1 minute..."}'
    except Exception as e:
        return '{"output": "' + str(e) + '"}'

@app.route("/restartserver", methods=['POST'])
def restartserver():
    try:
        os.system("systemctl restart servminecraft")
        output_discord("Quelqu'un a demandé le redémarrage du serveur") #bot discord
        return '{"output": "Serveur relancé, veuillez patienter 1 minute..."}'
    except Exception as e:
        return '{"output": "' + str(e) + '"}'

@app.route("/stopserver", methods=['POST'])
def stopserver():
    try:
        os.system("systemctl stop servminecraft")
        output_discord("Quelqu'un a demandé l'arret du serveur") #bot discord
        return '{"output": "Serveur éteint."}'
    except Exception as e:
        return '{"output": "' + str(e) + '"}'


@app.route('/sendcommand', methods=['POST'])
async def command():
    try:
        request_command = request.json["command"]
    except:
        return '{"output": "Please give a command"}'
    try:
        client = Client("193.203.191.5", 25566, "Noelefdp")
        await client.connect()
        resp = await client.send_cmd(request_command)
        await client.close()
        return '{"output": "' + str(resp[0]) + '"}'
    except Exception as e:
        print(str(e))
        return '{"output": "' + str(e) + '"}'

if __name__ == '__main__':
    app.run("panel.leteh.fr", port=80) # original : app.run("0.0.0.0", port=8000)