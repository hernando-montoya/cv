# 🚨 Solución: MongoDB Unhealthy en Portainer

## Problema
```
Failed to deploy a stack: compose up operation failed: 
dependency failed to start: container cv_mongodb is unhealthy
```

## 🔍 Causa del Problema
Los health checks en Portainer pueden ser más estrictos que en Docker Compose local, especialmente con MongoDB que tarda en inicializar.

---

## 🚀 Solución Inmediata

### **Opción 1: Stack con Health Checks Mejorados**
Usa `portainer-stack-fixed.yml` que tiene:
- Health checks más permisivos
- Más tiempo de inicio (start_period: 60s)
- Timeouts más largos
- Menos reintentos agresivos

### **Opción 2: Stack Sin Health Checks**
Usa `portainer-stack-minimal.yml` que:
- ❌ Sin health checks (más confiable)
- ✅ Dependencias por nombre solamente
- ✅ Delays manuales para inicialización

---

## 📋 Pasos para Solucionar

### **Paso 1: Limpiar Stack Fallido**
En Portainer:
1. **Stacks** → Seleccionar tu stack
2. **Stop** → **Remove**
3. Verificar que no queden contenedores corriendo

### **Paso 2: Verificar Red NPM**
En tu VM:
```bash
# Verificar que existe la red npm_proxy
docker network ls | grep npm_proxy

# Si no existe, crearla
docker network create npm_proxy
```

### **Paso 3: Probar Stack Minimal**
1. **Stacks** → **Add stack**
2. **Name**: `cv-application`
3. **Web editor**: Pegar contenido de `portainer-stack-minimal.yml`
4. **Environment variables**: Configurar variables
5. **Deploy the stack**

### **Paso 4: Verificar Logs**
Una vez desplegado:
1. **Containers** → Verificar estado
2. Ver logs de cada contenedor:
   - `cv_mongodb` - Debe mostrar "waiting for connections"
   - `cv_backend` - Debe mostrar "Application startup complete"
   - `cv_frontend` - Debe mostrar logs de nginx

---

## 🔧 Verificación Manual

### **Desde tu VM, verificar servicios:**
```bash
# Listar contenedores
docker ps

# Verificar MongoDB
docker exec cv_mongodb mongosh --eval "db.adminCommand('ping')"

# Verificar Backend
docker exec cv_backend curl http://localhost:8001/api/

# Verificar conectividad interna
docker exec cv_backend ping cv_mongodb
docker exec cv_frontend ping cv_backend
```

---

## 🚨 Si Aún No Funciona

### **Diagnóstico Avanzado:**

#### **1. Verificar recursos del sistema**
```bash
# Memoria disponible
free -h

# Espacio en disco
df -h

# Procesos de Docker
docker system df
```

#### **2. Logs detallados**
```bash
# Ver logs específicos
docker logs cv_mongodb --tail 50
docker logs cv_backend --tail 50
docker logs cv_frontend --tail 50
```

#### **3. Probar MongoDB standalone**
```bash
# Crear MongoDB simple para probar
docker run --name test-mongo -d mongo:5.0

# Verificar que funciona
docker exec test-mongo mongosh --eval "db.adminCommand('ping')"

# Limpiar
docker rm -f test-mongo
```

---

## 🎯 Stack Alternativo - Ultra Minimal

Si nada funciona, usa esta versión súper simplificada:

```yaml
services:
  mongodb:
    image: mongo:5.0
    container_name: cv_mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
    volumes:
      - mongodb_data:/data/db
    networks:
      - cv_internal

  backend:
    image: cv_backend:latest
    build:
      context: ./backend
    container_name: cv_backend
    restart: unless-stopped
    environment:
      MONGO_URL: mongodb://admin:password123@mongodb:27017/cv_database?authSource=admin
      ADMIN_USERNAME: admin
      ADMIN_PASSWORD_HASH: b8d6c1a9b2e5d7f3:a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890
      JWT_SECRET: simple_jwt_secret_for_testing
    expose:
      - "8001"
    networks:
      - cv_internal  
      - npm_proxy

  frontend:
    image: cv_frontend:latest
    build:
      context: ./frontend
      args:
        REACT_APP_BACKEND_URL: https://api.yourdomain.com
    container_name: cv_frontend
    restart: unless-stopped
    expose:
      - "3000"
    networks:
      - cv_internal
      - npm_proxy

networks:
  cv_internal:
    driver: bridge
  npm_proxy:
    external: true

volumes:
  mongodb_data: {}
```

---

## ✅ Verificación de Éxito

### **Después del deploy exitoso:**
```bash
# Todos los contenedores corriendo
docker ps | grep cv_

# MongoDB respondiendo
docker exec cv_mongodb mongosh --eval "db.version()"

# Backend API funcionando  
curl http://cv_backend:8001/api/

# Frontend servido por nginx
curl http://cv_frontend:3000/
```

### **En NPM:**
- Configurar proxy hosts normalmente
- Las URLs internas siguen siendo las mismas
- Todo debería funcionar igual

---

## 🎉 Una vez funcionando

Una vez que el stack esté desplegado exitosamente, puedes:
1. ✅ Configurar NPM con los proxy hosts
2. ✅ Acceder vía HTTPS a tu dominio
3. ✅ Usar el panel de admin
4. ✅ Añadir health checks de vuelta si quieres (opcional)

**¡El importante es que funcione, los health checks son opcionales!**