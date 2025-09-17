# 🔧 Solución al Error de Conexión MongoDB

## 🚨 Error actual:
```
localhost:27017: [Errno 111] Connection refused
```

## 📋 Pasos para solucionarlo:

### **Paso 1: Ejecutar diagnóstico**
```bash
# Desde tu servidor donde tienes Docker/Portainer:
python3 diagnose.py
```

### **Paso 2A: Si el contenedor no existe**
1. **Re-deploy el stack** en Portainer usando `portainer-fixed.yml`
2. **Espera 2-3 minutos** hasta que todos los contenedores estén "running"

### **Paso 2B: Si el contenedor existe pero el puerto no está expuesto**
1. **Actualiza tu stack** en Portainer con `portainer-fixed.yml`
2. Este YML **expone el puerto 27017** temporalmente

### **Paso 3: Inicializar datos**
```bash
# Opción 1: Inicializador inteligente (RECOMENDADO)
python3 init_smart.py

# Opción 2: Si lo anterior falla, desde dentro del contenedor
docker exec -it cv_backend python init_data.py

# Opción 3: Manual en el Admin Panel
# Accede a http://tu-servidor:8006/admin
```

## 🔍 **¿Qué hacer ahora?**

**DESDE TU SERVIDOR** (donde tienes Docker/Portainer), ejecuta:

```bash
# 1. Verificar estado
docker ps | grep cv_

# 2. Si ves cv_mongodb running, verificar puertos
docker port cv_mongodb

# 3. Si NO ves el puerto 27017, usa portainer-fixed.yml
```

## 📝 **YML correcto con puerto expuesto**

Asegúrate de usar `portainer-fixed.yml` que incluye:
```yaml
mongodb:
  ports:
    - "27017:27017"  # 👈 ESTO ES CLAVE
```

## ⚡ **Solución rápida:**

1. **Update stack** en Portainer con `portainer-fixed.yml`
2. **Espera que arranque** MongoDB (2-3 min)
3. **Ejecuta**: `python3 init_smart.py`
4. **¡Listo!** Tu CV estará funcionando

## 🔒 **Después de inicializar (opcional):**

Por seguridad, puedes remover el puerto expuesto cambiando de vuelta a:
```yaml
mongodb:
  # ports:
  #   - "27017:27017"  # Comentado para mayor seguridad
```

---

**¿Necesitas que te ayude con algún paso específico?**