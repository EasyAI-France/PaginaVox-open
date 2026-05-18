import os
import pickle
import re
import shutil
import subprocess
import sys
import uuid


if getattr(sys, "frozen", False):
    COMMAND_DIR = os.path.dirname(sys.executable)
else:
    COMMAND_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(COMMAND_DIR, "audio")
TEXT_DIR = os.path.join(COMMAND_DIR, "txt")
OUTPUT_DIR = os.path.join(COMMAND_DIR, "output")
PROFILE_DIR = os.path.join(COMMAND_DIR, "profiles")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PROFILE_DIR, exist_ok=True)

QWEN_VOICES = [
    ("vivian", "Vivian - voix jeune et brillante"),
    ("serena", "Serena - voix feminine chaude et douce"),
    ("uncle_fu", "Uncle Fu - voix masculine grave et douce"),
    ("dylan", "Dylan - voix masculine claire et naturelle"),
    ("eric", "Eric - voix masculine vive"),
    ("ryan", "Ryan - voix masculine dynamique"),
    ("aiden", "Aiden - voix masculine ensoleillee"),
    ("ono_anna", "Anna - voix feminine enjouee"),
    ("sohee", "Sohee - voix feminine chaleureuse"),
]

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".m4a", ".ogg"}
TEXT_EXTENSIONS = {".txt"}

UI_LANG = "fr"
AUDIO_LANGUAGE = "French"
_CUSTOM_MODEL = None
_VOICE_CLONE_MODEL = None

