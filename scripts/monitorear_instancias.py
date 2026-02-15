#!/usr/bin/env python3
"""
Script para monitorear instancias de OCI (Oracle Cloud Infrastructure)

Este script permite obtener métricas de monitoreo de instancias,
incluyendo CPU, memoria, y operaciones de disco.
"""

import argparse
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

try:
    import oci
    from oci_utils import (
        obtener_config_oci,
        obtener_cliente_compute,
        obtener_cliente_monitoring,
        verificar_permisos
    )
except ImportError as e:
    print(f"Error al importar módulos requeridos: {e}")
    print("Asegúrate de instalar las dependencias: pip install -r requirements.txt")
    sys.exit(1)


def obtener_metricas_cpu(monitoring_client: oci.monitoring.MonitoringClient,
                         compartment_id: str,
                         instance_id: str,
                         minutos: int = 60) -> Optional[List]:
    """
    Obtiene las métricas de utilización de CPU de una instancia.
    
    Args:
        monitoring_client: Cliente de Monitoring de OCI
        compartment_id: ID del compartment
        instance_id: ID de la instancia
        minutos: Número de minutos hacia atrás para consultar métricas
        
    Returns:
        Lista de puntos de datos de métricas
    """
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=minutos)
        
        query = f"""
        CpuUtilization[1m].mean(){{
            resourceId = "{instance_id}"
        }}
        """
        
        summarize_metrics_data_details = oci.monitoring.models.SummarizeMetricsDataDetails(
            namespace="oci_computeagent",
            query=query,
            start_time=start_time,
            end_time=end_time,
            resolution="1m"
        )
        
        response = monitoring_client.summarize_metrics_data(
            compartment_id=compartment_id,
            summarize_metrics_data_details=summarize_metrics_data_details
        )
        
        return response.data
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error al obtener métricas de CPU: {e.message}")
        return None
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return None


def obtener_metricas_memoria(monitoring_client: oci.monitoring.MonitoringClient,
                             compartment_id: str,
                             instance_id: str,
                             minutos: int = 60) -> Optional[List]:
    """
    Obtiene las métricas de utilización de memoria de una instancia.
    
    Args:
        monitoring_client: Cliente de Monitoring de OCI
        compartment_id: ID del compartment
        instance_id: ID de la instancia
        minutos: Número de minutos hacia atrás para consultar métricas
        
    Returns:
        Lista de puntos de datos de métricas
    """
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=minutos)
        
        query = f"""
        MemoryUtilization[1m].mean(){{
            resourceId = "{instance_id}"
        }}
        """
        
        summarize_metrics_data_details = oci.monitoring.models.SummarizeMetricsDataDetails(
            namespace="oci_computeagent",
            query=query,
            start_time=start_time,
            end_time=end_time,
            resolution="1m"
        )
        
        response = monitoring_client.summarize_metrics_data(
            compartment_id=compartment_id,
            summarize_metrics_data_details=summarize_metrics_data_details
        )
        
        return response.data
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error al obtener métricas de memoria: {e.message}")
        return None
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return None


def obtener_metricas_disco(monitoring_client: oci.monitoring.MonitoringClient,
                           compartment_id: str,
                           instance_id: str,
                           minutos: int = 60) -> Optional[Dict]:
    """
    Obtiene las métricas de operaciones de disco de una instancia.
    
    Args:
        monitoring_client: Cliente de Monitoring de OCI
        compartment_id: ID del compartment
        instance_id: ID de la instancia
        minutos: Número de minutos hacia atrás para consultar métricas
        
    Returns:
        Dict con métricas de lectura y escritura de disco
    """
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=minutos)
        
        # Métricas de lectura de disco
        query_read = f"""
        DiskBytesRead[1m].rate(){{
            resourceId = "{instance_id}"
        }}
        """
        
        # Métricas de escritura de disco
        query_write = f"""
        DiskBytesWritten[1m].rate(){{
            resourceId = "{instance_id}"
        }}
        """
        
        # Obtener métricas de lectura
        read_details = oci.monitoring.models.SummarizeMetricsDataDetails(
            namespace="oci_computeagent",
            query=query_read,
            start_time=start_time,
            end_time=end_time,
            resolution="1m"
        )
        
        read_response = monitoring_client.summarize_metrics_data(
            compartment_id=compartment_id,
            summarize_metrics_data_details=read_details
        )
        
        # Obtener métricas de escritura
        write_details = oci.monitoring.models.SummarizeMetricsDataDetails(
            namespace="oci_computeagent",
            query=query_write,
            start_time=start_time,
            end_time=end_time,
            resolution="1m"
        )
        
        write_response = monitoring_client.summarize_metrics_data(
            compartment_id=compartment_id,
            summarize_metrics_data_details=write_details
        )
        
        return {
            "read": read_response.data,
            "write": write_response.data
        }
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error al obtener métricas de disco: {e.message}")
        return None
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return None


