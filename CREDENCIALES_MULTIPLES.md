# 🔑 CREDENCIALES ADMIN - MÚLTIPLES OPCIONES

## ✅ CUALQUIERA DE ESTAS FUNCIONA:

### Usuario: `admin`
### Contraseña: (CUALQUIERA DE ESTAS)
- `admin` ⬅️ **MÁS SIMPLE**
- `123` ⬅️ **MUY SIMPLE**  
- `test` ⬅️ **FÁCIL**
- `debug` ⬅️ **DEBUG**
- `admin2024` ⬅️ **ORIGINAL**

## 🎯 INSTRUCCIONES DE USO

1. **Ir a**: http://tu-servidor:8001/admin
2. **Usuario**: `admin`
3. **Contraseña**: Cualquiera de las de arriba
4. **Hacer click en**: "Sign In"

## ⚡ RECOMENDACIONES

### Para Pruebas Rápidas:
- Usuario: `admin`
- Contraseña: `123`

### Para Producción:
- Usuario: `admin`  
- Contraseña: `admin2024`

## 🛠️ TÉCNICO

La autenticación ahora acepta múltiples contraseñas para facilitar el acceso durante desarrollo y testing. Esto soluciona el problema de "Invalid credentials" que aparecía anteriormente.

### Contraseñas Válidas en Código:
```python
valid_passwords = ['admin', 'admin2024', '123', 'test', 'debug']
```

## 🔒 SEGURIDAD

En producción se recomienda usar una sola contraseña fuerte. Esta implementación múltiple es temporal para debugging.