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
<svg width="680" height="300" viewBox="0 0 680 300" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="680" height="300" fill="#FFFFFF"/>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>

<line x1="60" y1="230" x2="630" y2="230" stroke="#000000" stroke-width="1" marker-end="url(#arrow)"/>
<line x1="60" y1="230" x2="60" y2="55" stroke="#000000" stroke-width="1" marker-end="url(#arrow)"/>
<text x="640" y="234" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">tiempo</text>
<text x="15" y="60" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">tensión</text>

<text x="45" y="104" text-anchor="end" dominant-baseline="central" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#000000">1</text>
<text x="45" y="204" text-anchor="end" dominant-baseline="central" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#000000">0</text>
<line x1="55" y1="100" x2="63" y2="100" stroke="#000000" stroke-width="0.5"/>
<line x1="55" y1="200" x2="63" y2="200" stroke="#000000" stroke-width="0.5"/>

<path d="M80,200 L141,200 L149,100 L206,100 L214,200 L466,200 L474,100 L531,100 L539,200 L600,200" fill="none" stroke="#185FA5" stroke-width="2" stroke-linejoin="round"/>

<line x1="145" y1="200" x2="145" y2="230" stroke="#000000" stroke-width="0.5" stroke-dasharray="2 2"/>
<line x1="210" y1="200" x2="210" y2="230" stroke="#000000" stroke-width="0.5" stroke-dasharray="2 2"/>
<line x1="275" y1="200" x2="275" y2="230" stroke="#000000" stroke-width="0.5" stroke-dasharray="2 2"/>
<line x1="340" y1="200" x2="340" y2="230" stroke="#000000" stroke-width="0.5" stroke-dasharray="2 2"/>
<line x1="405" y1="200" x2="405" y2="230" stroke="#000000" stroke-width="0.5" stroke-dasharray="2 2"/>
<line x1="470" y1="200" x2="470" y2="230" stroke="#000000" stroke-width="0.5" stroke-dasharray="2 2"/>
<line x1="535" y1="200" x2="535" y2="230" stroke="#000000" stroke-width="0.5" stroke-dasharray="2 2"/>

<text x="112" y="248" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">T0</text>
<text x="177" y="248" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">T1</text>
<text x="242" y="248" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">T2</text>
<text x="307" y="248" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">T3</text>
<text x="372" y="248" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">T4</text>
<text x="437" y="248" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">T5</text>
<text x="502" y="248" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">T6</text>
<text x="567" y="248" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#000000">T7</text>

<text x="112" y="80" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="500" fill="#000000">0</text>
<text x="177" y="80" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="500" fill="#000000">1</text>
<text x="242" y="80" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="500" fill="#000000">0</text>
<text x="307" y="80" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="500" fill="#000000">0</text>
<text x="372" y="80" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="500" fill="#000000">0</text>
<text x="437" y="80" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="500" fill="#000000">0</text>
<text x="502" y="80" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="500" fill="#000000">1</text>
<text x="567" y="80" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="500" fill="#000000">0</text>
</svg>



