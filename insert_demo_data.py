import pymysql
import random

conn = pymysql.connect(host='127.0.0.1', user='root', password='', database='iconstruction', port=3306)
cur = conn.cursor()

print("=" * 60)
print("🏗️  CREANDO DATOS DE EJEMPLO PARA ICONSTRUCTION")
print("=" * 60)

# ============================================================
# 1. CREAR MATERIALES
# ============================================================
print("\n📦 Creando materiales...")
materiales = [
    ('Cemento Portland', 'kg', 5000, 500),
    ('Arena gruesa', 'm3', 150, 20),
    ('Ripio', 'm3', 200, 30),
    ('Ladrillos', 'un', 10000, 1000),
    ('Tuberías PVC', 'un', 500, 50),
    ('Cables eléctricos', 'm', 2000, 200),
    ('Acero de refuerzo', 'kg', 3000, 300),
    ('Pintura', 'lt', 800, 100),
]

for name, unit, stock, min_stock in materiales:
    try:
        cur.execute('INSERT IGNORE INTO inventory_material (name, unit, stock, min_stock) VALUES (%s, %s, %s, %s)',
                    (name, unit, stock, min_stock))
        print(f"  ✓ {name:25} - {stock} {unit}")
    except Exception as e:
        print(f"  ! {name} - {str(e)[:50]}")

conn.commit()

# ============================================================
# 2. CREAR HERRAMIENTAS
# ============================================================
print("\n🔧 Creando herramientas...")
herramientas = [
    ('Excavadora', 'EXCA001', 'disponible'),
    ('Grúa móvil', 'GRUA001', 'disponible'),
    ('Compresor', 'COMP001', 'asignada'),
    ('Sierra circular', 'SIER001', 'disponible'),
    ('Taladro industrial', 'TALD001', 'disponible'),
    ('Hormigonera', 'HORM001', 'asignada'),
    ('Andamios', 'ANDA001', 'asignada'),
    ('Carretilla elevadora', 'CARE001', 'disponible'),
]

for name, code, status in herramientas:
    try:
        cur.execute('INSERT IGNORE INTO inventory_tool (name, code, status) VALUES (%s, %s, %s)',
                    (name, code, status))
        print(f"  ✓ {name:25} ({code}) - {status}")
    except Exception as e:
        print(f"  ! {name} - {str(e)[:50]}")

conn.commit()

# ============================================================
# 3. CREAR PROYECTOS
# ============================================================
print("\n🏢 Creando proyectos...")
proyectos = [
    ('Construcción Centro Comercial Downtown', 'Proyecto de construcción de centro comercial de 5 pisos ubicado en zona céntrica. Incluye estacionamientos, locales comerciales y área de oficinas.'),
    ('Remodelación Edificio Administrativo', 'Remodelación completa del edificio administrativo. Incluye actualización de sistemas eléctricos, plomería y acabados.'),
    ('Puente Vehicular San José', 'Construcción de nuevo puente vehicular que conectará las comunas de San José y Las Condes. Largo total: 2.5 km.'),
    ('Complejo Residencial Parque del Sur', 'Desarrollo inmobiliario con 150 departamentos, áreas verdes comunes y servicios complementarios.'),
    ('Escuela Municipal Nueva Esperanza', 'Construcción de nueva infraestructura educativa con capacidad para 800 estudiantes.'),
]

for name, desc in proyectos:
    try:
        cur.execute('INSERT IGNORE INTO activities_project (name, description) VALUES (%s, %s)',
                    (name, desc))
        print(f"  ✓ {name:45}")
    except Exception as e:
        print(f"  ! {name} - {str(e)[:50]}")

conn.commit()

# ============================================================
# 4. CREAR ACTIVIDADES
# ============================================================
print("\n✅ Creando actividades para proyectos...")

# Obtener IDs de proyectos
cur.execute('SELECT id, name FROM activities_project')
proyectos_ids = cur.fetchall()

fases = ['Excavación', 'Cimentación', 'Estructura', 'Instalaciones', 'Acabados', 'Pintura']
estados = ['pendiente', 'en_progreso', 'completada']

for project_id, project_name in proyectos_ids:
    num_actividades = random.randint(3, 6)
    for i in range(num_actividades):
        status = random.choice(estados)
        if status == 'completada':
            progress = 100
        elif status == 'en_progreso':
            progress = random.randint(20, 90)
        else:
            progress = 0
        
        fase = random.choice(fases)
        name = f'Fase {i+1}: {fase}'
        description = f'Actividad {i+1} del proyecto {project_name}'
        
        try:
            cur.execute('''INSERT IGNORE INTO activities_activity 
                          (project_id, name, description, progress_percent, status) 
                          VALUES (%s, %s, %s, %s, %s)''',
                        (project_id, name, description, progress, status))
            print(f"    ✓ {name:40} ({status:12}) - {progress}%")
        except Exception as e:
            print(f"    ! {name} - {str(e)[:50]}")

conn.commit()

# ============================================================
# RESUMEN
# ============================================================
cur.execute('SELECT COUNT(*) FROM inventory_material')
mat_count = cur.fetchone()[0]
cur.execute('SELECT COUNT(*) FROM inventory_tool')
tool_count = cur.fetchone()[0]
cur.execute('SELECT COUNT(*) FROM activities_project')
proj_count = cur.fetchone()[0]
cur.execute('SELECT COUNT(*) FROM activities_activity')
act_count = cur.fetchone()[0]

print("\n" + "=" * 60)
print("✨ DATOS DE EJEMPLO CREADOS EXITOSAMENTE")
print("=" * 60)
print(f"\n📊 RESUMEN:")
print(f"  • Materiales: {mat_count}")
print(f"  • Herramientas: {tool_count}")
print(f"  • Proyectos: {proj_count}")
print(f"  • Actividades: {act_count}")
print(f"\n🌐 Accede a: http://127.0.0.1:8000/dashboard/")
print(f"👤 Usuarios de prueba: admin / bodeguero / planificador / supervisor")
print(f"🔑 Contraseña para todos: hola1234")
print(f"\n✅ ¡Sistema listo para demostración!")
print("=" * 60)

conn.close()
