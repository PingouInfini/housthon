# housthon
Brique de lancement

activation du virtual env
venv\Scripts\activate.bat

lancement du serveur pour service rest
python launch.py

Attention le script launch.py a besoin de variable d'environnement pour fonctionner
COLISSITHON_IP >ip de la brique collissithon
COLISSITHON_PORT ->port de la brique collissithon
HOUSTHON_PORT ->port pour le service rest start_process94A

adresse du service REST
http://localhost:HOUSTHON_PORT/start_process94A

recupere 'nom de famille', 1er 'prenom', 'photo' dans un json 94A
pour creer un bioGraphics dans insight via le service create_bio dans collissithon