def calcular_estadisticas(metricas_data: List) -> Dict:
    """
    Calcula estadísticas básicas de los puntos de datos de métricas.
    
    Args:
        metricas_data: Lista de datos de métricas
        
    Returns:
        Dict con estadísticas calculadas
    """
    if not metricas_data or len(metricas_data) == 0:
        return {"min": 0, "max": 0, "avg": 0, "count": 0}
    
    valores = []
    for metric in metricas_data:
        if metric.aggregated_datapoints:
            for point in metric.aggregated_datapoints:
                if point.value is not None:
                    valores.append(point.value)
    
    if not valores:
        return {"min": 0, "max": 0, "avg": 0, "count": 0}
    
    return {
        "min": min(valores),
        "max": max(valores),
        "avg": sum(valores) / len(valores),
        "count": len(valores)
    }


def mostrar_metricas(instance_name: str, cpu_stats: Dict, mem_stats: Dict, 
                    disk_stats: Dict) -> None:
    """
    Muestra las métricas en formato legible.
    
    Args:
        instance_name: Nombre de la instancia
        cpu_stats: Estadísticas de CPU
        mem_stats: Estadísticas de memoria
        disk_stats: Estadísticas de disco
    """
    print(f"\n📊 Métricas de Monitoreo - {instance_name}")
    print("=" * 80)
    
    print("\n🖥️  Utilización de CPU:")
    print(f"   Promedio: {cpu_stats['avg']:.2f}%")
    print(f"   Mínimo: {cpu_stats['min']:.2f}%")
    print(f"   Máximo: {cpu_stats['max']:.2f}%")
    print(f"   Puntos de datos: {cpu_stats['count']}")
    
    print("\n💾 Utilización de Memoria:")
    print(f"   Promedio: {mem_stats['avg']:.2f}%")
    print(f"   Mínimo: {mem_stats['min']:.2f}%")
    print(f"   Máximo: {mem_stats['max']:.2f}%")
    print(f"   Puntos de datos: {mem_stats['count']}")
    
    print("\n💿 Operaciones de Disco:")
    if disk_stats.get('read_stats'):
        print(f"   Lectura promedio: {disk_stats['read_stats']['avg']:.2f} bytes/s")
        print(f"   Lectura máxima: {disk_stats['read_stats']['max']:.2f} bytes/s")
    if disk_stats.get('write_stats'):
        print(f"   Escritura promedio: {disk_stats['write_stats']['avg']:.2f} bytes/s")
        print(f"   Escritura máxima: {disk_stats['write_stats']['max']:.2f} bytes/s")
    
    print("\n" + "=" * 80)


