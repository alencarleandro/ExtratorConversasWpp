import pandas as pd
import os
import math
import sys
from argparse import Namespace
from pathlib import Path

def ensure_folder_exists(folder_path):
    """
    Verifica se um diretório existe em um caminho específico. Se não existe,
    o diretório é criado.

    Args:
        folder_path (str): The path to the folder to check/create.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Diretório '{folder_path}' criado com sucesso.\n")
    
def ensure_files_exists(args: Namespace):
    """
    Verifica se os arquivos de mensagem de texto, de mídia e o diretório raiz dos áudios existem.

    Args:
        args (Namespace): argumentos passados por linha de comando.
    """

    # Verifica se os diretórios existem
    for path in [args.text, args.media, args.audios]:
        if not Path(path).exists():
            sys.exit(f"Caminho inválido: {path}")
        if path == args.text or path == args.media:
            if (path.split('/')[-1].split('.')[-1] != 'csv'):
                sys.exit(f"Formato do arquivo inválido (precisa ser .csv): {path}")
    