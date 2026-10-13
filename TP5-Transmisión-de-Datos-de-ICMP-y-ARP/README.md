# TP5 — Transmisión de Datos: de ICMP y ARP a Sockets TCP

Todas las capturas están en [`capturas/`](capturas/) y se abren con Wireshark. Los filtros que se mencionan son *display filters*.

## 1) ICMP y primer contacto con Wireshark

### Investigación

**a) ¿Qué es ICMP y para qué se usa?**
ICMP (Internet Control Message Protocol, RFC 792) es el protocolo de **mensajes de control y error** de la capa de red. Lo usan los hosts y routers para informar problemas en la entrega de datagramas IP (destino inalcanzable, TTL agotado, necesidad de fragmentar) y para diagnóstico (Echo Request/Reply, que usa `ping`; Time Exceeded, que aprovecha `traceroute`).
**No transporta datos de aplicaciones**: no tiene puertos ni entrega datos a procesos de usuario como TCP o UDP. Sus mensajes son generados y consumidos por el propio stack de red del sistema operativo.

**b) Relación con IP**
ICMP se considera parte de la capa de red (acompaña a IP), pero **viaja dentro de IP**: un mensaje ICMP es el payload de un datagrama IPv4. El receptor sabe que el contenido es ICMP por el campo **Protocol** del encabezado IPv4, que vale **1** (TCP = 6, UDP = 17).

**c) ¿Qué hace ping?**
`ping` envía mensajes **ICMP Echo Request** a un destino y espera los **ICMP Echo Reply** correspondientes; mide el tiempo de ida y vuelta (RTT) y cuenta las pérdidas. Sirve para comprobar alcanzabilidad y latencia.
Se distinguen por los campos **Type** y **Code**: Echo Request = **Type 8, Code 0**; Echo Reply = **Type 0, Code 0**.

**d) Contenido mínimo de un mensaje ICMP Echo**
Encabezado de 8 bytes:

| Campo | Tamaño | Función |
|---|---|---|
| Type | 1 B | 8 (Request) / 0 (Reply) |
| Code | 1 B | 0 |
| Checksum | 2 B | Integridad del mensaje ICMP completo |
| Identifier | 2 B | Identifica el proceso/sesión de ping |
| Sequence number | 2 B | Numera cada Echo dentro de la sesión |

Más un campo **Data** opcional de longitud variable, que el Reply debe devolver idéntico.

### Configuración de red de la computadora usada

Comandos: `ip addr` y `ip route` (Linux).

```
$ ip addr show wlp1s0
2: wlp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 58:02:05:53:72:b1 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.46/24 brd 192.168.1.255 scope global dynamic noprefixroute wlp1s0
$ ip route
default via 192.168.1.1 dev wlp1s0 proto dhcp src 192.168.1.46 metric 600
192.168.1.0/24 dev wlp1s0 proto kernel scope link src 192.168.1.46 metric 600
```

| Parámetro | Valor |
|---|---|
| Interfaz | `wlp1s0` (Wi-Fi) |
| Dirección IPv4 / máscara | 192.168.1.46/24 → 255.255.255.0 |
| Gateway por defecto | 192.168.1.1 |
| Dirección MAC | 58:02:05:53:72:b1 |

### Captura de ping

Archivo: [`capturas/01_icmp.pcapng`](capturas/01_icmp.pcapng) — comandos `ping -4 -c 4 192.168.1.1` y `ping -4 -c 4 8.8.8.8`, filtro `icmp`.

```
$ ping -4 -c 4 192.168.1.1
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=2.39 ms
...
4 packets transmitted, 4 received, 0% packet loss
$ ping -4 -c 4 8.8.8.8
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=72.6 ms
...
4 packets transmitted, 4 received, 0% packet loss
```

Paquetes 1–8: ping al gateway; 9–18: ping a 8.8.8.8 (los paquetes 14 y 15 son un ARP que se coló en la captura, ver punto 2).

