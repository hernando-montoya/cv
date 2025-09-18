#!/usr/bin/env python3
"""
Diagnosticar por qué el contenedor MongoDB se está crasheando
"""

import subprocess
import json
import time
import sys

def run_command(cmd, timeout=10):
    """Ejecutar comando con timeout"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timeout"
    except Exception as e:
        return -1, "", str(e)

def check_container_logs(container_name):
    """Obtener logs del contenedor MongoDB"""
    print(f"🔍 OBTENIENDO LOGS DE {container_name}")
    print("-" * 50)
    
    # Intentar obtener logs del contenedor (aunque haya salido)
    cmd = f"docker logs {container_name}"
    returncode, stdout, stderr = run_command(cmd, timeout=15)
    
    if returncode == 0:
        print("📋 LOGS DEL CONTENEDOR:")
        print(stdout)
        if stderr:
            print("\n❌ STDERR:")
            print(stderr)
    else:
        print(f"❌ No se pudieron obtener logs: {stderr}")
    
    return stdout, stderr

def check_container_status():
    """Verificar estado de todos los contenedores"""
    print("🔍 ESTADO DE CONTENEDORES")
    print("-" * 40)
    
    # Contenedores en ejecución
    cmd = "docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'"
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print("✅ CONTENEDORES ACTIVOS:")
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")
    
    print()
    
    # Todos los contenedores (incluyendo detenidos)
    cmd = "docker ps -a --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'"
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print("📋 TODOS LOS CONTENEDORES:")
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")

def check_docker_events():
    """Verificar eventos recientes de Docker"""
    print("🔍 EVENTOS DOCKER RECIENTES")
    print("-" * 40)
    
    cmd = "docker events --since 10m --until now"
    returncode, stdout, stderr = run_command(cmd, timeout=5)
    
    if returncode == 0:
        lines = stdout.split('\n')
        mongodb_events = [line for line in lines if 'mongodb' in line.lower() or 'cv_mongodb' in line.lower()]
        
        if mongodb_events:
            print("📋 EVENTOS DE MONGODB:")
            for event in mongodb_events[-10:]:  # Últimos 10 eventos
                print(event)
        else:
            print("ℹ️ No hay eventos recientes de MongoDB")
    else:
        print(f"❌ Error obteniendo eventos: {stderr}")

def check_disk_space():
    """Verificar espacio en disco"""
    print("🔍 ESPACIO EN DISCO")
    print("-" * 30)
    
    cmd = "df -h"
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print("💾 ESPACIO DISPONIBLE:")
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")

def check_memory_usage():
    """Verificar uso de memoria"""
    print("🔍 USO DE MEMORIA")
    print("-" * 25)
    
    cmd = "free -h"
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print("🧠 MEMORIA:")
        print(stdout)
    else:
        print(f"❌ Error: {stderr}")

def inspect_container(container_name):
    """Inspeccionar configuración del contenedor"""
    print(f"🔍 INSPECCIÓN DE {container_name}")
    print("-" * 50)
    
    cmd = f"docker inspect {container_name}"
    returncode, stdout, stderr = run_command(cmd, timeout=15)
    
    if returncode == 0:
        try:
            data = json.loads(stdout)[0]
            
            # Estado del contenedor
            state = data.get('State', {})
            print(f"📊 ESTADO:")
            print(f"  Status: {state.get('Status')}")
            print(f"  Running: {state.get('Running')}")
            print(f"  ExitCode: {state.get('ExitCode')}")
            print(f"  Error: {state.get('Error', 'None')}")
            
            if state.get('FinishedAt'):
                print(f"  FinishedAt: {state.get('FinishedAt')}")
            
            # Configuración de restart
            restart_policy = data.get('RestartPolicy', {})
            print(f"\n🔄 RESTART POLICY:")
            print(f"  Name: {restart_policy.get('Name')}")
            print(f"  MaximumRetryCount: {restart_policy.get('MaximumRetryCount')}")
            
            # Mounts/Volúmenes
            mounts = data.get('Mounts', [])
            print(f"\n💾 VOLÚMENES:")
            for mount in mounts:
                print(f"  {mount.get('Source')} -> {mount.get('Destination')}")
            
        except json.JSONDecodeError:
            print("❌ Error parseando JSON de inspect")
    else:
        print(f"❌ No se pudo inspeccionar contenedor: {stderr}")

def main():
    print("🚨 DIAGNÓSTICO: MONGODB CONTAINER CRASHEANDO")
    print("=" * 60)
    
    # 1. Estado general
    check_container_status()
    print()
    
    # 2. Recursos del sistema
    check_disk_space()
    print()
    check_memory_usage()
    print()
    
    # 3. Eventos de Docker
    check_docker_events()
    print()
    
    # 4. Logs del contenedor MongoDB
    containers_to_check = ['cv_mongodb', 'mongodb']
    
    for container in containers_to_check:
        print(f"\n{'='*60}")
        logs_out, logs_err = check_container_logs(container)
        
        # 5. Inspeccionar configuración
        inspect_container(container)
        
        if logs_out or logs_err:
            break
    
    print(f"\n🎯 POSIBLES CAUSAS DEL CRASH:")
    print("1. Permisos en volúmenes de datos")
    print("2. Configuración incorrecta de MongoDB")
    print("3. Conflicto de puertos") 
    print("4. Recursos insuficientes (memoria/disco)")
    print("5. Variables de entorno incorrectas")
    print("6. Usuario/grupo incorrecto para MongoDB")

if __name__ == "__main__":
    main()