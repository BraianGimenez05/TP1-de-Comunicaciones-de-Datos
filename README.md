# TP1-de-Comunicaciones-de-Datos


1.b 
El gráfico, la onda completa un ciclo cada 60 mm, así que λ = 60 mm = 0,06 m

Con c = λ·f:

f = c / λ = (3×10⁸ m/s) / (0,06 m) = 5×10⁹ Hz = 5 GHz

1.c 
5 GHz cae dentro de la región de microondas, y específicamente en la banda SHF (Super High Frequency, 3–30 GHz), es decir en la frecuencia superalta

1.d 
Los dispostivos que operan son los routers/access points Wi-Fi que operan en la banda de 5 GHz. También hay radares y enlaces satelitales en esta zona del espectro, pero el ejemplo más comun es el Wi-Fi de 5 GHz

1.e 
Quiere representar la atenuación: la pérdida de intensidad o amplitud de la señal a medida que se aleja de la fuente es decir a mayor distancia, menor energía

1.f
Sí por que en un router de 5 GHz, la atenuación hace que la señal se debilite cuanto más lejos estamos del router. Esto lo notamos en nuestro día a día: la señal de Wi-Fi es excelente al lado del router, pero se pone lenta o directamente se corta en otra habitación o en otro piso de la casa. Además, la banda de 5 GHz atenúa más rápido frente a paredes y obstáculos que la de 2,4 GHz, por eso suele tener menos alcance.

1.g
La telefonía celular: sí, también sufre atenuación (por eso hay menos señal lejos de la antena o dentro de un edificio).

El cable coaxial: sí, toda línea de transmisión atenúa la señal a medida que aumenta la distancia, por eso los sistemas de cable necesitan amplificadores o repetidores.

La fibra óptica: también se atenúa, pero mucho menos que en el cobre, lo que permite transmitir a distancias mucho más largas sin tantos repetidores.

2.a
En el esquema, los datos viajan en un solo sentido junto con una señal de reloj que los acompaña. Esto representa una transmisión simplex (un solo sentido) y de tipo síncrona, ya que ambos módulos comparten una señal de clock para sincronizarse.

2.b
No, porque al ser simplex no permite comunicación bidireccional. Si quisiéramos transmitir rápido en ambos sentidos, necesitaríamos un esquema dúplex, y probablemente convendría pasar a una comunicación asíncrona, que no depende de compartir una línea de reloj entre ambos extremos.

2.c

<img width="694" height="228" alt="Captura desde 2026-08-24 11-48-34" src="https://github.com/user-attachments/assets/42073028-8d5d-472f-b25e-e30bc327a6e6" />

2.d
Como los flancos de la señal no son instantáneos (tienen pendiente), no conviene medir el valor justo en la transición, porque ahí el nivel es impreciso. Lo correcto es muestrear en el centro de cada bit, una vez que la señal ya se estabilizó en su nivel final.

3
No conviene transmitir una señal digital escalonada (en banda base) de forma inalámbrica porque tiene componentes de muy baja frecuencia, lo que requeriría antenas enormes y mucha potencia para poder irradiarla de forma eficiente. Además, ocuparía el espectro de manera poco eficiente y sería muy susceptible al ruido. Por eso se modula la información sobre una portadora de alta frecuencia, que sí puede transmitirse con antenas de tamaño razonable y permite además que varias señales convivan en distintas frecuencias sin interferirse.

3.a
En el gráfico, la portadora mantiene la misma amplitud pero cambia la cantidad de ciclos según el bit transmitido (más ciclos para un valor, menos para el otro). Esto corresponde a FSK (Frequency Shift Keying), cada bit se representa con una frecuencia distinta de la portadora.

3.b


<img width="1509" height="381" alt="Captura desde 2026-08-24 12-29-02" src="https://github.com/user-attachments/assets/79ff62f2-6c46-48d7-8286-7bd1df9aa1ab" />

3.c
ASK (Amplitude Shift Keying) o modulacion de amplitud varía la amplitud de la portadora.
PSK (Phase Shift Keying) o modulacion de fase varía la fase de la portadora.
QAM: combina variaciones de amplitud y fase al mismo tiempo.

3.d
El Bit Error Rate (BER) es la proporción de bits que llegan con error respecto del total de bits transmitidos. Es la métrica más usada para medir la calidad de un enlace digital. En términos de BER, PSK generalmente tiene mejor desempeño que ASK y FSK bajo el mismo nivel de ruido, porque la fase es menos sensible a interferencias que la amplitud.

