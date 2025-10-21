import pandas as pd
import os
import math
import sys
from argparse import Namespace
from pathlib import Path

def tempo_execucao(start:float, end:float) -> None:
    """
    Calcula e printa o tempo de execução no formato horas:minutos:segundos

    Args:
        start (float): tempo de início da contagem
        end (float): tempo de término da contagem
    """
    # Calcula o tempo decorrido em segundos
    tempo_total = end - start
    
    # Converte para horas, minutos e segundos
    horas = int(tempo_total // 3600)
    minutos = int((tempo_total % 3600) // 60)
    segundos = int(tempo_total % 60)
    print(f"Tempo total de execução: {horas:02d}:{minutos:02d}:{segundos:02d}")

def tempo_parcial_execucao(start:float, end:float) -> None:
    """
    Calcula e printa o tempo de execução no formato horas:minutos:segundos

    Args:
        start (float): tempo de início da contagem
        end (float): tempo de término da contagem
    """
    # Calcula o tempo decorrido em segundos
    tempo_total = end - start
    
    # Converte para horas, minutos e segundos
    horas = int(tempo_total // 3600)
    minutos = int((tempo_total % 3600) // 60)
    segundos = int(tempo_total % 60)
    print(f"Tempo parcial de execução: {horas:02d}:{minutos:02d}:{segundos:02d}")