# Script om data uit database te halen en naar JSON te schrijven

# Imports
import mysql.connector
import json


# ---------------- VERBINDING ----------------
def maak_verbinding():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Azadegan24",
        database="attractiepark"
    )


# ---------------- BEZOEKER OPHALEN ----------------
def haal_bezoeker_op(cursor):
    query = "SELECT * FROM bezoeker WHERE id = %s"
    cursor.execute(query, (1,))
    return cursor.fetchone()


# ---------------- ATTRACTIES OPHALEN ----------------
def haal_attracties_op(cursor):
    query = """
    SELECT * FROM voorziening
    WHERE actief = 1
    AND (soort = 'attractie' OR soort = 'achtbaan')
    AND geschatte_wachttijd <= 25
    """
    cursor.execute(query)
    return cursor.fetchall()


# ---------------- HORECA OPHALEN ----------------
def haal_horeca_op(cursor):
    query = """
    SELECT * FROM voorziening
    WHERE actief = 1
    AND soort = 'horeca'
    ORDER BY geschatte_wachttijd ASC
    LIMIT 1
    """
    cursor.execute(query)
    return cursor.fetchone()


# ---------------- JSON SCHRIJVEN ----------------
def schrijf_json(data):
    with open("output.json", "w") as bestand:
        json.dump(data, bestand, indent=4)


# ---------------- MAIN PROGRAMMA ----------------
def main():
    verbinding = maak_verbinding()
    cursor = verbinding.cursor(dictionary=True)

    bezoeker = haal_bezoeker_op(cursor)
    attracties = haal_attracties_op(cursor)
    horeca = haal_horeca_op(cursor)

    output_data = {
        "bezoeker": bezoeker,
        "geschikte_attracties": attracties,
        "geschikte_horeca": horeca
    }

    schrijf_json(output_data)

    print("output.json is gemaakt.")

    cursor.close()
    verbinding.close()


# Start het programma
main()
