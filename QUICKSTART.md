# 🚀 Guía de Inicio Rápido

Esta guía te ayudará a comenzar a usar los scripts de administración de OCI en minutos.

## Paso 1: Instalar dependencias

```bash
pip install -r requirements.txt
```

## Paso 2: Configurar credenciales de OCI

### Opción A: Configuración manual

1. Crea el directorio de configuración:
```bash
mkdir -p ~/.oci
```

2. Crea el archivo `~/.oci/config`:
```bash
nano ~/.oci/config
```

3. Agrega tu configuración:
```ini
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaxxxxx
fingerprint=aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99
tenancy=ocid1.tenancy.oc1..aaaaaaaxxxxx
region=us-ashburn-1
key_file=~/.oci/oci_api_key.pem
```

4. Copia tu clave privada API:
```bash
cp /ruta/a/tu/clave.pem ~/.oci/oci_api_key.pem
chmod 600 ~/.oci/oci_api_key.pem
```

### Opción B: Usar OCI CLI

Si ya tienes OCI CLI instalado y configurado, los scripts usarán automáticamente esa configuración.

## Paso 3: Probar la conexión

```bash
cd scripts
python listar_instancias.py --list-compartments
```

Si ves una lista de compartments, ¡estás listo para comenzar!

## Ejemplos de Uso Común

### Ver todas tus instancias

```bash
# 1. Obtén tu compartment ID
python listar_instancias.py --list-compartments

# 2. Lista las instancias
python listar_instancias.py --compartment-id ocid1.compartment.oc1..xxxxx
```

### Iniciar/Detener instancias

```bash
# Iniciar
python actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --iniciar

# Detener
python actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --detener
```

### Monitorear rendimiento

```bash
python monitorear_instancias.py \
    --instance-id ocid1.instance.oc1..xxxxx \
    --compartment-id ocid1.compartment.oc1..xxxxx
```

## Solución de Problemas

### Error: "No module named 'oci'"
```bash
pip install oci
```

### Error: "Error al cargar la configuración de OCI"
- Verifica que el archivo `~/.oci/config` existe
- Verifica que las credenciales son correctas
- Asegúrate de que la clave privada está en la ubicación correcta

### Error: "ServiceError"
- Verifica que tienes los permisos necesarios en IAM
- Confirma que el compartment ID o instance ID es correcto
- Verifica que estás usando la región correcta

## Recursos Adicionales

- [Generar claves API de OCI](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm)
- [Configurar el SDK de OCI](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm)
- [Permisos de IAM](https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/policies.htm)

## ¿Necesitas ayuda?

Si encuentras problemas:
1. Revisa la [documentación completa](README.md)
2. Verifica que tu configuración de OCI es correcta
3. Asegúrate de tener los permisos necesarios en tu tenancy
