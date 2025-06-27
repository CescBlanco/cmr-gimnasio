import bd
from datetime import datetime

def register_client():
    """
    Registers a new client by collecting user input for personal information, 
    validates if the client already exists based on email, and adds the client 
    to the database if not present. Displays confirmation and registration date.
    
    Prompts:
        - Nombre (Name)
        - Apellidos (Last name)
        - Email
        - Teléfono (Phone, optional)
        - Dirección (Address, optional)
    
    Returns:
        None
    """
   
    print("\n=== REGISTRO DE NUEVO USUARIO ===\n")
    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")
    email = input("Email: ")

    if bd.find_client(email):
        print("Ya existe un cliente con ese email.")
        return

    telefono = input("Teléfono (opcional): ")
    direccion = input("Dirección (opcional): ")

    bd.add_client(nombre, apellidos, email, telefono, direccion)
    print(" ")
    print("Usuario registrado exitosamente!")

    fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M")
    print(f"Fecha de registro: {fecha_registro}")

def show_clients():
    """
    Displays a list of registered clients retrieved from the database.
    Fetches client data using the `bd.get_clients()` function. If no clients are found,
    prints a message indicating that there are no registered clients. Otherwise, prints
    a formatted list of all clients, including their ID, name, email, phone number (or
    a placeholder if not specified), and registration date. Also displays the total
    number of registered users at the end.
    
    Returns:
    None
    """
   
    clientes = bd.get_clients()
    
    if not clientes:
        print("No hay clientes registrados.")
        return
    
    print(" ")
    print("=== LISTA DE USUARIOS ===\n")

    for idx, c in enumerate(clientes, start=1):
        print(f"Usuario #{idx}:")
        print(f"ID: USR{c[0]:03}")
        print(f"Nombre: {c[1]} {c[2]}")
        print(f"Email: {c[3]}")
        print(f"Teléfono: {c[4] if c[4] else 'No especificado'}")
        print(f"Fecha de registro: {c[6].strftime('%d/%m/%Y')}\n")

    print(f"Total de usuarios registrados: {len(clientes)}")



def find_and_show_client():
    """
    Allows searching for a client by email or name and displays their information.

    Prompts the user to choose the search method (by email or by name).
    - If searching by email, retrieves and displays the client if found.
    - If searching by name, retrieves and displays all clients matching the name.
    - If no client is found, displays an appropriate message.

    Returns:
        None
    """
    print(" ")
    print("=== BUSCAR UN USUARIO ===")
    print("1. Buscar por email")
    print("2. Buscar por nombre")
    print(" ")
    opcion = input("Seleccione método de búsqueda: ")

    if opcion == "1":
        email = input("Ingrese email: ")
        cliente = bd.find_client(email)
        if cliente:
            print(" ")
            print("--- USUARIO ENCONTRADO ---")
            print(f"ID: USR{cliente[0]:03}")
            print(f"Nombre: {cliente[1]} {cliente[2]}")
            print(f"Email: {cliente[3]}")
            print(f"Teléfono: {cliente[4] if cliente[4] else 'No especificado'}")
            print(f"Dirección: {cliente[5] if cliente[5] else 'No especificado'}")
            print(f"Fecha de registro: {cliente[6].strftime('%d/%m/%Y')}")
        else:
            print("Usuario no encontrado.")
    
    elif opcion == "2":
        nombre = input("Ingrese nombre: ")
        clientes = bd.find_client_by_name(nombre)
        if clientes:
            for c in clientes:
                print(" ")
                print("--- USUARIO ENCONTRADO ---")
                print(f"ID: USR{c[0]:03}")
                print(f"Nombre: {c[1]} {c[2]}")
                print(f"Email: {c[3]}")
                print(f"Teléfono: {c[4] if c[4] else 'No especificado'}")
                print(f"Dirección: {c[5] if c[5] else 'No especificado'}")
                print(f"Fecha de registro: {c[6].strftime('%d/%m/%Y')}\n")
        else:
            print("No se encontraron usuarios con ese nombre.")
    else:
        print("Opción no válida.")

def delete_client():
    """
    Deletes a client and their invoices from the database based on the provided email.
    Prompts the user to enter the email of the client to be deleted. If the client is found and deleted successfully,
    a confirmation message is displayed. If the client is not found, an error message is shown and the function
    recursively prompts the user to enter another email.
    
    Returns:
        None
    """
    
    email = input("\nEmail del cliente a eliminar: ")
    if bd.delete_client_by_email(email):
        print("Cliente y facturas eliminados correctamente.")
    else:
        print("Cliente no encontrado.")
        delete_client()
    

