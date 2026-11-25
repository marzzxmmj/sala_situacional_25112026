import io
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sala Situacional SSU",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS VISUALES (FONDO OSCURO, TÍTULO BLANCO, SELECTOR CON LETRA NEGRA Y FUENTES MÁS GRANDES) ---
st.markdown("""
<style>
    /* Fondo general más oscuro y profesional */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #0B192C 0%, #13294B 55%, #0F233C 100%);
    }

    /* Barra lateral oscura */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #081322 0%, #0E1F36 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.22);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #F8FAFC;
        font-size: 1rem;
    }

    /* Cuadro de selección de patología: fondo claro y letras negras */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #F8FAFC !important;
        border: 1.5px solid #38BDF8 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] div,
    [data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #0F172A !important;
    }

    /* Menú desplegable de opciones (popover) también con texto negro */
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] div,
    [data-baseweb="popover"] span {
        color: #0F172A !important;
        font-size: 1rem !important;
    }

    /* Botón de la barra lateral */
    [data-testid="stSidebar"] button {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #0369A1 !important;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.2rem;
    }

    /* Banner principal con título y subtítulo grandes y llamativos */
    .hero-banner {
        background: linear-gradient(120deg, #091E3A 0%, #1D4ED8 60%, #0284C7 100%);
        border-radius: 16px;
        padding: 1.9rem 2.3rem;
        margin-bottom: 1.35rem;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(125, 211, 252, 0.28);
    }
    .hero-badge {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.18);
        color: #FFFFFF;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.34rem 0.85rem;
        border-radius: 999px;
        margin-bottom: 0.7rem;
    }
    .hero-title {
        font-size: 2.85rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 0;
        line-height: 1.15;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.35);
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #E0F2FE !important;
        margin: 0.55rem 0 0 0;
        font-weight: 500;
    }

    /* Semáforo de alerta y lectura rápida */
    .semaforo-box {
        border-radius: 12px;
        padding: 1.05rem 1.4rem;
        margin-bottom: 1.35rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.85rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.22);
    }
    .semaforo-titulo {
        font-size: 1.18rem;
        font-weight: 800;
        margin: 0;
    }
    .semaforo-detalle {
        font-size: 1.05rem;
        margin: 0.22rem 0 0 0;
        opacity: 0.98;
    }

    /* Tarjetas de indicadores con medida idéntica y fuente más grande */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 14px;
        padding: 1.15rem 1.3rem;
        height: 128px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.22);
        transition: transform 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 0.92rem;
        font-weight: 800;
        color: #334155;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-value {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    .kpi-accent-blue { border-top: 4px solid #1D4ED8; background: linear-gradient(180deg, #EFF6FF 0%, #FFFFFF 35%); }
    .kpi-accent-teal { border-top: 4px solid #0D9488; background: linear-gradient(180deg, #F0FDFA 0%, #FFFFFF 35%); }
    .kpi-accent-amber { border-top: 4px solid #D97706; background: linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 35%); }
    .kpi-accent-indigo { border-top: 4px solid #4338CA; background: linear-gradient(180deg, #EEF2FF 0%, #FFFFFF 35%); }

    /* Subtítulos / títulos de secciones más grandes y visibles */
    .section-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        padding-left: 0.85rem;
        border-left: 5px solid #38BDF8;
        letter-spacing: -0.01em;
    }

    /* Tarjetas de zonas para comparación con cuartiles */
    .zona-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        height: 112px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border-left: 6px solid #64748B;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.18);
    }
    .zona-card-label {
        font-size: 0.9rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #334155;
        white-space: nowrap;
    }
    .zona-card-num {
        font-size: 1.95rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }

    /* Texto más legible en tablas y botones de descarga */
    [data-testid="stDataFrame"] {
        font-size: 1rem !important;
    }
    [data-testid="stDownloadButton"] button {
        font-size: 1.02rem !important;
        font-weight: 700 !important;
        padding: 0.55rem 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Vigilancia Epidemiológica · Gestión 2026</div>
    <h1 class="hero-title">SALA SITUACIONAL DE SALUD</h1>
    <p class="hero-subtitle">Monitoreo semanal de canales endémicos y comportamiento epidemiológico</p>
</div>
""", unsafe_allow_html=True)

