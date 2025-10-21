import pandas as pd
import os
import math
import sys
from argparse import Namespace
from pathlib import Path

def pairing_text_audio(df_text:pd.DataFrame, filtered_df_media:pd.DataFrame) -> pd.DataFrame:
    """
    Associa os diretórios dos áudios com os chats correpondentes na ordem correspondente.

    Args:
        df_text (pd.DataFrame): dataset das mensagens de texto
        filtered_df_media (pd.DataFrame): dataset com os diretórios das mensagens de áudio 

    Returns:
        pd.DataFrame: O dataset df_text_audio_no_description concatenado com os textos e os diretórios dos áudios, 
        sem a transcrição dos áudios
    """

    df_text_audio_no_description = df_text.copy()
    df_text_audio_no_description['audio_path'] = None

    # Percorre por chat_row_id único
    for chat_id, group in df_text_audio_no_description.groupby('chat_row_id', sort=False):
        # Seleciona os paths correspondentes ao chat_id
        paths = filtered_df_media.loc[
            filtered_df_media['chat_row_id'] == chat_id, 'file_path'
        ].tolist()
        
        # Índices das mensagens de áudio (message_type == 2.0)
        audio_indices = group.index[group['message_type'] == 2.0].tolist()
        
        # Atribui paths na ordem, mas pula se path for NaN
        path_idx = 0
        for audio_idx in audio_indices:
            # Se acabaram os paths, interrompe
            if path_idx >= len(paths):
                break

            path = paths[path_idx]

            # Se o path for NaN, pula e avança
            if pd.isna(path) or (isinstance(path, float) and math.isnan(path)):
                path_idx += 1
                continue

            # Atribui o caminho válido
            df_text_audio_no_description.at[audio_idx, 'audio_path'] = path
            path_idx += 1
    
    return df_text_audio_no_description