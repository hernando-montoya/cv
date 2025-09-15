#!/bin/bash

# Script para preparar archivos para subir a la VM
echo "📦 Preparando archivos para deploy en VM con Portainer..."

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 1. Crear directorio de deploy
print_status "Creando directorio de deploy..."
mkdir -p deploy_vm

# 2. Copiar archivos necesarios
print_status "Copiando archivos necesarios..."

# Copiar código fuente
cp -r backend deploy_vm/
cp -r frontend deploy_vm/

# Copiar archivos de configuración
cp portainer-stack.yml deploy_vm/
cp portainer-env-template.txt deploy_vm/
cp INSTRUCCIONES_PORTAINER.md deploy_vm/
cp NPM_CONFIGURATION.md deploy_vm/
cp README_DOCKER.md deploy_vm/

# Copiar scripts útiles
cp backend/generate_credentials.py deploy_vm/

# 3. Limpiar archivos innecesarios
print_status "Limpiando archivos innecesarios..."
rm -rf deploy_vm/frontend/node_modules
rm -rf deploy_vm/frontend/build
rm -rf deploy_vm/backend/__pycache__
rm -f deploy_vm/backend/*.pyc

# 4. Crear archivo README para la VM
cat > deploy_vm/README_VM.md << 'EOF'
# 🚀 CV Application - Deploy en VM

## 📋 Archivos incluidos
- `backend/` - Código del backend (FastAPI)
- `frontend/` - Código del frontend (React)
- `portainer-stack.yml` - Stack para Portainer
- `portainer-env-template.txt` - Variables de entorno
- `INSTRUCCIONES_PORTAINER.md` - Guía completa de deploy
- `NPM_CONFIGURATION.md` - Configuración de Nginx Proxy Manager

## 🚀 Deploy rápido

### 1. Generar credenciales
```bash
python generate_credentials.py
```

### 2. Crear red NPM
```bash
docker network create npm_proxy
```

### 3. En Portainer
1. Stacks > Add stack
2. Copiar contenido de `portainer-stack.yml`
3. Configurar variables de entorno (ver `portainer-env-template.txt`)
4. Deploy

### 4. Configurar NPM
Ver `NPM_CONFIGURATION.md` para detalles completos.

## 🌐 URLs finales
- Frontend: https://tudominio.com
- API: https://api.tudominio.com
- Admin: https://tudominio.com → "Admin"

¡Todo está listo para producción! 🎉
EOF

# 5. Crear archivo de variables de entorno de ejemplo
cat > deploy_vm/.env.production << 'EOF'
# Variables de producción - CAMBIAR TODOS LOS VALORES

# Base de datos
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=CAMBIAR_PASSWORD_SEGURO
DB_NAME=cv_database

# Autenticación (generar con generate_credentials.py)
ADMIN_USERNAME=CAMBIAR_USUARIO
ADMIN_PASSWORD_HASH=CAMBIAR_HASH_GENERADO
JWT_SECRET=CAMBIAR_JWT_SECRET_GENERADO

# URLs (cambiar por tu dominio)
BACKEND_URL=https://api.tudominio.com
EOF

# 6. Información final
print_success "✅ Archivos preparados en directorio 'deploy_vm/'"
echo ""
print_warning "📤 Para subir a tu VM, usa uno de estos métodos:"
echo ""
echo "🔹 SCP:"
echo "  scp -r deploy_vm/ usuario@tu-vm-ip:/home/usuario/cv"
echo ""
echo "🔹 rsync:"
echo "  rsync -avz deploy_vm/ usuario@tu-vm-ip:/home/usuario/cv/"
echo ""
echo "🔹 Git (recomendado):"
echo "  # Sube deploy_vm/ a tu repositorio Git"
echo "  # git add deploy_vm/ && git commit && git push"
echo "  # En la VM: git clone tu-repo"
echo ""
print_success "🎯 Archivos incluidos:"
echo "  ✅ Código fuente completo"
echo "  ✅ Configuración para Portainer"
echo "  ✅ Documentación completa"
echo "  ✅ Scripts de configuración"
echo ""
print_warning "📋 Próximos pasos en la VM:"
echo "  1. python generate_credentials.py"
echo "  2. docker network create npm_proxy"
echo "  3. Configurar stack en Portainer"
echo "  4. Configurar NPM"
echo ""
print_success "🎉 ¡Todo listo para producción!"