### Tabla de capas de un Echo Request (paquete 9, hacia 8.8.8.8)

| Capa (Wireshark) | Origen | Destino | ¿Qué campo indica qué viene "adentro"? |
|---|---|---|---|
| Ethernet II | 58:02:05:53:72:b1 (nuestra placa) | 4c:d7:c8:f6:10:4c (gateway) | **Type = 0x0800** (IPv4) |
| Internet Protocol Version 4 | 192.168.1.46 | 8.8.8.8 | **Protocol = 1** (ICMP) |
| Internet Control Message Protocol | — (ICMP no tiene direcciones ni puertos; lo identifican **Identifier = 0x5092** y **Sequence = 1**) | — | Ninguno: **Type = 8, Code = 0** dicen *qué mensaje* es; lo que sigue son sus datos |
| Datos / payload | — (56 bytes) | — | — (último nivel) |

### Preguntas

**a) MAC destino del Echo Request a 8.8.8.8**
No es la MAC de 8.8.8.8: es **4c:d7:c8:f6:10:4c, la MAC del gateway (router)**, y es exactamente la misma MAC destino que tiene el ping al gateway (paquete 1). Es decir, a nivel Ethernet las dos tramas van al mismo equipo; lo único que cambia es la IP destino.
Conclusión: la **dirección MAC tiene alcance local (un solo enlace/LAN)**; cada salto reescribe el encabezado Ethernet. La **dirección IP es extremo a extremo**: el destino IP sigue siendo 8.8.8.8 durante todo el recorrido. Cuando el destino no está en la propia subred (192.168.1.0/24), el host le entrega la trama al gateway (MAC del gateway, IP de 8.8.8.8).

**b) Echo Request vs Echo Reply** (paquetes 9 y 10; Wireshark los vincula con `[Response frame: 10]`)

| Capa | Campos que cambian | Campos que se mantienen |
|---|---|---|
| Ethernet | MAC origen y destino se **invierten** | Type (0x0800) |
| IP | IP origen y destino se **invierten**; **TTL** 64 → 118; **Identification** 0x3ce7 → 0x0000; **Header checksum** (recalculado porque cambian campos) | Versión, IHL (20 B), Protocol (1), Total length (84 B) |
| ICMP | **Type** 8 → 0; **Checksum** 0x6d2c → 0x752c (cambia porque cambió Type: exactamente 0x0800 de diferencia) | Code (0), **Identifier** (0x5092), **Sequence number** (1), Data (56 B idénticos) |

El identificador y el número de secuencia se mantienen porque son la forma en que `ping` **asocia cada respuesta con su pedido**: el identifier separa sesiones de ping simultáneas (se ve que el ping al gateway usó 0x5091 y el de 8.8.8.8 usó 0x5092) y el sequence permite calcular el RTT de cada Echo y detectar pérdidas o desorden. El receptor está obligado a devolverlos sin cambios.

**c) Payload de ping**
Está en el campo **Data** de ICMP, después de los 8 bytes de encabezado. En nuestra captura (Linux) tiene **56 bytes**:

```
46 8d cd 6a 00 00 00 00  5a 75 0d 00 00 00 00 00   ← 16 B: marca de tiempo (struct timeval: segundos + microsegundos)
10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f   ← 40 B: patrón incremental 0x10, 0x11, … 0x37
20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f
30 31 32 33 34 35 36 37
```

ICMP total = 64 B, IP = 84 B, trama = 98 B. En el Reply el payload es **idéntico** (el receptor lo copia); por eso `ping` puede calcular el RTT con la marca de tiempo que vuelve.
En Windows el payload es de **32 bytes** con el texto `abcdefghijklmnopqrstuvwabcdefghi` (ICMP = 40 B, IP = 60 B, trama = 74 B). Que sea distinto entre sistemas operativos muestra que **el contenido del Echo lo decide la implementación de ping**, no el protocolo; además es una huella que permite inferir el SO que generó el ping.

