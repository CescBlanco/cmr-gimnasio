import logica

#ARCHIVO PRINCIPAL

def menu():
    """
    Displays the main menu for the gym CRM system and handles user input.
    This function presents a list of options to the user, allowing them to:
    1. Register a new client.
    2. View all registered clients.
    3. Search for a specific client.
    4. Delete a client.
    5. Create a new invoice.
    6. View invoices for a specific client.
    7. View a financial summary for a client.
    8. Exit the program.
    Based on the user's selection, the corresponding function from the 'logica' module is called.
    The menu continues to display until the user chooses to exit.
    """
   
    while True:
        print("\n=== CRM DEL GIMNASIO ===")
        print("1. Registrar cliente")
        print("2. Ver todos los clientes")
        print("3. Buscar cliente")
        print("4. Eliminar cliente")
        print("5. Crear factura")
        print("6. Ver facturas de un cliente")
        print("7. Ver resumen financiero por cliente")
        print("8. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            logica.register_client()
        elif opcion == "2":
            logica.show_clients()
        elif opcion == "3":
            logica.find_and_show_client()
        elif opcion == "4":
            logica.delete_client()
        elif opcion == "5":
            logica.new_invoice()
        elif opcion == "6":
            logica.show_invoices()
        elif opcion == "7":
            logica.show_financial_summary()
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
