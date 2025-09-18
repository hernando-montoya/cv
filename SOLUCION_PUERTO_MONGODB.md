# 🔧 SOLUCIÓN: Puerto MongoDB No Expuesto Correctamente

## 📋 PROBLEMA IDENTIFICADO
El contenedor MongoDB en Portainer **NO está exponiendo el puerto 27017** correctamente, por eso el backend no puede conectar.

## ✅ SOLUCIÓN APLICADA

### 1. Problema en Stack Actual
- **Archivo**: `portainer-back-to-basics.yml`
- **Error**: MongoDB sin sección `ports:` 
- **Resultado**: Backend no puede conectar a MongoDB

### 2. Corrección Realizada
- ✅ Agregado: `ports: - "27017:27017"` al servicio MongoDB
- ✅ Creado: `portainer-mongodb-fixed.yml` con configuración corregida

## 📝 PASOS PARA SOLUCIONAR

### Opción A: Actualizar Stack Existente
1. Ve a **Portainer → Stacks → [tu-stack]**
2. Click **Editor**
3. Busca la sección `mongodb:`
4. Agrega estas líneas después de `environment:`:
   ```yaml
   ports:
     - "27017:27017"
   ```
5. Click **Update the stack**
6. Selecciona **Re-deploy the stack**

### Opción B: Usar Stack Corregido
1. Ve a **Portainer → Stacks → Add Stack**
2. Copia el contenido de `/app/portainer-mongodb-fixed.yml`
3. Pega en el editor
4. Deploy stack

## 🧪 VERIFICAR SOLUCIÓN

### Desde tu servidor, ejecuta:
```bash
# Probar conectividad MongoDB
telnet localhost 27017

# O con netcat
nc -zv localhost 27017

# Verificar contenedores
docker ps | grep mongodb
```

### Resultado esperado:
```
✅ localhost:27017 - Connected
✅ cv_mongodb container running
✅ Port 27017/tcp mapped to 0.0.0.0:27017
```

## 📍 ARCHIVOS CORREGIDOS
- `/app/portainer-back-to-basics.yml` ← **Corregido**
- `/app/portainer-mongodb-fixed.yml` ← **Nuevo stack completo**

## 🎯 DESPUÉS DE LA CORRECCIÓN
1. **Frontend**: http://tu-servidor:8006
2. **Backend**: http://tu-servidor:8007  
3. **MongoDB**: localhost:27017 (accesible desde host)
4. **Admin Panel**: http://tu-servidor:8006/admin
5. **Import/Export**: Debería funcionar correctamente

## ⚠️ IMPORTANTE
- El puerto 27017 ahora estará expuesto desde tu servidor
- Backend podrá conectar usando hostname `mongodb:27017`
- Sistema de import/export debería funcionar inmediatamente
- No es necesario cambiar URLs ni realizar configuraciones adicionales

## 🔍 SI AÚN NO FUNCIONA
Ejecuta el diagnóstico completo:
```bash
python3 /app/test_mongodb_port.py
```