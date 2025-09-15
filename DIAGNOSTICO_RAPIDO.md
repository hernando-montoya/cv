# 🚨 Diagnóstico Rápido - Servicios No Accesibles

## Problema: Debug dice "Todo listo" pero no puedo acceder

### 🔍 Paso 1: Verificar Estado Real
```bash
./check_containers.sh
```

Esto te mostrará:
- ✅ Estado real de contenedores
- 📋 Logs de errores
- 🔗 Conectividad interna vs externa
- 🚪 Puertos expuestos

### 🔧 Paso 2: Solución Automática
```bash
./fix_containers.sh
```

Este script:
- Para y limpia contenedores
- Verifica configuración
- Reconstruye imágenes
- Inicia servicios paso a paso
- Verifica cada servicio

### 🕵️ Paso 3: Diagnóstico Manual

#### A. Verificar que los contenedores están corriendo:
```bash
docker-compose ps
# O
docker ps
```

**Esperado**: Todos los servicios "Up" y saludables

#### B. Verificar logs por errores:
```bash
# Backend
docker logs cv_backend

# Frontend  
docker logs cv_frontend

# MongoDB
docker logs cv_mongodb
```

**Buscar**: Errores, crashes, problemas de conexión

#### C. Probar conectividad:
```bash
# Desde tu máquina
curl http://localhost:8001/api/
curl http://localhost:3000/

# Estado de puertos
netstat -tulpn | grep :3000
netstat -tulpn | grep :8001
```

## 🚨 Problemas Comunes

### 1. **Contenedores no inician**
```bash
# Ver por qué falló
docker-compose logs

# Reconstruir desde cero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### 2. **Puertos no están expuestos**
Verificar en `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8001"  # ← Debe estar presente
  frontend:
    ports:
      - "3000:3000"  # ← Debe estar presente
```

### 3. **Frontend no construye**
```bash
cd frontend
rm -rf node_modules build yarn.lock
yarn install --legacy-peer-deps
GENERATE_SOURCEMAP=false npx react-scripts build
```

### 4. **Backend no conecta a MongoDB**
```bash
# Verificar MongoDB
docker exec cv_mongodb mongosh --eval "db.adminCommand('ping')"

# Verificar string de conexión en .env
cat .env | grep MONGO_URL
```

### 5. **Variables de entorno incorrectas**
```bash
# Verificar .env
cat .env

# Debe contener:
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=securepass123
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=valor_largo_hash
JWT_SECRET=clave_muy_larga
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🎯 Verificación de Éxito

### ✅ Contenedores Saludables:
```bash
docker-compose ps
```
Resultado esperado:
```
     Name        State    Ports
cv_backend      Up       0.0.0.0:8001->8001/tcp
cv_frontend     Up       0.0.0.0:3000->3000/tcp  
cv_mongodb      Up       0.0.0.0:27017->27017/tcp
```

### ✅ Servicios Accesibles:
```bash
curl http://localhost:8001/api/
# Debería devolver: {"message": "Hello World"}

curl http://localhost:3000/
# Debería devolver HTML de React
```

### ✅ Admin Panel Funcional:
1. Ir a http://localhost:3000
2. Clic en botón "Admin"
3. Login: admin / admin2024
4. Debería abrir panel de gestión

## 🆘 Si Nada Funciona

### Limpieza Completa:
```bash
# Parar todo
docker-compose down -v

# Limpiar imágenes
docker system prune -a

# Limpiar proyecto
rm -rf frontend/node_modules frontend/build

# Empezar desde cero
./fix_containers.sh
```

### Verificar Sistema:
```bash
# Versiones
docker --version
docker-compose --version
node --version

# Recursos disponibles
docker system df
```

### Logs Detallados:
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Logs específicos con timestamps
docker logs cv_backend --timestamps
docker logs cv_frontend --timestamps
```

---

## 📞 Checklist de Solución

- [ ] `./check_containers.sh` ejecutado
- [ ] `./fix_containers.sh` ejecutado  
- [ ] Contenedores muestran estado "Up"
- [ ] Puertos 3000 y 8001 responden
- [ ] Frontend carga en navegador
- [ ] Backend responde en /api/
- [ ] Admin panel funciona

Si sigues todos estos pasos y aún no funciona, comparte:
1. Output completo de `./check_containers.sh`
2. Logs específicos de servicios que fallan
3. Tu sistema operativo y versiones de Docker

¡Vamos a solucionarlo! 🚀