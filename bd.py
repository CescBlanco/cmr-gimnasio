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
def add_client( nombre, apellidos, email, telefono, direccion):
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
    """, ( nombre, apellidos, email, telefono, direccion))
    conexion.commit()
    return cursor.lastrowid 

def find_client(email):
    """
    Searches for a client in the 'clientes' table by their email address.

    Args:
        email (str): The email address of the client to search for.

    Returns:
        tuple or None: Returns a tuple containing the client's data if found, or None if no client with the given email exists.
    """
    cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
    return cursor.fetchone()

def find_client_by_name(nombre):
    cursor.execute("SELECT * FROM clientes WHERE nombre LIKE %s", (f"%{nombre}%",))
    return cursor.fetchall()

def get_clients():
    """
    Fetches all clients from the 'clientes' table.

    Returns:
        list of tuple: A list containing tuples with the following client information:
            - id_cliente (int): The unique identifier of the client.
            - nombre (str): The first name of the client.
            - apellidos (str): The last name(s) of the client.
            - email (str): The email address of the client.
    """
    cursor.execute("SELECT * FROM clientes")
    return cursor.fetchall()

def delete_invoce_by_client(id_cliente):
    """
    Deletes all invoices associated with a given client ID from the 'facturas' table.

    Args:
        id_cliente (int): The unique identifier of the client whose invoices will be deleted.

    Side Effects:
        Removes all invoice records for the specified client from the database.
        Commits the transaction.
    """
    cursor.execute("DELETE FROM facturas WHERE id_cliente = %s", (id_cliente,))
    conexion.commit()

def delete_client_by_email(email):
    """
    Deletes a client from the 'clientes' table by their email address.

    Args:
        email (str): The email address of the client to delete.

    Returns:
        bool: True if the client was found and deleted, False otherwise.

    Side Effects:
        - Deletes all invoices associated with the client.
        - Removes the client record from the database.
        - Commits the transaction.
    """
    cliente = find_client(email)
    if not cliente:
        return False

    delete_invoce_by_client(cliente[0])  # First delete the invoices
    cursor.execute("DELETE FROM clientes WHERE email = %s", (email,))
    conexion.commit()
    return True
    
# INVOCES
def create_invoice(id_cliente, descripcion, monto, estado):
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
    return codigo

def client_invoices(id_cliente):
    """
    Retrieves all invoices for a given client by their ID.

    Args:
        id_cliente (int): The unique identifier of the client.

    Returns:
        list of tuple: A list of tuples, each containing:
            - codigo_factura (str): The invoice code.
            - descripcion (str): The invoice description.
            - monto (float): The invoice amount.
            - estado (str): The invoice status.
            - fecha_emision (datetime): The invoice issue date.
    """
    cursor.execute("""
        SELECT codigo_factura, descripcion, monto, estado, fecha_emision
        FROM facturas WHERE id_cliente = %s
    """, (id_cliente,))
    return cursor.fetchall()

def financial_summary():
    """
    Retrieves a financial summary for each client, including:
        - Client's first name, last name, and email.
        - Total number of invoices.
        - Total amount invoiced.
        - Total amount of paid invoices.
        - Total amount of pending invoices.

    Returns:
        list of tuple: Each tuple contains the above information for a client.
    """
    consulta = """
    SELECT 
        c.nombre,
        c.apellidos,
        c.email,
        COUNT(f.id_factura) AS total_facturas,
        COALESCE(SUM(f.monto), 0) AS monto_total,
        COALESCE(SUM(CASE WHEN f.estado = 'Pagada' THEN f.monto ELSE 0 END), 0) AS pagadas,
        COALESCE(SUM(CASE WHEN f.estado = 'Pendiente' THEN f.monto ELSE 0 END), 0) AS pendientes
    FROM clientes c
    LEFT JOIN facturas f ON c.id_cliente = f.id_cliente
    GROUP BY c.id_cliente
    """
    cursor.execute(consulta)
    return cursor.fetchall()
