# 🐳 CV App - Stack Simple para Portainer

## 📋 Información del Stack

**Archivo**: `portainer-simple.yml`

**Puertos configurados**:
- ✅ Frontend: **Puerto 8006**
- ✅ Backend: **Puerto 8007** 
- ✅ MongoDB: Interno (no expuesto)

## 🚀 Despliegue en Portainer

### Paso 1: Subir el Stack
1. Accede a tu Portainer
2. Ve a **Stacks** → **Add Stack**  
3. Nombre del stack: `cv-app`
4. Pega el contenido de `portainer-simple.yml`
5. Click en **Deploy the stack**

### Paso 2: Configuración NPM (Manual)
Configura en tu Nginx Proxy Manager:

**Para el Frontend (Puerto 8006)**:
- Domain: `tu-dominio.com`
- Scheme: `http`
- Forward Hostname: `IP_DE_TU_SERVER`
- Forward Port: `8006`

**Para el Backend API (Puerto 8007)**:
- Domain: `api.tu-dominio.com` 
- Scheme: `http`
- Forward Hostname: `IP_DE_TU_SERVER`
- Forward Port: `8007`

### Paso 3: Variables de Entorno (Opcional)
Si necesitas cambiar configuraciones, edita el stack:

```yaml
environment:
  MONGO_INITDB_ROOT_USERNAME: admin           # Usuario MongoDB
  MONGO_INITDB_ROOT_PASSWORD: securepassword123  # Contraseña MongoDB
  DB_NAME: cv_database                        # Nombre de la base de datos
  JWT_SECRET: tu_jwt_secret_aqui              # Secreto JWT
```

## ⚡ Características

✅ **Inicialización automática**: Los datos del CV se cargan automáticamente  
✅ **Sin Health Checks problemáticos**: Eliminados para evitar errores  
✅ **Configuración simplificada**: Sin redes externas, solo comunicación interna  
✅ **Recursos optimizados**: Límites de memoria configurados  
✅ **Persistencia de datos**: MongoDB con volúmenes persistentes  

## 🔍 Verificación del Despliegue

1. **Frontend**: `http://tu-servidor:8006`
2. **Backend API**: `http://tu-servidor:8007/api/`
3. **Admin Panel**: `http://tu-servidor:8006/admin`

**Credenciales por defecto**:
- Usuario: `admin`
- Contraseña: `password123`

## 📝 Contenedores Incluidos

1. **cv_mongodb**: Base de datos MongoDB
2. **cv_backend**: API FastAPI en puerto 8007
3. **cv_frontend**: Aplicación React en puerto 8006  
4. **cv_data_init**: Inicialización automática de datos (se ejecuta una vez)

## 🛠️ Mantenimiento

**Reiniciar servicios**:
```bash
# En Portainer, ve al stack y click en "Restart"
```

**Ver logs**:
```bash  
# En Portainer: Containers → Seleccionar contenedor → Logs
```

**Actualizar aplicación**:
1. Rebuild images en Portainer
2. Restart stack

## ⚠️ Notas Importantes

- El contenedor `cv_data_init` se ejecuta UNA sola vez para inicializar datos
- Los datos persisten en volúmenes Docker incluso si reinicias el stack
- NPM debe configurarse manualmente según tus dominios
- Los puertos 8006 y 8007 deben estar libres en tu servidor

## 🆘 Solución de Problemas

**Si el backend no responde**:
- Verifica que MongoDB esté running
- Espera 30-60 segundos después del deploy inicial
- Revisa logs del contenedor `cv_backend`

**Si no aparecen datos**:  
- Verifica logs de `cv_data_init`
- El contenedor debe mostrar "✅ Aplicación CV lista para usar!"

**Si hay problemas de conexión**:
- Verifica que los puertos 8006 y 8007 no estén ocupados
- Reinicia el stack completo si es necesario