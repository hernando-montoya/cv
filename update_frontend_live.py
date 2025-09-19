#!/usr/bin/env python3
"""
Script para actualizar el frontend directamente en el contenedor en ejecución
"""

import subprocess
import os

def update_frontend_in_container():
    print("🔄 ACTUALIZANDO FRONTEND EN CONTENEDOR EN VIVO")
    print("=" * 50)
    
    container_name = "cv_app"
    
    # Verificar que el contenedor está corriendo
    try:
        result = subprocess.run(['docker', 'ps', '--filter', f'name={container_name}', '--format', '{{.Names}}'], 
                              capture_output=True, text=True)
        if container_name not in result.stdout:
            print(f"❌ Contenedor {container_name} no encontrado")
            print("💡 Verifica el nombre del contenedor con: docker ps")
            return False
        else:
            print(f"✅ Contenedor {container_name} encontrado y corriendo")
    except Exception as e:
        print(f"❌ Error verificando contenedor: {e}")
        return False
    
    # Copiar archivos HTML al contenedor
    files_to_copy = [
        ("/app/frontend_build/index.html", "/app/frontend_build/index.html"),
        ("/app/frontend_build/admin.html", "/app/frontend_build/admin.html")
    ]
    
    for local_file, container_path in files_to_copy:
        if os.path.exists(local_file):
            try:
                cmd = ['docker', 'cp', local_file, f'{container_name}:{container_path}']
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Copiado: {os.path.basename(local_file)}")
                else:
                    print(f"❌ Error copiando {local_file}: {result.stderr}")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print(f"❌ Archivo no encontrado: {local_file}")
    
    print("\n🎉 ACTUALIZACIÓN COMPLETADA")
    print("🌐 Prueba tu CV en: http://tu-servidor:8006")
    print("🔧 Admin Panel en: http://tu-servidor:8006/admin")
    
    return True

if __name__ == "__main__":
    update_frontend_in_container()