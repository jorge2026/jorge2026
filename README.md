# 🚀 Scripts de Administración OCI

<div align="center">
  
[![OCI](https://img.shields.io/badge/Oracle-Cloud-F80000?style=for-the-badge&logo=oracle&logoColor=white)](https://www.oracle.com/cloud/)
[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

<div align="center">
  <img height="140" src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExeW40Z2FnMjFjcThubG9jcWJ3bXFrdGFsZWxwNTU3NW4xengzNXY1MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/kXixecGzl2gBlpO4SQ/giphy.gif" alt="Welcome"/> 
</div>

Repositorio con **scripts simples** para la administración de instancias en **Oracle Cloud Infrastructure (OCI)**. Scripts en Python que permiten listar, actualizar y monitorear instancias de compute de manera eficiente.

> 🚀 **[Ver Guía de Inicio Rápido](QUICKSTART.md)** para comenzar en minutos

## 📋 Descripción

Este repositorio proporciona herramientas de línea de comandos para facilitar la administración diaria de recursos de OCI, específicamente instancias de compute. Los scripts están diseñados para ser simples, directos y fáciles de usar.

### ✨ Características

- 📊 **Listar instancias**: Visualiza todas las instancias en tus compartments
- 🔄 **Actualizar instancias**: Inicia, detén, reinicia o renombra instancias
- 📈 **Monitorear instancias**: Obtén métricas de CPU, memoria y disco
- 🔐 **Seguro**: Utiliza el SDK oficial de OCI con autenticación estándar
- 🌍 **Multi-región**: Soporte para múltiples regiones y perfiles

## 📁 Estructura del Repositorio

```
jorge2026/
├── scripts/
│   ├── oci_utils.py              # Utilidades y funciones comunes
│   ├── listar_instancias.py      # Script para listar instancias
│   ├── actualizar_instancias.py  # Script para actualizar instancias
│   └── monitorear_instancias.py  # Script para monitorear instancias
├── .env.example                   # Ejemplo de configuración
├── requirements.txt               # Dependencias de Python
├── .gitignore                     # Archivos ignorados
└── README.md                      # Este archivo
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.7 o superior
- Cuenta de Oracle Cloud Infrastructure
- Credenciales de API de OCI configuradas

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/jorge2026/jorge2026.git
cd jorge2026
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar credenciales de OCI

1. Crea el directorio de configuración:
```bash
mkdir -p ~/.oci
```

2. Configura tu archivo de credenciales `~/.oci/config`:
```ini
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaxxxxx
fingerprint=aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99
tenancy=ocid1.tenancy.oc1..aaaaaaaxxxxx
region=us-ashburn-1
key_file=~/.oci/oci_api_key.pem
```

3. Genera y configura tu clave API de OCI siguiendo la [documentación oficial](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm)

## 📖 Uso

### 1️⃣ Listar Instancias

Visualiza todas las instancias en un compartment:

```bash
# Listar compartments disponibles
python scripts/listar_instancias.py --list-compartments

# Listar todas las instancias en un compartment
python scripts/listar_instancias.py --compartment-id ocid1.compartment.oc1..xxxxx

# Listar solo instancias en ejecución
python scripts/listar_instancias.py --compartment-id ocid1.compartment.oc1..xxxxx --estado RUNNING
```

**Salida de ejemplo:**
```
🔐 Verificando credenciales de OCI...
✓ Autenticado como: jorge.rodriguez@example.com

📋 Se encontraron 3 instancia(s):

====================================================================================================

1. web-server-prod
   ID: ocid1.instance.oc1.iad.xxxxx
   Estado: RUNNING
   Tipo: VM.Standard2.1
   Zona de Disponibilidad: AD-1
   Fecha de Creación: 2024-01-15 10:30:00
```

### 2️⃣ Actualizar Instancias

Realiza operaciones de gestión sobre instancias:

```bash
# Iniciar una instancia detenida
python scripts/actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --iniciar

# Detener una instancia en ejecución
python scripts/actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --detener

# Reiniciar una instancia
python scripts/actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --reiniciar

# Cambiar el nombre de una instancia
python scripts/actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --nombre "nuevo-nombre"

# Ver estado actual
python scripts/actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --estado
```

**Salida de ejemplo:**
```
🔐 Verificando credenciales de OCI...
✓ Autenticado como: jorge.rodriguez@example.com

🚀 Iniciando instancia: web-server-prod
   Estado actual: STOPPED
   ✓ Solicitud de inicio enviada.
   ⏳ Esperando que la instancia esté en ejecución...
   ✓ Instancia iniciada correctamente.
```

### 3️⃣ Monitorear Instancias

Obtén métricas de rendimiento de tus instancias:

```bash
# Monitorear instancia (última hora)
python scripts/monitorear_instancias.py \
    --instance-id ocid1.instance.oc1..xxxxx \
    --compartment-id ocid1.compartment.oc1..xxxxx

# Monitorear con período personalizado (últimas 4 horas)
python scripts/monitorear_instancias.py \
    --instance-id ocid1.instance.oc1..xxxxx \
    --compartment-id ocid1.compartment.oc1..xxxxx \
    --minutos 240
```

**Salida de ejemplo:**
```
🔐 Verificando credenciales de OCI...
✓ Autenticado como: jorge.rodriguez@example.com

🔍 Monitoreando instancia: web-server-prod
   ID: ocid1.instance.oc1..xxxxx
   Estado: RUNNING
   Período: últimos 60 minutos

📊 Métricas de Monitoreo - web-server-prod
================================================================================

🖥️  Utilización de CPU:
   Promedio: 45.32%
   Mínimo: 12.50%
   Máximo: 89.20%
   Puntos de datos: 60

💾 Utilización de Memoria:
   Promedio: 62.15%
   Mínimo: 55.30%
   Máximo: 78.90%
   Puntos de datos: 60

💿 Operaciones de Disco:
   Lectura promedio: 1024.50 bytes/s
   Lectura máxima: 5120.00 bytes/s
   Escritura promedio: 2048.75 bytes/s
   Escritura máxima: 8192.00 bytes/s
```

## 🔧 Opciones Avanzadas

### Múltiples Perfiles

Puedes usar diferentes perfiles de configuración para gestionar múltiples tenancies o regiones:

```bash
# Usar un perfil específico
python scripts/listar_instancias.py --compartment-id ocid1.compartment.oc1..xxxxx --profile PROD
```

## 🛡️ Permisos Requeridos

Los scripts requieren los siguientes permisos de IAM en OCI:

- `INSTANCE_READ` - Para listar y obtener información de instancias
- `INSTANCE_UPDATE` - Para iniciar, detener y actualizar instancias
- `METRICS_READ` - Para leer métricas de monitoreo
- `COMPARTMENT_READ` - Para listar compartments

## 🔗 Relación con OCI

Estos scripts utilizan el [SDK oficial de Python para OCI](https://docs.oracle.com/en-us/iaas/tools/python/latest/index.html), lo que garantiza:

- ✅ Compatibilidad total con la API de OCI
- ✅ Autenticación segura mediante claves API
- ✅ Soporte para todas las regiones de OCI
- ✅ Actualizaciones regulares con nuevas características

## 📚 Recursos Adicionales

- [Documentación de OCI](https://docs.oracle.com/en-us/iaas/Content/home.htm)
- [SDK de Python para OCI](https://docs.oracle.com/en-us/iaas/tools/python/latest/index.html)
- [Guía de configuración del SDK](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm)
- [OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cliconcepts.htm)

## 👨‍💻 Autor

<div align="center"> 
  
**Jorge Rodriguez**

Enterprise Systems Engineer | AWS x3 - OCI x5 ☁️ | FinOps x2 - GreenOps x1 ♻️💰 | CyberSec 🔒 | Enterprise Arch 🏗️

<a href="https://www.linkedin.com/in/jorge-rodriguez-n/overlay/about-this-profile/" target="_blank"> <img src="https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white&style=for-the-badge" height="25" alt="LinkedIn"/> </a> <a href="https://www.youtube.com/@jorgeluisrn" target="_blank"> <img src="https://img.shields.io/badge/Youtube-FF0000?logo=youtube&logoColor=white&style=for-the-badge" height="25" alt="YouTube"/> </a> <a href="https://twitter.com/jorgeluisrn" target="_blank"> <img src="https://img.shields.io/badge/Twitter-1DA1F2?logo=twitter&logoColor=white&style=for-the-badge" height="25" alt="Twitter"/> </a>

</div>

---

<div align="center">

<h1 align="center">Habilidades y Experiencia 💼</h1>

</div>

## Habilidades técnicas (selección)
<p align="center">
  <a href="https://skillicons.dev" target="_blank">
    <img src="https://skillicons.dev/icons?i=git,githubactions,gitlab,jenkins,aws,gcp,azure,kubernetes,docker,ansible,terraform,kafka,prometheus,nginx,linux" alt="Tech icons" />
  </a>
  <a href="https://go-skill-icons.vercel.app/" target="_blank">
    <img src="https://go-skill-icons.vercel.app/api/icons?i=windows,bash,vim,vscode,go,py,oracle,opentelemetry,rancher,grafana,argocd,airflow,helm" alt="More tech icons" />
  </a>
</p>

## Marcos de Gobierno y Arquitectura (destacados)

<p align="center">
  <!-- Gobierno de servicios TI -->
  <a href="https://www.axelos.com/best-practice-solutions/itil" target="_blank">
    <img src="https://img.shields.io/badge/ITIL-4-0052CC?style=for-the-badge&logo=itil" alt="ITIL"/>
  </a>
  <a href="https://www.isaca.org/resources/cobit" target="_blank">
    <img src="https://img.shields.io/badge/COBIT-2019-0A2740?style=for-the-badge" alt="COBIT"/>
  </a>
  <a href="https://www.opengroup.org/it4it" target="_blank">
    <img src="https://img.shields.io/badge/IT4IT-OTG-007ACC?style=for-the-badge" alt="IT4IT"/>
  </a>
  <a href="https://www.tmforum.org/" target="_blank">
    <img src="https://img.shields.io/badge/Service-Governance-6f42c1?style=for-the-badge" alt="Service Governance"/>
  </a>
</p>

<p align="center">
  <!-- Arquitectura Empresarial -->
  <a href="https://pubs.opengroup.org/architecture/togaf9-doc/arch/" target="_blank">
    <img src="https://img.shields.io/badge/TOGAF-9.2-3E7CB1?style=for-the-badge" alt="TOGAF"/>
  </a>
  <a href="https://www.zachman.com/" target="_blank">
    <img src="https://img.shields.io/badge/Zachman-Framework-2E8B57?style=for-the-badge" alt="Zachman"/>
  </a>
</p>

<p align="center">
  <!-- Marcos de referencia por dominios de AE -->
  <a href="https://bian.org/" target="_blank">
    <img src="https://img.shields.io/badge/BIAN-Banking-0066CC?style=for-the-badge" alt="BIAN"/>
  </a>
  <a href="https://learn.microsoft.com/azure/architecture/cloud-adoption/" target="_blank">
    <img src="https://img.shields.io/badge/CAF-Cloud%20Adoption-0089D6?style=for-the-badge" alt="CAF"/>
  </a>
  <a href="https://www.dama.org/" target="_blank">
    <img src="https://img.shields.io/badge/DAMA-DMBOK-943b97?style=for-the-badge" alt="DAMA"/>
  </a>
  <a href="https://businessarchitectureguild.org/bizbok/" target="_blank">
    <img src="https://img.shields.io/badge/BIZBOK-Business%20Architecture-EA2B1D?style=for-the-badge" alt="BIZBOK"/>
  </a>
</p>
