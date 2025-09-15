# 🚨 SOLUCIÓN: Docker no está ejecutándose

## Problema Identificado
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. 
Is the docker daemon running?
```

**Causa**: El servicio de Docker no está iniciado en tu sistema.

---

## 🔧 Solución Rápida

### Opción 1: Script Automático
```bash
./start_docker.sh
```

### Opción 2: Manual según tu sistema operativo

#### 🍎 **macOS**
```bash
# Verificar si Docker Desktop está instalado
ls /Applications/Docker.app

# Iniciar Docker Desktop
open -a Docker

# O desde Spotlight: Cmd+Space → "Docker"
```

**Esperar hasta que**:
- Aparezca la ballena en la barra de menú superior
- El ícono no tenga puntos de carga
- Diga "Docker Desktop is running"

#### 🐧 **Linux (Ubuntu/Debian)**
```bash
# Verificar estado
sudo systemctl status docker

# Iniciar Docker
sudo systemctl start docker

# Habilitar inicio automático
sudo systemctl enable docker

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Aplicar cambios (reiniciar sesión o):
newgrp docker
```

#### 🪟 **Windows**
1. **Instalar Docker Desktop** (si no está instalado):
   - Descargar de: https://docs.docker.com/desktop/windows/install/
   
2. **Iniciar Docker Desktop**:
   - Buscar "Docker Desktop" en el menú inicio
   - Ejecutar como administrador si es necesario
   - Esperar hasta que aparezca la ballena en la bandeja del sistema

---

## ✅ Verificación

### Verificar que Docker funciona:
```bash
docker --version
docker info
docker run hello-world
```

**Resultado esperado**:
```
Docker version 20.x.x
Server: Docker Desktop
...
Hello from Docker!
```

---

## 🚀 Después de iniciar Docker

### 1. Verificar que Docker está corriendo:
```bash
docker info
```

### 2. Ejecutar el deploy de tu aplicación:
```bash
./fix_containers.sh
```

### 3. O manualmente:
```bash
docker-compose up -d --build
```

### 4. Verificar servicios:
```bash
docker-compose ps
```

---

## 🚨 Problemas Comunes

### **"Permission denied"** (Linux)
```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión o aplicar cambios
newgrp docker

# Verificar
groups $USER
```

### **Docker Desktop no inicia** (macOS/Windows)
1. **Reiniciar la aplicación**
2. **Verificar recursos del sistema** (RAM, CPU)
3. **Actualizar Docker Desktop**
4. **Reiniciar el sistema**

### **"docker: command not found"**
- **macOS**: Instalar Docker Desktop
- **Linux**: 
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```
- **Windows**: Instalar Docker Desktop

### **WSL2 requerido** (Windows)
1. Habilitar WSL2
2. Instalar distribución Linux (Ubuntu)
3. Configurar Docker Desktop para usar WSL2

---

## 📋 Checklist de Instalación

### macOS:
- [ ] Docker Desktop descargado e instalado
- [ ] Docker Desktop iniciado
- [ ] Ballena visible en barra de menú
- [ ] `docker info` funciona

### Linux:
- [ ] Docker instalado (`docker --version`)
- [ ] Servicio iniciado (`sudo systemctl start docker`)
- [ ] Usuario en grupo docker (`groups $USER`)
- [ ] `docker info` funciona sin sudo

### Windows:
- [ ] WSL2 habilitado (si es necesario)
- [ ] Docker Desktop instalado
- [ ] Docker Desktop corriendo
- [ ] Ballena en bandeja del sistema
- [ ] `docker info` funciona

---

## 🎯 Pasos Siguientes

Una vez que Docker esté funcionando:

1. **Verificar Docker**:
   ```bash
   docker run hello-world
   ```

2. **Deployar tu aplicación**:
   ```bash
   ./fix_containers.sh
   ```

3. **Acceder a la aplicación**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8001/api
   - Admin: Clic "Admin" → admin/admin2024

---

## 📞 Si Sigues Teniendo Problemas

1. **Comparte**:
   - Tu sistema operativo
   - Versión de Docker (`docker --version`)
   - Output completo del error

2. **Verifica recursos**:
   - RAM disponible (Docker necesita ~2GB)
   - Espacio en disco
   - CPU no saturada

3. **Logs del sistema**:
   - **macOS**: Console.app → buscar "Docker"
   - **Linux**: `journalctl -u docker.service`
   - **Windows**: Event Viewer → Application logs

---

🎉 **Una vez que Docker esté corriendo, tu aplicación funcionará perfectamente!**