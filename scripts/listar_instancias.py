#!/usr/bin/env python3
"""
Script para listar instancias de OCI (Oracle Cloud Infrastructure)

Este script permite visualizar todas las instancias de compute en tu tenancy de OCI,
con opciones para filtrar por compartment y estado.
"""

import argparse
import sys
from typing import List, Optional

try:
    import oci
    from oci_utils import (
        obtener_config_oci,
        obtener_cliente_compute,
        formatear_instancia,
        listar_compartments,
        verificar_permisos
    )
except ImportError as e:
    print(f"Error al importar módulos requeridos: {e}")
    print("Asegúrate de instalar las dependencias: pip install -r requirements.txt")
    sys.exit(1)


def listar_instancias(compartment_id: str, 
                      estado: Optional[str] = None,
                      config_profile: str = "DEFAULT") -> List[dict]:
    """
    Lista todas las instancias en un compartment específico.
    
    Args:
        compartment_id: ID del compartment a consultar
        estado: Estado de las instancias a filtrar (RUNNING, STOPPED, etc.)
        config_profile: Perfil de configuración de OCI a utilizar
        
    Returns:
        Lista de diccionarios con información de las instancias
    """
    config = obtener_config_oci(config_profile)
    compute_client = obtener_cliente_compute(config)
    
    try:
        print(f"\n🔍 Buscando instancias en compartment: {compartment_id}")
        
        # Listar instancias con paginación
        if estado:
            print(f"   Filtrando por estado: {estado}")
            response = compute_client.list_instances(
                compartment_id=compartment_id,
                lifecycle_state=estado
            )
        else:
            response = compute_client.list_instances(
                compartment_id=compartment_id
            )
        
        instances = list(response.data)
        
        # Manejar paginación para obtener todas las instancias
        while response.has_next_page:
            if estado:
                response = compute_client.list_instances(
                    compartment_id=compartment_id,
                    lifecycle_state=estado,
                    page=response.headers['opc-next-page']
                )
            else:
                response = compute_client.list_instances(
                    compartment_id=compartment_id,
                    page=response.headers['opc-next-page']
                )
            instances.extend(response.data)
        
        instancias_formateadas = [formatear_instancia(inst) for inst in instances]
        
        return instancias_formateadas
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error del servicio OCI: {e.message}")
        return []
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return []


def mostrar_instancias(instancias: List[dict]) -> None:
    """
    Muestra las instancias en formato legible.
    
    Args:
        instancias: Lista de instancias a mostrar
    """
    if not instancias:
        print("\n📋 No se encontraron instancias.")
        return
    
    print(f"\n📋 Se encontraron {len(instancias)} instancia(s):\n")
    print("=" * 100)
    
    for idx, inst in enumerate(instancias, 1):
        print(f"\n{idx}. {inst['nombre']}")
        print(f"   ID: {inst['id']}")
        print(f"   Estado: {inst['estado']}")
        print(f"   Tipo: {inst['tipo']}")
        print(f"   Zona de Disponibilidad: {inst['disponibilidad']}")
        print(f"   Fecha de Creación: {inst['fecha_creacion']}")
        print("-" * 100)


def listar_todos_los_compartments(config_profile: str = "DEFAULT") -> None:
    """
    Lista todos los compartments disponibles en el tenancy.
    
    Args:
        config_profile: Perfil de configuración de OCI a utilizar
    """
    config = obtener_config_oci(config_profile)
    identity_client = oci.identity.IdentityClient(config)
    
    try:
        tenancy_id = config["tenancy"]
        print(f"\n📂 Compartments disponibles en el tenancy:\n")
        
        # Listar el compartment raíz
        root_compartment = identity_client.get_compartment(tenancy_id).data
        print(f"1. {root_compartment.name} (Root)")
        print(f"   ID: {root_compartment.id}")
        print(f"   Estado: {root_compartment.lifecycle_state}")
        
        # Listar sub-compartments
        compartments = listar_compartments(identity_client, tenancy_id)
        for idx, comp in enumerate(compartments, 2):
            print(f"\n{idx}. {comp.name}")
            print(f"   ID: {comp.id}")
            print(f"   Estado: {comp.lifecycle_state}")
            print(f"   Descripción: {comp.description or 'N/A'}")
        
    except Exception as e:
        print(f"✗ Error al listar compartments: {e}")


def main():
    """
    Función principal del script.
    """
    parser = argparse.ArgumentParser(
        description="Lista instancias de OCI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Listar compartments disponibles
  python listar_instancias.py --list-compartments
  
  # Listar todas las instancias en un compartment
  python listar_instancias.py --compartment-id ocid1.compartment.oc1..xxxxx
  
  # Listar solo instancias en ejecución
  python listar_instancias.py --compartment-id ocid1.compartment.oc1..xxxxx --estado RUNNING
  
  # Usar un perfil de configuración diferente
  python listar_instancias.py --compartment-id ocid1.compartment.oc1..xxxxx --profile PROD
        """
    )
    
    parser.add_argument(
        "--compartment-id",
        help="ID del compartment a consultar"
    )
    
    parser.add_argument(
        "--estado",
        choices=["RUNNING", "STOPPED", "TERMINATED", "TERMINATING", "STOPPING", "STARTING"],
        help="Filtrar por estado de la instancia"
    )
    
    parser.add_argument(
        "--profile",
        default="DEFAULT",
        help="Perfil de configuración de OCI (default: DEFAULT)"
    )
    
    parser.add_argument(
        "--list-compartments",
        action="store_true",
        help="Listar todos los compartments disponibles"
    )
    
    args = parser.parse_args()
    
    # Verificar permisos
    print("🔐 Verificando credenciales de OCI...")
    if not verificar_permisos():
        sys.exit(1)
    
    # Listar compartments si se solicita
    if args.list_compartments:
        listar_todos_los_compartments(args.profile)
        return
    
    # Validar que se proporcione compartment-id
    if not args.compartment_id:
        parser.error("Se requiere --compartment-id o --list-compartments")
    
    # Listar instancias
    instancias = listar_instancias(
        args.compartment_id,
        args.estado,
        args.profile
    )
    
    mostrar_instancias(instancias)


if __name__ == "__main__":
    main()
