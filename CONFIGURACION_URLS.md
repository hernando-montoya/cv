# 🔧 Configuración de URLs - CV App

## 📍 URLs después del despliegue

### Configuración Interna (Docker)
- Frontend → Backend: `http://backend:8001` (comunicación entre contenedores)
- MongoDB: `mongodb://admin:securepassword123@mongodb:27017/cv_database`

### Configuración Externa (NPM)
- Frontend público: `http://tu-servidor:8006`
- Backend API público: `http://tu-servidor:8007`

## ⚙️ Si necesitas cambiar la URL del Backend

### Opción 1: Actualizar después del despliegue
1. En Portainer, ve a tu stack
2. Click en **Editor**
3. Cambia estas líneas en el servicio `frontend`:

```yaml
args:
  REACT_APP_BACKEND_URL: https://api.tu-dominio.com
environment:
  REACT_APP_BACKEND_URL: https://api.tu-dominio.com
```

4. Click **Update the stack**
5. Rebuild la imagen del frontend

### Opción 2: Configurar Variables de Entorno
Antes del despliegue, añade estas variables al stack:

```yaml
environment:
  REACT_APP_BACKEND_URL: ${BACKEND_URL:-https://api.tu-dominio.com}
```

Y en Portainer, en la sección **Environment variables**:
- `BACKEND_URL`: `https://api.tu-dominio.com`

## 🌐 Configuración NPM Recomendada

### Backend API:
- **Domain Names**: `api.tu-dominio.com`
- **Scheme**: `http`
- **Forward Hostname/IP**: `IP_DE_TU_SERVIDOR`
- **Forward Port**: `8007`
- **Block Common Exploits**: ✅
- **Access List**: Según necesites

### Frontend Web:
- **Domain Names**: `tu-dominio.com`
- **Scheme**: `http`  
- **Forward Hostname/IP**: `IP_DE_TU_SERVIDOR`
- **Forward Port**: `8006`
- **Block Common Exploits**: ✅

## 🔄 Para cambios rápidos

Si ya tienes el stack deployado y solo necesitas cambiar la URL:

1. **SSH a tu servidor**
2. **Edita la variable directamente**:
```bash
docker exec -it cv_frontend /bin/sh
# Dentro del contenedor, verifica la variable:
env | grep REACT_APP_BACKEND_URL
```

3. **O reconstruye con nueva URL**:
```bash
# En Portainer: Stack → Editor → Cambiar REACT_APP_BACKEND_URL → Update
```

## 📝 URLs por defecto en el YML

```yaml
# Comunicación interna (no cambiar):
MONGO_URL: mongodb://admin:securepassword123@mongodb:27017/cv_database

# URL del backend para el frontend (modificar según necesidad):
REACT_APP_BACKEND_URL: http://backend:8001  # Para comunicación interna Docker
# O cambiar por:
REACT_APP_BACKEND_URL: https://api.tu-dominio.com  # Para producción con NPM
```

## ⚠️ Importante

- Si usas HTTPS en NPM, cambia `http://` por `https://` en `REACT_APP_BACKEND_URL`
- El puerto interno `8001` es para comunicación entre contenedores
- Los puertos externos `8006` y `8007` son los que mapeas en NPM
- Después de cambiar URLs, siempre rebuild el frontend para aplicar cambios