# Mr Finanzas Studio

Prototipo de una fábrica de producción para videos largos del canal Mr Finanzas Stickman. Funciona en navegador en Windows y Android si se ejecuta localmente en el computador o se despliega en la nube.

## Qué hace
- Crea una estructura de escenas según el tema y la duración.
- Prepara narraciones iniciales y prompts de imágenes que describen la apariencia de Nico.
- Genera título, descripción, etiquetas y prompt de miniatura.
- Permite descargar guion, narración y paquete de publicación.

## Qué no hace todavía
- No genera imágenes ni voces directamente.
- No exporta un MP4 final.
- No publica en YouTube automáticamente.
- El texto es un borrador estructural y debe revisarse, ampliarse y comprobarse antes de usarlo.

## Ejecutar en Windows
1. Instala Python 3.11 o una versión compatible desde https://www.python.org/downloads/
2. Descomprime el ZIP.
3. Abre una terminal dentro de la carpeta `mr_finanzas_studio`.
4. Ejecuta:
   `python -m pip install -r requirements.txt`
5. Luego:
   `python -m streamlit run app.py`
6. Abre la dirección local que muestra la terminal.

## Usarlo en Android
La forma más cómoda es desplegarlo en Streamlit Community Cloud:
1. Crea una cuenta de GitHub y un repositorio para el proyecto.
2. Sube `app.py` y `requirements.txt` al repositorio.
3. En https://share.streamlit.io/ crea una app seleccionando ese repositorio y `app.py`.
4. Cuando se despliegue, abre el enlace en el navegador del celular. Puedes añadirlo a la pantalla de inicio.
5. No subas claves API ni contraseñas al repositorio.

## Cómo mantener a Nico consistente
Sube la imagen de referencia de Nico a tu generador de imágenes cada vez que permita usar una imagen de referencia. Usa los prompts de la app como base, y comprueba que el personaje conserve cabello negro despeinado, rostro blanco, sudadera azul, pantalón negro y zapatillas blancas.

## Importante
La app genera un paquete de planificación, no una producción final totalmente automática. Para conectar generación de imágenes, voz o publicación se necesitarían integraciones adicionales, claves/API cuando corresponda y revisar sus precios, límites y permisos.
