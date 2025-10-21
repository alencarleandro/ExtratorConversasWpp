import pandas as pd
import utils

def pre_process_text_data(df_text:pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o pre-processamento do arquivo das mensagens de texto (message_db.csv)

    Args:
        df_text (pd.DataFrame): dataset das mensagens de texto

    Returns:
        pd.DataFrame: O dataset df_text pré-processado
    """

    # Remoção das colunas desnecessárias
    df_text_columns_to_drop = ['_id','key_id','sender_jid_row_id',
       'status', 'broadcast', 'recipient_count', 'participant_hash',
       'origination_flags', 'origin', 'timestamp', 'received_timestamp',
       'receipt_server_timestamp', 'starred',
       'lookup_tables','message_add_on_flags', 'view_mode',
       'translated_text']
    df_text.drop(labels=df_text_columns_to_drop, axis=1, inplace=True)
    
    df_text = df_text.sort_values(by=['chat_row_id', 'sort_id'], ascending=[True, True]) # Ordena  df_text por chat_row_id (identificador dos chats) e por sort_id (ordem das mensagens)
    df_text = df_text[df_text['message_type'].isin([0.0, 2.0])] # Filtra apenas as mensagens dos tipos texto(0.0) e áudio(2.0)
    df_text = df_text.reset_index(drop=True)                                                            

    return df_text

def pre_process_media_data(df_media:pd.DataFrame, df_text:pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o pre-processamento do arquivo das mensagens de mídia (message_db.csv)

    Args:
        df_media (pd.DataFrame): dataset que contém os diretórios das mídias (message_media_db.csv)
        df_text (pd.DataFrame): dataset que contém as mensagens de texto pre-processado
    Returns:
        pd.DataFrame: O dataset df_text_audio_no_description pré-processado, contendo apenas os diretório para os arquivos de áudio
    """

    # Remoção das colunas desnecessárias
    media_columns_to_drop = ['message_row_id', 'autotransfer_retry_enabled',
       'multicast_id', 'media_job_uuid', 'transferred', 'transcoded','file_size', 
        'suspicious_content', 'trim_from', 'trim_to',
       'face_x', 'face_y', 'media_key', 'media_key_timestamp', 'width',
       'height', 'has_streaming_sidecar', 'gif_attribution',
       'thumbnail_height_width_ratio', 'direct_path', 'first_scan_sidecar',
       'first_scan_length', 'message_url', 'mime_type', 'file_length',
       'media_name', 'file_hash', 'media_duration', 'page_count',
       'enc_file_hash', 'partial_media_hash', 'partial_media_enc_hash',
       'is_animated_sticker', 'original_file_hash', 'mute_video',
       'media_caption', 'media_upload_handle', 'sticker_flags',
       'raw_transcription_text', 'first_viewed_timestamp', 'doodle_id',
       'media_source_type', 'accessibility_label', 'media_transcode_quality',
       'metadata_url', 'motion_photo_presentation_offset_ms', 'qr_url']
    df_media.drop(labels=media_columns_to_drop, axis=1, inplace=True)
    
    filtered_df_media = df_media[df_media['file_path'].str.contains('WhatsApp Business Voice Notes', na=False)] # filtra apenas os diretórios que contém mensagens de áudio 
    filtered_df_media = filtered_df_media.sort_values(by=['chat_row_id', 'file_path'], ascending=[True, True])
    filtered_df_media = filtered_df_media.reset_index(drop=True)

    df_text_audio_no_description = utils.pairing_text_audio(df_text=df_text, filtered_df_media=filtered_df_media)

    print(f'- Quantidade de áudios: {len(filtered_df_media)}')
    print(f'- Quantidade de áudios linkados aos chats: {df_text_audio_no_description["audio_path"].notna().sum()}')
    print(f'- Quantidade de áudios não atribuídos a nenhum chat: {len(filtered_df_media) - df_text_audio_no_description["audio_path"].notna().sum()}\n')

    return df_text_audio_no_description