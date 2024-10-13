from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Налаштування MySQL для віддаленого сервера
app.config['MYSQL_HOST'] = 'localhost'  # IP сервера MySQL
app.config['MYSQL_USER'] = 'new_user'  # Ім'я користувача MySQL
app.config['MYSQL_PASSWORD'] = 'strong_password'  # Пароль користувача MySQL
app.config['MYSQL_DB'] = 'simple_Ad'  # Назва бази даних

mysql = MySQL(app)

# Отримати всі оголошення
@app.route('/ads', methods=['GET'])
def get_ads():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, ip_address, ad_text FROM ads")
    ads = cur.fetchall()
    cur.close()
    return jsonify(ads)

# Додати нове оголошення
@app.route('/ads', methods=['POST'])
def add_ad():
    user_ip = request.remote_addr
    ad_text = request.json.get('ad_text')
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO ads (ip_address, ad_text) VALUES (%s, %s)", (user_ip, ad_text))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message': 'Ad added successfully'})

# Видалити оголошення за IP-адресою користувача та ID
@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    user_ip = request.remote_addr
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ads WHERE id = %s AND ip_address = %s", (ad_id, user_ip))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message': 'Ad deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
