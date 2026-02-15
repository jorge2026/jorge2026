#!/usr/bin/env python3
"""
Script para actualizar instancias de OCI (Oracle Cloud Infrastructure)

Este script permite realizar operaciones de actualización sobre instancias,
como iniciar, detener, reiniciar, y cambiar el nombre de las instancias.
"""

import argparse
import sys
import time
from typing import Optional

try:
    import oci
    from oci_utils import (
        obtener_config_oci,
        obtener_cliente_compute,
        formatear_instancia,
        verificar_permisos
    )
except ImportError as e:
    print(f"Error al importar módulos requeridos: {e}")
    print("Asegúrate de instalar las dependencias: pip install -r requirements.txt")
    sys.exit(1)


def obtener_instancia(compute_client: oci.core.ComputeClient, 
                      instance_id: str) -> Optional[oci.core.models.Instance]:
    """
    Obtiene la información de una instancia específica.
    
    Args:
        compute_client: Cliente de Compute de OCI
        instance_id: ID de la instancia
        
    Returns:
        Objeto Instance o None si no se encuentra
    """
    try:
        instance = compute_client.get_instance(instance_id).data
        return instance
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error al obtener instancia: {e.message}")
        return None


def iniciar_instancia(instance_id: str, config_profile: str = "DEFAULT") -> bool:
    """
    Inicia una instancia detenida.
    
    Args:
        instance_id: ID de la instancia a iniciar
        config_profile: Perfil de configuración de OCI
        
    Returns:
        True si la operación fue exitosa, False en caso contrario
    """
    config = obtener_config_oci(config_profile)
    compute_client = obtener_cliente_compute(config)
    
    try:
        instance = obtener_instancia(compute_client, instance_id)
        if not instance:
            return False
        
        print(f"\n🚀 Iniciando instancia: {instance.display_name}")
        print(f"   Estado actual: {instance.lifecycle_state}")
        
        if instance.lifecycle_state == "RUNNING":
            print("   ℹ️  La instancia ya está en ejecución.")
            return True
        
        compute_client.instance_action(instance_id, "START")
        print("   ✓ Solicitud de inicio enviada.")
        print("   ⏳ Esperando que la instancia esté en ejecución...")
        
        # Esperar hasta que la instancia esté en ejecución
        oci.wait_until(
            compute_client,
            compute_client.get_instance(instance_id),
            'lifecycle_state',
            'RUNNING',
            max_wait_seconds=300
        )
        
        print("   ✓ Instancia iniciada correctamente.")
        return True
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error del servicio OCI: {e.message}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False


def detener_instancia(instance_id: str, config_profile: str = "DEFAULT") -> bool:
    """
    Detiene una instancia en ejecución.
    
    Args:
        instance_id: ID de la instancia a detener
        config_profile: Perfil de configuración de OCI
        
    Returns:
        True si la operación fue exitosa, False en caso contrario
    """
    config = obtener_config_oci(config_profile)
    compute_client = obtener_cliente_compute(config)
    
    try:
        instance = obtener_instancia(compute_client, instance_id)
        if not instance:
            return False
        
        print(f"\n🛑 Deteniendo instancia: {instance.display_name}")
        print(f"   Estado actual: {instance.lifecycle_state}")
        
        if instance.lifecycle_state == "STOPPED":
            print("   ℹ️  La instancia ya está detenida.")
            return True
        
        compute_client.instance_action(instance_id, "STOP")
        print("   ✓ Solicitud de detención enviada.")
        print("   ⏳ Esperando que la instancia se detenga...")
        
        # Esperar hasta que la instancia esté detenida
        oci.wait_until(
            compute_client,
            compute_client.get_instance(instance_id),
            'lifecycle_state',
            'STOPPED',
            max_wait_seconds=300
        )
        
        print("   ✓ Instancia detenida correctamente.")
        return True
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error del servicio OCI: {e.message}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False


def reiniciar_instancia(instance_id: str, config_profile: str = "DEFAULT") -> bool:
    """
    Reinicia una instancia (soft reboot).
    
    Args:
        instance_id: ID de la instancia a reiniciar
        config_profile: Perfil de configuración de OCI
        
    Returns:
        True si la operación fue exitosa, False en caso contrario
    """
    config = obtener_config_oci(config_profile)
    compute_client = obtener_cliente_compute(config)
    
    try:
        instance = obtener_instancia(compute_client, instance_id)
        if not instance:
            return False
        
        print(f"\n🔄 Reiniciando instancia: {instance.display_name}")
        print(f"   Estado actual: {instance.lifecycle_state}")
        
        if instance.lifecycle_state != "RUNNING":
            print("   ✗ La instancia debe estar en ejecución para ser reiniciada.")
            return False
        
        compute_client.instance_action(instance_id, "SOFTRESET")
        print("   ✓ Solicitud de reinicio enviada.")
        print("   ⏳ Esperando que la instancia se reinicie...")
        
        # Esperar 5 segundos para que el comando de reinicio sea procesado
        # antes de empezar a verificar el estado de la instancia
        time.sleep(5)
        
        # Esperar hasta que la instancia vuelva a estar en ejecución
        oci.wait_until(
            compute_client,
            compute_client.get_instance(instance_id),
            'lifecycle_state',
            'RUNNING',
            max_wait_seconds=300
        )
        
        print("   ✓ Instancia reiniciada correctamente.")
        return True
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error del servicio OCI: {e.message}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False


