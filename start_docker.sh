#!/bin/bash

# Script para iniciar Docker según el sistema operativo
echo "🐳 Iniciando Docker..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detectar sistema operativo  
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

print_status "Sistema detectado: $MACHINE"

# Función para verificar si Docker está corriendo
check_docker() {
    if docker info >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Función para macOS
start_docker_mac() {
    print_status "Iniciando Docker en macOS..."
    
    # Verificar si Docker Desktop está instalado
    if [ -d "/Applications/Docker.app" ]; then
        print_status "Docker Desktop encontrado, iniciando..."
        open -a Docker
        
        print_status "Esperando que Docker inicie..."
        for i in {1..30}; do
            if check_docker; then
                print_success "Docker iniciado correctamente!"
                return 0
            fi
            echo -n "."
            sleep 2
        done
        
        print_error "Docker no inició después de 60 segundos"
        return 1
    else
        print_error "Docker Desktop no está instalado"
        echo "Descarga Docker Desktop desde: https://docs.docker.com/desktop/mac/install/"
        return 1
    fi
}

# Función para Linux
start_docker_linux() {
    print_status "Iniciando Docker en Linux..."
    
    # Verificar si Docker está instalado
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        echo "Instala Docker con:"
        echo "curl -fsSL https://get.docker.com -o get-docker.sh"
        echo "sudo sh get-docker.sh"
        return 1
    fi
    
    # Iniciar servicio de Docker
    if systemctl is-active --quiet docker; then
        print_success "Docker ya está corriendo"
    else
        print_status "Iniciando servicio de Docker..."
        sudo systemctl start docker
        
        if systemctl is-active --quiet docker; then
            print_success "Docker iniciado correctamente!"
        else
            print_error "No se pudo iniciar Docker"
            echo "Intenta manualmente:"
            echo "sudo systemctl start docker"
            echo "sudo systemctl enable docker"
            return 1
        fi
    fi
    
    # Verificar permisos
    if ! docker info >/dev/null 2>&1; then
        print_warning "Problema de permisos detectado"
        echo "Agregando usuario al grupo docker..."
        sudo usermod -aG docker $USER
        print_warning "Necesitas cerrar sesión y volver a entrar, o ejecutar:"
        echo "newgrp docker"
        return 1
    fi
    
    return 0
}

# Función para Windows
start_docker_windows() {
    print_status "Sistema Windows detectado"
    print_warning "Para Windows, debes:"
    echo "1. Asegúrate de que Docker Desktop esté instalado"
    echo "2. Inicia Docker Desktop desde el menú de inicio"
    echo "3. Espera a que aparezca la ballena en la bandeja del sistema"
    echo ""
    echo "Si no tienes Docker Desktop:"
    echo "https://docs.docker.com/desktop/windows/install/"
}

# Ejecutar según el sistema
case $MACHINE in
    Mac)
        start_docker_mac
        ;;
    Linux)
        start_docker_linux
        ;;
    Cygwin|MinGw)
        start_docker_windows
        ;;
    *)
        print_error "Sistema operativo no soportado: $MACHINE"
        exit 1
        ;;
esac

# Verificación final
print_status "Verificando Docker..."
if check_docker; then
    print_success "✅ Docker está funcionando correctamente!"
    echo ""
    echo "Información de Docker:"
    docker version --format 'Version: {{.Server.Version}}'
    echo ""
    echo "Ahora puedes ejecutar:"
    echo "  ./fix_containers.sh"
    echo "  O: docker-compose up -d"
else
    print_error "❌ Docker aún no está funcionando"
    echo ""
    echo "Soluciones manuales:"
    echo ""
    case $MACHINE in
        Mac)
            echo "macOS:"
            echo "  1. Abre Docker Desktop desde Applications"
            echo "  2. Espera a que aparezca la ballena en la barra de menú"
            echo "  3. Verifica que diga 'Docker Desktop is running'"
            ;;
        Linux)
            echo "Linux:"
            echo "  1. sudo systemctl start docker"
            echo "  2. sudo systemctl enable docker"
            echo "  3. sudo usermod -aG docker \$USER"
            echo "  4. Reinicia sesión o ejecuta: newgrp docker"
            ;;
        *)
            echo "Windows:"
            echo "  1. Instala Docker Desktop"
            echo "  2. Inicia Docker Desktop"
            echo "  3. Espera a que esté 'running'"
            ;;
    esac
fi