def new_invoice():
    """
    Creates a new invoice for a client.
    Prompts the user to enter the client's email, finds the client in the database,
    and collects invoice details (description, amount, and status). If the client is not found,
    prompts again recursively. After creation, displays the invoice summary.
    
    Returns:
        None
    """

    print(" ")
    print("--- CREAR FACTURA ---")
    email = input("Ingrese email del cliente: ")
    cliente = bd.find_client(email)
    if cliente:
        print(" ")
        print("Cliente encontrado")
    else: 
        print("Cliente no encontrado.")
        print(" ")
        # If client not found, prompt again recursively
        return new_invoice()

    print(" ")
    descripcion = input("Descripción del servicio: ")
    monto = float(input("Ingrese monto total: "))
    print("Estado: 1. Pendiente  2. Pagada  3. Cancelada")
    estado = {
        "1": "Pendiente",
        "2": "Pagada",
        "3": "Cancelada"
    }.get(input("Elige estado: "), "Pendiente")

    # Create the invoice in the database
    codigo = bd.create_invoice(cliente[0], descripcion, monto, estado)

    fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M")
    nombre_cliente = f"{cliente[1]} {cliente[2]}"

    # Display invoice summary
    print("\nFactura creada exitosamente!")
    print(f"Número de factura: {codigo}")
    print(f"Fecha de emisión: {fecha_emision}")
    print(f"Cliente: {nombre_cliente}")
    print(f"Descripción: {descripcion}")
    print(f"Monto: ${monto:.2f}")
    print(f"Estado: {estado}")

def show_invoices():
    """
    Displays all invoices for a user based on their email address.
    Prompts the user to enter an email, searches for the corresponding client,
    and retrieves all invoices associated with that client. For each invoice,
    prints its details including number, date, description, amount, and status.
    Also displays the total number of invoices, the total amount invoiced, and
    the total amount pending. If the client or invoices are not found, prints
    an appropriate message.
    Returns:
        None
    """
    
    print(" ")
    print("=== FACTURAS POR USUARIO ===")
    print(" ")
    email = input("Ingrese email del usuario: ")
    print(" ")
    cliente = bd.find_client(email)
    
    if not cliente:
        print("Cliente no encontrado.")
        return

    facturas = bd.client_invoices(cliente[0])
    
    if not facturas:
        print(f"No hay facturas registradas para {cliente[1]} {cliente[2]}.")
        return
    print(" ")
    print(f"--- FACTURAS DE {cliente[1]} {cliente[2]} ---\n")

    total_monto = 0
    total_pendiente = 0

    for idx, f in enumerate(facturas, start=1):
        codigo, descripcion, monto, estado, fecha = f
        print(f"Factura #{idx}:")
        print(f"Número: {codigo}")
        print(f"Fecha: {fecha.strftime('%d/%m/%Y %H:%M')}")
        print(f"Descripción: {descripcion}")
        print(f"Monto: ${monto:.2f}")
        print(f"Estado: {estado}\n")

        total_monto += monto
        if estado == "Pendiente":
            total_pendiente += monto

    print(f"Total de facturas: {len(facturas)}")
    print(f"Monto total facturado: ${total_monto:.2f}")
    print(f"Monto pendiente: ${total_pendiente:.2f}")


def show_financial_summary():
    """
    Displays a financial summary for all users.
    Retrieves summary data from the database using bd.financial_summary().
    For each user, prints their name, email, total invoices, total amount,
    amount paid, and amount pending. At the end, prints a general summary
    including total users, total invoices, total income, received income,
    and pending income.

    Returns:
        None
    """
    
    print("=== RESUMEN FINANCIERO ===\n")
    resumen = bd.financial_summary()

    total_usuarios = 0
    total_facturas = 0
    total_ingresos = 0
    total_pendientes = 0

    for r in resumen:
        nombre = f"{r[0]} {r[1]}"
        email = r[2]
        num_facturas = r[3]
        monto_total = r[4]
        pagado = r[5]
        pendiente = r[6]

        print(f"Usuario: {nombre} ({email})")
        print(f"- Total facturas: {num_facturas}")
        print(f"- Monto total: ${monto_total:.2f}")
        print(f"- Facturas pagadas: ${pagado:.2f}")
        print(f"- Facturas pendientes: ${pendiente:.2f}\n")

        total_usuarios += 1
        total_facturas += num_facturas
        total_ingresos += monto_total
        total_pendientes += pendiente

    print("--- RESUMEN GENERAL ---")
    print(f"Total usuarios: {total_usuarios}")
    print(f"Total facturas emitidas: {total_facturas}")
    print(f"Ingresos totales: ${total_ingresos:.2f}")
    print(f"Ingresos recibidos: ${total_ingresos - total_pendientes:.2f}")
    print(f"Ingresos pendientes: ${total_pendientes:.2f}")