MESSAGES = {
    "fr": {
        "value_required": "Merci d'entrer une valeur.",
        "manual_end": "Ecris ton texte. Termine avec une ligne contenant seulement FIN.",
        "empty_text": "Le texte est vide, on recommence.",
        "text_folder": "Dossier des textes",
        "text_found": "Fichiers texte trouves :",
        "manual_text": "0. Saisir le texte a la main",
        "text_choice": "Numero du texte a utiliser : ",
        "invalid_choice": "Choix invalide.",
        "no_text_file": "Aucun fichier .txt trouve. Tu peux saisir le texte a la main.",
        "audio_folder": "Place ton audio de reference dans ce dossier",
        "audio_ready": "Quand le fichier est dans le dossier, appuie sur Entree...",
        "no_audio": "Aucun audio trouve dans",
        "audio_found": "Audios trouves :",
        "audio_choice": "Numero de l'audio a utiliser : ",
        "voices": "Voix Qwen disponibles :",
        "voice_choice": "Numero de la voix : ",
        "output_name": "Nom du fichier de sortie : ",
        "ref_text": "Texte prononce dans l'audio de reference",
        "ref_text_source": "Comment veux-tu donner le texte prononce dans l'audio de reference ?",
        "ref_text_manual": "1. Le saisir a la main",
        "ref_text_file": "2. Choisir un fichier .txt",
        "text_clone": "Texte a generer avec la voix clonee",
        "text_qwen": "Texte a generer",
        "no_lines": "Aucune ligne de texte a generer.",
        "clone_running": "Generation avec clonage de voix en cours...",
        "clone_prompt": "Creation de l'empreinte de voix...",
        "profile_folder": "Dossier des profils",
        "profile_found": "Profils de voix trouves :",
        "profile_new": "0. Creer un nouveau profil depuis un audio",
        "profile_choice": "Numero du profil a utiliser : ",
        "profile_name": "Nom du nouveau profil : ",
        "profile_saved": "Profil sauvegarde",
        "missing_ref_txt": "Transcription introuvable pour cet audio.",
        "linked_ref_txt": "Transcription liee trouvee",
        "transcribe_missing": "Transcription introuvable. Lancement automatique de Whisper...",
        "transcribe_running": "Transcription en cours...",
        "transcribe_done": "Transcription terminee",
        "whisper_missing": "Whisper est introuvable. Installe openai-whisper dans l'environnement actif: python -m pip install openai-whisper",
        "whisper_empty": "Whisper n'a pas retourne de texte.",
        "whisper_error": "Erreur Whisper",
        "short_line_warning": "Attention: certaines lignes sont tres courtes. Le clonage peut produire du bruit sur des segments trop petits.",
        "compile_question": "Compiler les fichiers audio en un seul fichier ? (o/n) : ",
        "compile_running": "Compilation audio en cours...",
        "compile_done": "Fichier compile cree",
        "compile_no_files": "Aucun fichier audio a compiler.",
        "qwen_running": "Generation avec voix Qwen existante en cours...",
        "done": "Generation terminee.",
        "created": "fichier(s) cree(s) dans",
        "title": "PaginaVox - mode ligne de commande",
        "clone_menu": "1. Cloner une voix depuis un audio",
        "qwen_menu": "2. Utiliser une voix Qwen existante",
        "quit_menu": "0. Quitter",
        "main_choice": "Ton choix : ",
        "bye": "Au revoir.",
        "main_invalid": "Choix invalide. Tape 1, 2 ou 0.",
        "cancelled": "Operation annulee.",
        "error": "Erreur",
    },
    "en": {
        "value_required": "Please enter a value.",
        "manual_end": "Type your text. Finish with a line containing only END.",
        "empty_text": "The text is empty, let's try again.",
        "text_folder": "Text folder",
        "text_found": "Text files found:",
        "manual_text": "0. Type the text manually",
        "text_choice": "Text file number to use: ",
        "invalid_choice": "Invalid choice.",
        "no_text_file": "No .txt file found. You can type the text manually.",
        "audio_folder": "Put your reference audio in this folder",
        "audio_ready": "When the file is in the folder, press Enter...",
        "no_audio": "No audio found in",
        "audio_found": "Audio files found:",
        "audio_choice": "Audio number to use: ",
        "voices": "Available Qwen voices:",
        "voice_choice": "Voice number: ",
        "output_name": "Output file name: ",
        "ref_text": "Text spoken in the reference audio",
        "ref_text_source": "How do you want to provide the text spoken in the reference audio?",
        "ref_text_manual": "1. Type it manually",
        "ref_text_file": "2. Choose a .txt file",
        "text_clone": "Text to generate with the cloned voice",
        "text_qwen": "Text to generate",
        "no_lines": "No text line to generate.",
        "clone_running": "Generating with voice cloning...",
        "clone_prompt": "Creating the voice print...",
        "profile_folder": "Profile folder",
        "profile_found": "Voice profiles found:",
        "profile_new": "0. Create a new profile from audio",
        "profile_choice": "Profile number to use: ",
        "profile_name": "New profile name: ",
        "profile_saved": "Profile saved",
        "missing_ref_txt": "No linked transcription found for this audio.",
        "linked_ref_txt": "Linked transcription found",
        "transcribe_missing": "No linked transcription found. Starting Whisper automatically...",
        "transcribe_running": "Transcribing...",
        "transcribe_done": "Transcription complete",
        "whisper_missing": "Whisper was not found. Install openai-whisper in the active environment: python -m pip install openai-whisper",
        "whisper_empty": "Whisper did not return any text.",
        "whisper_error": "Whisper error",
        "short_line_warning": "Warning: some lines are very short. Voice cloning may produce noise on tiny segments.",
        "compile_question": "Compile audio files into a single file? (y/n): ",
        "compile_running": "Compiling audio...",
        "compile_done": "Compiled file created",
        "compile_no_files": "No audio file to compile.",
        "qwen_running": "Generating with an existing Qwen voice...",
        "done": "Generation complete.",
        "created": "file(s) created in",
        "title": "PaginaVox - command line mode",
        "clone_menu": "1. Clone a voice from audio",
        "qwen_menu": "2. Use an existing Qwen voice",
        "quit_menu": "0. Quit",
        "main_choice": "Your choice: ",
        "bye": "Goodbye.",
        "main_invalid": "Invalid choice. Type 1, 2 or 0.",
        "cancelled": "Operation cancelled.",
        "error": "Error",
    },
}


def msg(key: str) -> str:
    """Retourne le texte dans la langue choisie pour l'interface."""
    return MESSAGES[UI_LANG][key]


def clean_output_name(value: str, default: str = "sortie") -> str:
    """Transforme le nom donne par l'utilisateur en nom de fichier simple."""
    name = os.path.splitext(value.strip())[0]
    name = re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_")
    return name or default


def ask_not_empty(question: str) -> str:
    """Pose une question jusqu'a obtenir une reponse non vide."""
    while True:
        value = input(question).strip()
        if value:
            return value
        print(msg("value_required"))


