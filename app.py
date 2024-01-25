from flask import Flask, jsonify, request
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

@app.route('/cards', methods=['GET'])
def get_cards():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 5432)
        )

        cursor = connection.cursor()

        card_name = request.args.get('cardName')
        booster = request.args.get('booster')

        sql_query = "SELECT * FROM cartas WHERE TRUE"
        if card_name:
            sql_query += f" AND nombre ILIKE '%{card_name}%'"

        if booster:
            sql_query += f" AND booster = '{booster}'"

        cursor.execute(sql_query)

        cards = cursor.fetchall()

        result = []
        for card in cards:
            result.append({
                'id': card[0],
                'cardName': card[1],
                'imageUrl': card[2],
                'booster': card[3]
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