**d) TTL**
Echo Request enviado: **TTL = 64** (valor inicial de Linux). Reply recibido de 8.8.8.8: **TTL = 118**. En cambio, el Reply del gateway llega con TTL = 64 (está en la misma LAN, no pasó por ningún router).
No son iguales porque **cada sistema elige su TTL inicial** y **cada router que reenvía el datagrama decrementa el TTL en 1** (si llega a 0 lo descarta y envía un ICMP Time Exceeded). El TTL que vemos en el Request es el inicial (todavía no pasó por ningún router); el del Reply ya fue decrementado por todos los routers del camino de vuelta. Como 118 es menor que 128, lo más probable es que el servidor de Google use un TTL inicial de 128, con lo que el Reply atravesó aproximadamente **128 − 118 = 10 routers**.

**e) Encapsulación ("cajas dentro de cajas")** — valores del paquete 9:

```
┌──────────────────────── Trama Ethernet II: 98 B ────────────────────────┐
│ Encab. Ethernet 14 B │ ┌──────────── Datagrama IPv4: 84 B ────────────┐ │
│ dst MAC | src MAC |  │ │ Encab. IP 20 B │ ┌─── Mensaje ICMP: 64 B ───┐ │ │
│ Type 0x0800          │ │ Protocol = 1   │ │ Encab. ICMP 8 B │ Datos  │ │ │
│                      │ │                │ │ Type 8 / Code 0 │ 56 B   │ │ │
│                      │ │                │ └─────────────────┴────────┘ │ │
│                      │ └──────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```
14 + 20 + 8 + 56 = 98 B. (Wireshark no muestra el FCS de 4 B ni el preámbulo, que la placa quita antes de entregar la trama.)

---

## 2) ARP: de una IP a una dirección MAC

### Investigación

**a) ¿Qué problema resuelve ARP? ¿En qué capa?**
ARP (Address Resolution Protocol, RFC 826) traduce una **dirección IPv4 de la red local** en la **dirección MAC** necesaria para armar la trama Ethernet. Su ubicación es discutible: sirve a la capa de red (resuelve direcciones IP) pero **no viaja dentro de IP**, va directamente en una trama Ethernet y su alcance es un solo enlace, como la capa 2. Por eso suele decirse que está "entre la 2 y la 3" (a veces "capa 2,5").

**b) ARP Request y ARP Reply**
- **Request** (opcode 1): "¿Quién tiene la IP X? Decíselo a (mi IP, mi MAC)". Se envía en **broadcast** (`ff:ff:ff:ff:ff:ff`) porque todavía no se conoce la MAC del destino; lo reciben todos los equipos de la LAN.
- **Reply** (opcode 2): "La IP X está en la MAC Y". Lo envía solo el dueño de la IP, en **unicast** a la MAC de quien preguntó (que venía en el Request).

**c) Caché ARP**
Es una tabla en el sistema operativo con asociaciones IP → MAC aprendidas recientemente, con tiempo de vida. Existe para **no hacer un broadcast antes de cada paquete**: reduce tráfico y latencia. Las entradas vencen para adaptarse a cambios (equipo reemplazado, IP reasignada).

**d) Con nuestras palabras**
Primero miro mi caché ARP: si ya tengo la MAC asociada a esa IP, la uso. Si no, mando a toda la LAN un ARP Request en broadcast preguntando quién tiene esa IP; el equipo que la tiene me contesta con un ARP Reply dirigido a mí que contiene su MAC. La guardo en la caché y recién entonces armo la trama con esa MAC destino. (Si la IP no fuera de mi subred, no pregunto por ella: pregunto por la MAC del gateway.)

**e) Caché ARP de la computadora** — `ip neigh show`

```
192.168.1.1 dev wlp1s0 lladdr 4c:d7:c8:f6:10:4c REACHABLE
```
La MAC asociada al gateway, **4c:d7:c8:f6:10:4c**, **coincide** con la MAC destino de todos los Echo Request del punto 1 (tanto al gateway como a 8.8.8.8): de esa entrada de la caché salió la MAC que usó `ping`.

