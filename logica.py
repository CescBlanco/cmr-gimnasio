import bd

def registrar_cliente():
    
    """
    Registers a new client by prompting for their information via the console.
    Prompts the user to enter the client's first name, last name, and email address.
    Checks if a client with the same email already exists in the database.
    If the client does not exist, optionally prompts for the client's phone number and address,
    then adds the client to the database.
    Prints informative messages about the outcome of the operation.
    """
    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")
    email = input("Email: ")

    if bd.buscar_cliente(email):
        print("Ya existe un cliente con ese email.")
        return

    telefono = input("Teléfono (opcional): ")
    direccion = input("Dirección (opcional): ")

    bd.agregar_cliente(nombre, apellidos, email, telefono, direccion)
    print("Cliente registrado correctamente.")

def mostrar_clientes():
    """
    Displays a list of clients retrieved from the database.

    This function fetches all clients using the `bd.obtener_clientes()` method and prints each client's
    ID, first name, last name, and an additional attribute (such as email or phone number) in a formatted string.

    Returns:
        None
    """
    clientes = bd.obtener_clientes()
    for c in clientes:
        print(f"{c[0]}. {c[1]} {c[2]} - {c[3]}")


def buscar_cliente_y_mostrar():
    """
    Prompts the user to enter a client's email, searches for the client in the database,
    and displays the client's information if found.

    The function interacts with the user via the console to obtain the email address.
    It then calls 'bd.buscar_cliente' to search for the client in the database.
    If the client exists, their name and additional information are printed.
    If not, a message indicating that the client was not found is displayed.
    """
    email = input("Email del cliente: ")
    cliente = bd.buscar_cliente(email)
    if cliente:
        print(f"Cliente: {cliente[1]} {cliente[2]} - {cliente[3]}")
    else:
        print("Cliente no encontrado.")

def eliminar_cliente():
    """
    Deletes a client from the database based on their email address.

    Prompts the user to enter the email of the client to be removed. If the client is found in the database,
    the client is deleted and a confirmation message is displayed. If the client is not found, an error message is shown.

    Returns:
        None
    """
    email = input("Email del cliente a eliminar: ")
    cliente = bd.buscar_cliente(email)
    if not cliente:
        print("Cliente no encontrado.")
        return
    bd.eliminar_cliente(email)
    print("Cliente eliminado correctamente.")

def nueva_factura():
    """
    Creates a new invoice for a client.
    Prompts the user to input the client's email, searches for the client in the database,
    and if found, collects the service description, amount, and invoice status from the user.
    Then, creates a new invoice record in the database for the specified client.
    Returns:
        None
    """
    email = input("Email del cliente: ")
    cliente = bd.buscar_cliente(email)
    if not cliente:
        print("Cliente no encontrado.")
        return

    descripcion = input("Descripción del servicio: ")
    monto = float(input("Monto: "))
    print("Estado: 1. Pendiente  2. Pagada  3. Cancelada")
    estado = {
        "1": "Pendiente",
        "2": "Pagada",
        "3": "Cancelada"
    }.get(input("Elige estado: "), "Pendiente")

    bd.crear_factura(cliente[0], descripcion, monto, estado)

def ver_facturas():
    """
    Displays the invoices associated with a client based on their email address.
    Prompts the user to enter the client's email, searches for the client in the database,
    and retrieves all invoices related to that client. If the client is found, prints a list
    of their invoices with details. If the client is not found or has no invoices, displays
    an appropriate message.
    """
    email = input("Email del cliente: ")
    cliente = bd.buscar_cliente(email)
    if not cliente:
        print("Cliente no encontrado.")
        return

    facturas = bd.facturas_de_cliente(cliente[0])
    if facturas:
        print(f"Facturas de {cliente[1]} {cliente[2]}:")
        for f in facturas:
            print(f"{f[0]}: {f[1]} - ${f[2]} - {f[3]}")
    else:
        print("No hay facturas registradas.")
