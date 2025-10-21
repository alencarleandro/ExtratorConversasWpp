import os
import csv
import time
import torch
import utils
from faster_whisper import WhisperModel

def audio_transcription(out_file:str, root_dir: str, model:WhisperModel) -> None:
    """
    Transcreve os aúdios e salva as transcrições e os diretórios dos aúdios em formato .csv

    Args: 
        out_file (str): diretório onde o.csv será salvo
        root_dir (str): diretório raiz (datasets/audios) dos aúdios. Ex.: datasets/audios/2025XX/PTT-20XXXXXX-WAXXXX.opus
        model (WhisperModel): modelo usando para realizar a transcrição
    """

    # Abre o arquivo CSV para escrita
    with open(out_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["audio_path", "transcription"])

        # Percorre todos os diretórios e arquivos dentro da pasta raiz
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith(".opus"):

                    caminho_completo = os.path.join(root, file).replace("\\","/")
                    print(f"Transcrevendo: {caminho_completo}")

                    start = time.time()

                    try:
                        # Transcreve o áudio
                        segments, info = model.transcribe(
                            caminho_completo,
                            beam_size=5,
                            vad_filter=True,
                            condition_on_previous_text=True,
                        )

                        # Concatena todos os segmentos em um texto só
                        texto = " ".join([segment.text for segment in segments]).strip()

                        # Extrai apenas o nome da pasta pai e o nome do arquivo
                        nome_arquivo = os.path.basename(caminho_completo)               # Ex: PTT-20251008-WA0019.opus
                        pasta_pai = os.path.basename(os.path.dirname(caminho_completo)) # Ex: 202541
                        caminho_relativo = os.path.join(f"/{pasta_pai}", nome_arquivo)  # Ex: /202541/PTT-20251008-WA0019.opus

                        # Escreve no CSV
                        writer.writerow([caminho_relativo.replace("\\","/"), texto])
                        print(f"Finalizado ({info.language})\n")
                        end = time.time()
                        
                        utils.tempo_parcial_execucao(start=start, end=end)

                    except Exception as e:
                        print(f"Erro ao processar {caminho_completo}: {e}\n")

    print(f"Transcrições salvas em: {os.path.abspath(out_file)}")

def main(audios_path:str):
    root_dir = audios_path
    out_file = "./outputs/transcriptions.csv"   
    model_size = "large-v2" # Size of the model to use (tiny, tiny.en, base, base.en, small, small.en, distil-small.en,
                            # medium, medium.en, distil-medium.en, large-v1, large-v2, large-v3, large, distil-large-v2,
                            # distil-large-v3, large-v3-turbo, or turbo), a path to a converted model directory, or a 
                            # CTranslate2-converted Whisper model ID from the HF Hub. When a size or a model ID is 
                            # configured, the converted model is downloaded from the Hugging Face Hub.                     
    device = "cuda" if torch.cuda.is_available() else "cpu" # Verifica se CUDA está disponível
    compute_type = "int8_float32"
    
    print("Iniciando transcrições\n")
    model = WhisperModel(model_size_or_path=model_size, device=device, compute_type=compute_type) 
    start = time.time()
    audio_transcription(out_file=out_file, root_dir=root_dir, model=model)
    end = time.time()
    utils.tempo_execucao(start=start, end=end)

if __name__ == '__main__':
    main('./datasets/audios/')