def ask_multiline_text(title: str) -> str:
    """
    Demande un texte sur une ou plusieurs lignes.

    L'utilisateur termine la saisie avec une ligne contenant uniquement FIN.
    """
    print()
    print(title)
    print(msg("manual_end"))
    lines = []
    while True:
        line = input()
        end_word = "FIN" if UI_LANG == "fr" else "END"
        if line.strip().upper() in {"FIN", "END", end_word}:
            break
        lines.append(line)
    text = "\n".join(lines).strip()
    if not text:
        print(msg("empty_text"))
        return ask_multiline_text(title)
    return text


def split_text_lines(text: str) -> list[str]:
    """Separe le texte en segments: une ligne non vide = un audio."""
    return [line.strip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n") if line.strip()]


def normalize_reference_text(text: str) -> str:
    """Nettoie la transcription de reference pour Qwen voice cloning."""
    return " ".join(text.replace("\r\n", "\n").replace("\r", "\n").split()).strip()


def list_voice_clone_profiles():
    """Liste les profils .pkl presents dans profiles."""
    profiles = []
    for name in os.listdir(PROFILE_DIR):
        path = os.path.join(PROFILE_DIR, name)
        if os.path.isfile(path) and name.lower().endswith(".pkl"):
            profiles.append({
                "name": os.path.splitext(name)[0],
                "filename": name,
                "path": path,
            })
    return sorted(profiles, key=lambda item: item["name"].lower())


def load_voice_clone_prompt(profile_path: str):
    """Recharge une empreinte de voix depuis un profil .pkl."""
    with open(profile_path, "rb") as f:
        return pickle.load(f)


def list_text_files():
    """Liste les fichiers texte disponibles dans txt."""
    files = []
    for name in os.listdir(TEXT_DIR):
        path = os.path.join(TEXT_DIR, name)
        if os.path.isfile(path) and os.path.splitext(name)[1].lower() in TEXT_EXTENSIONS:
            files.append(name)
    return sorted(files, key=str.lower)


def read_text_file(path: str) -> str:
    """Lit un fichier texte avec un encodage courant."""
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def linked_text_for_audio(audio_path: str) -> str:
    """Retourne txt/<nom_audio>.txt pour l'audio donne."""
    audio_base = os.path.splitext(os.path.basename(audio_path))[0]
    return os.path.join(AUDIO_DIR, f"{audio_base}.txt")


def whisper_executable():
    """Trouve l'executable Whisper de l'environnement courant."""
    exe_dir = os.path.dirname(sys.executable)
    env_dir = os.path.dirname(exe_dir) if os.path.basename(exe_dir).lower() == "scripts" else exe_dir
    candidates = [
        os.path.join(exe_dir, "whisper.exe"),
        os.path.join(exe_dir, "whisper"),
        os.path.join(exe_dir, "Scripts", "whisper.exe"),
        os.path.join(env_dir, "Scripts", "whisper.exe"),
        os.path.join(COMMAND_DIR, "env", "Scripts", "whisper.exe"),
        shutil.which("whisper"),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def transcribe_audio_with_python(audio_path: str, language: str, model: str, output_path: str):
    """Utilise le module Python Whisper si l'executable n'est pas disponible."""
    try:
        import whisper
    except ImportError as exc:
        raise FileNotFoundError(msg("whisper_missing")) from exc

    loaded_model = whisper.load_model(model)
    result = loaded_model.transcribe(audio_path, language=language.lower())
    text = str(result.get("text", "")).strip()
    if not text:
        raise RuntimeError(msg("whisper_empty"))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


def transcribe_audio(audio_path: str, language: str, model: str = "small"):
    """Lance Whisper et cree txt/<nom_audio>.txt."""
    exe = whisper_executable()
    audio_base = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join(AUDIO_DIR, f"{audio_base}.txt")

    print()
    print(msg("transcribe_running"))
    if exe is None:
        transcribe_audio_with_python(audio_path, language, model, output_path)
    else:
        cmd = [
            exe,
            audio_path,
            "--model", model,
            "--language", language,
            "--output_format", "txt",
            "--output_dir", AUDIO_DIR,
        ]
        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or msg("whisper_error"))

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"{msg('missing_ref_txt')} ({output_path})")
    print(f"{msg('transcribe_done')} : {output_path}")
    return output_path


