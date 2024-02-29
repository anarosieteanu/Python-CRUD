def get_options(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT denumire, id_produs FROM produs")
    products = cur.fetchall()
    product_options = [
        {"label": product['denumire'], "id": product['id_produs']} for product in products
    ]

    cur.execute("SELECT nume, prenume, id_client FROM client")
    clients = cur.fetchall()
    client_options = [
        {
            "label": f"{client['nume']} {client['prenume']}",
            "id": client['id_client'],
        }
        for client in clients
    ]

    status = ["In procesare", "Preluata", "In curs de livrare","Livrata"]
    options = {
        "products": product_options,
        "clients": client_options,
        "status": status,
    }
    return options