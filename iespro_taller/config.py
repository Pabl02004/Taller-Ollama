import mysql.connector
import os
from pathlib import Path

def inicializar_base_de_datos():
    # Variables de entorno con fallbacks seguros basados en config.py
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "P@blomontero21")
    database = os.getenv("MYSQL_DATABASE", "iespro_taller_app")

    try:
        # 1. Conexión al servidor MySQL
        conexion = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = conexion.cursor()

        # Asegurar la existencia de la base de datos
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        cursor.execute(f"USE {database};")

        # Desactivar la verificación de FK para evitar errores de orden (Error 1824)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        print("Verificación de llaves foráneas desactivada temporalmente.")

        # Definir la ruta correcta de la carpeta sql en la raíz de iespro_taller
        base_dir = Path(__file__).resolve().parent
        ruta_sql = base_dir / "sql" / "init.sql"
        
        # Si este script corre dentro de la carpeta 'services', sube un nivel
        if base_dir.name == "services":
            ruta_sql = base_dir.parent / "sql" / "init.sql"

        if ruta_sql.exists():
            print(f"Leyendo archivo de inicialización desde: {ruta_sql}")
            with open(ruta_sql, 'r', encoding='utf-8') as f:
                # Filtrar líneas vacías y comentarios simples para no romper la ejecución
                contenido_sql = f.read()
                sentencias = contenido_sql.split(';')
                
                for sentencia in sentencias:
                    sentencia_limpia = sentencia.strip()
                    if sentencia_limpia and not sentencia_limpia.startswith('--'):
                        try:
                            cursor.execute(sentencia_limpia)
                        except mysql.connector.Error as sql_err:
                            # Muestra exactamente qué tabla o consulta falló dentro del init.sql
                            print(f"Error en sentencia: {sentencia_limpia[:50]}... -> {sql_err}")
                            raise sql_err
            print("Sentencias SQL ejecutadas con éxito.")
        else:
            print(f"Advertencia: No se encontró el archivo SQL en {ruta_sql}")

        # Reactivar la verificación de restricciones
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("Verificación de llaves foráneas reactivada.")

        conexion.commit()
        cursor.close()
        conexion.close()
        print("Base de datos inicializada correctamente.")

    except mysql.connector.Error as err:
        print(f"Error inicializando BD: {err}")
        # Asegura que si algo falla estrepitosamente, el script lo notifique al contenedor
        raise err

if __name__ == "__main__":
    inicializar_base_de_datos()