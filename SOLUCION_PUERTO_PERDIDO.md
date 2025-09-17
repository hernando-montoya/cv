# 🔧 Solución: MongoDB pierde el puerto expuesto

## 🚨 Problema identificado:
MongoDB **expone el puerto inicialmente** pero luego **deja de estar disponible**.

## 🔍 Posibles causas:
1. **Reinicio del contenedor** sin configuración persistente
2. **Health check failing** causando reinicios
3. **Configuración de red** que se pierde
4. **Restart policy** inadecuada
5. **Recursos insuficientes** causando crashes

## 🛠️ Herramientas creadas para ti:

### **1. Monitor en tiempo real** 📊
```bash
python3 monitor_mongo.py
```
- Detecta cuándo se pierde el puerto
- Auto-reinicia MongoDB si es necesario
- Log detallado del problema

### **2. Solucionador automático** 🔧
```bash
python3 fix_mongo_port.py
```
- Analiza por qué se pierde el puerto
- Intenta varias soluciones automáticamente
- Crea un monitor permanente

### **3. YML reforzado** 💪
**Usa `portainer-persistent.yml`** que incluye:
- ✅ `restart: always` (en lugar de unless-stopped)
- ✅ Health checks robustos
- ✅ Depends_on con condiciones
- ✅ Monitor interno del puerto
- ✅ Configuración de recursos estable

## 🚀 **Solución inmediata:**

### **Opción A: Monitor y diagnóstico**
```bash
# 1. Ejecutar monitor para capturar el problema
python3 monitor_mongo.py

# En otra terminal, inicializar cuando el puerto esté disponible
python3 init_smart.py
```

### **Opción B: YML más robusto**
1. **Replace tu stack** en Portainer con `portainer-persistent.yml`
2. **Deploy** y espera 3-5 minutos
3. **El puerto debería mantenerse estable**

### **Opción C: Solución rápida temporal**
```bash
# Forzar restart y mantener el puerto
docker restart cv_mongodb
sleep 30
python3 init_smart.py
```

## 🔍 **Para identificar la causa exacta:**

**Ejecuta desde tu servidor:**
```bash
# Ver logs detallados de MongoDB
docker logs cv_mongodb --tail 50

# Ver estadísticas de recursos
docker stats cv_mongodb

# Ver configuración actual
docker inspect cv_mongodb | grep -i port -A 5 -B 5
```

## ⚡ **Plan recomendado:**

1. **Ahora mismo**: Usa `python3 fix_mongo_port.py` para diagnosticar
2. **Deploy**: `portainer-persistent.yml` para una solución permanente
3. **Monitor**: `python3 monitor_mongo.py` para prevenir futuros problemas

---

**¿Qué herramienta quieres probar primero? ¿O prefieres que cambiemos a una configuración completamente diferente sin MongoDB expuesto?**