#!/usr/bin/env python3
"""
Monitor de MongoDB - Detecta cuando el puerto deja de estar disponible
"""

import time
import socket
import subprocess
import json
from datetime import datetime

def check_port(host, port, timeout=3):
    """Verificar si un puerto está accesible"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_container_status():
    """Obtener estado detallado del contenedor MongoDB"""
    try:
        # Estado básico
        result = subprocess.run(['docker', 'ps', '--filter', 'name=cv_mongodb', '--format', 'json'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0 or not result.stdout.strip():
            return {"status": "not_running", "details": "Container not found"}
        
        container_info = json.loads(result.stdout.strip())
        
        # Puertos expuestos
        port_result = subprocess.run(['docker', 'port', 'cv_mongodb'], 
                                   capture_output=True, text=True, timeout=5)
        
        ports = port_result.stdout.strip() if port_result.returncode == 0 else "No ports exposed"
        
        # Health check
        inspect_result = subprocess.run(['docker', 'inspect', 'cv_mongodb'], 
                                      capture_output=True, text=True, timeout=5)
        
        health_status = "unknown"
        restart_count = "unknown"
        
        if inspect_result.returncode == 0:
            inspect_data = json.loads(inspect_result.stdout)[0]
            restart_count = inspect_data.get('RestartCount', 'unknown')
            
            health = inspect_data.get('State', {}).get('Health', {})
            health_status = health.get('Status', 'no-health-check')
        
        return {
            "status": "running",
            "name": container_info.get('Names', 'unknown'),
            "state": container_info.get('State', 'unknown'),
            "ports": ports,
            "restart_count": restart_count,
            "health": health_status,
            "created": container_info.get('CreatedAt', 'unknown')
        }
        
    except Exception as e:
        return {"status": "error", "details": str(e)}

def log_event(message):
    """Log con timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    print("🔍 MONITOR DE MONGODB - Detectando cuando el puerto se desconecta")
    print("=" * 70)
    print("Presiona Ctrl+C para parar")
    print()
    
    consecutive_failures = 0
    last_status = None
    check_interval = 10  # segundos
    
    try:
        while True:
            # Check conectividad
            port_accessible = check_port('localhost', 27017)
            container_status = get_container_status()
            
            current_status = {
                "port_accessible": port_accessible,
                "container_running": container_status.get("status") == "running"
            }
            
            # Solo log si hay cambios
            if current_status != last_status:
                log_event("=" * 50)
                log_event(f"🔌 Puerto 27017 accesible: {'✅ SÍ' if port_accessible else '❌ NO'}")
                log_event(f"📦 Contenedor corriendo: {'✅ SÍ' if current_status['container_running'] else '❌ NO'}")
                
                if container_status.get("status") == "running":
                    log_event(f"   📋 Puertos: {container_status['ports']}")
                    log_event(f"   🔄 Reinicios: {container_status['restart_count']}")
                    log_event(f"   💊 Health: {container_status['health']}")
                
                # Si perdimos el puerto pero el contenedor sigue corriendo
                if not port_accessible and current_status['container_running']:
                    consecutive_failures += 1
                    log_event(f"🚨 PROBLEMA DETECTADO: Puerto no accesible pero contenedor corriendo (#{consecutive_failures})")
                    
                    if consecutive_failures >= 3:
                        log_event("🔧 INTENTANDO SOLUCIÓN: Reiniciando contenedor...")
                        try:
                            subprocess.run(['docker', 'restart', 'cv_mongodb'], 
                                         timeout=30, check=True)
                            log_event("✅ Contenedor reiniciado")
                            consecutive_failures = 0
                        except Exception as e:
                            log_event(f"❌ Error reiniciando: {e}")
                
                # Si recuperamos la conexión
                if port_accessible and last_status and not last_status["port_accessible"]:
                    log_event("🎉 CONEXIÓN RECUPERADA")
                    consecutive_failures = 0
                
                last_status = current_status
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        log_event("🛑 Monitor detenido por el usuario")
    except Exception as e:
        log_event(f"💥 Error inesperado: {e}")

if __name__ == "__main__":
    main()