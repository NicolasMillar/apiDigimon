from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

@app.route('/products', methods=['GET'])
def get_products():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 5432)
        )

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