**f) Captura de tráfico ARP**
Opción usada: **A** (ping a 192.168.1.253, que no aparecía en la caché). Archivo: [`capturas/02_arp.pcapng`](capturas/02_arp.pcapng), filtro `arp || icmp`.

```
$ ping -4 -c 2 192.168.1.253
From 192.168.1.46 icmp_seq=1 Destination Host Unreachable
From 192.168.1.46 icmp_seq=2 Destination Host Unreachable
2 packets transmitted, 0 received, +2 errors, 100% packet loss
$ ip neigh show
192.168.1.253 dev wlp1s0 FAILED
192.168.1.1 dev wlp1s0 lladdr 4c:d7:c8:f6:10:4c REACHABLE
```

Contenido de la captura:

| N° | Tiempo | Qué es |
|---|---|---|
| 1–3 | 0 s, 1,06 s, 2,08 s | ARP Request broadcast: "¿quién tiene 192.168.1.253?" — sin respuesta |
| 4–6 | 68,1 s, 69,2 s, 70,2 s | Lo mismo, al repetir el ping un minuto después |
| 7–10 | 71,2 s | Ping al gateway: Echo Request/Reply **sin ningún ARP previo** (usó la caché) |
| 11 | 76,3 s | ARP Request del **router** preguntando por 192.168.1.46, en **unicast** a nuestra MAC |
| 12 | 76,3 s | ARP Reply nuestro al router |

Como la IP de la Opción A no existe, ningún Request nuestro tuvo respuesta; el par Request/Reply completo que se ve en la captura es el que inició el router (paquetes 11 y 12):

| Campo | ARP Request (paq. 11) | ARP Reply (paq. 12) |
|---|---|---|
| MAC destino (encabezado Ethernet) | 58:02:05:53:72:b1 | 4c:d7:c8:f6:10:4c |
| MAC origen (encabezado Ethernet) | 4c:d7:c8:f6:10:4c | 58:02:05:53:72:b1 |
| Opcode | 1 (request) | 2 (reply) |
| Sender MAC address | 4c:d7:c8:f6:10:4c | 58:02:05:53:72:b1 |
| Sender IP address | 192.168.1.1 | 192.168.1.46 |
| Target MAC address | `00:00:00:00:00:00` | 4c:d7:c8:f6:10:4c |
| Target IP address | 192.168.1.46 | 192.168.1.1 |

> El mismo intercambio (Request del router + Reply nuestro) aparece también en `01_icmp.pcapng`, paquetes 14 y 15, en medio del ping a 8.8.8.8.

### Preguntas

**a) Broadcast en el Request, unicast en el Reply**
El que pregunta **no conoce la MAC** del destino (es justamente lo que busca), así que la única forma de llegar a él es mandarle la trama a todos. El que responde ya conoce la MAC del que preguntó porque vino en el campo Sender MAC del Request, así que contesta directo. La **Target MAC del Request vale `00:00:00:00:00:00`** porque es el dato desconocido: queda como un "hueco" a completar.
Observación: el Request del router (paquete 11) fue **unicast**. No es una contradicción: el router ya tenía nuestra MAC en su caché y solo quería **confirmar que sigue siendo válida** antes de que la entrada venza, así que le pregunta directamente al dueño en lugar de molestar a toda la LAN. El broadcast hace falta solo cuando la MAC es realmente desconocida.

**b) Type de Ethernet y encabezado IP**
Type = **0x0806** (ARP). **No hay encabezado IP**: el mensaje ARP va directamente dentro de la trama Ethernet. Eso muestra que ARP "vive" por debajo de IP, ligado al enlace local: no es ruteable y nunca sale de la LAN. Las tramas ARP de la captura miden **42 B**: 14 de Ethernet + 28 de ARP. (Las tramas recibidas por cable suelen verse de 60 B por el relleno mínimo de Ethernet; acá, por Wi-Fi, se ven de 42 B.)

