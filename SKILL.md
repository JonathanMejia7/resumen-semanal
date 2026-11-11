---
name: resumen-semanal
description: Arma un resumen semanal de lo que publicaron tus fuentes favoritas (blogs, canales de YouTube, boletines) sobre el tema que elijas, con fecha y enlace original, sin repetir lo de semanas anteriores y diciendo para qué te puede servir cada novedad. La primera vez te ayuda a elegir el tema y de 3 a 5 fuentes. Úsala cuando pidas «resumen semanal», «ponme al día», «qué publicaron mis fuentes», «configura mi resumen» o «cambia mis fuentes», y en una tarea programada cada semana.
---

# Resumen semanal

Prepara un resumen de lo que publicaron las fuentes que la persona eligió en los últimos siete días. Lo valioso no es resumir: es no perder nada importante, no inventar y no repetir. Por eso cada novedad lleva fecha y enlace original, y se dice con honestidad qué se pudo leer y qué no.

## Carpeta de datos

Todo lo de la persona se guarda fuera de la skill, en una carpeta de datos. Por defecto es `~/resumen-semanal/`. Si la persona indica otra, úsala, guárdala en el campo `carpeta_datos` de `config.json` y ponla también en el texto de la tarea programada (por ejemplo: «Usa la skill resumen-semanal con la carpeta de datos D:/Resumen»), porque cada ejecución empieza sin saberla.

```
~/resumen-semanal/
├── config.json      # tema, para qué, idioma, zona horaria, entrega y fuentes
├── registro.md      # lo que ya se resumió, para no repetirlo
└── informes/        # un archivo por semana: AAAA-MM-DD.md
```

Si `config.json` no existe, empieza por **Configurar**. Si existe, ve a **Preparar el resumen**.

Los comandos `python3 scripts/inventario.py …` se ejecutan desde la carpeta de esta skill (o con la ruta completa al script). Necesitan Python 3.9 o superior, sin instalar nada más. En Windows el comando suele ser `python` o `py` en vez de `python3`; si el script avisa que no reconoce la zona horaria, sugiere `python -m pip install tzdata` (mientras tanto usa la hora del equipo).

## Configurar (la primera vez, o cuando pida cambiar fuentes)

Pregunta solo lo necesario, en un mensaje:

1. **Tema**: sobre qué quiere estar al día (por ejemplo, «logística para pequeñas empresas», «marketing en redes», «IA para contadores»).
2. **Para qué**: trabajo, estudio, negocio propio u otro. Sirve para decir el posible uso de cada novedad.
3. **País o región**, **idioma** del resumen y **zona horaria**. El país sirve para priorizar fuentes de su región y para que el posible uso tenga sentido allí.
4. **Cómo lo quiere recibir**: en el chat, como archivo en su computadora, como documento (Google Docs o Word), subido a una carpeta de Google Drive, o por correo a su propia dirección o a otra (por ejemplo, la de su equipo). Puede elegir más de una. Antes de guardar, comprueba que la herramienta necesaria está disponible: busca entre tus herramientas las de Gmail u otro correo, Google Drive o Google Docs (en algunos entornos hay que cargarlas o activarlas primero). Si eligió Drive, abre la carpeta con la herramienta de Drive para confirmar que existe y que puede escribir en ella. Si algo no está disponible, dile qué conectar y, mientras tanto, usa archivo. Si su herramienta pide confirmar cada envío, ofrécele crear el correo como borrador en vez de enviarlo.
5. Si ya tiene fuentes en mente, que las pegue.

Si no tiene fuentes, búscalas en la web y propón de 5 a 8 candidatas. Para cada una muestra nombre, enlace, qué publica, cada cuánto y la fecha de su última publicación. Descarta las que no publican hace más de tres meses y las que no puedas abrir. Prefiere autores y medios reconocidos en el tema, de su país o región cuando existan (si propones uno de otro país, dilo), y mezcla formatos: al menos un medio (periódico o revista especializada del sector) y un blog o boletín de un autor, no solo canales de YouTube, que suelen tener títulos exagerados. El script te da el título del feed y cuántas publicaciones hace por semana: úsalo para mostrar la frecuencia. Si un sitio responde que bloquea lectores automáticos, ábrelo en el navegador antes de descartarlo. La persona elige de 3 a 5. No inventes fuentes: cada enlace tiene que abrir.