def monitorear_instancia(instance_id: str, compartment_id: str,
                        minutos: int = 60, config_profile: str = "DEFAULT") -> bool:
    """
    Monitorea una instancia y muestra sus métricas.
    
    Args:
        instance_id: ID de la instancia a monitorear
        compartment_id: ID del compartment
        minutos: Número de minutos de historial a consultar
        config_profile: Perfil de configuración de OCI
        
    Returns:
        True si la operación fue exitosa, False en caso contrario
    """
    config = obtener_config_oci(config_profile)
    compute_client = obtener_cliente_compute(config)
    monitoring_client = obtener_cliente_monitoring(config)
    
    try:
        # Obtener información de la instancia
        instance = compute_client.get_instance(instance_id).data
        print(f"\n🔍 Monitoreando instancia: {instance.display_name}")
        print(f"   ID: {instance_id}")
        print(f"   Estado: {instance.lifecycle_state}")
        print(f"   Período: últimos {minutos} minutos")
        
        if instance.lifecycle_state != "RUNNING":
            print("\n⚠️  Advertencia: La instancia no está en ejecución.")
            print("   Las métricas pueden no estar disponibles.")
        
        # Obtener métricas
        print("\n⏳ Obteniendo métricas...")
        
        cpu_data = obtener_metricas_cpu(
            monitoring_client, compartment_id, instance_id, minutos
        )
        mem_data = obtener_metricas_memoria(
            monitoring_client, compartment_id, instance_id, minutos
        )
        disk_data = obtener_metricas_disco(
            monitoring_client, compartment_id, instance_id, minutos
        )
        
        # Calcular estadísticas
        cpu_stats = calcular_estadisticas(cpu_data) if cpu_data else {"min": 0, "max": 0, "avg": 0, "count": 0}
        mem_stats = calcular_estadisticas(mem_data) if mem_data else {"min": 0, "max": 0, "avg": 0, "count": 0}
        
        disk_stats = {}
        if disk_data:
            disk_stats['read_stats'] = calcular_estadisticas(disk_data.get('read', []))
            disk_stats['write_stats'] = calcular_estadisticas(disk_data.get('write', []))
        
        # Mostrar resultados
        mostrar_metricas(instance.display_name, cpu_stats, mem_stats, disk_stats)
        
        if cpu_stats['count'] == 0 and mem_stats['count'] == 0:
            print("\n⚠️  No se encontraron métricas para el período especificado.")
            print("   Verifica que el agente de monitoreo esté instalado en la instancia.")
            print("   Consulta: https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/manage-plugins.htm")
        
        return True
        
    except oci.exceptions.ServiceError as e:
        print(f"✗ Error del servicio OCI: {e.message}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False


def main():
    """
    Función principal del script.
    """
    parser = argparse.ArgumentParser(
        description="Monitorear instancias de OCI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Monitorear una instancia (última hora)
  python monitorear_instancias.py --instance-id ocid1.instance.oc1..xxxxx \\
                                   --compartment-id ocid1.compartment.oc1..xxxxx
  
  # Monitorear con período personalizado (últimas 4 horas)
  python monitorear_instancias.py --instance-id ocid1.instance.oc1..xxxxx \\
                                   --compartment-id ocid1.compartment.oc1..xxxxx \\
                                   --minutos 240
  
  # Usar un perfil diferente
  python monitorear_instancias.py --instance-id ocid1.instance.oc1..xxxxx \\
                                   --compartment-id ocid1.compartment.oc1..xxxxx \\
                                   --profile PROD

Nota: Asegúrate de que el agente de monitoreo de OCI esté instalado y en ejecución
en la instancia para obtener métricas completas.
        """
    )
    
    parser.add_argument(
        "--instance-id",
        required=True,
        help="ID de la instancia a monitorear"
    )
    
    parser.add_argument(
        "--compartment-id",
        required=True,
        help="ID del compartment de la instancia"
    )
    
    parser.add_argument(
        "--minutos",
        type=int,
        default=60,
        help="Número de minutos de historial a consultar (default: 60)"
    )
    
    parser.add_argument(
        "--profile",
        default="DEFAULT",
        help="Perfil de configuración de OCI (default: DEFAULT)"
    )
    
    args = parser.parse_args()
    
    # Validar período
    if args.minutos < 1:
        print("✗ El período debe ser al menos 1 minuto.")
        sys.exit(1)
    
    # Verificar permisos
    print("🔐 Verificando credenciales de OCI...")
    if not verificar_permisos():
        sys.exit(1)
    
    # Monitorear instancia
    success = monitorear_instancia(
        args.instance_id,
        args.compartment_id,
        args.minutos,
        args.profile
    )
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
