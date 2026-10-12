import streamlit as st
import textwrap, json, re
from datetime import date

st.set_page_config(page_title="Mr Finanzas Studio", page_icon="💰", layout="wide")

st.markdown("""
<style>
.main {background:#f7f8fc}
.block-container {padding-top:1.5rem; max-width:1150px}
.hero {padding:1.2rem 1.4rem; border-radius:18px; background:linear-gradient(120deg,#10213a,#1d4773); color:white}
.hero h1 {margin:0; color:white}
.hero p {margin:.35rem 0 0; color:#e1eaf5}
div[data-testid="stMetric"] {background:white;padding:14px;border-radius:14px;border:1px solid #e6eaf0}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>💰 Mr Finanzas Studio</h1><p>Fábrica de videos largos con Nico como protagonista · Guiones, escenas, prompts y paquete de publicación</p></div>', unsafe_allow_html=True)
st.write("Prepara un paquete de producción para un video educativo. Esta versión organiza el trabajo y genera borradores editables; no genera imágenes, voces ni sube videos por sí sola.")

with st.sidebar:
    st.header("⚙️ Ajustes del canal")
    channel = st.text_input("Nombre del canal", "Mr Finanzas Stickman")
    protagonist = st.text_input("Personaje principal", "Nico")
    length_min = st.slider("Duración objetivo (minutos)", 5, 10, 5)
    scene_seconds = st.select_slider("Duración aproximada por escena", options=[5, 8, 10, 12, 15], value=10)
    tone = st.selectbox("Estilo de narración", ["Cercano y curioso", "Documental sencillo", "Humor ligero", "Motivador y práctico"])
    audience = st.selectbox("Público", ["Principiantes en finanzas", "Adolescentes y jóvenes", "Familias", "Público general"])
    cta = st.text_input("Llamada a la acción", "Comenta qué hábito de dinero quieres mejorar.")

st.subheader("1. Idea del video")
col1, col2 = st.columns([2,1])
with col1:
    topic = st.text_input("Tema principal", "Por qué algunas personas nunca consiguen ahorrar")
    hook = st.text_input("Gancho inicial (opcional)", "¿Te ha pasado que recibes dinero y desaparece antes de terminar el mes?")
    key_lesson = st.text_area("Lección principal", "Registrar los gastos, distinguir necesidades de deseos y separar una cantidad realista para ahorrar.", height=90)
with col2:
    format_kind = st.selectbox("Tipo de historia", ["Historia con dos personajes", "Problema y solución", "Mito vs realidad", "Reto de 30 días", "Lista explicada"])
    research_mode = st.selectbox("Base del contenido", ["Conceptos generales", "Incluir datos que debo verificar"])
    notes = st.text_area("Notas o ejemplos propios", "Usa cantidades ilustrativas y aclara que son ejemplos.", height=90)

def make_package():
    minutes = length_min
    total_seconds = minutes * 60
    n = max(5, round(total_seconds / scene_seconds))
    # Allocate a clear narrative arc
    phases = [
        ("Gancho", "Presenta una pregunta o situación que despierte curiosidad."),
        ("Contexto", "Muestra la situación cotidiana de Nico y el problema financiero."),
        ("Conflicto", "Nico toma una decisión común que empeora el problema."),
        ("Explicación", "Explica el concepto financiero con un ejemplo sencillo y verificable."),
        ("Alternativas", "Muestra dos o tres decisiones posibles y sus consecuencias."),
        ("Plan práctico", "Nico aplica pasos concretos y realistas."),
        ("Cierre", "Resume la lección y formula una pregunta para la audiencia.")
    ]
    # distribute scene count among phases
    weights = [1,1,1,2,1,2,1]
    counts = [max(1, round(n*w/sum(weights))) for w in weights]
    while sum(counts) > n: 
        idx = max(range(len(counts)), key=lambda i: counts[i])
        if counts[idx] > 1: counts[idx] -= 1
        else: break
    while sum(counts) < n:
        counts[3 if counts[3] < counts[5] else 5] += 1
    scene_list = []
    for phase_idx, ((phase, direction), count) in enumerate(zip(phases, counts)):
        for j in range(count):
            idx = len(scene_list)+1
            if phase == "Gancho":
                visual = f"{protagonist} revisa su billetera y mira unas pocas monedas con expresión de sorpresa; plano cercano, fondo limpio."
                narration = hook.strip() or f"¿Alguna vez te has preguntado qué ocurre con tu dinero antes de terminar el mes?"
            elif phase == "Contexto":
                visual = f"{protagonist} entra a una tienda de barrio y paga una compra pequeña; ambiente cotidiano, composición clara."
                narration = f"Todo comienza con una situación común: {topic.lower()}. Muchas veces no vemos el patrón hasta que lo ponemos en orden."
            elif phase == "Conflicto":
                visual = f"{protagonist} mira varias compras pequeñas, recibos y monedas que se acumulan sobre una mesa; gesto pensativo."
                narration = "El problema no siempre es una sola compra grande. A veces son decisiones repetidas que nunca revisamos."
            elif phase == "Explicación":
                visual = f"{protagonist} organiza monedas, recibos y una libreta con tres grupos visuales: necesidades, deseos y ahorro; sin texto legible en la imagen."
                narration = f"Una forma sencilla de entenderlo es mirar cada gasto y preguntarse si era necesario, si podía esperar y qué alternativa existía. La lección central es: {key_lesson}"
            elif phase == "Alternativas":
                visual = f"Composición dividida en dos situaciones: {protagonist} compra por impulso en una y compara opciones con calma en la otra; mismo diseño del personaje."
                narration = "Antes de gastar, conviene detenerse un momento, comparar opciones y decidir con intención. No se trata de no disfrutar, sino de elegir mejor."
            elif phase == "Plan práctico":
                visual = f"{protagonist} escribe un presupuesto sencillo en una libreta, usa una calculadora y separa unas monedas en un frasco de ahorro."
                narration = "Puedes empezar con pasos pequeños: anotar los gastos, fijar un límite realista y apartar el ahorro que puedas mantener sin descuidar necesidades básicas."
            else:
                visual = f"{protagonist} sonríe junto a una libreta ordenada y un frasco con monedas; composición positiva y sencilla."
                narration = f"Quédate con esta idea: {key_lesson} {cta}"
            scene_list.append({"n":idx, "phase":phase, "visual":visual, "narration":narration})
    # timing evenly approximate
    per_scene = total_seconds / len(scene_list)
    for s in scene_list:
        start = round((s["n"]-1)*per_scene)
        end = round(s["n"]*per_scene)
        s["time"] = f"{start//60:02d}:{start%60:02d}–{end//60:02d}:{end%60:02d}"
        s["prompt"] = (
            f"Ilustración 2D limpia para video educativo de finanzas, estilo cartoon consistente. "
            f"Usar como referencia visual la imagen adjunta de Nico y conservar exactamente su identidad: "
            f"cabello negro despeinado, rostro blanco sencillo, sudadera azul, pantalón negro, zapatillas blancas y mochila negra "
            f"(si la escena no requiere mochila, puede quedar fuera de plano). Escena: {s['visual']} "
            f"Composición horizontal 16:9, líneas claras, colores suaves, iluminación coherente, fondo detallado sin saturar, "
            f"sin palabras, sin logotipos, sin marcas de agua, anatomía consistente, no cambiar el diseño del personaje."
        )
    title = f"{topic.strip().capitalize()} | {channel}"
    desc = f"En este video de {channel}, Nico explora: {topic.lower()}. Aprenderás ideas sencillas para pensar mejor tus decisiones financieras.\\n\\nContenido educativo: los ejemplos son ilustrativos y no constituyen asesoría financiera personalizada.\\n\\n#FinanzasPersonales #Ahorro #EducacionFinanciera"
    tags = "finanzas personales, educación financiera, ahorro, hábitos financieros, administrar dinero, presupuesto, Mr Finanzas Stickman, Nico"
    thumb = f"Miniatura 16:9: Nico en primer plano sosteniendo una billetera abierta y mirando unas monedas; expresión de sorpresa; fondo azul y verde con alto contraste; texto corto grande: “¿ADÓNDE VA TU DINERO?”; mantener exactamente el diseño de Nico; no añadir otros textos."
    return {"channel":channel, "protagonist":protagonist, "topic":topic, "duration_minutes":minutes, "audience":audience, "tone":tone, "format":format_kind, "lesson":key_lesson, "title":title, "description":desc, "tags":tags, "thumbnail_prompt":thumb, "scenes":scene_list, "notes":notes, "research_mode":research_mode}

if st.button("🚀 Generar paquete del video", type="primary", use_container_width=True):
    if not topic.strip():
        st.error("Escribe un tema para el video.")
    else:
        st.session_state["package"] = make_package()

if "package" in st.session_state:
    p = st.session_state["package"]
    st.divider()
    st.subheader("2. Tu paquete de producción")
    m1,m2,m3 = st.columns(3)
    m1.metric("Duración objetivo", f"{p['duration_minutes']} min")
    m2.metric("Escenas", len(p["scenes"]))
    m3.metric("Personaje", p["protagonist"])
    tabs = st.tabs(["Guion y escenas", "Título y publicación", "Miniatura", "Lista de control"])
    with tabs[0]:
        st.info("La narración generada es una estructura inicial. Léela en voz alta, amplía las partes necesarias y verifica cualquier dato antes de grabar.")
        script = []
        for s in p["scenes"]:
            script.append(f"## Escena {s['n']} — {s['phase']} ({s['time']})\\n**Narración:** {s['narration']}\\n\\n**Visual:** {s['visual']}\\n\\n**Prompt de imagen:** {s['prompt']}\\n")
        all_script = "\\n".join(script)
        st.text_area("Guion + prompts (editable)", all_script, height=520)
        st.download_button("⬇️ Descargar guion y prompts (.md)", all_script, file_name="mr_finanzas_guion_escenas.md", mime="text/markdown", use_container_width=True)
        narration = " ".join(s["narration"] for s in p["scenes"])
        st.text_area("Narración unida para voz IA", narration, height=150)
        st.download_button("⬇️ Descargar narración (.txt)", narration, file_name="narracion_mr_finanzas.txt", mime="text/plain", use_container_width=True)
    with tabs[1]:
        st.text_input("Título sugerido", p["title"])
        st.text_area("Descripción", p["description"], height=140)
        st.text_input("Etiquetas separadas por comas", p["tags"])
        st.caption("Revisa que título y descripción representen realmente el contenido. No agregues afirmaciones o cifras que el video no respalde.")
        st.download_button("⬇️ Descargar paquete de publicación (.json)", json.dumps({k:v for k,v in p.items() if k!="scenes"}, ensure_ascii=False, indent=2), file_name="publicacion_mr_finanzas.json", mime="application/json", use_container_width=True)
    with tabs[2]:
        st.write(p["thumbnail_prompt"])
        st.download_button("⬇️ Descargar prompt de miniatura (.txt)", p["thumbnail_prompt"], file_name="prompt_miniatura.txt", mime="text/plain", use_container_width=True)
    with tabs[3]:
        checks = [
            "La narración dura aproximadamente lo previsto al leerla en voz alta.",
            "Verifiqué los datos y las cifras con fuentes fiables.",
            "Nico conserva el mismo diseño en todas las escenas.",
            "La música y los efectos tienen permiso de uso.",
            "Los subtítulos coinciden con la voz.",
            "La miniatura se entiende en una pantalla pequeña.",
            "El video aporta explicación original, no solo imágenes repetidas.",
            "Revisé el video completo antes de publicarlo."
        ]
        for item in checks:
            st.checkbox(item, key="check_"+str(checks.index(item)))
        st.caption("La app no publica automáticamente ni crea imágenes o audio. Usa los prompts en tu generador visual y la narración en tu herramienta de voz; luego monta el resultado en tu editor.")

st.divider()
st.caption("Mr Finanzas Studio · Prototipo local. No guarda tus proyectos en la nube ni envía contenido a YouTube.")
