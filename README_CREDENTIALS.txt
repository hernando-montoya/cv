================================================================================
                    CREDENCIALES DE PRODUCCIÓN - CV GESTOR DE CONTENIDO
================================================================================

CREDENCIALES ACTUALES (DESARROLLO):
----------------------------------
Usuario: admin
Contraseña: admin2024

¡ATENCIÓN! Estas credenciales son SOLO para desarrollo y pruebas.
NUNCA las uses en producción.

================================================================================
                           CONFIGURACIÓN DE PRODUCCIÓN
================================================================================

PASO 1: GENERAR CREDENCIALES SEGURAS
------------------------------------
Ejecuta el siguiente comando en tu servidor:

cd /app/backend
python generate_credentials.py

Esto te pedirá:
- Nuevo usuario admin
- Nueva contraseña segura
- Generará automáticamente un JWT secret

PASO 2: CONFIGURAR VARIABLES DE ENTORNO
--------------------------------------
En tu servidor de producción, configura estas variables:

ADMIN_USERNAME=tu_usuario_seguro
ADMIN_PASSWORD_HASH=hash_generado_por_el_script
JWT_SECRET=jwt_secret_generado_por_el_script
MONGO_URL=mongodb://localhost:27017/cv_production
DB_NAME=cv_production
REACT_APP_BACKEND_URL=https://tu-dominio.com

PASO 3: EJEMPLOS DE CONFIGURACIÓN
---------------------------------

Para servidor Linux con systemd:
sudo nano /etc/systemd/system/cv-backend.service

[Unit]
Description=CV Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/ruta/a/tu/app/backend
Environment=ADMIN_USERNAME=tu_usuario_seguro
Environment=ADMIN_PASSWORD_HASH=tu_hash_generado
Environment=JWT_SECRET=tu_jwt_secret
Environment=MONGO_URL=mongodb://localhost:27017/cv_production
Environment=DB_NAME=cv_production
ExecStart=/ruta/a/tu/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target

Luego ejecuta:
sudo systemctl daemon-reload
sudo systemctl enable cv-backend
sudo systemctl start cv-backend

Para Docker:
Crea un archivo .env:
ADMIN_USERNAME=tu_usuario_seguro
ADMIN_PASSWORD_HASH=tu_hash_generado
JWT_SECRET=tu_jwt_secret
MONGO_URL=mongodb://mongo:27017/cv_production
DB_NAME=cv_production

PASO 4: VERIFICACIÓN
-------------------
1. Reinicia los servicios
2. Accede a tu página web
3. Haz clic en "Admin" en el header
4. Usa las nuevas credenciales
5. Verifica que puedas editar el contenido

================================================================================
                              RECOMENDACIONES DE SEGURIDAD
================================================================================

1. Usuario Admin: Mínimo 8 caracteres, evita nombres obvios como "admin"
2. Contraseña: Mínimo 12 caracteres con números y símbolos
3. Usa HTTPS en producción (certificado SSL)
4. Cambia las credenciales regularmente
5. Mantén copias de seguridad de la base de datos
6. Monitorea los logs de acceso

================================================================================
                                    SOPORTE
================================================================================

Si tienes problemas:
1. Verifica que todas las variables de entorno estén configuradas
2. Revisa los logs del backend: tail -f /var/log/supervisor/backend.*.log
3. Confirma que MongoDB esté ejecutándose
4. Prueba la conectividad entre frontend y backend

================================================================================