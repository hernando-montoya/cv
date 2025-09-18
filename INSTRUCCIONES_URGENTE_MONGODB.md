# 🚨 INSTRUCCIONES URGENTES: MongoDB Crasheando

## ⚡ ACCIÓN INMEDIATA REQUERIDA

Tu MongoDB se está **crasheando** (no es problema de puertos). Necesitas diagnosticar **POR QUÉ** está crasheando.

### PASO 1: DIAGNÓSTICO (OBLIGATORIO)
Ejecuta en tu servidor:
```bash
# Descargar el script de diagnóstico
curl -o debug_mongodb.sh https://tu-servidor/path/debug_mongodb_server.sh
chmod +x debug_mongodb.sh
./debug_mongodb.sh
```

**O ejecutar comandos manualmente**:
```bash
# Ver estado actual
docker ps -a | grep mongodb

# Ver logs del crash
docker logs cv_mongodb

# Ver eventos Docker
docker events --since 10m | grep mongodb
```

### PASO 2: APLICAR SOLUCIÓN SEGÚN RESULTADO

#### Si ves "permission denied" en logs:
**CAUSA**: Problemas de permisos en volúmenes
**SOLUCIÓN**: Usar stack sin volúmenes persistentes
```bash
docker volume prune -f
```
**Stack a usar**: `/app/portainer-mongodb-simple-fix.yml`

#### Si ves "killed" o "out of memory":
**CAUSA**: Recursos insuficientes
**SOLUCIÓN**: Stack con límites de memoria
**Stack a usar**: `/app/portainer-mongodb-crash-fixed.yml`

#### Si ves "port already in use":
**CAUSA**: Conflicto de puertos
**SOLUCIÓN**:
```bash
sudo lsof -ti:27017 | xargs sudo kill -9
```

## 🚀 SOLUCIÓN RÁPIDA (Si tienes prisa)

### Opción Express: Stack Simplificado
1. **Portainer → Stacks → [eliminar stack actual]**
2. **Add stack** con nombre `cv-app-debug`
3. **Copiar contenido completo** de: `/app/portainer-mongodb-simple-fix.yml`
4. **Deploy**
5. **Verificar**: `docker ps` debe mostrar `cv_mongodb` corriendo por >1 minuto

### ⚠️ Importante de la Solución Express:
- ✅ MongoDB será estable
- ❌ Datos se perderán al reiniciar (están en memoria)
- 🎯 Solo para verificar que funciona

## 📋 ARCHIVOS IMPORTANTES

### Para Diagnóstico:
- `/app/debug_mongodb_server.sh` ← Script de diagnóstico
- `/app/SOLUCION_MONGODB_CRASHEANDO.md` ← Guía completa

### Para Solución:
- `/app/portainer-mongodb-simple-fix.yml` ← **Stack temporal (sin datos persistentes)**
- `/app/portainer-mongodb-crash-fixed.yml` ← **Stack robusto (con datos persistentes)**

## 🎯 OBJETIVO INMEDIATO

**Meta**: Conseguir que MongoDB **NO crashee** y se mantenga corriendo estable.

**Verificación exitosa**:
```bash
# Esperar 2 minutos y verificar
sleep 120 && docker ps | grep cv_mongodb
# Debe mostrar: cv_mongodb ... Up 2 minutes
```

## 🆘 SI NECESITAS AYUDA

**Comparte la salida de estos comandos**:
```bash
docker ps -a
docker logs cv_mongodb
docker events --since 30m | grep mongodb
```

Una vez MongoDB esté estable, podremos continuar con:
- ✅ Conectividad Backend ↔ MongoDB
- ✅ Frontend cargando correctamente
- ✅ Sistema Import/Export funcional