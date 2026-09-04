
# TP2-de-Comunicaciones-de-Datos



### 1.a

El fenómeno representado es la atenuación de la señal (pérdida de potencia) a medida que la onda electromagnética viaja desde la superficie terrestre hasta el satélite. Sus características principales: la potencia recibida cae con la distancia recorrida (pérdida en el espacio libre, proporcional al cuadrado de la distancia y de la frecuencia), y se suma una atenuación adicional al atravesar la atmósfera. Es un fenómeno acumulativo y dependiente de la frecuencia: no afecta igual a todas las bandas.

### 1.b 

El caso concreto más estudiado es el desvanecimiento por lluvia en enlaces satelitales. Las bandas Ku y Ka (SHF/EHF, longitudes de onda cercanas al tamaño de una gota de lluvia) son las más afectadas: las gotas actúan como pequeños espejos/prismas que reflejan, refractan y dispersan la señal. La banda C (frecuencias más bajas, longitud de onda mayor) es mucho más resiliente y casi inmune a estas condiciones climáticas, por eso se prefiere para enlaces críticos en zonas tropicales, aunque a costa de necesitar antenas más grandes y ofrecer menos ancho de banda disponible.

### 1.c 

El motivo real es la altitud de crucero, un celular queda dentro del alcance de muchas antenas de celdas terrestres al mismo tiempo, porque no hay edificios, terreno ni la curvatura normal que atenúen la señal entre celdas vecinas. Eso es exactamente el fenómeno del punto (a) pero en sentido inverso: en tierra, la atenuación por obstáculos y distancia es lo que mantiene aisladas a las celdas entre sí; en el aire, esa atenuación natural desaparece (línea de vista despejada, menor densidad atmosférica) y el teléfono termina "viéndose" con decenas de torres a la vez, saturando la red de handoffs y generando interferencia entre celdas.


### 2.a 

EL fenómeno representado es el ruido en el canal, una fuente externa (en la figura, el martillo neumático, es una fuente típica de ruido eléctrico) distorsiona localmente la forma de onda de la señal transmitida. A diferencia de la atenuación (que reduce la amplitud de toda la señal de forma gradual y predecible), el ruido se superpone a la señal de forma aditiva, aleatoria, y solo afecta el tramo donde la fuente de ruido está presente.

### 2.b
 
El ruido de origen producido por las personas como motores, soldadoras, herramientas eléctricas, líneas de potencia, etc. Donde predomina fuertemente en frecuencias bajas de entre aproximadamente 20 y 40 MHz es la fuente dominante de interferencia, y por debajo de 30 MHz gran parte de ese ruido queda "atrapado" y se propaga a grandes distancias. Por eso las bandas LF/MF/HF son las más vulnerables a este tipo de interferencia. Por encima de 30 MHz (bandas VHF/UHF y superiores) ese ruido se irradia libremente y se disipa, así que el ruido térmico interno del propio receptor pasa a ser el factor limitante en vez del ruido externo. Es decir: cuanto más alta la banda, más resiliente es a este tipo de interferencia electromecánica.

### 2.c

La SNR (Signal-to-Noise Ratio) es la relación entre la potencia de la señal útil y la potencia del ruido presente en el canal, habitualmente expresada en decibeles: SNR(dB) = 10·log₁₀(P_señal/P_ruido). Cuanto mayor la SNR, más "limpia" llega la señal y más fácil es para el receptor discriminar los símbolos transmitidos. Esto se conecta directamente con el BER (Bit Error Rate) visto en el TP1, por que para un esquema de modulación dado, la probabilidad de que un bit se decodifique mal es una función decreciente de la SNR, a mayor SNR, menor BER. El teorema de Shannon-Hartley define esta relación desde el otro extremo: la capacidad máxima del canal (bits/s sin errores) depende directamente de la SNR disponible. En resumen: SNR es la causa física (cuánto ruido hay relativo a la señal) y BER es el efecto observable (cuántos bits se reciben mal como consecuencia de esa relación señal/ruido).

### 3

Frente al ruido del canal, los sistemas digitales usan mecanismos de detección (bits/campos de paridad, checksums,código de redundancia cíclica (CRC)) que permiten al receptor darse cuenta de que un bloque llegó corrupto, y mecanismos de corrección: por retransmisión (ARQ, "pedir de nuevo" el paquete dañado) o por corrección adelantada de errores (códigos de Hamming, convolucionales, etc), que agregan redundancia calculada de antemano para que el receptor pueda reconstruir el dato original sin pedir reenvío. Frente a corrimientos de frecuencia (por ejemplo, desajuste entre el reloj del emisor y el del receptor, o efecto Doppler), se usan técnicas de recuperación de portadora y de reloj: lazos de enganche de fase (PLL), control automático de frecuencia (AFC), códigos de línea autosincronizantes y secuencias de entrenamiento conocidas que el receptor usa como referencia para recalibrarse.

### 4.a 

La sincronización significa que el receptor y el emisor comparten una referencia común de tiempo para interpretar la señal correctamente. Hay dos niveles: la sincronización de bits asegura que el receptor sepa exactamente cuándo empieza y termina cada bit individual, para poder muestrear la señal en el instante correcto (se logra con relojes recuperados de la propia señal, códigos autosincronizantes); la sincronización de trama es un nivel superior: una vez que los bits se leen bien, el receptor necesita saber dónde empieza y dónde termina cada trama completa, para agrupar los bits en unidades de datos con sentido.

### 4.b

Una trama (frame) es la unidad básica de datos que se transmite en la capa de enlace, con una estructura definida. El header (encabezado) va al principio y contiene metadatos de control: direcciones, tipo de protocolo, número de secuencia, longitud, etc. El payload (carga útil) es la información real que se quiere transmitir, el contenido de interés para las capas superiores. El trailer (tráiler) va al final y típicamente contiene información de verificación de integridad, como un CRC, para que el receptor pueda detectar si la trama llegó corrupta.

### 4.c 

El preámbulo es una secuencia de bits conocida y fija que se envía justo antes de la trama, cuya función es darle tiempo y una referencia al receptor para sincronizar su reloj y detectar el nivel de la señal antes de que llegue la información real (por ejemplo, en Ethernet es una secuencia de 1 y 0 alternados). No forma parte de la información que se quiere transmitir: es pura sobrecarga (overhead) de control, se descarta una vez cumplida su función y nunca se entrega a las capas superiores.

### 4.d 

Los 3 mecanismos clásicos son la longitud fija, donde todas las tramas miden lo mismo y el receptor simplemente cuenta bits/bytes; el campo de longitud dentro del header que le indica al receptor cuántos bytes de payload esperar, y los caracteres o secuencias delimitadoras, donde bytes o patrones de bits especiales marcan el inicio y el fin de la trama con la complicación de que, si esa secuencia aparece dentro de los propios datos, hace falta "byte stuffing" o "bit stuffing" para diferenciarla del contenido real (técnica usada en protocolos como HDLC o PPP).