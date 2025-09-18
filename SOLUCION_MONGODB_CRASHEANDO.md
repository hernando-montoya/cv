# 🚨 SOLUCIÓN: MongoDB Container Crasheando

## 📋 PROBLEMA IDENTIFICADO
- ✅ MongoDB inicia y expone puerto 27017
- ❌ Después de unos segundos el contenedor desaparece de `docker ps`
- ❌ El contenedor se está **CRASHEANDO/SALIENDO** automáticamente

## 🔍 PASO 1: DIAGNÓSTICO COMPLETO

### A) Ejecutar Script de Diagnóstico
En tu servidor, ejecuta:
```bash
chmod +x /app/debug_mongodb_server.sh
./app/debug_mongodb_server.sh
```

### B) Verificación Manual Rápida
```bash
# Ver contenedores activos
docker ps

# Ver TODOS los contenedores (incluyendo detenidos)
docker ps -a

# Ver logs del contenedor MongoDB
docker logs cv_mongodb

# Ver eventos recientes
docker events --since 10m | grep mongodb
```

## 🎯 POSIBLES CAUSAS Y SOLUCIONES

### CAUSA 1: Problemas de Permisos en Volúmenes
**Síntomas**: Error `permission denied` en logs
**Solución**:
```bash
# Limpiar volúmenes existentes
docker volume prune -f

# Usar stack sin volúmenes persistentes (temporal)
```
**Stack**: `portainer-mongodb-simple-fix.yml`

### CAUSA 2: Recursos Insuficientes (Memoria)
**Síntomas**: Container killed por OOM (Out of Memory)
**Solución**: Stack con límites de memoria
**Stack**: `portainer-mongodb-crash-fixed.yml`

### CAUSA 3: Conflicto de Puertos o Configuración
**Síntomas**: Error `port already in use` o configuración inválida
**Solución**:
```bash
# Verificar puertos ocupados
netstat -tlnp | grep :27017

# Matar procesos en puerto 27017 si existen
sudo lsof -ti:27017 | xargs sudo kill -9
```

### CAUSA 4: Volúmenes Corruptos
**Síntomas**: MongoDB no puede inicializar base de datos
**Solución**:
```bash
# Eliminar volúmenes específicos
docker volume rm $(docker volume ls -q | grep mongodb)
docker volume rm $(docker volume ls -q | grep cv)
```

## 🚀 SOLUCIONES PASO A PASO

### SOLUCIÓN A: Stack Simplificado (Recomendado para debugging)

1. **Eliminar stack actual** en Portainer
2. **Limpiar volúmenes**:
   ```bash
   docker volume prune -f
   ```
3. **Crear nuevo stack** con contenido de: `/app/portainer-mongodb-simple-fix.yml`
4. **Deploy** y verificar que MongoDB NO crashee

### SOLUCIÓN B: Stack Robusto (Para producción)

1. **Preparar directorios** en el servidor:
   ```bash
   sudo mkdir -p /opt/cv-app/{mongodb-data,mongodb-config}
   sudo chown -R 999:999 /opt/cv-app/
   sudo chmod -R 755 /opt/cv-app/
   ```
2. **Usar stack**: `/app/portainer-mongodb-crash-fixed.yml`

### SOLUCIÓN C: MongoDB Sin Autenticación (Emergencia)

Si todo falla, usar MongoDB sin auth temporalmente:

```yaml
mongodb:
  image: mongo:5.0
  container_name: cv_mongodb
  restart: unless-stopped
  ports:
    - "27017:27017"
  networks:
    - cv_network
  # SIN environment de autenticación
  command: mongod --bind_ip_all --noauth
```

## 🧪 VERIFICACIÓN DE SOLUCIÓN

### Después del deploy, verificar:

```bash
# 1. Contenedor corriendo por más de 1 minuto
sleep 60 && docker ps | grep mongodb

# 2. Logs sin errores
docker logs cv_mongodb

# 3. Puerto accesible
telnet localhost 27017

# 4. Conexión MongoDB funcional
echo "db.ping()" | mongosh localhost:27017 --quiet
```

### Resultado esperado:
```
✅ cv_mongodb container RUNNING por >1 minuto
✅ Logs sin errores de crash
✅ Puerto 27017 responde
✅ MongoDB acepta conexiones
```

## 📋 ARCHIVOS DE SOLUCIÓN

### Stacks Disponibles:
1. `/app/portainer-mongodb-simple-fix.yml` ← **Sin volúmenes persistentes**
2. `/app/portainer-mongodb-crash-fixed.yml` ← **Configuración robusta**
3. `/app/debug_mongodb_server.sh` ← **Script de diagnóstico**

### Elección de Stack:
- **Para debugging**: `portainer-mongodb-simple-fix.yml`
- **Para producción**: `portainer-mongodb-crash-fixed.yml`

## 🆘 SI AÚN CRASHEA

### Diagnóstico Avanzado:
```bash
# Monitorear en tiempo real
docker logs -f cv_mongodb &
docker stats cv_mongodb

# Ejecutar MongoDB manualmente para debug
docker run -it --rm mongo:5.0 mongod --help
```

### Últimos Recursos:
1. **Cambiar imagen**: `mongo:4.4` (más estable que 5.0)
2. **Usar MongoDB managed**: MongoDB Atlas u otro servicio
3. **Alternar a PostgreSQL**: Cambiar completamente de DB

## 🎯 RESULTADO FINAL ESPERADO

Una vez solucionado:
- ✅ `docker ps` muestra `cv_mongodb` corriendo estable
- ✅ MongoDB responde en puerto 27017
- ✅ Backend puede conectar a MongoDB
- ✅ Frontend carga en puerto 8006
- ✅ Sistema import/export funcional