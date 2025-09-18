# 🔧 Solución: MongoDB Hostname Resolution Error

## 🎯 **Problema identificado:**
```
mongodb:27017: [Errno -3] Temporary failure in name resolution
```

**Causa:** El contenedor `cv_app` no puede resolver el hostname `mongodb`.

## 🔍 **Análisis del diagnóstico:**
- ✅ **Importaciones Python:** OK
- ✅ **Variables de entorno:** OK (MongoDB URL configurada)
- ❌ **Base de datos:** Error de código (corregido)
- ❌ **Colecciones:** No puede resolver hostname `mongodb`

## 🛠️ **Herramientas de diagnóstico agregadas:**

### **1. Corrección del código debug**
- ✅ Arreglado error `MotorCollection object is not callable`
- ✅ Usar `client.admin.command('ping')` en lugar de `db.admin.command('ping')`

### **2. Nueva pestaña "Network"**
- ✅ Test de resolución de hostnames (`mongodb`, `cv_mongodb`, `localhost`)
- ✅ Test de conectividad MongoDB con diferentes URLs
- ✅ Información de red del contenedor

### **3. Stack mejorado** (`portainer-single-fixed.yml`)
- ✅ `hostname: mongodb` explícito en el servicio MongoDB
- ✅ Health check para MongoDB
- ✅ `depends_on` con condición de salud
- ✅ Script de inicio que espera MongoDB

## 🚀 **Soluciones disponibles:**

### **Solución A: Re-deploy con stack corregido (RECOMENDADO)**
1. En Portainer → Stack → Editor
2. Reemplazar con `portainer-single-fixed.yml`
3. Update stack → Re-deploy
4. Esperar 5-10 minutos

### **Solución B: Debug de red primero**
1. Ve a Admin Panel → pestaña **"Network"**
2. Click **"Debug Red"**
3. Verificar qué hostnames se resuelven correctamente
4. Identificar si el problema es DNS o conectividad

### **Solución C: Cambiar a IP específica**
Si el hostname no se resuelve, podemos usar la IP del contenedor:
```yaml
environment:
  MONGO_URL: mongodb://admin:securepassword123@172.18.0.2:27017/cv_database?authSource=admin
```

## 🧪 **Para diagnosticar específicamente:**

### **Paso 1: Debug de red**
- Pestaña "Network" → "Debug Red"
- Verificar si `mongodb` se resuelve a una IP
- Ver qué URL de MongoDB funciona

### **Paso 2: Re-test sistema**
- Pestaña "System" → "Debug Sistema"
- Debería mostrar mejores resultados

### **Paso 3: Probar importación**
- Si red OK, probar importación de nuevo

## 🎯 **Lo que esperamos ver:**

### **✅ En Network Debug:**
```json
{
  "hostname_resolution": {
    "mongodb": {"status": "ok", "ip": "172.18.0.2"},
    "cv_mongodb": {"status": "ok", "ip": "172.18.0.2"}
  },
  "mongo_connection_tests": {
    "mongodb://...@mongodb:27017/...": {"status": "ok"}
  }
}
```

### **✅ En System Debug:**
```json
{
  "checks": {
    "database": {"status": "ok", "ping_result": "ok"},
    "collections": {"status": "ok", "content_count": 0}
  }
}
```

## 📋 **Archivos creados:**
- ✅ `portainer-single-fixed.yml` - Stack con hostname y health checks
- ✅ `network_debug.py` - Endpoint de debug de red
- ✅ `NetworkDebug.js` - Componente de debug de red
- ✅ Corrección en `import_data.py` - Fix del ping a MongoDB

## 💡 **¿Por qué pasa esto?**

En Docker Compose, los servicios se comunican usando sus nombres como hostnames. Si `mongodb` no se resuelve, puede ser por:

1. **Red no configurada correctamente**
2. **Contenedor MongoDB no ha arrancado completamente**
3. **Orden de inicio incorrecto**
4. **Configuración de hostname faltante**

---

**Próximo paso:** Usar la pestaña "Network" para ver exactamente qué hostname funciona, y luego re-deploy con el stack corregido.** 🎯