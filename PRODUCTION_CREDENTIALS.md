# 🔐 Credenciales de Producción - Sistema de Gestión de Contenido

## Credenciales Actuales (Demo/Desarrollo)

**Para acceso inmediato al sistema:**
- **Usuario**: `admin`
- **Contraseña**: `admin2024`

---

## 🚨 Configuración de Producción OBLIGATORIA

### Variables de Entorno Requeridas

Para desplegar en producción, debes configurar las siguientes variables de entorno:

```bash
# Autenticación de Admin
ADMIN_USERNAME=tu_usuario_admin_seguro
ADMIN_PASSWORD_HASH=hash_generado_automaticamente
JWT_SECRET=clave_secreta_jwt_muy_larga_y_segura

# Base de datos
MONGO_URL=mongodb://tu-servidor-mongo:27017/cv_database
DB_NAME=cv_production

# Frontend
REACT_APP_BACKEND_URL=https://tu-dominio-backend.com
```

### 🔧 Script de Configuración Segura

Ejecuta este comando para generar credenciales seguras de producción:

```bash
cd /app/backend
python -c "
import secrets, hashlib, os

# Generar credenciales seguras
username = input('Nuevo usuario admin: ')
password = input('Nueva contraseña admin: ')
jwt_secret = secrets.token_urlsafe(64)

# Hash de contraseña
salt = secrets.token_hex(16)
password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
full_hash = f'{salt}:{password_hash.hex()}'

# Mostrar variables de entorno
print('\\n=== VARIABLES DE ENTORNO PARA PRODUCCIÓN ===')
print(f'ADMIN_USERNAME={username}')
print(f'ADMIN_PASSWORD_HASH={full_hash}')
print(f'JWT_SECRET={jwt_secret}')
print('\\n=== GUARDA ESTAS VARIABLES EN TU SERVIDOR ===')
"
```

### 🔒 Recomendaciones de Seguridad

1. **Nunca uses las credenciales por defecto en producción**
2. **Usuario Admin**: Mínimo 8 caracteres, sin nombres obvios
3. **Contraseña**: Mínimo 12 caracteres, caracteres especiales, números
4. **JWT Secret**: Generado automáticamente, mínimo 256 bits
5. **HTTPS**: Obligatorio en producción
6. **Variables de entorno**: Nunca en código, solo en servidor

### 🌐 Configuración de Servidor

#### Ejemplo para servidor con systemd:

```bash
# /etc/systemd/system/cv-backend.service
[Unit]
Description=CV Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/app/backend
Environment=ADMIN_USERNAME=tu_usuario_seguro
Environment=ADMIN_PASSWORD_HASH=tu_hash_generado
Environment=JWT_SECRET=tu_jwt_secret_muy_largo
Environment=MONGO_URL=mongodb://localhost:27017/cv_production
Environment=DB_NAME=cv_production
ExecStart=/path/to/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Ejemplo para Docker:

```dockerfile
# Variables de entorno en docker-compose.yml
environment:
  - ADMIN_USERNAME=tu_usuario_seguro
  - ADMIN_PASSWORD_HASH=tu_hash_generado
  - JWT_SECRET=tu_jwt_secret_muy_largo
  - MONGO_URL=mongodb://mongo:27017/cv_production
  - DB_NAME=cv_production
```

### 🎯 Proceso de Despliegue Seguro

1. **Genera credenciales**: Usa el script arriba
2. **Configura variables**: En tu servidor/contenedor
3. **Prueba autenticación**: Verifica acceso con nuevas credenciales
4. **Reinicia servicios**: Backend y frontend
5. **Verifica funcionamiento**: Accede al gestor de contenido

### 📞 Soporte

Si necesitas ayuda con la configuración de producción:
- Verifica que todas las variables de entorno estén configuradas
- Comprueba los logs del backend para errores de autenticación
- Asegúrate de que MongoDB esté accesible con la URL configurada

---

## ⚠️ Nota de Seguridad

**Las credenciales actuales (`admin`/`admin2024`) son SOLO para desarrollo y pruebas.**

**NUNCA las uses en un entorno de producción accesible desde internet.**