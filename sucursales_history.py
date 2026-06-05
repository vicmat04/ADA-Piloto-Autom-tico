import sqlite3
import pandas as pd
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
import logging

DB_NAME = 'historial_sucursales.db'

def init_db():
    """Inicializa la base de datos si no existe."""
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_reporte TEXT,
                regional TEXT,
                sucursal TEXT,
                dias_sin_sinc INTEGER,
                observacion TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error inicializando DB historial: {e}")

def registrar_historial(df_incidentes, regional):
    """
    Registra los datos del reporte actual en el histórico.
    df_incidentes: DataFrame con columnas ['Carpeta', 'Días sin Sincronizar', 'Observación', ...]
    """
    if df_incidentes.empty:
        return

    init_db()
    
    try:
        conn = sqlite3.connect(DB_NAME)
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')
        
        dados_a_insertar = []
        
        for _, row in df_incidentes.iterrows():
            sucursal = row.get('Carpeta', 'Desconocida')
            dias_val = row.get('Días sin Sincronizar', 0)
            
            # Convertir a int de forma segura
            try:
                # Si es string, limpiamos posibles caracteres no numéricos si los hubiera, aunque suele ser limpio
                dias_int = int(pd.to_numeric(dias_val, errors='coerce'))
                if pd.isna(dias_int): dias_int = 0
            except:
                dias_int = 0
                
            obs = row.get('Observación', '')
            
            dados_a_insertar.append((fecha_hoy, regional, sucursal, dias_int, obs))
            
        c = conn.cursor()
        c.executemany('INSERT INTO historial (fecha_reporte, regional, sucursal, dias_sin_sinc, observacion) VALUES (?, ?, ?, ?, ?)', dados_a_insertar)
        conn.commit()
        conn.close()
        logging.info(f"Historial registrado para {len(dados_a_insertar)} registros de {regional}")
    except Exception as e:
        logging.error(f"Error registrando historial: {e}")

def obtener_estadisticas():
    """Obtiene estadísticas de sucursales excluyendo las cerradas definitivamente."""
    init_db()
    try:
        conn = sqlite3.connect(DB_NAME)
        
        # Filtramos 'CERRADA DEFINITIVAMENTE'
        query = "SELECT * FROM historial WHERE observacion != 'CERRADA DEFINITIVAMENTE'"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return pd.DataFrame()
            
        # Agrupamos por sucursal y regional
        # Calculamos:
        # - Promedio de días sin sincronizar
        # - Veces que ha aparecido en reportes (frecuencia de incidencia)
        # - Máximo de días sin sincronizar registrado
        resumen = df.groupby(['sucursal', 'regional']).agg(
            promedio_dias=('dias_sin_sinc', 'mean'),
            veces_reportada=('id', 'count'),
            max_dias=('dias_sin_sinc', 'max')
        ).reset_index()
        
        # Ordenamos por las que tienen mayor problema (mayor promedio de días)
        resumen = resumen.sort_values(by='promedio_dias', ascending=False)
        
        # Formato
        resumen['promedio_dias'] = resumen['promedio_dias'].round(1)
        
        return resumen
    except Exception as e:
        logging.error(f"Error obteniendo estadísticas: {e}")
        return pd.DataFrame()

class HistorialWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Historial de Sincronización de Sucursales")
        self.geometry("1000x600")
        
        # Centrar ventana
        try:
            self.state('normal') # Asegurar que no esté minimizada
        except: pass
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Título
        lbl = ttk.Label(self, text="Análisis Histórico de Sucursales", font=("Helvetica", 16, "bold"), bootstyle="primary")
        lbl.pack(pady=(20, 5))
        
        lbl_sub = ttk.Label(self, text="(Se excluyen sucursales 'CERRADA DEFINITIVAMENTE')", font=("Helvetica", 10), bootstyle="secondary")
        lbl_sub.pack(pady=(0, 15))
        
        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5, fill=X, padx=20)
        
        btn_refresh = ttk.Button(btn_frame, text="Actualizar Datos", command=self.load_data, bootstyle="info-outline")
        btn_refresh.pack(side=LEFT)
        
        ttk.Button(btn_frame, text="Cerrar", command=self.destroy, bootstyle="danger-outline").pack(side=RIGHT)
        
        # Tabla Principal
        self.tree_frame = ttk.Frame(self, padding=10)
        self.tree_frame.pack(fill=BOTH, expand=True)
        
        cols = ('sucursal', 'regional', 'promedio_dias', 'veces_reportada', 'max_dias')
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, show='headings', bootstyle="info")
        
        headings = {
            'sucursal': 'Sucursal / Carpeta',
            'regional': 'Regional',
            'promedio_dias': 'Promedio Días Sin Sinc.',
            'veces_reportada': 'Apariciones en Reportes',
            'max_dias': 'Máx. Días Registrado'
        }
        
        for col in cols:
            self.tree.heading(col, text=headings[col], command=lambda c=col: self.sort_treeview(self.tree, c, False))
            self.tree.column(col, anchor=CENTER)
            
        self.tree.column('sucursal', anchor=W, width=300)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        sb = ttk.Scrollbar(self.tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side=RIGHT, fill=Y)
        
        self.tree.tag_configure('high_risk', background='#5e2129') # Rojizo oscuro para casos graves
        
    def load_data(self):
        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        resumen = obtener_estadisticas()
        
        if resumen.empty:
            return

        for _, row in resumen.iterrows():
            vals = (row['sucursal'], row['regional'], row['promedio_dias'], row['veces_reportada'], row['max_dias'])
            
            # Highlight si el promedio es alto (> 15 días)
            tags = ()
            if row['promedio_dias'] > 15:
                tags = ('high_risk',)
                
            self.tree.insert('', END, values=vals, tags=tags)

    def sort_treeview(self, tree, col, reverse):
        # Función de ordenamiento igual a la app principal
        data = [(tree.set(item, col), item) for item in tree.get_children('')]
        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except (ValueError, TypeError):
            data.sort(key=lambda t: str(t[0]), reverse=reverse)
            
        for index, (val, item) in enumerate(data):
            tree.move(item, '', index)
            
        tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))

def mostrar_ventana_historial(output_parent):
    # Crea la ventana como hija de output_parent
    HistorialWindow(output_parent)