def ask_yes_no(question: str) -> bool:
    """Retourne True pour oui/yes, False pour non/no."""
    yes_values = {"o", "oui", "y", "yes"}
    no_values = {"n", "non", "no"}
    while True:
        choice = input(question).strip().lower()
        if choice in yes_values:
            return True
        if choice in no_values:
            return False
        print(msg("invalid_choice"))


def compile_audio_files(audio_paths: list[str], output_name: str):
    """Concatene les fichiers audio generes dans un seul WAV."""
    if not audio_paths:
        raise ValueError(msg("compile_no_files"))

    import soundfile as sf
    import numpy as np

    print(msg("compile_running"))
    chunks = []
    target_sr = None
    target_channels = None

    for path in audio_paths:
        data, sr = sf.read(path, always_2d=True)
        if target_sr is None:
            target_sr = sr
            target_channels = data.shape[1]
        elif sr != target_sr:
            raise ValueError(f"Frequence audio differente pour {os.path.basename(path)} ({sr} != {target_sr})")
        elif data.shape[1] != target_channels:
            raise ValueError(f"Nombre de canaux different pour {os.path.basename(path)}")
        chunks.append(data)

    compiled = np.concatenate(chunks, axis=0)
    output_path = os.path.join(OUTPUT_DIR, f"{output_name}-compile.wav")
    sf.write(output_path, compiled, target_sr)
    print(f"{msg('compile_done')} : {output_path}")
    return output_path


def offer_compile_audio(audio_paths: list[str], output_name: str):
    """Propose de compiler les segments WAV en un seul fichier."""
    if audio_paths and ask_yes_no(msg("compile_question")):
        compile_audio_files(audio_paths, output_name)


def choose_text_source(title: str) -> str:
    """Permet de choisir un fichier .txt ou de saisir le texte a la main."""
    files = list_text_files()
    print()
    print(f"{msg('text_folder')} : {TEXT_DIR}")

    if files:
        print(msg("text_found"))
        for idx, name in enumerate(files, start=1):
            print(f"{idx}. {name}")
        print(msg("manual_text"))

        while True:
            choice = input(msg("text_choice")).strip()
            if choice == "0":
                return ask_multiline_text(title)
            if choice.isdigit():
                index = int(choice)
                if 1 <= index <= len(files):
                    return read_text_file(os.path.join(TEXT_DIR, files[index - 1]))
            print(msg("invalid_choice"))

    print(msg("no_text_file"))
    return ask_multiline_text(title)


def choose_reference_text_source() -> str:
    """Demande la transcription de l'audio de reference, au clavier ou depuis un .txt."""
    print()
    print(msg("ref_text_source"))
    print(msg("ref_text_manual"))
    print(msg("ref_text_file"))

    while True:
        choice = input(msg("main_choice")).strip()
        if choice == "1":
            return ask_multiline_text(msg("ref_text"))
        if choice == "2":
            return choose_text_source(msg("ref_text"))
        print(msg("invalid_choice"))


def choose_or_create_voice_clone_prompt():
    """Utilise un profil existant ou cree un nouveau profil depuis un audio."""
    profiles = list_voice_clone_profiles()

    print()
    print(f"{msg('profile_folder')} : {PROFILE_DIR}")
    if profiles:
        print(msg("profile_found"))
        for idx, profile in enumerate(profiles, start=1):
            print(f"{idx}. {profile['name']}")
        print(msg("profile_new"))

        while True:
            choice = input(msg("profile_choice")).strip()
            if choice == "0":
                break
            if choice.isdigit():
                index = int(choice)
                if 1 <= index <= len(profiles):
                    selected = profiles[index - 1]
                    return selected["name"], load_voice_clone_prompt(selected["path"])
            print(msg("invalid_choice"))

    ref_audio = choose_reference_audio()
    profile_name = clean_output_name(ask_not_empty(msg("profile_name")), "voice_profile")
    ref_txt_path = linked_text_for_audio(ref_audio)
    if not os.path.exists(ref_txt_path):
        print(f"{msg('missing_ref_txt')} ({ref_txt_path})")
        print(msg("transcribe_missing"))
        ref_txt_path = transcribe_audio(ref_audio, AUDIO_LANGUAGE, "small")

    print(f"{msg('linked_ref_txt')} : {ref_txt_path}")
    ref_text = normalize_reference_text(read_text_file(ref_txt_path))
    if not ref_text:
        raise ValueError(msg("empty_text"))

    print(msg("clone_prompt"))
    profile_path = os.path.join(PROFILE_DIR, f"{profile_name}.pkl")
    if os.path.exists(profile_path):
        profile_path = os.path.join(PROFILE_DIR, f"{profile_name}_{uuid.uuid4().hex[:8]}.pkl")

    prompt_items = create_voice_clone_prompt(ref_audio, ref_text)
    with open(profile_path, "wb") as f:
        pickle.dump(prompt_items, f)

    print(f"{msg('profile_saved')} : {profile_path}")
    return os.path.splitext(os.path.basename(profile_path))[0], load_voice_clone_prompt(profile_path)


