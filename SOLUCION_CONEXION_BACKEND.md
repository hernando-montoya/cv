# 🔧 Solución: Error de Conexión Frontend → Backend

## 🚨 **Problema:**
El frontend no puede conectarse al backend, causando errores en importación e inicialización.

## 🎯 **Causa Principal:**
La variable `REACT_APP_BACKEND_URL` en `/app/frontend/.env` apunta a una URL incorrecta:
```
REACT_APP_BACKEND_URL=https://docker-cv-bridge.preview.emergentagent.com
```

## ✅ **Soluciones disponibles:**

### **🚀 Solución 1: Script Automático (RECOMENDADO)**
```bash
# Desde tu entorno donde tienes los archivos:
python3 fix_frontend_config.py
```
Este script:
- ✅ Detecta qué URL del backend funciona
- ✅ Actualiza automáticamente el .env
- ✅ Te da instrucciones para continuar

### **🔧 Solución 2: Manual**
1. **Edita `/app/frontend/.env`:**
   ```bash
   # Para Docker (comunicación interna):
   REACT_APP_BACKEND_URL=http://backend:8001
   
   # O para acceso externo:
   REACT_APP_BACKEND_URL=http://localhost:8007
   ```

2. **Rebuild el frontend:**
   - En Portainer → Tu Stack → Editor → Update Stack
   - Marca "Re-deploy" para rebuild las imágenes

### **🌟 Solución 3: Stack Corregido**
Usa `portainer-corrected.yml` que incluye:
- ✅ Configuración automática de URLs
- ✅ Contenedor que detecta y configura la URL correcta
- ✅ Variables de entorno optimizadas

## 🧪 **Para diagnosticar:**

### **1. Ve al Admin Panel → pestaña "Debug"**
- Verás un diagnóstico completo de conexión
- Te mostrará qué URLs funcionan
- Te dará recomendaciones específicas

### **2. Revisa los logs del frontend:**
```bash
docker logs cv_frontend
```

### **3. Prueba manualmente:**
```bash
# Desde tu servidor:
curl http://localhost:8007/health
curl http://localhost:8007/api/import/status
```

## 📋 **URLs según el entorno:**

### **Docker (interno):**
```bash
REACT_APP_BACKEND_URL=http://backend:8001
```

### **Docker (externo):**
```bash
REACT_APP_BACKEND_URL=http://localhost:8007
```

### **Con NPM:**
```bash
REACT_APP_BACKEND_URL=https://api.tu-dominio.com
```

## 🎯 **Plan de acción inmediato:**

1. **Ejecuta el diagnóstico:**
   ```bash
   python3 fix_frontend_config.py
   ```

2. **O usa el stack corregido:**
   - Deploy `portainer-corrected.yml`
   - Incluye auto-configuración

3. **Verifica en el Admin Panel:**
   - Ve a la pestaña "Debug"
   - Debería mostrar "Backend Conectado"

4. **Prueba la importación:**
   - Ve a la pestaña "Import"
   - Usa "Inicialización Rápida"

## 💡 **Mejoras implementadas:**

### **🔍 Diagnóstico mejorado:**
- ✅ Panel "Debug" en Admin Panel
- ✅ Test automático de múltiples URLs
- ✅ Información detallada del entorno
- ✅ Recomendaciones específicas

### **📤 Exportación mejorada:**
- ✅ Función de exportar siempre visible
- ✅ Mejor manejo de errores
- ✅ Logs detallados en consola
- ✅ Descarga automática de JSON

### **🛠️ Herramientas automáticas:**
- ✅ `fix_frontend_config.py` - Corrector automático
- ✅ `portainer-corrected.yml` - Stack con auto-configuración
- ✅ `ConnectionDiagnostic.js` - Diagnóstico en tiempo real

---

**¿Qué solución prefieres probar primero?**

1. **Script automático** → `python3 fix_frontend_config.py`
2. **Stack corregido** → `portainer-corrected.yml`
3. **Diagnóstico manual** → Admin Panel → "Debug"