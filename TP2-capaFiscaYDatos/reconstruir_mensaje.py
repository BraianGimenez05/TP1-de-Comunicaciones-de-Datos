"""
Punto b) del TP - Reordenar los paquetes de TODOS los grupos según su
SEQ y reconstruir la información final concatenando los payloads.

Nota: para que el mensaje quede completo, 'frames.bin' tiene que tener
los frames de todos los grupos (el mismo archivo que usamos en el
punto a), o bien tenés que juntar acá los datos que cada grupo cargó
en la planilla compartida.
"""

from pathlib import Path

INPUT_FILE = "frames.bin"
OUTPUT_FILE = "mensaje_final.txt"


def parse_frames(data: bytes):
    """Recorre 'data' byte a byte y devuelve todos los frames válidos (de cualquier grupo)."""
    n = len(data)
    frames = []
    i = 0
    while i <= n - 7:
        group_bytes = data[i:i + 5]

        # Un header válido empieza con 5 bytes ascii minúscula (a-z)
        if all(0x61 <= b <= 0x7A for b in group_bytes):
            seq = data[i + 5]
            length = data[i + 6]
            payload_start = i + 7
            payload_end = payload_start + length

            if payload_end <= n:
                payload = data[payload_start:payload_end]
                frames.append({
                    "group": group_bytes.decode("ascii"),
                    "seq": seq,
                    "length": length,
                    "payload": payload,
                })
                i = payload_end  # saltamos al final del frame
                continue
        i += 1
    return frames


def main():
    data = Path(INPUT_FILE).read_bytes()
    frames = parse_frames(data)

    # Ordenamos todos los frames (de todos los grupos) por SEQ ascendente
    ordenados = sorted(frames, key=lambda f: f["seq"])

    # Concatenamos los payloads en ese orden
    mensaje_bytes = b"".join(f["payload"] for f in ordenados)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"Total de frames encontrados: {len(frames)}\n\n")
        out.write("Orden de reconstrucción (por SEQ):\n")
        for f in ordenados:
            try:
                texto = f["payload"].decode("ascii")
            except UnicodeDecodeError:
                texto = f"(bytes no ascii: {f['payload'].hex()})"
            out.write(f"  SEQ={f['seq']:<4} grupo={f['group']:<6} payload={texto!r}\n")

        out.write("\nMensaje final reconstruido:\n")
        try:
            out.write(mensaje_bytes.decode("ascii"))
        except UnicodeDecodeError:
            out.write(f"(no decodifica como ascii puro, bytes en hex: {mensaje_bytes.hex()})")
        out.write("\n")

    print(f"Listo. Resultado guardado en {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
