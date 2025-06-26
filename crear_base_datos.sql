CREATE DATABASE crm_gimnasio;
USE crm_gimnasio;

-- Tabla de clientes
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de facturas
CREATE TABLE facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    estado ENUM('Pendiente', 'Pagada', 'Cancelada'),
    codigo_factura VARCHAR(50),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Insertar clientes de prueba
INSERT INTO clientes (nombre, apellidos, email, telefono, direccion)
VALUES 
('Juan', 'Pérez', 'juan.perez@gym.com', '666111222', 'Calle Fit 123'),
('María', 'López', 'maria.lopez@gym.com', '667222333', 'Av. Fitness 456');

-- Insertar facturas de prueba (sin ID personalizado por ahora)
INSERT INTO facturas (id_cliente, descripcion, monto, estado, codigo_factura)
VALUES
(1, 'Membresía enero', 30.00, 'Pagada', 'enero_2025_1'),
(1, 'Clases spinning', 25.00, 'Pendiente', 'enero_2025_2'),
(2, 'Entrenamiento personalizado', 40.00, 'Pagada', 'enero_2025_3');