**Periódicos y medios grandes**: publican de todo y su feed suele guardar solo las últimas 50 o 100 noticias, a veces menos de dos días. Para no llenar el resumen de temas ajenos ni perder la semana:
- Usa el feed de la sección que interesa (economía, tecnología…) si el medio lo tiene.
- Añade a la fuente un `filtro` con palabras del tema. El script solo deja pasar las noticias cuyo título o resumen contengan alguna como palabra completa; con `*` al final acepta cualquier terminación (`export*` encuentra «exporta» y «exportaciones»). Evita palabras genéricas o propias del medio (en un medio de comercio electrónico, «ecommerce» deja pasar todo). Si el script avisa que el filtro deja pasar casi todo, ajústalo. Es un primer filtro: igual descarta al leer lo que no sea del tema.
- Si el script avisa que un feed redirige a otro, comprueba que sea el que querías: a veces el feed de una sección devuelve el general.
- Si el script avisa que el feed no cubre toda la semana, revisa también el listado de la sección o busca en el sitio las noticias del tema de esos días.

Con las elegidas, busca cómo leerlas de forma fiable:

- **Canal de YouTube**: `python3 scripts/inventario.py canal <url-del-canal>` devuelve su feed. Los feeds muestran los últimos 15 videos con fecha exacta, aunque la página del canal salga vacía.
- **Blog, periódico o sitio**: `python3 scripts/inventario.py feed <url-del-sitio>` busca su RSS.
- **Sin feed** (LinkedIn, boletines sin archivo público, páginas dinámicas): guárdala como `manual`, con la URL de su listado. Se revisa a mano cada semana.

Guarda `config.json` con este formato:

```json
{
  "tema": "logística para pequeñas empresas",
  "para_que": "trabajo en operaciones de una distribuidora",
  "pais": "Ecuador",
  "idioma": "español",
  "zona_horaria": "America/Guayaquil",
  "carpeta_datos": "~/resumen-semanal",
  "entrega": {
    "formas": ["archivo", "correo"],
    "correo_para": ["persona@ejemplo.com"],
    "correo_modo": "enviar",
    "carpeta_drive": "",
    "tipo_documento": ""
  },
  "fuentes": [
    {"nombre": "Autor o medio", "tipo": "youtube", "feed": "https://www.youtube.com/feeds/videos.xml?channel_id=UC...", "listado": "https://www.youtube.com/@canal", "notas": ""},
    {"nombre": "Blog", "tipo": "sitio", "feed": "https://ejemplo.com/feed/", "listado": "https://ejemplo.com/blog/", "notas": ""},
    {"nombre": "Periódico", "tipo": "sitio", "feed": "https://periodico.com/rss", "listado": "https://periodico.com/economia/", "filtro": ["logística", "puerto", "transporte"], "notas": "Solo noticias del tema"},
    {"nombre": "Boletín", "tipo": "manual", "feed": "", "listado": "https://ejemplo.com/boletin", "notas": "Sin feed; revisar el listado"}
  ]
}
```

`entrega.formas` admite una o varias de estas opciones:

| Forma | Qué hace | Qué necesita |
|---|---|---|
| `chat` | Muestra el resumen en la conversación | Nada |
| `archivo` | Guarda `informes/AAAA-MM-DD.md` | Nada. Siempre se guarda también como respaldo |
| `documento` | Crea un documento nuevo por semana (`tipo_documento`: `google-docs` o `word`) | Google Docs conectado, o crear un .docx en la carpeta de datos |
| `drive` | Sube el resumen a la carpeta de Google Drive de `carpeta_drive` (enlace o ID), convertido en documento de Google | Google Drive conectado |
| `correo` | Lo envía a cada dirección de `correo_para`, o lo deja como borrador si `correo_modo` es `borrador` | Gmail u otra herramienta de correo conectada |

Las direcciones de `correo_para` las escribe la persona y las confirma una por una al configurar. Si incluye una dirección que no es la suya, pregúntale si esa persona está de acuerdo en recibirlo. No añadas direcciones por tu cuenta. Crea `registro.md` vacío con el encabezado de la sección **Registrar**.

Al terminar, muéstrale el resumen de su configuración y dile cómo programarla (sección **Programarla**).

## Preparar el resumen

### 1. Fijar la ventana

Fin: ahora, en la zona horaria de `config.json`. Inicio: las 00:00 del día de hace siete días (el script lo calcula así por defecto). Usar días completos trata igual a las fuentes que ponen hora y a las que solo ponen la fecha. Si `registro.md` muestra que el último resumen se hizo hace más de siete días y menos de quince, empieza en la fecha de ese último resumen para no dejar un hueco.

### 2. Hacer el inventario

