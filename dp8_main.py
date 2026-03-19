# Script om data uit database te halen en naar JSON te schrijven

# Imports
import mysql.connector
import json

# ---------------- DATABASE VERBINDING ----------------

verbinding = mysql.connector.connect(
    host="localhost",
    user="root",
    password="***",
    database="attractiepark"
)

cursor = verbinding.cursor(dictionary=True)

# ---------------- BEZOEKER OPHALEN ----------------

bezoeker_id = 1
query_bezoeker = "SELECT * FROM bezoeker WHERE id = %s"

cursor.execute(query_bezoeker, (bezoeker_id,))
bezoeker = cursor.fetchone()

# ---------------- ATTRACTIES OPHALEN ----------------

query_attracties = """
SELECT * FROM voorziening
WHERE actief = 1
AND (soort = 'attractie' OR soort = 'achtbaan')
AND geschatte_wachttijd <= 25
"""

cursor.execute(query_attracties)
attracties = cursor.fetchall()

# ---------------- HORECA OPHALEN ----------------

query_horeca = """
SELECT * FROM voorziening
WHERE actief = 1
AND soort = 'horeca'
ORDER BY geschatte_wachttijd ASC
LIMIT 1
"""

cursor.execute(query_horeca)
horeca = cursor.fetchone()

# ---------------- GEGEVENS SAMENVOEGEN ----------------

output_data = {
    "bezoeker": bezoeker,
    "geschikte_attracties": attracties,
    "geschikte_horeca": horeca
}

# ---------------- JSON BESTAND SCHRIJVEN ----------------

with open("output.json", "w") as json_bestand:
    json.dump(output_data, json_bestand, indent=4)

# ---------------- AFSLUITEN ----------------

print("output.json is gemaakt.")

cursor.close()
verbinding.close()
