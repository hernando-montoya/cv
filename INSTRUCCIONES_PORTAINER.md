# 🚀 Deploy en Portainer - Guía Completa

## 📋 Preparación Previa

### 1. **Subir código a tu VM**
```bash
# Opción A: Git
git clone tu-repositorio
cd tu-repositorio

# Opción B: SCP/SFTP
scp -r /ruta/local/cv usuario@tu-vm:/home/usuario/cv

# Opción C: rsync
rsync -avz /ruta/local/cv/ usuario@tu-vm:/home/usuario/cv/
```

### 2. **Generar credenciales seguras**
```bash
# En tu VM
cd /ruta/a/tu/cv/backend
python generate_credentials.py

# Guarda la salida, la necesitarás en Portainer
```

### 3. **Crear red NPM (si no existe)**
```bash
# En tu VM
docker network create npm_proxy
```

---

## 🐳 Deploy en Portainer

### **Paso 1: Acceder a Portainer**
- URL: `http://tu-vm-ip:9000`
- Login con tus credenciales de Portainer

### **Paso 2: Crear Stack**
1. **Sidebar** → `Stacks`
2. **Add stack**
3. **Name**: `cv-application`
4. **Build method**: `Web editor`

### **Paso 3: Configurar Stack**

#### **A. Pegar el YAML**
Copia y pega el contenido de `portainer-stack.yml` en el editor.

#### **B. Configurar Variables de Entorno**
Scroll down hasta **Environment variables** y agrega:

```
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=TuPasswordSeguro123!
DB_NAME=cv_database
ADMIN_USERNAME=tu_usuario_admin
ADMIN_PASSWORD_HASH=hash_generado_por_script
JWT_SECRET=jwt_secret_generado_por_script
BACKEND_URL=https://api.tudominio.com
```

**⚠️ IMPORTANTE**: Usa las credenciales generadas por `generate_credentials.py`

#### **C. Configurar Build**
En **Advanced mode**:
- ✅ **Build**: Habilitado (para construir las imágenes)
- **Build path**: `/ruta/a/tu/cv` (ruta donde subiste el código)

### **Paso 4: Deploy**
1. **Deploy the stack**
2. Esperar que construya las imágenes
3. Verificar que todos los servicios estén **running**

---

## 🔍 Verificación en Portainer

### **Containers**
Deberías ver:
- ✅ `cv_backend` - Status: running, healthy
- ✅ `cv_frontend` - Status: running, healthy  
- ✅ `cv_mongodb` - Status: running, healthy
- ⏹️ `cv_data_init` - Status: exited (0) - normal

### **Logs**
Verificar logs sin errores:
- **cv_backend**: `INFO: Application startup complete`
- **cv_frontend**: Nginx logs normales
- **cv_mongodb**: Conexiones exitosas

### **Networks**
- ✅ `cv_internal` - Para comunicación interna
- ✅ `npm_proxy` - Para NPM

---

## 🌐 Configurar Nginx Proxy Manager

### **Paso 1: Frontend**
En NPM > Proxy Hosts:
- **Domain**: `tudominio.com`, `www.tudominio.com`
- **Forward**: `cv_frontend:3000`
- **SSL**: ✅ Let's Encrypt

### **Paso 2: Backend API**  
En NPM > Proxy Hosts:
- **Domain**: `api.tudominio.com`
- **Forward**: `cv_backend:8001`
- **SSL**: ✅ Let's Encrypt

**Ver detalles completos en `NPM_CONFIGURATION.md`**

---

## ✅ Testing y Verificación

### **URLs a probar**:
```bash
# Salud de servicios (desde la VM)
curl http://cv_backend:8001/api/
curl http://cv_frontend:3000/health

# URLs públicas
https://tudominio.com/
https://api.tudominio.com/api/
```

### **Admin Panel**:
1. Ir a `https://tudominio.com`
2. Clic en botón "Admin"  
3. Login con credenciales configuradas
4. Verificar que puedes editar contenido

---

## 🔧 Troubleshooting

### **Stack no se despliega**
```bash
# Verificar logs en Portainer
# O desde SSH:
docker logs cv_backend
docker logs cv_frontend  
docker logs cv_mongodb
```

### **Error de build**
- Verificar que el **Build path** sea correcto
- Verificar que los archivos `Dockerfile` existan
- Verificar variables de entorno

### **502 Bad Gateway en NPM**
```bash
# Verificar conectividad
docker network inspect npm_proxy
docker exec cv_backend ping cv_frontend
```

### **Admin no funciona**
- Verificar `BACKEND_URL` apunte a `https://api.tudominio.com`
- Verificar que NPM proxy del backend funcione
- Verificar credenciales en variables de entorno

---

## 🔄 Actualizaciones

### **Para actualizar la aplicación**:
1. **Subir código nuevo** a la VM
2. En Portainer > Stacks > `cv-application`
3. **Editor** → Hacer cambios si necesario
4. **Update the stack** ✅ Re-pull and redeploy
5. Verificar que todo funcione

### **Backup de datos**:
```bash
# Backup MongoDB
docker exec cv_mongodb mongodump --db cv_database --archive=/backup/cv_backup_$(date +%Y%m%d).archive

# Backup volúmenes
docker run --rm -v cv_mongodb_data:/data -v $(pwd):/backup alpine tar czf /backup/mongodb_backup.tar.gz /data
```

---

## 📊 Stack Template Completo

Si prefieres, puedes crear un **App Template** en Portainer:

1. **Settings** > **App Templates**
2. **Add template**
3. Usar el YAML de `portainer-stack.yml`
4. Definir variables como **required**

---

## 🎯 Resumen de Archivos

Para el deploy necesitas:
- ✅ `portainer-stack.yml` - Stack principal
- ✅ `portainer-env-template.txt` - Variables de entorno
- ✅ `NPM_CONFIGURATION.md` - Configuración NPM
- ✅ Todo el código fuente en la VM

---

🎉 **¡Tu aplicación CV estará disponible 24/7 con SSL automático!**

URLs finales:
- **Frontend**: https://tudominio.com
- **API**: https://api.tudominio.com/api
- **Admin**: https://tudominio.com → "Admin"