def cambiar_nombre_instancia(instance_id: str, nuevo_nombre: str, 
                             config_profile: str = "DEFAULT") -> bool:
    """
    Cambia el nombre de visualización de una instancia.
    
    Args:
        instance_id: ID de la instancia
        nuevo_nombre: Nuevo nombre para la instancia
        config_profile: Perfil de configuración de OCI
        
    Returns:
        True si la operación fue exitosa, False en caso contrario
    """
    config = obtener_config_oci(config_profile)
    compute_client = obtener_cliente_compute(config)
    
    try:
        instance = obtener_instancia(compute_client, instance_id)
        if not instance:
            return False
        
        print(f"\n✏️  Cambiando nombre de instancia")
        print(f"   Nombre actual: {instance.display_name}")
        print(f"   Nombre nuevo: {nuevo_nombre}")
        
        update_details = oci.core.models.UpdateInstanceDetails(
            display_name=nuevo_nombre
        )
        
        compute_client.update_instance(instance_id, update_details)
        print("   ✓ Nombre actualizado correctamente.")
        return True
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error del servicio OCI: {e.message}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False


def mostrar_estado_instancia(instance_id: str, config_profile: str = "DEFAULT") -> None:
    """
    Muestra el estado actual de una instancia.
    
    Args:
        instance_id: ID de la instancia
        config_profile: Perfil de configuración de OCI
    """
    config = obtener_config_oci(config_profile)
    compute_client = obtener_cliente_compute(config)
    
    instance = obtener_instancia(compute_client, instance_id)
    if instance:
        info = formatear_instancia(instance)
        print(f"\n📊 Estado actual de la instancia:")
        print(f"   Nombre: {info['nombre']}")
        print(f"   Estado: {info['estado']}")
        print(f"   Tipo: {info['tipo']}")
        print(f"   Zona: {info['disponibilidad']}")


def main():
    """
    Función principal del script.
    """
    parser = argparse.ArgumentParser(
        description="Actualizar instancias de OCI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Iniciar una instancia
  python actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --iniciar
  
  # Detener una instancia
  python actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --detener
  
  # Reiniciar una instancia
  python actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --reiniciar
  
  # Cambiar nombre de una instancia
  python actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --nombre "Nuevo Nombre"
  
  # Ver estado actual
  python actualizar_instancias.py --instance-id ocid1.instance.oc1..xxxxx --estado
        """
    )
    
    parser.add_argument(
        "--instance-id",
        required=True,
        help="ID de la instancia a actualizar"
    )
    
    parser.add_argument(
        "--profile",
        default="DEFAULT",
        help="Perfil de configuración de OCI (default: DEFAULT)"
    )
    
    # Acciones
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--iniciar",
        action="store_true",
        help="Iniciar la instancia"
    )
    action_group.add_argument(
        "--detener",
        action="store_true",
        help="Detener la instancia"
    )
    action_group.add_argument(
        "--reiniciar",
        action="store_true",
        help="Reiniciar la instancia"
    )
    action_group.add_argument(
        "--nombre",
        help="Cambiar el nombre de la instancia"
    )
    action_group.add_argument(
        "--estado",
        action="store_true",
        help="Mostrar el estado actual de la instancia"
    )
    
    args = parser.parse_args()
    
    # Verificar permisos
    print("🔐 Verificando credenciales de OCI...")
    if not verificar_permisos():
        sys.exit(1)
    
    # Ejecutar la acción solicitada
    if args.iniciar:
        success = iniciar_instancia(args.instance_id, args.profile)
    elif args.detener:
        success = detener_instancia(args.instance_id, args.profile)
    elif args.reiniciar:
        success = reiniciar_instancia(args.instance_id, args.profile)
    elif args.nombre:
        success = cambiar_nombre_instancia(args.instance_id, args.nombre, args.profile)
    elif args.estado:
        mostrar_estado_instancia(args.instance_id, args.profile)
        return
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
