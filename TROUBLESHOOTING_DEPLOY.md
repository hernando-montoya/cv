# 🛠️ TROUBLESHOOTING - Deploy de Un Solo Contenedor

## 🚨 PROBLEMAS COMUNES Y SOLUCIONES

### ❌ **Error: "yarn.lock not found"**

**Causa**: Dockerfile no puede encontrar yarn.lock durante el build

**✅ Solución**:
1. **Usar Dockerfile.prebuilt** (recomendado):
   - Ya incluido en `portainer-single-app.yml`
   - Frontend pre-compilado, sin dependencias Node.js
   
2. **O compilar frontend antes**:
   ```bash
   cd frontend
   yarn build
   cd ..
   # Luego deploy con Dockerfile.prebuilt
   ```

---

### ❌ **Error: "frontend/build directory not found"**

**Causa**: Frontend no está compilado

**✅ Solución**:
```bash
# Ejecutar script de preparación
./prepare_for_deploy.sh

# O manualmente:
cd frontend
yarn install
yarn build
cd ..
```

---

### ❌ **Error: "Container fails to start"**

**Causa**: Problema en el backend o configuración

**✅ Solución**:
1. **Ver logs del contenedor**:
   ```bash
   docker logs cv_app_all_in_one
   ```

2. **Health check**:
   ```bash
   curl http://tu-servidor:8000/health
   ```

3. **Verificar puerto**:
   - Asegurar que puerto 8000 esté libre
   - Cambiar puerto en stack si es necesario:
   ```yaml
   ports:
     - "9000:8000"  # Usar puerto 9000 externamente
   ```

---

### ❌ **Error: "Repository access failed"**

**Causa**: Portainer no puede acceder al repositorio

**✅ Soluciones**:
1. **Repositorio público**: Asegurar que sea público
2. **Usar editor web**: Copiar contenido del YML directamente
3. **Subir archivos**: Usar upload de archivos en Portainer

---

### ❌ **Error: "Build context too large"**

**Causa**: Directorio incluye archivos innecesarios

**✅ Solución**:
Crear `.dockerignore`:
```
node_modules
.git
*.log
.env.local
coverage
build
.DS_Store
```

---

### ❌ **Frontend carga pero APIs no funcionan**

**Causa**: Problemas de ruteo interno

**✅ Verificaciones**:
1. **Health check**:
   ```bash
   curl http://tu-servidor:8000/health
   # Debe devolver: {"status":"healthy","storage":"connected"}
   ```

2. **API test**:
   ```bash
   curl http://tu-servidor:8000/api/content/
   # Debe devolver JSON con datos del CV
   ```

3. **Logs backend**:
   ```bash
   docker logs cv_app_all_in_one | grep -i error
   ```

---

### ❌ **Admin panel no carga**

**Causa**: Ruteo de frontend o credenciales

**✅ Solución**:
1. **Verificar URL**: `http://tu-servidor:8000/admin`
2. **Credenciales por defecto**:
   - Usuario: `admin`
   - Password: `password123`
3. **Check responsive**: Probar en desktop, no mobile

---

### ❌ **Datos no se persisten**

**Causa**: Volumen no configurado correctamente

**✅ Solución**:
1. **Verificar volumen en stack**:
   ```yaml
   volumes:
     - cv_data:/app/data
   ```

2. **Check datos**:
   ```bash
   docker exec cv_app_all_in_one ls -la /app/data/
   # Debe mostrar cv_content.json
   ```

---

## 🔄 **RESET COMPLETO**

Si nada funciona, reset completo:

### 1. **Limpiar Portainer**:
- Eliminar stack actual
- Eliminar volúmenes: `Volumes → cv_data → Remove`

### 2. **Preparar desde cero**:
```bash
# Limpiar y preparar
cd /app
rm -rf frontend/build
./prepare_for_deploy.sh
```

### 3. **Deploy nuevo**:
- Portainer → Add Stack
- Usar `portainer-single-app.yml`
- Deploy

---

## 🧪 **TESTING LOCAL**

Antes de deploy en Portainer, probar localmente:

### **Opción 1: Docker Compose**
```bash
docker-compose -f docker-compose.single.yml up --build
```

### **Opción 2: Docker directo**
```bash
docker build -f Dockerfile.prebuilt -t cv-app .
docker run -p 8000:8000 cv-app
```

### **Verificar funcionamiento**:
- Frontend: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`
- Health: `http://localhost:8000/health`
- API: `http://localhost:8000/api/content/`

---

## 📋 **CHECKLIST PRE-DEPLOY**

Antes de deploy, verificar:
- ✅ `frontend/build/` existe y tiene archivos
- ✅ `backend/server.py` existe
- ✅ `backend/json_storage.py` existe
- ✅ `backend/requirements.txt` existe
- ✅ `Dockerfile.prebuilt` existe
- ✅ `portainer-single-app.yml` existe
- ✅ Puerto 8000 está libre en el servidor

---

## 🆘 **SOPORTE ADICIONAL**

### **Scripts útiles**:
- `./prepare_for_deploy.sh` - Preparar aplicación
- `./test_single_container.sh` - Testing automático

### **Archivos importantes**:
- `GUIA_UN_SOLO_CONTENEDOR.md` - Guía completa
- `RESUMEN_ARCHIVOS_IMPORTANTES.md` - Índice archivos

### **Logs importantes**:
```bash
# Logs del contenedor
docker logs cv_app_all_in_one

# Logs en tiempo real
docker logs -f cv_app_all_in_one

# Solo errores
docker logs cv_app_all_in_one 2>&1 | grep -i error
```