```bash
python3 scripts/inventario.py lista --datos ~/resumen-semanal
```

El script lee los feeds de `config.json` y devuelve lo publicado en la ventana, con fecha local, tipo (video, short o artículo) y si ya consta en `registro.md`. Acepta `--inicio` y `--fin` (formato `AAAA-MM-DDTHH:MM`). En los blogs con WordPress pide páginas anteriores del feed hasta cubrir la semana. Después revisa a mano las fuentes `manual` y cualquier feed que el script marque como no disponible, en su listado original.

Si no puedes ejecutar el script, abre los feeds directamente. Si un feed responde pero no tiene nada en la ventana y su última publicación es de hace semanas, la fuente simplemente no publicó: anótalo así en la cobertura. Si el feed no respondió o parece incompleto, haz una búsqueda por autor y semana antes de concluir que no hay nada.

**Si hay muchas piezas** (más de 15): lee primero las que más se acercan al «para qué» de la persona, hasta unas 15. Las demás van en la cobertura como «solo listado», con título, fecha y enlace. Mejor pocas bien leídas que muchas a medias.

### 3. Abrir y verificar cada novedad

Abre cada pieza. Comprueba la fecha original, el autor y el contenido. Una fecha nueva en un listado no basta: si el original es más antiguo y no hay cambios importantes, exclúyela. Si la página no permite confirmar si es nueva o reeditada, inclúyela con la nota «no se pudo confirmar si es una reedición». Compara la URL **y el tema** con el historial para no repetir.

**Interés comercial**: si la pieza viene de una empresa que vende lo que recomienda (el blog de un proveedor, una nota patrocinada, un autor que dirige una empresa del rubro), dilo en una frase: «Contenido de [empresa], que vende [producto]». Sus cifras y casos de clientes son afirmaciones de la empresa, no hechos comprobados.

Para videos de YouTube: abre la página del video, páusalo apenas cargue (el navegador puede reproducirlo con sonido en la computadora de la persona) y busca la transcripción («Mostrar transcripción»). Si no hay, o el panel dice «No se encontraron resultados» (pasa a menudo con videos con doblaje automático), revisa si la descripción trae capítulos. Cierra la pestaña de cada video apenas termines de leerlo y, al final, no dejes ninguna pestaña abierta. No descargues audio ni video ni uses servicios externos para extraer subtítulos. Haz como máximo un reintento por acceso fallido y nunca sortees un inicio de sesión, un muro de pago o una verificación anti-bots.

Clasifica cada pieza:

| Estado | Qué se puede decir |
|---|---|
| Contenido leído (texto o transcripción) | Un resumen propio de una o dos frases. |
| Solo capítulos o descripción del autor | «Temas anunciados por el autor: …». No cuenta como leído. |
| Sin contenido accesible | Título, fecha y enlace. Nada más. |

Un título, una miniatura o el resumen de otra persona no prueban que se vio un video. Nunca inventes un resumen.

**Contra el clickbait**: resume lo que dice el contenido, nunca el título. Si el título promete más de lo que el contenido entrega («esto lo cambia todo», «el fin de…»), escribe tu propio título descriptivo y, si hace falta, una nota breve: «El título exagera: en realidad muestra…». Si una pieza no aporta nada nuevo al tema, puede ir solo en la cobertura con el motivo, sin un bloque propio.

Para no inflar el conteo: el video y el artículo de la misma pieza son un solo ítem con dos enlaces; un boletín que repite piezas anteriores cuenta como edición propia, sin volver a contar lo ya resumido; los Shorts no llevan resumen individual, van agrupados al final con su enlace.

### 4. Analizar

Solo después de resumir, piensa en el posible uso para lo que la persona dijo en «para qué». Una frase por tema. «Sin aplicación clara por ahora» es válido y no saca la pieza del resumen. Separa siempre lo que afirma el autor, lo que comprobaste y lo que sugieres tú. Las cifras de ingresos o resultados son del autor, no hechos verificados.

### 5. Entregar

Formato, en el idioma configurado:

```markdown
# Resumen semanal · [tema] · [inicio–fin, año]

Esta semana: [una frase con lo más importante].

## 1. [Título corto del tema]
- **Autor, «Título»**, fecha. Resumen en una o dos frases. [enlace](url)
- ...
**Posible uso:** [una frase, o «sin aplicación clara por ahora»].

## 2. ...

## Cobertura
| Fuente | Estado | Última publicación vista |
|---|---|---|
| ... | contenido leído · leído en parte (N de M) · solo listado · acceso limitado · sin publicaciones en la semana | ... |

En «leído en parte (N de M)», M cuenta las piezas que pasaron el filtro. Si hubo filtro, añade cuántas descartó: «40 publicadas, 9 del tema».

Sin contenido accesible: [título, fecha y enlace].
Shorts: [enlaces agrupados por autor].
```