def list_reference_audios():
    """Liste les fichiers audio disponibles dans audio."""
    files = []
    for name in os.listdir(AUDIO_DIR):
        path = os.path.join(AUDIO_DIR, name)
        if os.path.isfile(path) and os.path.splitext(name)[1].lower() in AUDIO_EXTENSIONS:
            files.append(name)
    return sorted(files, key=str.lower)


def choose_reference_audio() -> str:
    """Demande a l'utilisateur de choisir un audio de reference."""
    print()
    print(f"{msg('audio_folder')} : {AUDIO_DIR}")
    input(msg("audio_ready"))

    files = list_reference_audios()
    if not files:
        raise FileNotFoundError(f"{msg('no_audio')} {AUDIO_DIR}")

    print()
    print(msg("audio_found"))
    for idx, name in enumerate(files, start=1):
        print(f"{idx}. {name}")

    while True:
        choice = input(msg("audio_choice")).strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(files):
                return os.path.join(AUDIO_DIR, files[index - 1])
        print(msg("invalid_choice"))


def choose_qwen_voice() -> str:
    """Affiche les voix Qwen disponibles et retourne l'identifiant choisi."""
    print()
    print(msg("voices"))
    for idx, (_, label) in enumerate(QWEN_VOICES, start=1):
        print(f"{idx}. {label}")

    while True:
        choice = input(msg("voice_choice")).strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(QWEN_VOICES):
                return QWEN_VOICES[index - 1][0]
        print(msg("invalid_choice"))


def choose_interface_language():
    """Choisit la langue des questions du programme."""
    global UI_LANG
    print("Interface language / Langue de l'interface")
    print("1. Francais")
    print("2. English")
    while True:
        choice = input("> ").strip()
        if choice == "1":
            UI_LANG = "fr"
            return
        if choice == "2":
            UI_LANG = "en"
            return
        print("Choix invalide / Invalid choice.")


def choose_audio_language():
    """Choisit la langue envoyee a Qwen pour la generation audio."""
    global AUDIO_LANGUAGE
    print()
    if UI_LANG == "fr":
        print("Langue de generation audio")
        print("1. Francais")
        print("2. Anglais")
        prompt = "Ton choix : "
    else:
        print("Audio generation language")
        print("1. French")
        print("2. English")
        prompt = "Your choice: "

    while True:
        choice = input(prompt).strip()
        if choice == "1":
            AUDIO_LANGUAGE = "French"
            return
        if choice == "2":
            AUDIO_LANGUAGE = "English"
            return
        print(msg("invalid_choice"))


def get_custom_voice_model():
    """Charge le modele Qwen CustomVoice pour le mode ligne de commande."""
    global _CUSTOM_MODEL
    if _CUSTOM_MODEL is None:
        import torch
        from qwen_tts import Qwen3TTSModel

        _CUSTOM_MODEL = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
            device_map="cuda:0",
            dtype=torch.bfloat16,
            attn_implementation="sdpa",
        )
    return _CUSTOM_MODEL


def get_voice_clone_model():
    """Charge le modele Qwen utilise pour le clonage vocal."""
    global _VOICE_CLONE_MODEL
    if _VOICE_CLONE_MODEL is None:
        import torch
        from qwen_tts import Qwen3TTSModel

        _VOICE_CLONE_MODEL = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
            device_map="cuda:0",
            dtype=torch.bfloat16,
            attn_implementation="sdpa",
        )
    return _VOICE_CLONE_MODEL


