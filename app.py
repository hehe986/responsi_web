from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

hostname = "lhj5k.h.filess.io"
database = "ResponsiWeb_penreachso"
port = "3305"
username = "ResponsiWeb_penreachso"
password = "f6aa010f08366ade07e756cbcd47cf0f73726bf5"


def create_connection():
    """ Create a database connection """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port
        )
        if connection.is_connected():
            print("Connected to MariaDB Server")
    except Error as e:
        print("Error while connecting to MariaDB", e)
    return connection

@app.route('/')
def halaman_awal():
    connection = create_connection()
    if connection is None:
        return "Error: Unable to connect to the database.", 500  # Return an error response

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tbl_mhs")
        result = cursor.fetchall()
    except Error as e:
        print("Error fetching data:", e)
        return "Error fetching data from the database.", 500
    finally:
        cursor.close()
        connection.close()

    return render_template('index.html', hasil=result)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    
    connection = create_connection()
    if connection is None:
        return "Error: Unable to connect to the database.", 500

    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO tbl_mhs (nim, nama, asal) VALUES (%s, %s, %s)', (nim, nama, asal))
        connection.commit()
    except Error as e:
        print("Error inserting data:", e)
        return "Error inserting data into the database.", 500
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('halaman_awal'))

@app.route('/ubah/<nim>', methods=['GET'])
def ubah_data(nim):
    connection = create_connection()
    if connection is None:
        return "Error: Unable to connect to the database.", 500

    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tbl_mhs WHERE nim=%s', (nim,))
        res = cursor.fetchall()
    except Error as e:
        print("Error fetching data for update:", e)
        return "Error fetching data for update.", 500
    finally:
        cursor.close()
        connection.close()

    return render_template('ubah.html', hasil=res)

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    no_mhs = request.form['nim_ori']
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    
    connection = create_connection()
    if connection is None:
        return "Error: Unable to connect to the database.", 500

    try:
        cursor = connection.cursor()
        sql = "UPDATE tbl_mhs SET nim=%s, nama=%s, asal=%s WHERE nim=%s" 
        value = (nim, nama, asal, no_mhs)
        cursor.execute(sql, value)
        connection.commit()
    except Error as e:
        print("Error updating data:", e)
        return "Error updating data in the database.", 500
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('halaman_awal'))  

@app.route('/hapus/<nim>', methods=['GET'])
def hapus_data(nim):
    connection = create_connection()
    if connection is None:
        return "Error: Unable to connect to the database.", 500

    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM tbl_mhs WHERE nim=%s', (nim,))
        connection.commit()
    except Error as e:
        print("Error deleting data:", e)
        return "Error deleting data from the database.", 500
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('halaman_awal'))

if __name__ == '__main__':
    app.run(debug=True)