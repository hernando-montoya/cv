# 🌐 Configuración de Nginx Proxy Manager (NPM)

## 🎯 Configuración para tu CV App

### 1. **Frontend (React)**
```
Domain Names: tudominio.com, www.tudominio.com
Scheme: http
Forward Hostname/IP: cv_frontend
Forward Port: 3000
```

**SSL**: ✅ Habilitar (Let's Encrypt)
**Cache Assets**: ✅ Habilitar
**Block Common Exploits**: ✅ Habilitar
**Websockets Support**: ✅ Habilitar

### 2. **Backend API**
```
Domain Names: api.tudominio.com
Scheme: http
Forward Hostname/IP: cv_backend
Forward Port: 8001
```

**SSL**: ✅ Habilitar (Let's Encrypt)
**Block Common Exploits**: ✅ Habilitar

---

## 🔧 Configuración Avanzada de NPM

### **Frontend - Advanced Tab**
```nginx
# Optimización para React SPA
location / {
    try_files $uri $uri/ /index.html;
}

# Cache para assets estáticos
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### **Backend API - Advanced Tab**
```nginx
# Rate limiting para API
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;

# Rate limiting más estricto para admin
location /api/auth/ {
    limit_req_zone $binary_remote_addr zone=admin:10m rate=2r/s;
    limit_req zone=admin burst=5 nodelay;
    proxy_pass http://cv_backend:8001;
}

# CORS headers si necesario
add_header Access-Control-Allow-Origin "https://tudominio.com" always;
add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;
```

---

## 🚀 Pasos de Configuración en NPM

### **Paso 1: Crear Red Docker**
```bash
# Crear red para NPM si no existe
docker network create npm_proxy
```

### **Paso 2: Proxy Hosts en NPM**

#### **Frontend**
1. **Hosts > Proxy Hosts > Add Proxy Host**
2. **Details Tab**:
   - Domain Names: `tudominio.com`, `www.tudominio.com`
   - Scheme: `http`
   - Forward Hostname/IP: `cv_frontend`
   - Forward Port: `3000`
   - ✅ Cache Assets
   - ✅ Block Common Exploits
   - ✅ Websockets Support

3. **SSL Tab**:
   - ✅ SSL Certificate: Request a new SSL Certificate
   - ✅ Force SSL
   - ✅ HTTP/2 Support
   - Email: tu@email.com
   - ✅ I Agree to the Let's Encrypt Terms of Service

#### **Backend API**
1. **Hosts > Proxy Hosts > Add Proxy Host**
2. **Details Tab**:
   - Domain Names: `api.tudominio.com`
   - Scheme: `http`
   - Forward Hostname/IP: `cv_backend`
   - Forward Port: `8001`
   - ✅ Block Common Exploits

3. **SSL Tab**:
   - ✅ SSL Certificate: Request a new SSL Certificate
   - ✅ Force SSL
   - ✅ HTTP/2 Support

### **Paso 3: Configuración DNS**
Asegúrate de que tu DNS apunte a la IP de tu VM:
```
A tudominio.com → IP_DE_TU_VM
A www.tudominio.com → IP_DE_TU_VM
A api.tudominio.com → IP_DE_TU_VM
```

---

## 🔍 Verificación de Funcionamiento

### **URLs a probar**:
- ✅ `https://tudominio.com` → Frontend React
- ✅ `https://www.tudominio.com` → Frontend React (redirect)
- ✅ `https://api.tudominio.com/api/` → Backend API
- ✅ `https://tudominio.com` → Clic "Admin" → Panel funcional

### **Health Checks**:
```bash
# Desde tu VM
curl -f http://cv_frontend:3000/health
curl -f http://cv_backend:8001/api/

# Desde internet
curl -f https://tudominio.com/
curl -f https://api.tudominio.com/api/
```

---

## 🚨 Troubleshooting NPM

### **Problema**: "502 Bad Gateway"
**Solución**: Verificar que los contenedores estén en la misma red
```bash
docker network inspect npm_proxy
docker exec cv_backend ping cv_frontend
```

### **Problema**: SSL no funciona
**Solución**: 
1. Verificar que los puertos 80 y 443 estén abiertos
2. Verificar DNS apunta a la IP correcta
3. Verificar que NPM pueda acceder a internet

### **Problema**: Admin panel no carga
**Solución**: 
1. Verificar BACKEND_URL en variables de entorno
2. Verificar CORS si es necesario
3. Verificar que api.tudominio.com funcione

---

## 📋 Checklist Final

- [ ] Red `npm_proxy` creada
- [ ] Stack desplegado en Portainer
- [ ] Variables de entorno configuradas
- [ ] Proxy Host para frontend configurado
- [ ] Proxy Host para backend configurado  
- [ ] SSL certificados generados
- [ ] DNS apuntando a la VM
- [ ] Frontend accesible vía HTTPS
- [ ] Backend API accesible vía HTTPS
- [ ] Admin panel funcional
- [ ] Credenciales de producción configuradas

🎉 **¡Tu CV estará disponible 24/7 con SSL!**