**c) Opción A (IP inexistente)**
Aparecieron **3 ARP Request** por cada `ping -c 2`, separados ~1 s (paquetes 1–3: MAC destino `ff:ff:ff:ff:ff:ff`, Sender 58:02:05:53:72:b1 / 192.168.1.46, Target `00:00:00:00:00:00` / 192.168.1.253), y **ningún Reply**, porque ningún equipo tiene esa IP. **No apareció ningún ICMP Echo Request** en la captura: el ping se arma, pero el kernel no puede construir la trama sin la MAC destino, así que lo retiene esperando la resolución y al fallar lo descarta. `ping` informa `From 192.168.1.46 … Destination Host Unreachable`: el mensaje viene de **nuestra propia IP**, es decir, lo generó nuestro sistema localmente, no la red. La entrada queda en la caché en estado **FAILED**.

**d) Repetir el ping un minuto después**
- **A 192.168.1.253:** volvieron a salir **3 ARP Request en broadcast** (paquetes 4–6). La entrada FAILED no guarda ninguna MAC, así que no sirve: hay que volver a preguntar.
- **Al gateway:** **no apareció ningún ARP** antes del Echo Request (paquetes 7–10). La entrada del gateway estuvo en **REACHABLE** durante todo el experimento, porque se usa constantemente (todo el tráfico a Internet pasa por él) y Linux la va confirmando con ese mismo tráfico.
- Lo que sí apareció fue el **Request unicast del router** (paquete 11): él revalidó *su* caché con nosotros.

En Linux una entrada que no se usa pasa de REACHABLE a STALE tras unos segundos (aleatorio alrededor de 30 s); en STALE se sigue usando, y si hace falta confirmarla el kernel envía un **ARP Request unicast** a la MAC conocida (lo mismo que hizo el router) en lugar de un broadcast. Si nadie la usa, termina eliminándose.
- **Ventaja de la caché:** evita un broadcast y una espera por cada paquete; menos tráfico en la LAN y menor latencia. En la captura se ve: los 4 ping al gateway del punto 1 y los 2 de este punto no necesitaron ningún ARP.
- **Problema de una entrada vieja:** si el equipo cambió de MAC (placa reemplazada, IP reasignada a otro dispositivo), las tramas se envían a una MAC que ya no corresponde y la comunicación falla hasta que la entrada expire. Además, como la caché acepta respuestas sin autenticar, es la base del ataque de **ARP spoofing/poisoning**.

---

## 3) TCP y UDP "a mano" con ncat

### Investigación

**a) ¿Qué significa "establecer una conexión"?**
Que los dos extremos **acuerdan iniciar un intercambio y sincronizan su estado**: números de secuencia iniciales, tamaño de ventana y opciones (MSS, etc.), mediante el *three-way handshake* (SYN, SYN-ACK, ACK). La conexión TCP **existe solo en los extremos**: es estado guardado en los sistemas operativos de cliente y servidor (buffers, números de secuencia, timers). Los cables y routers no saben nada de ella; reenvían cada datagrama IP en forma independiente.

**b) ¿Qué es un puerto?**
Un número de 16 bits (0–65535) del encabezado TCP/UDP que identifica **a qué proceso/socket** dentro de un host corresponde un segmento. El par **(IP, puerto)** identifica un **extremo de comunicación** (un socket) en la red. Una conexión TCP queda identificada por la cuádrupla (IP origen, puerto origen, IP destino, puerto destino).

**c) ¿Qué significa que un proceso esté "escuchando"?**
Que le pidió al SO un socket asociado a ese puerto en estado **LISTEN**: a partir de ahí, el kernel responde con SYN-ACK a los SYN que lleguen a ese puerto y entrega las conexiones resultantes al proceso. Si nadie escucha, el SO responde con RST (TCP) o ICMP Port Unreachable (UDP). Se puede ver con `ss -tlnp` / `ss -ulnp`.

