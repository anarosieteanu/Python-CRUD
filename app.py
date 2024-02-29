from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL

from options import get_options


app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "l3LlRhDcVnKIzH"
app.config["MYSQL_DB"] = "companie"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def Index():
    return render_template("index.html")


@app.route("/clients/", methods=["POST", "GET"])
def clients():
    if request.method == "POST":
        nume = request.form["nume"]
        prenume = request.form["prenume"]
        nr_telefon = request.form["nr_telefon"]
        email = request.form["email"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO client (nume, prenume, nr_telefon, email) VALUES (%s, %s, %s, %s)",
            (nume, prenume, nr_telefon, email),
        )
        mysql.connection.commit()
        return redirect(url_for("clients"))
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM client")
        clients = cur.fetchall()
        return render_template(
            "clients.html",
            clients=clients,
        )


@app.route("/clients/delete/<id_client>", methods=["POST", "GET"])
def delete_client(id_client):
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM client WHERE id_client = %s", (id_client,))
        mysql.connection.commit()
        return redirect(url_for("clients"))
    if request.method == "GET":
        return render_template("deleteForm.html", id=id_client, url="clients")


@app.route("/clients/update/<id_client>", methods=["POST", "GET"])
def update_client(id_client):
    if request.method == "POST":
        nume = request.form["nume"]
        prenume = request.form["prenume"]
        nr_telefon = request.form["nr_telefon"]
        email = request.form["email"]
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE client SET nume = %s, prenume = %s, email = %s, nr_telefon = %s WHERE id_client = %s",
            (
                nume,
                prenume,
                email,
                nr_telefon,
                id_client,
            ),
        )
        mysql.connection.commit()
        return redirect(url_for("clients"))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM client WHERE id_client = %s", (id_client,))
        client = cur.fetchone()
        return render_template("editClient.html", client=client, url="clients")


@app.route("/orders/", methods=["POST", "GET"])
def orders():
    if request.method == "POST":
        id_client = request.form["id_client"]
        id_produs = request.form["id_produs"]
        status = request.form["status"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO comanda (id_client, id_produs, status) VALUES (%s, %s, %s)",
            (id_client, id_produs, status),
        )
        mysql.connection.commit()
        return redirect(url_for("orders"))

    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id_comanda, nume, prenume, denumire, status FROM companie.comanda JOIN client USING(id_client) JOIN produs USING(id_produs)"
        )
        orders = cur.fetchall()
        options = get_options(mysql)
        return render_template("orders.html", orders=orders, options=options)


@app.route("/orders/delete/<id_comanda>", methods=["POST", "GET"])
def delete_order(id_comanda):
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM comanda WHERE id_comanda = %s", (id_comanda,))
        mysql.connection.commit()
        return redirect(url_for("orders"))
    if request.method == "GET":
        return render_template("deleteForm.html", id=id_comanda, url="orders")


@app.route("/orders/update/<id_comanda>", methods=["POST", "GET"])
def update_order(id_comanda):
    if request.method == "POST":
        id_client = request.form["id_client"]
        id_produs = request.form["id_produs"]
        status = request.form["status"]
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE comanda SET id_client = %s, id_produs = %s, status=%s WHERE id_comanda = %s",
            (
                id_client,
                id_produs,
                status,
                id_comanda,
            ),
        )
        mysql.connection.commit()
        return redirect(url_for("orders"))
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM comanda WHERE id_comanda = %s", (id_comanda,))
        order = cur.fetchone()
        options = get_options(mysql)
        return render_template(
            "editOrder.html", order=order, url="orders", options=options
        )


@app.route("/products/", methods=["POST", "GET"])
def products():
    if request.method == "POST":
        denumire = request.form["denumire"]
        pret = request.form["pret"]
        stoc = request.form["stoc"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO produs (denumire, pret, stoc, data_primire) VALUES (%s, %s, %s, %s)",
            (denumire, pret, stoc, datetime.now()),
        )
        mysql.connection.commit()
        return redirect(url_for("products"))
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM produs")
        products = cur.fetchall()
        return render_template(
            "products.html",
            products=products,
        )


@app.route("/products/delete/<id_produs>", methods=["POST", "GET"])
def delete_product(id_produs):
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM produs WHERE id_produs = %s", (id_produs,))
        mysql.connection.commit()
        return redirect(url_for("products"))
    if request.method == "GET":
        return render_template("deleteForm.html", id=id_produs, url="products")


@app.route("/products/update/<id_produs>", methods=["POST", "GET"])
def update_product(id_produs):
    if request.method == "POST":
        denumire = request.form["denumire"]
        pret = request.form["pret"]
        stoc = request.form["stoc"]
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE produs SET denumire = %s, pret = %s, stoc = %s WHERE id_produs = %s",
            (
                denumire,
                pret,
                stoc,
                id_produs,
            ),
        )
        mysql.connection.commit()
        return redirect(url_for("products"))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM produs WHERE id_produs = %s", (id_produs,))
        product = cur.fetchone()
        return render_template("editProduct.html", product=product, url="products")


if __name__ == "__main__":
    app.run(debug=True)