def generate_custom_voice_file(text: str, speaker: str, output_path: str, language: str):
    """Genere directement un fichier WAV avec la langue choisie."""
    import soundfile as sf

    model = get_custom_voice_model()
    wavs, sr = model.generate_custom_voice(
        text=text,
        language=language,
        speaker=speaker,
        instruct="Use a neutral tone",
    )
    sf.write(output_path, wavs[0], sr)


def create_voice_clone_prompt(ref_audio: str, ref_text: str):
    """Cree une empreinte de voix reutilisable pour plusieurs lignes."""
    model = get_voice_clone_model()
    return model.create_voice_clone_prompt(
        ref_audio=ref_audio,
        ref_text=ref_text,
        x_vector_only_mode=False,
    )


def generate_voice_clone_file(text: str, voice_clone_prompt, output_path: str, language: str):
    """Genere un fichier WAV avec une empreinte de voix deja creee."""
    import soundfile as sf

    model = get_voice_clone_model()
    wavs, sr = model.generate_voice_clone(
        text=text,
        language=language,
        voice_clone_prompt=voice_clone_prompt,
    )
    sf.write(output_path, wavs[0], sr)


def generate_with_voice_clone():
    """Genere un fichier WAV en clonant une voix depuis un audio de reference."""
    output_name = clean_output_name(ask_not_empty(msg("output_name")), "voix_clonee")
    _, voice_clone_prompt = choose_or_create_voice_clone_prompt()
    text = choose_text_source(msg("text_clone"))
    lines = split_text_lines(text)
    if not lines:
        raise ValueError(msg("no_lines"))
    if any(len(line) < 12 for line in lines):
        print(msg("short_line_warning"))

    print()
    print(msg("clone_running"))
    generated = []
    total = len(lines)
    for index, line in enumerate(lines, start=1):
        output_filename = f"{output_name}-{index:03d}.wav"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        print(f"[{index}/{total}] {output_filename}")
        generate_voice_clone_file(
            text=line,
            voice_clone_prompt=voice_clone_prompt,
            output_path=output_path,
            language=AUDIO_LANGUAGE,
        )
        generated.append(output_path)

    print()
    print(msg("done"))
    print(f"{len(generated)} {msg('created')} : {OUTPUT_DIR}")
    offer_compile_audio(generated, output_name)


def generate_with_existing_voice():
    """Genere un fichier WAV avec une voix CustomVoice officielle de Qwen."""
    output_name = clean_output_name(ask_not_empty(msg("output_name")), "voix_qwen")
    speaker = choose_qwen_voice()
    text = choose_text_source(msg("text_qwen"))
    lines = split_text_lines(text)
    if not lines:
        raise ValueError(msg("no_lines"))

    print()
    print(msg("qwen_running"))
    generated = []
    total = len(lines)
    for index, line in enumerate(lines, start=1):
        final_filename = f"{output_name}-{index:03d}.wav"
        out_path = os.path.join(OUTPUT_DIR, final_filename)
        print(f"[{index}/{total}] {final_filename}")
        generate_custom_voice_file(line, speaker, out_path, AUDIO_LANGUAGE)
        generated.append(out_path)

    print()
    print(msg("done"))
    print(f"{len(generated)} {msg('created')} : {OUTPUT_DIR}")
    offer_compile_audio(generated, output_name)


def main():
    """Point d'entree du programme en ligne de commande."""
    choose_interface_language()
    choose_audio_language()

    print()
    print(msg("title"))
    print("----------------------------------")
    print(msg("clone_menu"))
    print(msg("qwen_menu"))
    print(msg("quit_menu"))

    while True:
        choice = input(msg("main_choice")).strip()
        if choice == "1":
            generate_with_voice_clone()
            return
        if choice == "2":
            generate_with_existing_voice()
            return
        if choice == "0":
            print(msg("bye"))
            return
        print(msg("main_invalid"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{msg('cancelled')}.")
    except Exception as exc:
        print()
        print(f"{msg('error')} : {exc}")
        sys.exit(1)
