# 🔧 Solución: "Failed to fetch" - Problema CORS

## 🚨 **Problema actual:**
El frontend puede ver que el backend funciona, pero cuando hace peticiones desde JavaScript obtiene "Failed to fetch".

## 🎯 **Causa más probable:**
**Problema de CORS (Cross-Origin Resource Sharing)** o variables de entorno incorrectas en el build del frontend.

## ✅ **Soluciones implementadas:**

### **1. Componente de diagnóstico CORS**
- ✅ Nueva pestaña "CORS" en Admin Panel
- ✅ Tests específicos de conectividad
- ✅ Información detallada de debug
- ✅ Test manual para copiar en consola

### **2. Dockerfile corregido**
- ✅ `Dockerfile.env-fixed` - Variables de entorno antes del build
- ✅ Crear archivo `.env` durante el build
- ✅ Asegurar que la IP correcta esté en el bundle

### **3. YML optimizado para CORS**
- ✅ `portainer-cors-fixed.yml` - CORS más permisivo
- ✅ Dockerfile corregido
- ✅ Variables de entorno explícitas

## 🚀 **Plan de acción:**

### **Paso 1: Re-deploy con stack corregido**
```bash
# En Portainer:
# 1. Stack → Editor
# 2. Reemplazar con portainer-cors-fixed.yml
# 3. Update stack → Re-deploy
# 4. ESPERAR 5 MINUTOS (build completo)
```

### **Paso 2: Diagnóstico CORS**
1. Ve a: `http://192.168.1.18:8006/admin`
2. Login: `admin` / `password123`
3. Click en pestaña **"CORS"**
4. Click **"Ejecutar Tests CORS"**
5. Analizar resultados

### **Paso 3: Test manual en navegador**
Abre la consola del navegador (F12) y prueba:

```javascript
// Test básico
fetch('http://192.168.1.18:8007/health')
  .then(r => r.json())
  .then(d => console.log('✅ Success:', d))
  .catch(e => console.log('❌ Error:', e));

// Test con headers CORS
fetch('http://192.168.1.18:8007/api/import/status', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
  .then(r => r.json())
  .then(d => console.log('✅ API Success:', d))
  .catch(e => console.log('❌ API Error:', e));
```

## 🔍 **Posibles resultados:**

### **A. Si el test manual funciona pero el componente no:**
- ✅ CORS está OK
- ❌ Problema en el componente React
- 🔧 **Solución:** El componente está usando URL incorrecta

### **B. Si el test manual falla:**
- ❌ Problema de CORS
- 🔧 **Solución:** Configurar CORS en backend o usar proxy

### **C. Si ambos fallan:**
- ❌ Problema de red/configuración
- 🔧 **Solución:** Verificar contenedores y puertos

## 💡 **Soluciones alternativas:**

### **Solución A: Proxy nginx (si CORS falla)**
```nginx
location /api/ {
    proxy_pass http://backend:8001/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### **Solución B: CORS headers manuales**
Agregar al backend:
```python
@app.middleware("http")
async def cors_handler(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response
```

### **Solución C: Usar IP del contenedor**
Si `192.168.1.18` no funciona, probar con la IP del contenedor backend:
```bash
docker inspect cv_backend | grep IPAddress
```

## 🧪 **Pasos de verificación:**

### **1. Verificar que el nuevo build use la IP correcta:**
```bash
# Después del re-deploy:
docker exec -it cv_frontend cat /usr/share/nginx/html/static/js/main.*.js | grep "192.168.1.18"
```

### **2. Verificar CORS en backend:**
```bash
curl -H "Origin: http://192.168.1.18:8006" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://192.168.1.18:8007/health
```

### **3. Verificar logs del backend:**
```bash
docker logs cv_backend --tail 20
```

## 🎯 **Lo que esperamos después del fix:**

✅ **Pestaña CORS:** Todos los tests en verde  
✅ **Pestaña Debug:** "Backend Conectado"  
✅ **Pestaña Import:** "Inicialización Rápida" funciona  
✅ **Console test:** `fetch()` responde correctamente  

## 📋 **Archivos creados:**
- ✅ `CorsDebug.js` - Componente de diagnóstico
- ✅ `Dockerfile.env-fixed` - Build con variables correctas
- ✅ `portainer-cors-fixed.yml` - Stack optimizado para CORS

---

**El problema "Failed to fetch" es muy común en aplicaciones web y casi siempre es CORS o variables de entorno. Con estas herramientas podemos identificar y solucionar la causa exacta.** 🎯