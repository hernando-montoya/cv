# 🔧 Diagnóstico: Error 500 Internal Server Error

## 🎯 **Estado actual:**
- ✅ **CORS resuelto** - La comunicación funciona
- ✅ **Frontend conecta al backend** - Sin "Failed to fetch"
- ❌ **Error 500** - Excepción interna en el servidor

## 🔍 **Error específico:**
```
Status: 500
Respuesta raw: Internal Server Error
```

Esto indica una **excepción no capturada** en el código Python del backend.

## 🛠️ **Herramientas de diagnóstico creadas:**

### **1. Nueva pestaña "System" en Admin Panel**
- ✅ **Debug Sistema:** Verifica importaciones, variables de entorno, MongoDB
- ✅ **Test Auth:** Prueba el sistema de autenticación JWT
- ✅ **Verificaciones específicas:** Cada componente por separado

### **2. Endpoints de diagnóstico en backend**
- ✅ `GET /api/import/debug` - Diagnóstico completo del sistema
- ✅ `POST /api/import/test-auth` - Test específico de autenticación

### **3. Logging mejorado**
- ✅ Logs detallados en cada paso del proceso
- ✅ Información específica de errores
- ✅ Traceback completo de excepciones

## 🚀 **Para diagnosticar el error 500:**

### **Paso 1: Usar la pestaña "System"**
1. Ve al Admin Panel → pestaña **"System"**
2. Click **"Debug Sistema"**
3. Verifica que todos los checks estén en verde:
   - ✅ **Importaciones Python:** Librerías cargadas correctamente
   - ✅ **Variables de Entorno:** MongoDB URL, JWT Secret, etc.
   - ✅ **Base de Datos:** Conexión a MongoDB funciona
   - ✅ **Colecciones:** Acceso a las tablas de datos

### **Paso 2: Test de autenticación**
1. En la misma pestaña, click **"Test Auth"**
2. Verifica que el JWT token funcione correctamente

### **Paso 3: Identificar el problema**
Según los resultados:

## 🔍 **Posibles causas y soluciones:**

### **A. Si falla "Base de Datos":**
- **Problema:** MongoDB no accesible
- **Solución:** Verificar contenedor `cv_mongodb`
- **Test manual:** `docker logs cv_mongodb`

### **B. Si falla "Variables de Entorno":**
- **Problema:** Configuración incorrecta
- **Solución:** Verificar variables en el YML de Portainer

### **C. Si falla "Test Auth":**
- **Problema:** JWT token inválido o expirado
- **Solución:** Logout y login de nuevo

### **D. Si todo está OK pero sigue error 500:**
- **Problema:** Error específico en el procesamiento del archivo
- **Solución:** Verificar logs del contenedor

## 📋 **Comandos útiles para debugging:**

### **Ver logs del backend:**
```bash
# Logs en tiempo real:
docker logs cv_app -f

# Últimas 50 líneas:
docker logs cv_app --tail 50

# Buscar errores específicos:
docker logs cv_app 2>&1 | grep -i error
```

### **Verificar contenedores:**
```bash
# Estado de contenedores:
docker ps

# Verificar salud de MongoDB:
docker logs cv_mongodb --tail 20
```

### **Test manual de endpoints:**
```bash
# Test debug sistema:
curl http://192.168.1.18:8006/api/import/debug

# Test health:
curl http://192.168.1.18:8006/health
```

## 🎯 **Plan de acción:**

### **1. Diagnóstico inmediato:**
- Ve a Admin Panel → pestaña "System"
- Ejecuta "Debug Sistema" y "Test Auth"
- Identifica qué componente falla

### **2. Según resultados:**
- **Si todo OK:** El problema está en el procesamiento específico del archivo
- **Si algo falla:** Solucionar el componente específico

### **3. Verificación:**
- Una vez solucionado, probar de nuevo la importación
- Usar pestaña "JSON" para importar con debug detallado

## 📊 **Lo que esperamos ver:**

### **✅ Sistema saludable:**
```json
{
  "checks": {
    "imports": {"status": "ok"},
    "environment": {"status": "ok", "mongo_url_exists": true},
    "database": {"status": "ok", "ping_result": "ok"},
    "collections": {"status": "ok", "content_count": 0}
  }
}
```

### **✅ Auth funcionando:**
```json
{
  "status": "ok",
  "message": "Authentication successful",
  "user": {"username": "admin"}
}
```

---

**El error 500 es muy específico y estos diagnósticos nos ayudarán a identificar exactamente dónde está el problema.** 🎯

**Próximo paso:** Usar la nueva pestaña "System" para ver qué componente está fallando.