### Experimento TCP
Archivo: [`capturas/03_tcp_ncat.pcapng`](capturas/03_tcp_ncat.pcapng) — interfaz `lo`, filtro `tcp.port == 12000`. Se mandaron 2 mensajes en cada sentido y luego se cerró el cliente con Ctrl+C.

```
# Terminal A                                 # Terminal B
$ ncat -v -l 12000                           $ ncat -v 127.0.0.1 12000
Ncat: Listening on [::]:12000                Ncat: Connected to 127.0.0.1:12000.
Ncat: Listening on 0.0.0.0:12000             Hola servidor
Ncat: Connection from 127.0.0.1:40188.       Hola cliente
Hola servidor                                Como andas?
Hola cliente                                 Todo bien por aca
Como andas?                                  ^C
Todo bien por aca
```

| N° | Tiempo | Sentido | Flags | Significado |
|---|---|---|---|---|
| 1 | 0,000 s | cliente (40188) → servidor (12000) | SYN | Pedido de conexión |
| 2 | 0,000 s | servidor → cliente | SYN, ACK | Aceptación |
| 3 | 0,000 s | cliente → servidor | ACK | Handshake completo |
| 4 | 0,988 s | cliente → servidor | PSH, ACK (len = 14) | `Hola servidor\n` |
| 5 | 0,988 s | servidor → cliente | ACK | Confirmación |
| 6 | 2,482 s | servidor → cliente | PSH, ACK (len = 13) | `Hola cliente\n` |
| 7 | 2,482 s | cliente → servidor | ACK | Confirmación |
| 8 | 3,993 s | cliente → servidor | PSH, ACK (len = 12) | `Como andas?\n` |
| 9 | 3,993 s | servidor → cliente | ACK | Confirmación |
| 10 | 4,486 s | servidor → cliente | PSH, ACK (len = 18) | `Todo bien por aca\n` |
| 11 | 4,486 s | cliente → servidor | ACK | Confirmación |
| 12 | 7,988 s | cliente → servidor | FIN, ACK | Cierre del cliente (Ctrl+C) |
| 13 | 7,988 s | servidor → cliente | FIN, ACK | Cierre del servidor (FIN y ACK en el mismo segmento) |
| 14 | 7,988 s | cliente → servidor | ACK | Fin de la conexión |

Total: 14 segmentos para 4 mensajes. El puerto del cliente (40188) lo eligió el SO.

> Nota: en `lo` Wireshark muestra un encabezado Ethernet con MAC `00:00:00:00:00:00` en origen y destino (Linux).

### Experimento UDP
Archivo: [`capturas/03_udp_ncat.pcapng`](capturas/03_udp_ncat.pcapng) — filtro `udp.port == 12001`.

| N° | Tiempo | Sentido | Contenido |
|---|---|---|---|
| 1 | 0,000 s | cliente (39601) → servidor (12001) | `Hola servidor\n` (UDP len = 22 = 8 + 14) |
| 2 | 1,495 s | servidor → cliente | `Hola cliente\n` |
| 3 | 3,005 s | cliente → servidor | `Como andas?\n` |
| 4 | 3,500 s | servidor → cliente | `Todo bien por aca\n` |

**a) Al ejecutar el cliente, antes del primer mensaje:** en UDP **no pasó nada en la red**: el primer paquete de la captura ya es el primer mensaje (el cliente se lanzó 2 s antes). Igual ncat imprime `Connected to 127.0.0.1:12001`, pero esa "conexión" es solo local (fija el destino del socket). En TCP, en cambio, apenas se ejecutó el cliente aparecieron los **3 segmentos del handshake** (paquetes 1–3) antes de cualquier dato.

**b) Datagramas por mensaje:** **uno por cada mensaje** (cada Enter genera un datagrama con la línea, incluido el `\n`). **No hay nada parecido a un ACK**: después de cada datagrama no viene ninguna confirmación. UDP no confirma la recepción; si el datagrama se pierde, nadie se entera.

