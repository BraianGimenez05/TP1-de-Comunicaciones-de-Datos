import socket
import sys

SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
MENSAJE = sys.argv[2] if len(sys.argv) > 2 else "Hola servidor"
SERVER_PORT = 12001

# 1. Crear el socket UDP (operación local).
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.settimeout(5)  # UDP no avisa si el datagrama se perdió: sin timeout esperaríamos para siempre

# 2. connect() en UDP NO genera tráfico: solo fija el destino por defecto y
#    permite que el SO nos informe un ICMP Port Unreachable como error.
cliente.connect((SERVER_IP, SERVER_PORT))
ip_local, puerto_local = cliente.getsockname()
print(f"[cliente UDP] destino {SERVER_IP}:{SERVER_PORT}, desde {ip_local}:{puerto_local}")

# 3. Enviar el mensaje: exactamente un datagrama.
cliente.send(MENSAJE.encode("utf-8"))
print(f"[cliente UDP] enviado: {MENSAJE!r}")

# 4. Esperar la respuesta.
try:
    datos = cliente.recv(1024)
except ConnectionRefusedError:
    sys.exit("[cliente UDP] el host respondió con ICMP Port Unreachable: nadie escucha en ese puerto")
except (socket.timeout, TimeoutError):
    sys.exit("[cliente UDP] sin respuesta (¿se perdió el datagrama? ¿firewall?)")

print(f"[cliente UDP] respuesta ({len(datos)} bytes): {datos.decode('utf-8', errors='replace')!r}")

# 5. Cerrar: no hay FIN, no viaja nada.
cliente.close()
