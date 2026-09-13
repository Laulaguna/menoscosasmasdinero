# Genera las carpetas de redirección del acortador a partir de enlaces.json.
# Uso: python build.py
import io, json, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
RESERVADAS = {"guia", "retiro", "comunidad", "privacidad"}  # carpetas con contenido propio, nunca se sobrescriben

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<title>Menos cosas, más dinero</title>
<script>location.replace({url_js});</script>
</head>
<body style="font:16px system-ui,sans-serif;padding:32px;color:#17211F;background:#FBFAF6">
Redirigiendo… si no pasa nada, <a href="{url}">pulsa aquí</a>.
</body>
</html>
"""

with io.open(os.path.join(ROOT, "enlaces.json"), encoding="utf-8") as f:
    enlaces = json.load(f)

generadas = []
for clave, url in enlaces.items():
    if clave.startswith("_"):
        continue
    if clave in RESERVADAS:
        print(f"AVISO: '{clave}' es una ruta reservada, se ignora")
        continue
    carpeta = os.path.join(ROOT, clave)
    os.makedirs(carpeta, exist_ok=True)
    with io.open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(PLANTILLA.format(url=url, url_js=json.dumps(url)))
    generadas.append(clave)

# marca las carpetas generadas para poder borrar las que ya no estén en el json
with io.open(os.path.join(ROOT, ".generadas"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(generadas) + "\n")

print("Enlaces cortos generados:", ", ".join(generadas))
