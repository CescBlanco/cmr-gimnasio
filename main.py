import logica

def menu():
    """
    Displays the main menu for the gym CRM system and handles user input to perform various operations.
    The menu provides the following options:
        1. Register a new client.
        2. View all registered clients.
        3. Search for a client and display their information.
        4. Delete a client from the system.
        5. Create a new invoice for a client.
        6. View invoices associated with a client.
        7. Exit the program.
    The function runs in a loop until the user selects the exit option.
    Delegates the actual operations to corresponding functions in the 'logica' module.
    """
    while True:
        print("\n=== CRM DEL GIMNASIO ===")
        print("1. Registrar cliente")
        print("2. Ver todos los clientes")
        print("3. Buscar cliente")
        print("4. Eliminar cliente")
        print("5. Crear factura")
        print("6. Ver facturas de un cliente")
        print("7. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            logica.registrar_cliente()
        elif opcion == "2":
            logica.mostrar_clientes()
        elif opcion == "3":
            logica.buscar_cliente_y_mostrar()
        elif opcion == "4":
            logica.eliminar_cliente()
        elif opcion == "5":
            logica.nueva_factura()
        elif opcion == "6":
            logica.ver_facturas()
        elif opcion == "7":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
