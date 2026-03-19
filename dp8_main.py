# Data uit de database halen en naar JSON schrijven

# Imports
import mysql.connector
import json

# Databaseverbinding maken
verbinding = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Azadegan24",
    database="attractiepark"
)

cursor = verbinding.cursor(dictionary=True)

# Bezoeker ophalen
bezoeker_id = 1
query_bezoeker = "SELECT * FROM bezoeker WHERE id = %s"
cursor.execute(query_bezoeker, (bezoeker_id,))
bezoeker = cursor.fetchone()

# Attracties ophalen
query_attracties = """
SELECT * FROM voorziening
WHERE actief = 1
AND (soort = 'attractie' OR soort = 'achtbaan')
AND geschatte_wachttijd <= 25
"""
cursor.execute(query_attracties)
attracties = cursor.fetchall()

# Eén horecavoorziening ophalen
query_horeca = """
SELECT * FROM voorziening
WHERE actief = 1
AND soort = 'horeca'
ORDER BY geschatte_wachttijd ASC
LIMIT 1
"""
cursor.execute(query_horeca)
horeca = cursor.fetchone()

# Gegevens verzamelen
output_data = {
    "bezoeker": bezoeker,
    "geschikte_attracties": attracties,
    "geschikte_horeca": horeca
}

# JSON-bestand schrijven
with open("output.json", "w", encoding="utf-8") as json_bestand:
    json.dump(output_data, json_bestand, indent=4, ensure_ascii=False)

# Bericht tonen
print("output.json is gemaakt.")

# Verbinding sluiten
cursor.close()
verbinding.close()