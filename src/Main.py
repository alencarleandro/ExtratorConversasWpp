import pandas as pd
import math
import argparse
import sys
from src.service import PreProcessService
from src.util import FolderUtil
from src.service.AudioTranscriptionService import main as audio_transcription

def get_args(argv=None):
    parser = argparse.ArgumentParser(description='Diretórios para os arquivos de mensagens de texto, mídia e áudios.')

    parser.add_argument('-t', '--text', type=str, default='./datasets/message_db.csv', help='Arquivo que contém as mensagens de texto (message_db.csv)')
    parser.add_argument('-m', '--media', type=str, default='./datasets/message_media_db.csv', help='Arquivo que contém os diretórios das mídias (message_media_db.csv)')
    parser.add_argument('-a', '--audios', type=str, default='./datasets/audios/', help='Diretório raiz que contem os áudios')

    return parser.parse_args()

def main():
    args = get_args()
    print(f'\nDiretório do arquivo de texto: {args.text}')
    print(f'Diretório do arquivo de mídia: {args.media}')
    print(f'Diretório raiz dos arquivos de aúdio: {args.audios}\n')
    
    # Verifica se os arquivos dos dados existem
    utils.ensure_files_exists(args=args)

    df_text = pd.read_csv(args.text) # Carrega o arquivo que contém as mensagens de texto
    df_media = pd.read_csv(args.media) # Carrega o arquivo que contém os diretórios de mídias

    df_text = pre_process.pre_process_text_data(df_text) # pré-processa o arquivo de mensagens de texto (message_db.csv)                                     
    df_text_audio_no_transcriptions = pre_process.pre_process_media_data(df_media=df_media, df_text=df_text) # pré-processa o arquivo de mídia (message_media_db.csv)
    # Salva o dataset sem a transcrição dos aúdios
    outputs_dir = 'outputs/'
    utils.ensure_folder_exists(outputs_dir)
    df_text_audio_no_transcriptions = df_text_audio_no_transcriptions.to_csv(f'./{outputs_dir}df_text_audio_no_transcriptions.csv', index=False) 
    
    audio_transcription(audios_path=args.audios) # Transcreve os áudios
    transcriptions = pd.read_csv(f'./{outputs_dir}transcriptions.csv') # Salva as trasncrições  

    df_text_audio_with_transcriptions = pd.read_csv(f'./{outputs_dir}df_text_audio_no_transcriptions.csv')


    df_text_audio_with_transcriptions['audio_path'] = ( 
        df_text_audio_with_transcriptions['audio_path'].str.replace(r"^.*(/20\d{3,}/.*)$", r"\1", regex=True)
    )

    # Associa cada transcrição com o devido chat, de forma ordenada
    mapping = dict(zip(transcriptions['audio_path'], transcriptions['transcription']))
    df_text_audio_with_transcriptions['text_data'] = (
        df_text_audio_with_transcriptions['audio_path'].map(mapping).combine_first(df_text_audio_with_transcriptions['text_data'])
    )

    df_text_audio_with_transcriptions = df_text_audio_with_transcriptions.to_csv(f'./{outputs_dir}df_text_audio_with_transcriptions.csv', index=False)
    
if __name__ == '__main__':
    main()