**c) Encabezados**

| | UDP | TCP |
|---|---|---|
| Tamaño | **8 B fijos** | **20 B mínimo**, hasta 60 B con opciones. En la captura: SYN y SYN-ACK con **40 B** (opciones MSS, SACK permitted, Timestamps, Window scale) y los segmentos con datos con **32 B** (20 + 12 de la opción Timestamps) |
| Campos | Puerto origen, puerto destino, longitud, checksum | Puerto origen, puerto destino, número de secuencia, número de ACK, longitud de encabezado, flags (SYN, ACK, FIN, RST, PSH, URG…), ventana, checksum, puntero urgente, opciones |

Por ejemplo, el mismo `Hola servidor\n` ocupa una trama de **56 B** con UDP (14 + 20 + 8 + 14) y de **80 B** con TCP (14 + 20 + 32 + 14). Todo lo que TCP tiene "de más" sirve para ordenar, confirmar, retransmitir, controlar el flujo y manejar la conexión.

**d) Al cerrar con Ctrl+C:** en UDP **no se generó ningún paquete** (no hay conexión que cerrar; el servidor ni se entera). En TCP se ve el **cierre con FIN** en ambos sentidos: 3 segmentos (12–14), porque el servidor mandó su FIN junto con el ACK del FIN del cliente.

**e) Paquetes totales para la misma frase:**
Para mandar solo `Hola servidor`: **TCP = 8** (handshake 3 + datos 1 + ACK 1 + cierre 3). **UDP = 1**.
Con los paquetes extra TCP "compra": **confiabilidad** (confirmación y retransmisión), **orden**, **control de flujo** y congestión, y saber que **el otro extremo existe y aceptó** la comunicación, además de un cierre ordenado. UDP es más liviano y con menor latencia, pero esas garantías quedan a cargo de la aplicación.

**f) ¿Y si nadie escucha?** Archivo: [`capturas/03_puertos_cerrados.pcapng`](capturas/03_puertos_cerrados.pcapng) — filtro `tcp.port == 12000 || udp.port == 12001 || icmp`.

```
$ ncat -v 127.0.0.1 12000
Ncat: Connection refused.
$ ncat -v -u 127.0.0.1 12001
Ncat: Connected to 127.0.0.1:12001.
hola?
Ncat: Connection refused.
```

| N° | Paquete |
|---|---|
| 1 | TCP 60664 → 12000 **SYN** |
| 2 | TCP 12000 → 60664 **RST, ACK** |
| 3 | UDP 34445 → 12001 `hola?\n` |
| 4 | **ICMP Destination Unreachable, Type 3 Code 3 (Port unreachable)** |

- **TCP:** el cliente envía **SYN** y el SO responde de inmediato con **RST, ACK** (2 paquetes en total). ncat informa `Connection refused` sin llegar a conectarse.
- **UDP:** al ejecutar no pasa nada en la red, y ncat hasta dice `Connected`. Recién al escribir y dar Enter sale el datagrama, y el SO responde con un **ICMP Port Unreachable**, que lleva adentro el encabezado IP (20 B) + UDP (8 B) + los datos del datagrama original (34 B de datos ICMP). Recién ahí ncat informa `Connection refused`.
Es decir: TCP avisa con un mecanismo propio (RST) y antes de mandar datos; UDP no tiene uno y depende de ICMP, que llega solo después de haber intentado enviar.

**¿Hacía falta usar puertos distintos para TCP y UDP?** No. Los espacios de puertos de TCP y UDP son **independientes**: el puerto 12000/TCP y el 12000/UDP son extremos distintos, porque el SO primero mira el campo Protocol de IP (6 o 17) y recién después el puerto. Los filtros `tcp.port` y `udp.port` también los separarían. Usar números distintos solo hace las capturas más fáciles de leer.

---

## 4) Servidor TCP mínimo