# --- CARGAR DATOS DESDE GOOGLE SHEETS ---
SHEET_ID = "154r2-YajFh_1MxxNFbHACJX1AWAjAss7xC_fnFTtBnE"

@st.cache_data(ttl=600)
def cargar_datos(sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    df_leido = pd.read_excel(url, sheet_name="BASE_CANAL")

    cols_numericas = [
        "Semana", "Casos_Actuales", "Q1", "Q2", "Q3",
        "Zona_Exito", "Zona_Seguridad", "Zona_Alarma", "Zona_Epidemia",
        "Es_Epidemia", "Es_Alerta"
    ]
    for col in cols_numericas:
        if col in df_leido.columns:
            if df_leido[col].dtype == object:
                df_leido[col] = df_leido[col].astype(str).str.replace(",", ".", regex=False)
            df_leido[col] = pd.to_numeric(df_leido[col], errors="coerce")

    # Filtrar estrictamente las 52 semanas epidemiológicas
    df_leido = df_leido[df_leido["Semana"].between(1, 52)].copy()
    df_leido["Semana"] = df_leido["Semana"].astype(int)

    return df_leido

try:
    df = cargar_datos(SHEET_ID)
except Exception:
    st.error("No se pudo conectar con Google Sheets. Verifica que el archivo tenga acceso público de lectura.")
    st.stop()

# --- BARRA LATERAL (CON PATOLOGÍA Y RANGO DE SEMANAS) ---
with st.sidebar:
    st.markdown("### Filtros de vigilancia")
    patologia = st.selectbox(
        "Seleccione una patología",
        df["Patologia"].dropna().unique()
    )

    rango_semanas = st.slider(
        "Rango de semanas epidemiológicas",
        min_value=1,
        max_value=52,
        value=(1, 52),
        step=1
    )

    datos = df[
        (df["Patologia"] == patologia) &
        (df["Semana"].between(rango_semanas[0], rango_semanas[1]))
    ].sort_values("Semana").copy()

    codigo_pat = ""
    if "Codigo" in datos.columns and datos["Codigo"].notna().any():
        codigo_pat = str(datos["Codigo"].dropna().iloc[0])

    ult_reporte = datos[datos["Casos_Actuales"].notna()]
    if not ult_reporte.empty:
        ultima_fila = ult_reporte.iloc[-1]
        ult_sem = int(ultima_fila["Semana"])
        ult_casos = int(ultima_fila["Casos_Actuales"])
        ult_clasif = str(ultima_fila.get("Clasificacion", "—"))
        ult_q2 = ultima_fila.get("Q2", None)
        ult_q3 = ultima_fila.get("Q3", None)
    else:
        ult_sem, ult_casos, ult_clasif = 0, 0, "Sin registro"
        ult_q2, ult_q3 = None, None

    st.divider()
    st.markdown("### Resumen del corte")
    if codigo_pat:
        st.write(f"**Código:** {codigo_pat}")
    st.write(f"**Rango activo:** SE {rango_semanas[0]:02d} – SE {rango_semanas[1]:02d}")
    st.write(f"**Última SE reportada:** SE {ult_sem:02d}")
    st.write(f"**Casos última SE:** {ult_casos}")
    st.write(f"**Clasificación actual:** {ult_clasif}")

    if st.button("Actualizar datos de Drive", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- SEMÁFORO DE ALERTA Y LECTURA RÁPIDA ---
if ult_sem > 0:
    clasif_lower = ult_clasif.lower()
    if "epidemia" in clasif_lower:
        bg_sem, txt_sem, border_sem, badge_txt = "#7F1D1D", "#FEF2F2", "#F87171", "BROTE / EPIDEMIA"
    elif "alarma" in clasif_lower:
        bg_sem, txt_sem, border_sem, badge_txt = "#78350F", "#FFFBEB", "#FBBF24", "ZONA DE ALARMA"
    elif "seguridad" in clasif_lower:
        bg_sem, txt_sem, border_sem, badge_txt = "#713F12", "#FEFCE8", "#FACC15", "ZONA DE SEGURIDAD"
    else:
        bg_sem, txt_sem, border_sem, badge_txt = "#064E3B", "#ECFDF5", "#34D399", "ZONA DE ÉXITO"

    if pd.notna(ult_q3) and ult_casos > ult_q3:
        umbral_msg = f"Superó el umbral de epidemia (Q3 = {int(round(ult_q3))})."
    elif pd.notna(ult_q2) and ult_casos > ult_q2:
        umbral_msg = f"Superó la mediana / seguridad (Q2 = {int(round(ult_q2))})."
    else:
        q2_txt = f"{int(round(ult_q2))}" if pd.notna(ult_q2) else "N/D"
        umbral_msg = f"Se mantiene dentro del margen esperado (Q2 = {q2_txt})."

    st.markdown(f"""
    <div class="semaforo-box" style="background-color: {bg_sem}; color: {txt_sem}; border-left: 6px solid {border_sem};">
        <div>
            <p class="semaforo-titulo">Semáforo epidemiológico — {patologia} ({badge_txt})</p>
            <p class="semaforo-detalle">Último corte en <strong>SE {ult_sem:02d}</strong> con <strong>{ult_casos} casos</strong> ({ult_clasif}). {umbral_msg}</p>
        </div>
        <div style="font-weight: 800; font-size: 1.02rem; padding: 0.4rem 0.9rem; border-radius: 999px; background: rgba(255,255,255,0.16);">
            Estado: {ult_clasif}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- INDICADORES (KPIs) CON MISMA ALTURA ---
total_casos = int(datos["Casos_Actuales"].fillna(0).sum())
semanas_transcurridas = len(datos[datos["Casos_Actuales"].notna()]["Semana"].dropna().unique())
semanas_sobre_seguridad = len(
    datos[
        datos["Casos_Actuales"].notna() &
        datos["Q2"].notna() &
        (datos["Casos_Actuales"] > datos["Q2"])
    ]["Semana"].dropna().unique()
)
total_semanas_gestion = len(datos)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card kpi-accent-blue">
        <div class="kpi-label">Total de casos</div>
        <div class="kpi-value">{total_casos:,}</div>
    </div>
    """.replace(",", " "), unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card kpi-accent-teal">
        <div class="kpi-label">Semanas transcurridas</div>
        <div class="kpi-value">{semanas_transcurridas}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card kpi-accent-amber">
        <div class="kpi-label">Semanas sobre seguridad</div>
        <div class="kpi-value">{semanas_sobre_seguridad}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card kpi-accent-indigo">
        <div class="kpi-label">Semanas en rango</div>
        <div class="kpi-value">{total_semanas_gestion}</div>
    </div>
    """, unsafe_allow_html=True)

# --- CANAL ENDÉMICO (IZQUIERDA) Y DETALLE EPIDEMIOLÓGICO (DERECHA) ---
ALTURA_PANEL = 530

col_graf, col_tabla = st.columns([1.75, 1], gap="large")

with col_graf:
    st.markdown(f'<div class="section-title">Canal endémico — {patologia}</div>', unsafe_allow_html=True)

    fig = go.Figure()

    zonas = [
        ("Zona_Exito", "Éxito", "#81C995"),
        ("Zona_Seguridad", "Seguridad", "#F5DF72"),
        ("Zona_Alarma", "Alarma", "#FFB65C"),
        ("Zona_Epidemia", "Epidemia", "#EF9A9A")
    ]

    for campo, nombre, color in zonas:
        fig.add_trace(go.Scatter(
            x=datos["Semana"],
            y=datos[campo],
            name=nombre,
            mode="lines",
            stackgroup="canal",
            line=dict(width=0),
            fillcolor=color,
            hovertemplate=f"<b>{nombre}</b>: %{{y:.0f}}<extra></extra>"
        ))

    fig.add_trace(go.Scatter(
        x=datos["Semana"],
        y=datos["Casos_Actuales"],
        name="Casos 2026",
        mode="lines+markers",
        connectgaps=False,
        line=dict(color="#0F172A", width=3.2),
        marker=dict(size=7, color="#1D4ED8", line=dict(color="#FFFFFF", width=1.2)),
        hovertemplate="<b>Casos 2026</b>: %{y:.0f}<extra></extra>"
    ))

    fig.update_layout(
        xaxis=dict(
            title=dict(text="Semana epidemiológica", font=dict(size=14, color="#0F172A")),
            tickfont=dict(size=13, color="#1E293B"),
            tickmode="linear",
            dtick=5,
            range=[rango_semanas[0], rango_semanas[1]],
            showgrid=True,
            gridcolor="#F1F5F9"
        ),
        yaxis=dict(
            title=dict(text="Número de casos", font=dict(size=14, color="#0F172A")),
            tickfont=dict(size=13, color="#1E293B"),
            showgrid=True,
            gridcolor="#E2E8F0",
            rangemode="tozero"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=13, color="#0F172A"),
            bgcolor="rgba(255,255,255,0.92)"
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#1E293B", size=13),
        hovermode="x unified",
        height=ALTURA_PANEL,
        margin=dict(l=25, r=25, t=50, b=25)
    )

    st.plotly_chart(fig, use_container_width=True)

with col_tabla:
    st.markdown('<div class="section-title">Detalle epidemiológico</div>', unsafe_allow_html=True)

    tabla_mostrar = datos[[
        "Semana",
        "Casos_Actuales",
        "Clasificacion"
    ]].rename(columns={
        "Semana": "Semana EP",
        "Casos_Actuales": "Casos 2026",
        "Clasificacion": "Clasificación"
    })

    st.dataframe(
        tabla_mostrar,
        use_container_width=True,
        hide_index=True,
        height=ALTURA_PANEL
    )

# --- GRÁFICO DE COLUMNAS: CASOS POR SEMANA EPIDEMIOLÓGICA (GESTIÓN 2026) ---
st.markdown(
    f'<div class="section-title">Casos reportados por semana epidemiológica · Gestión 2026 — {patologia}</div>',
    unsafe_allow_html=True
)

datos_2026 = datos[datos["Casos_Actuales"].notna()].copy()
datos_2026["Etiqueta_SE"] = datos_2026["Semana"].apply(lambda s: f"SE {int(s):02d}")
datos_2026["Casos_Entero"] = datos_2026["Casos_Actuales"].round(0).astype(int)

max_val_barras = int(datos_2026["Casos_Entero"].max()) if not datos_2026.empty else 10

fig_barras = go.Figure()

fig_barras.add_trace(go.Bar(
    x=datos_2026["Etiqueta_SE"],
    y=datos_2026["Casos_Entero"],
    text=datos_2026["Casos_Entero"],
    textposition="outside",
    textfont=dict(color="#0F172A", size=13, family="Arial"),
    marker=dict(
        color="#1D4ED8",
        line=dict(color="#0F294A", width=1)
    ),
    name="Casos Gestión 2026",
    hovertemplate="<b>%{x}</b><br>Total de casos (2026): %{y}<extra></extra>"
))

fig_barras.update_layout(
    title=dict(
        text=f"Distribución semanal de casos registrados — Gestión 2026 ({patologia})",
        font=dict(size=17, color="#0F172A"),
        x=0.01
    ),
    xaxis=dict(
        title=dict(text="Semana epidemiológica (Gestión 2026)", font=dict(size=14, color="#0F172A")),
        tickfont=dict(size=12.5, color="#1E293B"),
        showgrid=False,
        tickangle=-35 if len(datos_2026) > 15 else 0
    ),
    yaxis=dict(
        title=dict(text="Total de casos", font=dict(size=14, color="#0F172A")),
        tickfont=dict(size=13, color="#1E293B"),
        showgrid=True,
        gridcolor="#E2E8F0",
        rangemode="tozero",
        range=[0, max_val_barras * 1.18 + 1]
    ),
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(color="#1E293B", size=13),
    height=440,
    margin=dict(l=25, r=25, t=65, b=50),
    showlegend=False
)

st.plotly_chart(fig_barras, use_container_width=True)

# --- COMPARACIÓN 2026 FRENTE A CUARTILES (Q1, Q2, Q3) ---
st.markdown(
    f'<div class="section-title">Comparación 2026 frente a cuartiles históricos (Q1, Q2, Q3) — {patologia}</div>',
    unsafe_allow_html=True
)

clasif_serie = datos_2026["Clasificacion"].fillna("").astype(str).str.lower()
cnt_exito = int(clasif_serie.str.contains("éxito|exito").sum())
cnt_seguridad = int(clasif_serie.str.contains("seguridad").sum())
cnt_alarma = int(clasif_serie.str.contains("alarma").sum())
cnt_epidemia = int(clasif_serie.str.contains("epidemia").sum())

z1, z2, z3, z4 = st.columns(4)
with z1:
    st.markdown(f"""
    <div class="zona-card" style="border-left-color: #22C55E;">
        <div class="zona-card-label">Semanas en Éxito</div>
        <div class="zona-card-num">{cnt_exito}</div>
    </div>
    """, unsafe_allow_html=True)
with z2:
    st.markdown(f"""
    <div class="zona-card" style="border-left-color: #EAB308;">
        <div class="zona-card-label">Semanas en Seguridad</div>
        <div class="zona-card-num">{cnt_seguridad}</div>
    </div>
    """, unsafe_allow_html=True)
with z3:
    st.markdown(f"""
    <div class="zona-card" style="border-left-color: #F97316;">
        <div class="zona-card-label">Semanas en Alarma</div>
        <div class="zona-card-num">{cnt_alarma}</div>
    </div>
    """, unsafe_allow_html=True)
with z4:
    st.markdown(f"""
    <div class="zona-card" style="border-left-color: #EF4444;">
        <div class="zona-card-label">Semanas en Epidemia</div>
        <div class="zona-card-num">{cnt_epidemia}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 0.65rem;'></div>", unsafe_allow_html=True)

# Preparar tabla de cuartiles (sin 'None' en semanas aún no reportadas y fila pintada según comportamiento)
df_cuartiles_base = datos[["Semana", "Casos_Actuales", "Q1", "Q2", "Q3", "Clasificacion"]].copy()
df_cuartiles_base["Clasificacion_Limpia"] = df_cuartiles_base.apply(
    lambda r: "—" if pd.isna(r["Casos_Actuales"]) else r["Clasificacion"],
    axis=1
)

tabla_cuartiles = pd.DataFrame({
    "Semana EP": df_cuartiles_base["Semana"].astype(int),
    "Casos 2026": df_cuartiles_base["Casos_Actuales"].apply(lambda v: "" if pd.isna(v) else int(round(v))),
    "Q1": df_cuartiles_base["Q1"].apply(lambda v: "" if pd.isna(v) else int(round(v))),
    "Q2": df_cuartiles_base["Q2"].apply(lambda v: "" if pd.isna(v) else int(round(v))),
    "Q3": df_cuartiles_base["Q3"].apply(lambda v: "" if pd.isna(v) else int(round(v))),
    "Clasificación": df_cuartiles_base["Clasificacion_Limpia"]
})

def _pintar_fila_epidemiologica(row):
    if row["Casos 2026"] == "" or pd.isna(row["Casos 2026"]):
        return ["background-color: #FFFFFF; color: #475569;" for _ in row]

    estado = str(row["Clasificación"]).lower()
    if "epidemia" in estado:
        bg = "#EF9A9A"  # Zona Epidemia
    elif "alarma" in estado:
        bg = "#FFB65C"  # Zona Alarma
    elif "seguridad" in estado:
        bg = "#F5DF72"  # Zona Seguridad
    elif "éxito" in estado or "exito" in estado:
        bg = "#81C995"  # Zona Éxito
    else:
        bg = "#FFFFFF"

    return [f"background-color: {bg}; color: #0F172A; font-weight: 600;" for _ in row]

tabla_estilizada = tabla_cuartiles.style.apply(_pintar_fila_epidemiologica, axis=1)

st.dataframe(
    tabla_estilizada,
    use_container_width=True,
    hide_index=True,
    height=330
)

# --- 4. DESCARGA DE DATOS FILTRADOS (CSV Y EXCEL) ---
st.markdown('<div class="section-title">Exportar datos filtrados</div>', unsafe_allow_html=True)

nombre_base = f"{codigo_pat or 'canal'}_SE{rango_semanas[0]:02d}_a_SE{rango_semanas[1]:02d}_2026"
csv_bytes = tabla_cuartiles.to_csv(index=False).encode("utf-8-sig")

buffer_excel = io.BytesIO()
with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
    tabla_cuartiles.to_excel(writer, index=False, sheet_name="Datos_Filtrados")
excel_bytes = buffer_excel.getvalue()

d1, d2, _ = st.columns([1, 1, 2])
with d1:
    st.download_button(
        label="Descargar CSV",
        data=csv_bytes,
        file_name=f"{nombre_base}.csv",
        mime="text/csv",
        use_container_width=True
    )
with d2:
    st.download_button(
        label="Descargar Excel (.xlsx)",
        data=excel_bytes,
        file_name=f"{nombre_base}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )