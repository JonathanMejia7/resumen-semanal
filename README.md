# Resumen semanal · Weekly summary

Skill para Claude Code y Codex que arma cada semana un resumen de lo que publicaron tus fuentes favoritas, con fecha y enlace original.<br>
A skill for Claude Code and Codex that builds a weekly summary of what your favorite sources published, with date and original link.

**[⬇ Descargar / Download `resumen-semanal.zip`](https://github.com/JonathanMejia7/resumen-semanal/releases/latest/download/resumen-semanal.zip)**

<details>
  <summary>🇪🇸 Español</summary>

### Qué hace

- La primera vez te ayuda a elegir el tema y de 3 a 5 fuentes: blogs, canales de YouTube, medios o boletines.
- Cada semana trae solo lo publicado en los últimos 7 días, con fecha y enlace original.
- Recuerda lo que ya te resumió para no repetirlo.
- Ordena las novedades por tema y te dice para qué te podría servir cada una.
- Separa lo que dice el autor de lo comprobado y te avisa qué fuentes no pudo leer, en vez de inventar.
- Te lo entrega en el chat, como archivo, en un documento, en Google Drive o por correo.

### Cómo instalarla

El tutorial paso a paso está en mi web: **[jonathanmejia7.github.io/recursos/resumen-semanal](https://jonathanmejia7.github.io/recursos/resumen-semanal/#skill)**. Ahí también está el prompt para usarla en cualquier chat, sin instalar nada.

En corto: descarga el zip, descomprímelo y pídele a Claude Code o Codex «Instala la skill que está en mi carpeta Descargas/resumen-semanal». Después escribe «Configura mi resumen semanal».

### Qué hay en el repositorio

| Archivo | Para qué |
|---|---|
| `SKILL.md` | Las instrucciones que sigue Claude Code o Codex |
| `LEEME.md` | Instalación y uso, en corto |
| `scripts/inventario.py` | Lee los feeds de tus fuentes (Python 3.9 o superior, sin instalar nada más) |

Tus datos (configuración, memoria e informes) se guardan en tu computadora, en `~/resumen-semanal/`, fuera de la skill.

</details>

<details>
  <summary>🇺🇸 English</summary>

### What it does

- The first time, it helps you pick a topic and 3 to 5 sources: blogs, YouTube channels, news outlets or newsletters.
- Each week it brings only what was published in the last 7 days, with date and original link.
- It remembers what it already summarized so it doesn't repeat it.
- It groups the news by topic and tells you how each item could help you.
- It separates what the author claims from what was verified, and tells you which sources it couldn't read instead of making things up.
- It delivers the summary in the chat, as a file, in a document, in Google Drive or by email.

The skill's instructions are in Spanish, but it writes your summary in the language you choose when you set it up.

### How to install it

The step-by-step tutorial is on my website: **[jonathanmejia7.github.io/en/resources/resumen-semanal](https://jonathanmejia7.github.io/en/resources/resumen-semanal/#skill)**. You'll also find the prompt there, to use it in any chat without installing anything.

In short: download the zip, unzip it and ask Claude Code or Codex: "Install the skill in my Downloads/resumen-semanal folder". Then type "Set up my weekly summary in English".

### What's in the repository

| File | What it's for |
|---|---|
| `SKILL.md` | The instructions Claude Code or Codex follows |
| `LEEME.md` | Short install and usage guide (in Spanish) |
| `scripts/inventario.py` | Reads your sources' feeds (Python 3.9 or later, nothing else to install) |

Your data (settings, memory and reports) stays on your computer, in `~/resumen-semanal/`, outside the skill.

</details>

---

Creada por / Created by **Jonathan Mejía** · [LinkedIn](https://www.linkedin.com/in/jonathanmejia710) · [Instagram](https://www.instagram.com/jonathanmejia.ops/) · [TikTok](https://www.tiktok.com/@jonathanmejia.ops)
