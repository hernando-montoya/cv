# 🚀 INSTRUCCIONES: Solucionar Puerto MongoDB

## 📋 PROBLEMA CONFIRMADO
✅ **MongoDB está corriendo localmente**
❌ **Puerto 27017 NO está expuesto desde Portainer al servidor**
❌ **Backend no puede conectar a MongoDB**

## 🎯 SOLUCIÓN: RE-DEPLOY DEL STACK

### PASO 1: Acceder a Portainer
1. Ve a: `http://tu-servidor:9000`
2. Login con tus credenciales
3. Ve a **Stacks** en el menú lateral

### PASO 2: Editar Stack Actual
1. Busca tu stack (probablemente llamado `cv-app` o similar)
2. Click en el **nombre del stack**
3. Click en **Editor** (botón arriba a la derecha)

### PASO 3: Aplicar Corrección
Busca esta sección en tu YAML:
```yaml
  mongodb:
    image: mongo:5.0
    container_name: cv_mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: securepassword123
      MONGO_INITDB_DATABASE: cv_database
    volumes:
      - mongodb_data:/data/db
      - mongodb_config:/data/configdb
    networks:
      - cv_network
```

**REEMPLAZALA** con esta versión corregida:
```yaml
  mongodb:
    image: mongo:5.0
    container_name: cv_mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: securepassword123
      MONGO_INITDB_DATABASE: cv_database
    ports:
      - "27017:27017"  # 🔧 ESTA LÍNEA FALTABA
    volumes:
      - mongodb_data:/data/db
      - mongodb_config:/data/configdb
    networks:
      - cv_network
```

### PASO 4: Re-Deploy
1. Click **Update the stack**
2. ✅ Marca **Re-deploy the stack**
3. Click **Update**

### PASO 5: Verificar
Después del re-deploy, espera 1-2 minutos y verifica:

#### A) Estado de Contenedores
Ve a **Containers** y confirma que todos estén **running**:
- `cv_mongodb` - running
- `cv_backend` - running  
- `cv_frontend` - running

#### B) Puerto Expuesto
En la lista de contenedores, busca `cv_mongodb` y verifica que en la columna **Ports** aparezca:
```
0.0.0.0:27017->27017/tcp
```

### PASO 6: Probar la Aplicación
1. **Frontend**: `http://tu-servidor:8006`
2. **Admin Panel**: `http://tu-servidor:8006/admin`
3. **Import/Export**: Ve al Admin Panel → pestaña **Import** y prueba importar datos

## 🔍 SI NECESITAS USAR EL STACK NUEVO COMPLETO

Como alternativa, puedes crear un stack completamente nuevo:

### Opción B: Stack Nuevo
1. En Portainer: **Stacks → Add stack**
2. Nombre: `cv-app-fixed`
3. Copia todo el contenido del archivo: `/app/portainer-mongodb-fixed.yml`
4. Pega en el editor
5. Deploy stack
6. **Importante**: Elimina el stack anterior para evitar conflictos de puertos

## ✅ RESULTADO ESPERADO

Después de la corrección:
- ✅ Frontend carga en `http://tu-servidor:8006`
- ✅ Backend accesible en `http://tu-servidor:8007`
- ✅ Admin Panel funciona correctamente
- ✅ Sistema Import/Export operativo
- ✅ MongoDB accesible desde el backend

## 🆘 SI AÚN HAY PROBLEMAS

Ejecuta estos comandos desde tu servidor para diagnosticar:

```bash
# Verificar puertos abiertos
netstat -tlnp | grep :27017
netstat -tlnp | grep :8006
netstat -tlnp | grep :8007

# Probar conectividad
telnet localhost 27017
curl http://localhost:8006
curl http://localhost:8007/health
```

El resultado esperado:
```
✅ 27017/tcp LISTENING
✅ 8006/tcp LISTENING  
✅ 8007/tcp LISTENING
✅ MongoDB conecta
✅ Frontend responde
✅ Backend responde
```