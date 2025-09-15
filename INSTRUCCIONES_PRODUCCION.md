# 🚀 Instrucciones para Despliegue en Producción

## Credenciales Actuales (Solo Desarrollo)

```
Usuario: admin
Contraseña: admin2024
```

**⚠️ CRÍTICO: Estas credenciales DEBEN cambiarse antes de producción**

---

## 🔧 Configuración de Producción

### 1. Generar Credenciales Seguras

```bash
cd /app/backend
python generate_credentials.py
```

Este script:
- Te pedirá un nuevo usuario y contraseña
- Generará un JWT secret seguro
- Creará hashes seguros de la contraseña
- Guardará todo en `production.env`

### 2. Variables de Entorno Necesarias

Configura estas variables en tu servidor:

```bash
# Autenticación
ADMIN_USERNAME=tu_usuario_personalizado
ADMIN_PASSWORD_HASH=hash_generado_por_el_script
JWT_SECRET=clave_jwt_muy_larga_y_segura

# Base de datos
MONGO_URL=mongodb://localhost:27017/cv_production
DB_NAME=cv_production

# Frontend
REACT_APP_BACKEND_URL=https://tu-sitio-web.com
```

### 3. Configuración del Servidor

#### Opción A: Servidor Linux (systemd)

```bash
# Crear servicio del backend
sudo nano /etc/systemd/system/cv-backend.service
```

```ini
[Unit]
Description=CV Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/ruta/completa/a/app/backend
Environment=ADMIN_USERNAME=tu_usuario
Environment=ADMIN_PASSWORD_HASH=tu_hash_completo
Environment=JWT_SECRET=tu_jwt_secret
Environment=MONGO_URL=mongodb://localhost:27017/cv_production
Environment=DB_NAME=cv_production
ExecStart=/ruta/a/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Activar el servicio
sudo systemctl daemon-reload
sudo systemctl enable cv-backend
sudo systemctl start cv-backend
sudo systemctl status cv-backend
```

#### Opción B: Docker

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - ADMIN_USERNAME=tu_usuario
      - ADMIN_PASSWORD_HASH=tu_hash_completo
      - JWT_SECRET=tu_jwt_secret
      - MONGO_URL=mongodb://mongo:27017/cv_production
      - DB_NAME=cv_production
    ports:
      - "8001:8001"
    depends_on:
      - mongo
      
  frontend:
    build: ./frontend
    environment:
      - REACT_APP_BACKEND_URL=https://tu-dominio.com
    ports:
      - "3000:3000"
      
  mongo:
    image: mongo:5
    volumes:
      - mongo_data:/data/db
      
volumes:
  mongo_data:
```

### 4. Configuración de Nginx (Recomendado)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name tu-dominio.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🔒 Lista de Verificación de Seguridad

- [ ] Credenciales por defecto cambiadas
- [ ] HTTPS configurado (certificado SSL)
- [ ] Variables de entorno configuradas
- [ ] Firewall configurado (solo puertos 80, 443, 22)
- [ ] MongoDB con autenticación habilitada
- [ ] Copias de seguridad programadas
- [ ] Logs de acceso monitoreados

---

## 🧪 Verificación Post-Despliegue

1. **Acceso web**: `https://tu-dominio.com`
2. **API health**: `https://tu-dominio.com/api/`
3. **Autenticación**: Clic en "Admin" → usar nuevas credenciales
4. **Edición**: Modificar contenido y guardar
5. **Persistencia**: Recargar página y verificar cambios

---

## 🆘 Solución de Problemas

### Backend no inicia
```bash
# Verificar logs
sudo journalctl -u cv-backend -f

# Verificar variables de entorno
sudo systemctl show cv-backend | grep Environment
```

### Error de autenticación
```bash
# Verificar hash de contraseña
cd /app/backend
python -c "from models.auth import auth_manager; print('Usuario:', auth_manager.admin_username)"
```

### Base de datos no conecta
```bash
# Verificar MongoDB
sudo systemctl status mongod
mongo --eval "db.adminCommand('ismaster')"
```

---

## 📞 Contacto

Si necesitas ayuda adicional con el despliegue, verifica:
1. Logs del sistema
2. Variables de entorno
3. Conectividad de red
4. Permisos de archivos

**¡Tu CV ya está listo para producción!** 🎉