Scripts: [`tcp_server.py`](tcp_server.py), [`tcp_client.py`](tcp_client.py) (los de la consigna).

### c) Ejecución
Archivo: [`capturas/04_tcp_scripts.pcapng`](capturas/04_tcp_scripts.pcapng) — `lo`, filtro `tcp.port == 12000`.

```
$ python3 tcp_server.py
[servidor TCP] escuchando en 127.0.0.1:12000 ...
[servidor TCP] conexión aceptada desde 127.0.0.1:51336
[servidor TCP] recibido (22 bytes): 'Hola desde mi programa'
[servidor TCP] respuesta enviada: 'Recibido: Hola desde mi programa'
[servidor TCP] el cliente cerró la conexión

$ python3 tcp_client.py 127.0.0.1 "Hola desde mi programa"
[cliente TCP] conectado a 127.0.0.1:12000 desde 127.0.0.1:51336
[cliente TCP] enviado: 'Hola desde mi programa'
[cliente TCP] respuesta (32 bytes): 'Recibido: Hola desde mi programa'
```

| N° | Sentido | Flags | Len |
|---|---|---|---|
| 1 | cliente (51336) → servidor | SYN | 0 |
| 2 | servidor → cliente | SYN, ACK | 0 |
| 3 | cliente → servidor | ACK | 0 |
| 4 | cliente → servidor | PSH, ACK | 22 (`Hola desde mi programa`) |
| 5 | servidor → cliente | ACK | 0 |
| 6 | servidor → cliente | PSH, ACK | 32 (`Recibido: Hola desde mi programa`) |
| 7 | cliente → servidor | ACK | 0 |
| 8 | cliente → servidor | FIN, ACK | 0 |
| 9 | servidor → cliente | FIN, ACK | 0 |
| 10 | cliente → servidor | ACK | 0 |

### d) Llamadas al sistema vs. tráfico

| Llamada | ¿Dónde se ejecuta? | ¿Genera tráfico? | Segmentos que observan |
|---|---|---|---|
| `socket()` | servidor y cliente | **No** — solo crea la estructura en el SO | — |
| `bind()` | servidor | **No** — asocia IP:puerto localmente | — |
| `listen()` | servidor | **No** — pasa el socket a LISTEN; desde acá el kernel responderá SYN-ACK | — |
| `connect()` | cliente | **Sí** — dispara el three-way handshake | N° 1 SYN · N° 2 SYN, ACK · N° 3 ACK |
| `accept()` | servidor | **No** — el handshake ya lo completó el kernel; `accept()` solo retira la conexión lista de la cola y devuelve un socket nuevo | (se apoya en los 3 anteriores) |
| `sendall()` | servidor | **Sí** — segmento con datos | N° 6 PSH, ACK (32 B, `Recibido: Hola desde mi programa`) + N° 7 ACK del cliente |
| `recv()` | servidor | **No** — lee del buffer del SO; los datos ya llegaron en el N° 4 y el kernel los confirmó con el N° 5 (ACK), haya o no un `recv()` | — |
| `close()` | ambos | **Sí** — inicia el cierre | Cliente: N° 8 FIN, ACK · Servidor (tras `recv()` = b""): N° 9 FIN, ACK → N° 10 ACK del cliente |

**Conclusión:** solo las llamadas que cambian el estado de la conexión o entregan datos al SO para enviar (`connect`, `send`, `close`) producen segmentos; el resto son operaciones locales. Además, varias cosas que el programa no pide explícitamente (los ACK, la respuesta SYN-ACK) las hace el kernel por su cuenta: el programa trabaja con un flujo de bytes y el SO se encarga del protocolo.

---

## Archivos entregados
- Capturas: `capturas/01_icmp.pcapng`, `02_arp.pcapng`, `03_tcp_ncat.pcapng`, `03_udp_ncat.pcapng`, `03_puertos_cerrados.pcapng`, `04_tcp_scripts.pcapng`
- Scripts: `tcp_server.py`, `tcp_client.py`
