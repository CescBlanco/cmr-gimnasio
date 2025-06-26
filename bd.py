import os
import mysql.connector
from datetime import datetime

import os
import mysql.connector
from datetime import datetime

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Si no está instalado python-dotenv, simplemente ignora

# Leer configuración desde variables de entorno
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_HOST, DB_USER, DB_PASS, DB_NAME]):
    raise RuntimeError("Faltan variables de entorno para la conexión a la base de datos. Define DB_HOST, DB_USER, DB_PASS y DB_NAME.")

conexion = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)
cursor = conexion.cursor()

# Generate invoice code in the format: january_2025_1
def generate_invoice_code():
    """
    Generates a unique invoice code based on the current month and year,
    and the number of invoices already created in that period.
    Format: <month>_<year>_<sequential_number>
    Example: january_2025_1
    """
    date_now = datetime.now()
    month = date_now.strftime("%B").lower()
    year = date_now.year

    cursor.execute("""
        SELECT COUNT(*) FROM facturas
        WHERE MONTH(fecha_emision) = %s AND YEAR(fecha_emision) = %s
    """, (date_now.month, year))
    total = cursor.fetchone()[0] + 1

    return f"{month}_{year}_{total}"

# Clientes
def agregar_cliente(nombre, apellidos, email, telefono, direccion):
    """
    Adds a new client to the 'clientes' table in the database.

    Parameters:
        nombre (str): The first name of the client.
        apellidos (str): The last name(s) of the client.
        email (str): The email address of the client.
        telefono (str): The phone number of the client.
        direccion (str): The address of the client.

    Commits the transaction after inserting the new client.
    """
    cursor.execute("""
        INSERT INTO clientes (nombre, apellidos, email, telefono, direccion)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, apellidos, email, telefono, direccion))
    conexion.commit()

def buscar_cliente(email):
    """
    Searches for a client in the 'clientes' table by their email address.

    Args:
        email (str): The email address of the client to search for.

    Returns:
        tuple or None: Returns a tuple containing the client's data if found, or None if no client with the given email exists.
    """
    cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
    return cursor.fetchone()

def obtener_clientes():
    """
    Fetches all clients from the 'clientes' table.

    Returns:
        list of tuple: A list containing tuples with the following client information:
            - id_cliente (int): The unique identifier of the client.
            - nombre (str): The first name of the client.
            - apellidos (str): The last name(s) of the client.
            - email (str): The email address of the client.
    """
    cursor.execute("SELECT id_cliente, nombre, apellidos, email FROM clientes")
    return cursor.fetchall()

def eliminar_cliente(email):
    """
    Deletes a client from the 'clientes' table in the database based on the provided email address.

    Args:
        email (str): The email address of the client to be deleted.

    Returns:
        None

    Raises:
        Exception: If the database operation fails.
    """
    cursor.execute("DELETE FROM clientes WHERE email = %s", (email,))
    conexion.commit()
    
# Facturas
def crear_factura(id_cliente, descripcion, monto, estado):
    """
    Creates a new invoice record in the database for a given client.

    Args:
        id_cliente (int): The ID of the client for whom the invoice is created.
        descripcion (str): A description of the invoice.
        monto (float): The amount of the invoice.
        estado (str): The status of the invoice (e.g., 'paid', 'pending').
        
    Returns:
        None

    Side Effects:
        Inserts a new row into the 'facturas' table in the database.
        Commits the transaction.
        Prints the generated invoice code to the console.
    """
    codigo = generate_invoice_code()
    cursor.execute("""
        INSERT INTO facturas (id_cliente, descripcion, monto, estado, codigo_factura)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_cliente, descripcion, monto, estado, codigo))
    conexion.commit()
    print(f"Factura creada con código: {codigo}")

def facturas_de_cliente(id_cliente):
    """
    Retrieves all invoices associated with a specific client.

    Args:
        id_cliente (int): The unique identifier of the client whose invoices are to be fetched.

    Returns:
        list of tuple: A list of tuples, each containing the invoice code, description, amount, and status for the specified client.
    """
    cursor.execute("""
        SELECT codigo_factura, descripcion, monto, estado 
        FROM facturas WHERE id_cliente = %s
    """, (id_cliente,))
    return cursor.fetchall()
