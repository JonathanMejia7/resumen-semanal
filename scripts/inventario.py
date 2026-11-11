#!/usr/bin/env python3
"""Inventario de candidatos del resumen semanal a partir de feeds públicos.

Comandos:
  lista   Lista lo publicado por las fuentes de config.json dentro de la ventana,
          con fecha local, tipo (video, short, artículo) y si ya consta en
          registro.md. No lee contenido: solo arma la
          lista de candidatos que luego hay que abrir y comprobar.
  canal   Devuelve el feed de un canal de YouTube a partir de su URL.
  feed    Busca el feed RSS o Atom de un sitio a partir de su URL.

Uso:
  python3 inventario.py lista --datos ~/resumen-semanal
  python3 inventario.py lista --datos ~/resumen-semanal --inicio 2026-11-02T07:00 --fin 2026-11-09T07:00
  python3 inventario.py canal https://www.youtube.com/@canal
  python3 inventario.py feed https://ejemplo.com/blog/

Solo usa la biblioteca estándar de Python 3.9 o superior.
"""
import argparse
import html
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

UA = "Mozilla/5.0 (resumen-semanal)"
YT_FEED = "https://www.youtube.com/feeds/videos.xml?channel_id="
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


REDIRECCIONES = {}


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        final = r.geturl()
        if urllib.parse.urlsplit(final).path.rstrip("/") != urllib.parse.urlsplit(url).path.rstrip("/"):
            REDIRECCIONES[url] = final
        return r.read()


def aviso_redireccion(url):
    final = REDIRECCIONES.get(url)
    if final:
        return f"Aviso: {url} redirige a {final}. Comprueba que sea el feed que querías (por ejemplo, el de una sección y no el general)."
    return ""


def is_short(video_id):
    """/shorts/ID responde 200 para un Short y redirige a /watch para un video normal."""

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request("https://www.youtube.com/shorts/" + video_id, headers={"User-Agent": UA})
    try:
        return opener.open(req, timeout=10).status == 200
    except urllib.error.HTTPError:
        return False
    except Exception:
        return None


