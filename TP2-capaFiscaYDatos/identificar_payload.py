"""
Punto a) del TP - Identificar la carga util correspondiente
a nuestro grupo dentro de frames.bin, y guardar el resultado en un
archivo de texto (en vez de solo imprimirlo por consola).
"""

from pathlib import Path

INPUT_FILE = "frames.bin"          # archivo binario recibido
OUTPUT_FILE = "payload_bitbros.txt"  # acá se guarda el resultado
MI_GRUPO = "bitbros"


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
    todos_los_frames = parse_frames(data)

    # Nos quedamos solo con los frames de nuestro grupo
    prefijo = MI_GRUPO[:5].lower()
    mis_frames = [f for f in todos_los_frames if f["group"] == prefijo]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"Grupo: {MI_GRUPO} (prefijo buscado: '{prefijo}')\n")
        out.write(f"Frames encontrados para el grupo: {len(mis_frames)}\n\n")

        for f in mis_frames:
            try:
                texto = f["payload"].decode("ascii")
            except UnicodeDecodeError:
                texto = None

            out.write(f"SEQ: {f['seq']}\n")
            out.write(f"LENGTH: {f['length']}\n")
            out.write(f"PAYLOAD (hex): {f['payload'].hex()}\n")
            out.write(f"PAYLOAD (texto): {texto if texto is not None else '(no es ascii imprimible)'}\n")
            out.write("-" * 40 + "\n")

    print(f"Listo. Resultado guardado en {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