Agrupa por tema, no por fuente, y sin un número fijo de bloques. Junta noticias duplicadas. Cada fuente de `config.json` aparece en la tabla de cobertura con su estado. Antes de entregar, comprueba que cada pieza del inventario está en un bloque, en la cobertura o anotada como excluida, y que todos los enlaces son los originales.

Guarda siempre `informes/AAAA-MM-DD.md`: es el respaldo y la base de las demás formas. Después, según `entrega.formas`:
- `chat`: muéstralo en la conversación.
- `documento`: crea «Resumen semanal · [tema] · [fecha]» en Google Docs (o un .docx en `informes/`) con el mismo contenido, títulos y enlaces. Comparte el enlace o la ruta.
- `drive`: sube el resumen a `carpeta_drive` como documento de Google (si la herramienta convierte el texto al subirlo) o, si no puede, como archivo .md. Si además eligió `documento` en Google Docs, crea ese documento directamente en la carpeta, sin subir una segunda copia. Comprueba antes si ya existe uno con el mismo nombre para no duplicarlo, y después de subirlo confirma que aparece en la carpeta.
- `correo`: envíalo solo a las direcciones de `correo_para`, con asunto «Resumen semanal · [tema] · [rango de fechas]», el resumen en el cuerpo (HTML sencillo o texto, legible en el celular), sin copias ocultas ni adjuntos. Antes de enviar, busca en los enviados (y en borradores) que no exista ya el de esta semana, y revisa que el cuerpo que vas a enviar sea el resumen completo, no un texto de prueba ni un marcador vacío. Después de enviar, abre el mensaje enviado y comprueba destinatarios, asunto y que el cuerpo muestre el resumen completo. Si salió incompleto o vacío, envía una sola corrección en el mismo hilo, con «(versión corregida)» en el asunto, y avísale a la persona. Si `correo_modo` es `borrador`, créalo como borrador y dile a la persona que lo tiene listo para revisar y enviar.

Si una forma falla (herramienta no conectada, error al subir o al enviar), no la reintentes más de una vez: completa las demás, deja el archivo como respaldo y dile a la persona qué quedó pendiente y por qué. Ante un resultado dudoso, busca el correo o el archivo antes de reintentar, para no duplicar.

Si ya hay un informe con la fecha de hoy, actualízalo en vez de duplicarlo.

### 6. Registrar

Añade a `registro.md` una fila por cada pieza del inventario que pasó el filtro, también las que solo se listaron. Las que descartó el filtro no se registran: basta con el conteo en la cobertura. Es la memoria que evita repetir: el script marca como ya vista cualquier URL que esté aquí.

```markdown
| Fecha del resumen | Fuente | Título | URL | Estado |
|---|---|---|---|---|
```

`Estado`: resumido, solo anunciado, solo listado, sin acceso o excluido (con el motivo). No borres filas anteriores.

## Ajustarla con el tiempo

Cuando la persona diga que algo no le sirvió («esta fuente ya no», «quiero más detalle de X», «no me interesa Y»), actualiza `config.json` o añade una nota en el campo `notas` de la fuente, y aplícalo desde la semana siguiente. Si quiere cambiar de tema, vuelve a **Configurar**.

## Programarla

Para que llegue sola cada semana, crea una tarea programada en tu herramienta con un texto como este:

> Usa la skill resumen-semanal y prepara el resumen de esta semana.

- **Claude**: en la app de escritorio, pestaña Code, «Scheduled» y «New task»; frecuencia «Weekly».
- **Codex**: en la app, sección «Scheduled», crea una tarea programada con la frecuencia que quieras.

Elige un día y una hora en que tu computadora esté encendida, salvo que tu herramienta ejecute las tareas en la nube. Si la entrega es por correo, a un documento o a Drive, conecta antes esas herramientas: una tarea programada no puede pedirte permisos mientras corre.

## Límites

- No inventes fuentes, fechas, resúmenes ni cifras.
- No sortees inicios de sesión, muros de pago ni verificaciones anti-bots.
- No envíes correos a nadie más que a las direcciones confirmadas en `correo_para`.
- No compartas documentos ni carpetas de Drive con otras personas salvo que la persona lo pida.
- No compres, no te suscribas ni crees cuentas en nombre de la persona.
