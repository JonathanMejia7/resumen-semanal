# Resumen semanal · skill para Claude Code y Codex

Arma cada semana un resumen de lo que publicaron tus fuentes favoritas sobre el tema que elijas: con fecha y enlace original, sin repetir lo de semanas anteriores y con el posible uso de cada novedad. La primera vez te ayuda a elegir el tema y de 3 a 5 fuentes.

## Instalar

La forma fácil: abre Claude Code o Codex y escribe «Instala la skill que está en mi carpeta Descargas/resumen-semanal» (cambia la ruta si la guardaste en otro lugar).

A mano: copia la carpeta `resumen-semanal` completa (con `SKILL.md` y `scripts/`) en:

- **Claude Code**: `~/.claude/skills/resumen-semanal/`
- **Codex**: `~/.agents/skills/resumen-semanal/`

Si no la reconoce enseguida, reinicia la herramienta. El script que lee los feeds necesita Python 3.9 o superior:

- **Mac**: si nunca lo has usado, escribe `python3 --version` en la Terminal; si te ofrece instalar las herramientas de desarrollo de Apple, acepta.
- **Windows**: instálalo desde python.org y después ejecuta `python -m pip install tzdata` para que reconozca tu zona horaria.

Si no tienes Python, la skill igual funciona: abre los feeds directamente, aunque es más lenta.

## Usar

1. Escribe: «Configura mi resumen semanal». Te preguntará el tema, para qué lo quieres y te ayudará a elegir las fuentes.
2. Cada vez que quieras ponerte al día: «Prepara mi resumen semanal».
3. Para que llegue solo, crea una tarea programada semanal con el texto «Usa la skill resumen-semanal y prepara el resumen de esta semana». En Claude: pestaña Code, «Scheduled» y «New task». En Codex: la sección «Scheduled» de la app. Solo corre si la app está abierta y la computadora encendida.

Tus datos (configuración, memoria e informes) se guardan en `~/resumen-semanal/`, fuera de la skill.

## Cómo te llega

Eliges una o varias formas al configurarla:
- En el chat.
- Como archivo en tu computadora (siempre se guarda uno, como respaldo).
- Como documento de Google Docs o Word.
- Subido a una carpeta de Google Drive.
- Por correo, a tu dirección o a otras que tú indiques (por ejemplo, tu equipo).

Para documento, Drive o correo necesitas tener conectada esa herramienta (Google Drive, Google Docs, Gmail u otra) en Claude o Codex.

## Qué hace distinto a un prompt

- Recuerda lo que ya te resumió para no repetirlo.
- Lee los feeds de YouTube y blogs para no perder publicaciones.
- Ordena las novedades por tema y te dice para qué te podrían servir.
- Te avisa qué fuentes no pudo leer, en vez de inventar.

Creada por Jonathan Mejía · @jonathanmejia.ops

¿Te sirvió? Cuéntamelo en los comentarios del video y sígueme para más ideas como esta, de operaciones e IA.
