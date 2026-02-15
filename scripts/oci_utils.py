#!/usr/bin/env python3
"""
Utilidades para la administración de OCI (Oracle Cloud Infrastructure)
"""

import os
import sys
from typing import Dict, List, Optional

try:
    import oci
except ImportError:
    print("Error: El SDK de OCI no está instalado.")
    print("Instala con: pip install oci")
    sys.exit(1)


def obtener_config_oci(profile: str = "DEFAULT") -> Dict:
    """
    Obtiene la configuración de OCI desde el archivo de configuración.
    
    Args:
        profile: Perfil de configuración a utilizar
        
    Returns:
        Dict con la configuración de OCI
    """
    try:
        config = oci.config.from_file(profile_name=profile)
        oci.config.validate_config(config)
        return config
    except Exception as e:
        print(f"Error al cargar la configuración de OCI: {e}")
        print("\nAsegúrate de tener configurado el archivo ~/.oci/config")
        print("Consulta: https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm")
        sys.exit(1)


def obtener_cliente_compute(config: Dict) -> oci.core.ComputeClient:
    """
    Crea y retorna un cliente de Compute de OCI.
    
    Args:
        config: Configuración de OCI
        
    Returns:
        Cliente de Compute configurado
    """
    return oci.core.ComputeClient(config)


def obtener_cliente_monitoring(config: Dict) -> oci.monitoring.MonitoringClient:
    """
    Crea y retorna un cliente de Monitoring de OCI.
    
    Args:
        config: Configuración de OCI
        
    Returns:
        Cliente de Monitoring configurado
    """
    return oci.monitoring.MonitoringClient(config)


def formatear_instancia(instancia: oci.core.models.Instance) -> Dict:
    """
    Formatea la información de una instancia para su visualización.
    
    Args:
        instancia: Objeto de instancia de OCI
        
    Returns:
        Dict con información formateada
    """
    return {
        "id": instancia.id,
        "nombre": instancia.display_name,
        "estado": instancia.lifecycle_state,
        "compartment_id": instancia.compartment_id,
        "disponibilidad": instancia.availability_domain,
        "tipo": instancia.shape,
        "fecha_creacion": str(instancia.time_created),
    }


def listar_compartments(identity_client: oci.identity.IdentityClient, 
                        tenancy_id: str) -> List[oci.identity.models.Compartment]:
    """
    Lista todos los compartments en el tenancy.
    
    Args:
        identity_client: Cliente de Identity de OCI
        tenancy_id: ID del tenancy
        
    Returns:
        Lista de compartments
    """
    try:
        compartments = []
        # Implementar paginación para obtener todos los compartments
        response = identity_client.list_compartments(
            compartment_id=tenancy_id,
            compartment_id_in_subtree=True
        )
        compartments.extend(response.data)
        
        # Manejar paginación si hay más compartments
        while response.has_next_page:
            response = identity_client.list_compartments(
                compartment_id=tenancy_id,
                compartment_id_in_subtree=True,
                page=response.headers['opc-next-page']
            )
            compartments.extend(response.data)
        
        return compartments
    except Exception as e:
        print(f"Error al listar compartments: {e}")
        return []


def verificar_permisos() -> bool:
    """
    Verifica que las credenciales de OCI estén configuradas correctamente.
    
    Returns:
        True si las credenciales son válidas, False en caso contrario
    """
    try:
        config = obtener_config_oci()
        identity_client = oci.identity.IdentityClient(config)
        user = identity_client.get_user(config["user"]).data
        print(f"✓ Autenticado como: {user.name}")
        return True
    except Exception as e:
        print(f"✗ Error de autenticación: {e}")
        return False