def limpiar_titulo(texto):
    """Quita etiquetas HTML (algunos medios ponen <br> en el título) y espacios de más."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(texto or ""))).strip()


def con_zona(dt):
    """Las fechas sin zona horaria (por ejemplo, las que terminan en -0000) se toman como UTC,
    para poder compararlas con las demás."""
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def leer_fecha(texto):
    """Lee fechas RSS (RFC 822) e ISO 8601 (Atom, dc:date). Devuelve None si no la entiende."""
    texto = (texto or "").strip()
    if not texto:
        return None
    try:
        dt = parsedate_to_datetime(texto)
        if dt:
            return con_zona(dt)
    except (TypeError, ValueError, IndexError):
        pass
    m = re.match(r"^(\d{4}-\d{2}-\d{2})(?:[T ](\d{2}:\d{2}(?::\d{2})?)(?:[.,](\d+))?)?\s*(Z|[+-]\d{2}:?\d{2})?$", texto, flags=re.I)
    if not m:
        return None
    dia, hora, fraccion, zona = m.groups()
    iso = dia + "T" + (hora or "00:00:00")
    if hora and len(hora) == 5:
        iso += ":00"
    if fraccion:
        iso += "." + (fraccion + "000000")[:6]
    if zona:
        zona = "+00:00" if zona.upper() == "Z" else zona
        iso += zona if ":" in zona else zona[:3] + ":" + zona[3:]
    try:
        return con_zona(datetime.fromisoformat(iso))
    except ValueError:
        return None


def local(el):
    """Nombre de una etiqueta sin su espacio de nombres."""
    return el.tag.rsplit("}", 1)[-1] if isinstance(el.tag, str) else ""


def hijo(e, *nombres):
    """Texto del primer hijo cuyo nombre (sin espacio de nombres) esté en nombres, en ese orden."""
    for nombre in nombres:
        for c in e:
            if local(c) == nombre and (c.text or "").strip():
                return c.text
    return ""


def enlace_atom(e):
    """En Atom, el enlace al contenido es el rel="alternate" (o sin rel). Blogger pone primero el de comentarios."""
    links = [l for l in e if local(l) == "link"]
    for l in links:
        if l.get("rel", "alternate") == "alternate" and l.get("type", "text/html") in ("text/html", ""):
            return l.get("href", "")
    for l in links:
        if l.get("rel", "alternate") == "alternate":
            return l.get("href", "")
    return links[0].get("href", "") if links else ""


PARSE_OMITIDAS = {"n": 0}


def parse(raw):
    """Entradas de un feed Atom, RSS 2.0 o RSS 1.0 (RDF). Las que no tienen una fecha legible se omiten
    y se cuentan en PARSE_OMITIDAS."""
    root = ET.fromstring(raw)
    if local(root) not in ("feed", "rss", "RDF"):
        raise ET.ParseError(f"la respuesta es <{local(root)}>, no un feed")
    items = []
    if local(root) == "feed":  # Atom (YouTube, Blogger y otros)
        for e in [x for x in root if local(x) == "entry"]:
            fecha = leer_fecha(hijo(e, "published", "updated"))
            if not fecha:
                PARSE_OMITIDAS["n"] += 1
                continue
            items.append({
                "titulo": limpiar_titulo(hijo(e, "title")),
                "fecha": fecha,
                "url": enlace_atom(e),
                "id": hijo(e, "videoId"),
                "resumen": hijo(e, "summary", "content", "description"),
            })
    else:  # RSS 2.0 y RSS 1.0 (RDF)
        for e in [x for x in root.iter() if local(x) == "item"]:
            fecha = leer_fecha(hijo(e, "pubDate", "date", "published", "updated"))
            if not fecha:
                PARSE_OMITIDAS["n"] += 1
                continue
            url = hijo(e, "link").strip() or (e.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about") or "")
            items.append({
                "titulo": limpiar_titulo(hijo(e, "title")),
                "fecha": fecha,
                "url": url,
                "id": "",
                "resumen": hijo(e, "description", "summary", "encoded"),
            })
    return items


def motivo(exc):
    """Explica un error de acceso en palabras simples."""
    if isinstance(exc, urllib.error.HTTPError):
        if exc.code in (401, 403, 429):
            return f"el sitio bloquea lectores automáticos (HTTP {exc.code}); ábrelo en el navegador antes de descartarlo"
        if exc.code == 404:
            return "la dirección no existe (HTTP 404)"
        return f"error HTTP {exc.code}"
    if isinstance(exc, ET.ParseError):
        return "respondió, pero no es un feed válido (quizá es una página web y no el RSS)"
    if isinstance(exc, urllib.error.URLError) and "CERTIFICATE_VERIFY_FAILED" in str(exc):
        return ("Python no tiene los certificados de seguridad instalados; en Mac, abre la carpeta de Python en "
                "Aplicaciones y ejecuta «Install Certificates.command»")
    if isinstance(exc, (urllib.error.URLError, TimeoutError, ConnectionError)):
        return f"no respondió ({type(exc).__name__})"
    return f"no se pudo leer el feed ({type(exc).__name__}: {exc})"


def zona_horaria(nombre):
    """Zona horaria del config. En Windows Python no trae la base de zonas: si falta, se usa la del equipo."""
    try:
        return ZoneInfo(nombre or "UTC"), ""
    except (ZoneInfoNotFoundError, ValueError):
        tz = datetime.now().astimezone().tzinfo
        return tz, (f"Aviso: este Python no reconoce la zona «{nombre}» (pasa en Windows). Se usa la hora de este "
                    "equipo. Para usar la del config: python -m pip install tzdata")


def describir_feed(raw, items):
    """Título del feed, cantidad, última entrada y ritmo de publicación."""
    root = ET.fromstring(raw)
    titulo = root.findtext("a:title", default="", namespaces=NS) or root.findtext("channel/title") or ""
    lineas = [f"Título del feed: {html.unescape(titulo).strip() or '(sin título)'}"]
    if not items:
        return lineas + ["El feed no tiene entradas."]
    fechas = sorted(i["fecha"] for i in items)
    # El ritmo se calcula con los últimos 30 días: algunos feeds guardan unas pocas entradas viejas
    # que, si se cuentan, hacen parecer que el medio casi no publica.
    recientes = [d for d in fechas if fechas[-1] - d <= timedelta(days=30)]
    dias = max((fechas[-1] - recientes[0]).total_seconds() / 86400, 1)
    lineas.append(f"Entradas: {len(items)}; última: {fechas[-1]:%Y-%m-%d}; unas {len(recientes) * 7 / dias:.1f} por semana.")
    if len(items) >= 10 and dias < 7:
        lineas.append(f"Aviso: el feed solo guarda unos {dias:.0f} días, así que no cubre la semana completa. "
                      "Cada semana habrá que revisar el listado (o el canal) para los días que falten; "
                      "si es un medio general, usa el feed de una sección o un filtro.")
    if (datetime.now(fechas[-1].tzinfo) - fechas[-1]).days > 90:
        lineas.append("Aviso: no publica hace más de 90 días; descártala salvo que la persona la quiera igual.")
    return lineas


def normalizar(texto):
    """Minúsculas y sin tildes, para comparar palabras clave."""
    texto = unicodedata.normalize("NFD", html.unescape(texto).lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def pasa_filtro(item, filtro):
    """Sin filtro pasa todo. Con filtro, el título o el resumen del feed debe contener alguna de las
    palabras completas; una palabra que termina en * acepta cualquier final (export* = exporta, exportaciones)."""
    if not filtro:
        return True
    texto = normalizar(item["titulo"] + " " + re.sub(r"<[^>]+>", " ", item.get("resumen", "")))
    for palabra in filtro:
        p = normalizar(palabra).strip()
        patron = re.escape(p[:-1]) + r"\w*" if p.endswith("*") else re.escape(p)
        if re.search(r"(?<!\w)" + patron + r"(?!\w)", texto):
            return True
    return False


def historial(datos):
    textos = []
    for p in [datos / "registro.md"]:
        if p.exists():
            textos.append(p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(textos)


def ya_registrado(item, texto):
    if item["id"]:  # en YouTube la URL sin parámetros sería solo /watch
        return item["id"] in texto
    url = item["url"].split("?")[0].rstrip("/")
    return bool(url) and url in texto


def lista(args):
    datos = Path(args.datos).expanduser()
    config_path = datos / "config.json"
    if not config_path.exists():
        print(f"No existe {config_path}. Configura el resumen primero.")
        return 1
    config = json.loads(config_path.read_text(encoding="utf-8"))
    tz, aviso_tz = zona_horaria(config.get("zona_horaria"))
    if aviso_tz:
        print(aviso_tz + "\n")

    fin = datetime.fromisoformat(args.fin).replace(tzinfo=tz) if args.fin else datetime.now(tz)
    if args.inicio:
        inicio = datetime.fromisoformat(args.inicio).replace(tzinfo=tz)
    else:  # día completo, para tratar igual las fuentes con hora y las que solo ponen la fecha
        inicio = (fin - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    texto = historial(datos)

    print(f"Tema: {config.get('tema', '')}")
    print(f"Ventana: {inicio:%Y-%m-%d %H:%M} a {fin:%Y-%m-%d %H:%M} ({getattr(tz, 'key', None) or 'hora de este equipo'})\n")
    print("| Fuente | Fecha local | Tipo | Título | URL | Ya registrado |")
    print("|---|---|---|---|---|---|")
    estados = []
    for f in config.get("fuentes", []):
        nombre, tipo, feed = f.get("nombre", "?"), f.get("tipo", "sitio"), f.get("feed", "")
        if tipo == "manual" or not feed:
            estados.append(f"- {nombre}: sin feed; revisar a mano {f.get('listado', '')}")
            continue
        PARSE_OMITIDAS["n"] = 0
        try:
            items = parse(fetch(feed))
        except Exception as exc:  # una fuente caída no detiene el resto
            estados.append(f"- {nombre}: feed no disponible: {motivo(exc)}. Revisar {f.get('listado', '')}")
            continue
        try:
            procesar_fuente(f, nombre, feed, items, inicio, fin, tz, texto, estados)
        except Exception as exc:  # un error inesperado en una fuente tampoco detiene el resto
            estados.append(f"- {nombre}: no se pudo procesar el feed ({type(exc).__name__}: {exc}). Revisar {f.get('listado', '')}")

    print("\nEstado de las fuentes:")
    print("\n".join(estados))
    print("\nEl feed solo prueba existencia, título y fecha. Abrir cada candidato antes de resumirlo.")
    return 0


def procesar_fuente(f, nombre, feed, items, inicio, fin, tz, texto, estados):
    """Lista lo de la ventana para una fuente y anota su estado y sus avisos."""
    # Los feeds de WordPress aceptan ?paged=N: se piden páginas hasta cubrir la ventana.
    pagina = 2
    while items and min(i["fecha"] for i in items).astimezone(tz) > inicio and pagina <= 4 and "?" not in feed:
        try:
            mas = parse(fetch(f"{feed.rstrip('/')}/?paged={pagina}"))
        except Exception:
            break
        nuevos = [i for i in mas if i["url"] not in {x["url"] for x in items}]
        if not nuevos:
            break
        items += nuevos
        pagina += 1
    ultima = max((i["fecha"] for i in items), default=None)
    en_ventana = [i for i in items if inicio <= i["fecha"].astimezone(tz) <= fin]
    filtro = f.get("filtro") or []
    dentro = [i for i in en_ventana if pasa_filtro(i, filtro)]
    for i in sorted(dentro, key=lambda i: i["fecha"]):
        clase = "artículo"
        if i["id"]:
            corto = is_short(i["id"])
            clase = "short" if corto else ("video" if corto is False else "video?")
        titulo = i["titulo"].replace("|", "/")
        marca = "sí" if ya_registrado(i, texto) else ""
        print(f"| {nombre} | {i['fecha'].astimezone(tz):%Y-%m-%d %H:%M} | {clase} | {titulo} | {i['url']} | {marca} |")
    ult = f"{ultima.astimezone(tz):%Y-%m-%d}" if ultima else "sin entradas"
    nota = f" ({len(en_ventana)} antes del filtro)" if filtro else ""
    estados.append(f"- {nombre}: {len(dentro)} en ventana{nota}; última entrada del feed {ult}.")
    if filtro and len(en_ventana) >= 5 and len(dentro) > 0.8 * len(en_ventana):
        estados.append("  Aviso: el filtro deja pasar casi todo. Quita palabras genéricas o propias del medio y usa palabras más específicas del tema.")
    if aviso_redireccion(feed):
        estados.append("  " + aviso_redireccion(feed))
    primera = min((i["fecha"] for i in items), default=None)
    if primera and primera.astimezone(tz) > inicio:
        estados.append(f"  Aviso: el feed solo cubre desde {primera.astimezone(tz):%Y-%m-%d %H:%M}; "
                       f"lo publicado antes no aparece. "
                       + (f"Revisar los videos de esos días en {f.get('listado', '')}."
                          if f.get("tipo") == "youtube" else
                          f"Revisar {f.get('listado', '')} o una sección del sitio."))
    if PARSE_OMITIDAS["n"]:
        estados.append(f"  Aviso: entradas del feed con una fecha que no se pudo leer, que no aparecen: {PARSE_OMITIDAS['n']}. "
                       f"Revisar {f.get('listado', '')}.")


def canal(args):
    url = args.url
    m = re.search(r"channel/(UC[\w-]{22})", url)
    if m:
        cid = m.group(1)
    else:
        try:
            page = fetch(url).decode("utf-8", errors="ignore")
        except Exception as exc:
            print(f"No se pudo abrir {url}: {motivo(exc)}.")
            return 1
        m = (re.search(r'<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[\w-]{22})"', page)
             or re.search(r'"externalId":"(UC[\w-]{22})"', page)
             or re.search(r'"channelId":"(UC[\w-]{22})"', page))
        if not m:
            print("No encontré el identificador del canal. Abre el canal en el navegador y copia la URL /channel/UC...")
            return 1
        cid = m.group(1)
    feed = YT_FEED + cid
    try:
        raw = fetch(feed)
        print(feed)
        print("\n".join(describir_feed(raw, parse(raw))))
    except Exception as exc:
        print(f"{feed}\nEl feed {motivo(exc)}; comprobarlo más tarde.")
    return 0


def es_de_la_seccion(pagina, feed_url):
    """True si la página es la portada o si el feed comparte alguna parte de la ruta de la sección."""
    partes = [re.sub(r"\.\w+$", "", x) for x in urllib.parse.urlsplit(pagina).path.split("/") if x]
    generales = {"blog", "blogs", "news", "noticias", "articulos", "articles", "posts", "insights", "recursos"}
    if not partes or all(x.lower() in generales for x in partes):
        return True
    ruta_feed = urllib.parse.urlsplit(feed_url).path + "?" + urllib.parse.urlsplit(feed_url).query
    return any(len(x) > 3 and x.lower() in ruta_feed.lower() for x in partes[-2:])


def feed(args):
    url = args.url
    try:
        page = fetch(url).decode("utf-8", errors="ignore")
    except Exception as exc:
        print(f"No se pudo abrir {url}: {motivo(exc)}.")
        return 1
    desde_pagina = False
    if page.lstrip().startswith("<?xml") or "<rss" in page[:500] or "<feed" in page[:500]:
        candidatos = [url]
    else:
        desde_pagina = True
        candidatos = []
        for tag in re.findall(r"<link[^>]+>", page, flags=re.I):
            if re.search(r'type="application/(rss|atom)\+xml"', tag, flags=re.I):
                href = re.search(r'href="([^"]+)"', tag)
                if href:
                    candidatos.append(urllib.parse.urljoin(url, html.unescape(href.group(1))))
        if not candidatos:
            base = urllib.parse.urljoin(url, "/")
            candidatos = [base + "feed/", base + "feed", base + "rss", base + "rss.xml", base + "atom.xml"]
    for c in dict.fromkeys(candidatos):
        try:
            raw = fetch(c)
            items = parse(raw)
        except Exception:
            continue
        if items:
            print(c)
            print("\n".join(describir_feed(raw, items)))
            if aviso_redireccion(c):
                print(aviso_redireccion(c))
            if desde_pagina and not es_de_la_seccion(url, c):
                print("Aviso: parece el feed general del sitio, no el de esta sección. Busca un feed de la sección "
                      "o añade un «filtro» con palabras del tema.")
            return 0
    print("No encontré un feed que funcione. Guarda la fuente como «manual» con la URL de su listado.")
    return 1


def main():
    for flujo in (sys.stdout, sys.stderr):  # en Windows la consola puede no aceptar tildes ni «»
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Inventario de fuentes del resumen semanal.")
    sub = ap.add_subparsers(dest="comando", required=True)

    p = sub.add_parser("lista", help="lista lo publicado en la ventana")
    p.add_argument("--datos", default="~/resumen-semanal", help="carpeta con config.json, registro.md e informes/")
    p.add_argument("--inicio", help="AAAA-MM-DDTHH:MM en la zona horaria del config; por defecto fin menos 7 días")
    p.add_argument("--fin", help="AAAA-MM-DDTHH:MM en la zona horaria del config; por defecto ahora")
    p.set_defaults(func=lista)

    p = sub.add_parser("canal", help="feed de un canal de YouTube")
    p.add_argument("url")
    p.set_defaults(func=canal)

    p = sub.add_parser("feed", help="buscar el feed de un sitio")
    p.add_argument("url")
    p.set_defaults(func=feed)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
