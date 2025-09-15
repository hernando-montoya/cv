# 🚨 Solución al Error de Docker Build

## Error Encontrado
```
Error: Cannot find module 'react-scripts/config/env.js'
```

## 🔧 Solución Rápida

### Paso 1: Ejecutar Script de Diagnóstico
```bash
cd /ruta/a/tu/proyecto
./debug_docker.sh
```

### Paso 2: Si el Script No Funciona, Manual Fix
```bash
cd frontend

# Limpiar cache
rm -rf node_modules yarn.lock build

# Downgrade React a versión compatible
yarn add react@18.2.0 react-dom@18.2.0

# Reinstalar dependencias
yarn install --legacy-peer-deps

# Probar build
yarn docker:build
```

### Paso 3: Si Sigue Fallando, Usar React-Scripts Directamente
```bash
# En frontend/package.json, cambiar:
"scripts": {
  "build": "react-scripts build",
  "docker:build": "react-scripts build"
}

# Luego:
npx react-scripts build
```

## 🐳 Deploy Completo

### Opción A: Script Automático
```bash
./deploy.sh
```

### Opción B: Manual
```bash
# 1. Configurar credenciales
cp .env.example .env

# 2. Generar credenciales seguras (opcional)
cd backend && python generate_credentials.py

# 3. Deploy
docker-compose up -d --build

# 4. Verificar
docker-compose ps
```

## 🔍 Verificación de Servicios

### Comprobar que todo funciona:
```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs
docker-compose logs -f

# Probar endpoints
curl http://localhost:8001/api/
curl http://localhost:3000/
```

## 🚨 Problemas Comunes y Soluciones

### 1. Puerto en uso
```bash
# Ver qué usa el puerto
sudo lsof -i :3000
sudo lsof -i :8001
sudo lsof -i :27017

# Terminar proceso
sudo kill -9 PID_NUMBER
```

### 2. Error de permisos
```bash
# Dar permisos a scripts
chmod +x deploy.sh debug_docker.sh

# Si problemas de permisos con Docker
sudo usermod -aG docker $USER
# Luego reiniciar sesión
```

### 3. Build muy lento o falla por memoria
```bash
# Aumentar memoria de Node
export NODE_OPTIONS="--max-old-space-size=4096"

# O en Dockerfile ya está configurado
```

### 4. Dependencias incompatibles
```bash
cd frontend

# Limpiar completamente
rm -rf node_modules yarn.lock

# Instalar versiones específicas compatibles
yarn add react@18.2.0 react-dom@18.2.0
yarn add @craco/craco@6.4.5
yarn install --legacy-peer-deps
```

## 📋 Checklist de Verificación

- [ ] Docker instalado y funcionando
- [ ] Docker Compose disponible
- [ ] Puertos 3000, 8001, 27017 libres
- [ ] Archivo .env configurado
- [ ] Frontend builds sin errores
- [ ] Backend inicia correctamente
- [ ] MongoDB se conecta

## 🎯 URLs Finales

Una vez que todo funcione:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001/api
- **Admin Panel**: http://localhost:3000 → Clic "Admin"
- **Credenciales**: admin / admin2024

## 📞 Si Nada Funciona

1. **Ejecuta el diagnóstico**: `./debug_docker.sh`
2. **Revisa logs detallados**: `docker-compose logs`
3. **Verifica versiones**:
   ```bash
   node --version  # Debería ser 16+ pero < 19
   docker --version
   docker-compose --version
   ```

4. **Reinstalación completa**:
   ```bash
   # Limpiar todo Docker
   docker system prune -a
   
   # Limpiar proyecto
   rm -rf frontend/node_modules frontend/build
   
   # Volver a empezar
   ./debug_docker.sh
   ```

---

## ✅ Confirmación de Éxito

Sabrás que todo funciona cuando:

1. `docker-compose ps` muestra todos los servicios "Up"
2. Puedes acceder a http://localhost:3000
3. Puedes hacer login como admin
4. Puedes editar contenido en el panel

🎉 **¡Tu aplicación CV está lista para usar!**