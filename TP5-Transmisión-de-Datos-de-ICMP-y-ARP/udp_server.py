import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 12001

# 1. Crear el socket. SOCK_DGRAM = UDP (operación local).
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Asociar IP y puerto locales. No hay listen() ni accept(): UDP no tiene conexiones.
servidor.bind((HOST, PORT))
print(f"[servidor UDP] escuchando en {HOST}:{PORT} ...")

# 3. Esperar UN datagrama. recvfrom() devuelve también quién lo mandó,
#    porque cada datagrama puede venir de un cliente distinto.
datos, direccion_cliente = servidor.recvfrom(1024)
mensaje = datos.decode("utf-8", errors="replace")
print(f"[servidor UDP] recibido de {direccion_cliente[0]}:{direccion_cliente[1]} ({len(datos)} bytes): {mensaje!r}")

# 4. Responder a esa dirección. Un sendto() = un datagrama.
respuesta = f"Recibido: {mensaje}"
servidor.sendto(respuesta.encode("utf-8"), direccion_cliente)
print(f"[servidor UDP] respuesta enviada: {respuesta!r}")

# 5. Cerrar: solo libera el puerto, no viaja nada por la red.
servidor.close()
