import base64
import html
import mimetypes
import os
import shutil
import sys
import uuid


APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)

# On évite que Python importe par erreur des modules locaux
# qui auraient le même nom que des bibliothèques installées.
sys.path = [
    path for path in sys.path
    if os.path.abspath(path or os.getcwd()) not in {APP_DIR, PROJECT_DIR}
]

try:
    import gradio as gr
except ModuleNotFoundError:
    print("Gradio est introuvable. Installe les dépendances avec : pip install -r requirements.txt")
    raise SystemExit(1)

# On remet le dossier projet dans le path pour pouvoir importer main.py
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

import main as paginavox


# Langues disponibles dans l'interface.
# La clé est ce que l'utilisateur voit.
# La valeur est ce qui est envoyé aux fonctions de génération.
LANGUAGES = {
    "Français": "French",
    "Anglais": "English",
}

# Liste des voix Qwen disponibles.
VOICE_CHOICES = [(label, voice_id) for voice_id, label in paginavox.QWEN_VOICES]

# Valeur spéciale utilisée quand l'utilisateur veut créer un nouveau profil vocal.
NEW_PROFILE_VALUE = "__new_profile__"

# Image du titre.
# Mets ton logo ici : dossier assets/logo.png à côté de app.py
LOGO_PATH = os.path.join(APP_DIR, "assets", "logo.png")


# CSS personnalisé pour masquer le footer Gradio.
# Cela cache notamment :
# - Utiliser via API
# - Créé avec Gradio
# - Paramètres
CUSTOM_CSS = """
footer {
    /*display: none !important;*/
}

.title-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 18px;
    margin-bottom: 25px;
}

.title-logo {
    width: 90px;
    height: 90px;
    object-fit: contain;
    border-radius: 18px;
}

.title-text {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 800;
    text-align: center;
}
"""


# Traductions de l'interface.
# Important : l'objet s'appelle i18n en minuscule.
# Il faut donc utiliser i18n("clé") et non I18n("clé").
i18n = gr.I18n(
    en={
        "title": "Welcome to PaginaVox",
        "qwen_tab": "Qwen Voice",
        "clone_tab": "Voice cloning",
        "output_name": "Output name",
        "audio_language": "Audio language",
        "voice": "Voice",
        "text_to_generate": "Text to generate",
        "text_placeholder": "One line = one audio file",
        "compile": "Compile files into one WAV",
        "generate": "Generate",
        "status": "Status",
        "audio_preview": "Audio preview",
        "generated_files": "Generated files",
        "profile": "Profile",
        "new_profile_panel": "Create a new voice profile",
        "reference_audio": "Reference audio",
        "new_profile_name": "New profile name",
        "reference_text": "Optional reference transcription",
        "reference_text_placeholder": "Leave empty to run Whisper automatically",
    },
    fr={
        "title": "Bienvenue dans mon PaginaVox",
        "qwen_tab": "Voix Qwen",
        "clone_tab": "Clonage de voix",
        "output_name": "Nom de sortie",
        "audio_language": "Langue audio",
        "voice": "Voix",
        "text_to_generate": "Texte à générer",
        "text_placeholder": "Une ligne = un fichier audio",
        "compile": "Compiler les fichiers en un seul WAV",
        "generate": "Générer",
        "status": "Statut",
        "audio_preview": "Aperçu audio",
        "generated_files": "Fichiers générés",
        "profile": "Profil",
        "new_profile_panel": "Créer un nouveau profil vocal",
        "reference_audio": "Audio de référence",
        "new_profile_name": "Nom du nouveau profil",
        "reference_text": "Transcription de référence optionnelle",
        "reference_text_placeholder": "Laisse vide pour lancer Whisper automatiquement",
    },
)


def ensure_dirs():
    """
    Crée les dossiers nécessaires si ils n'existent pas encore.
    """
    os.makedirs(paginavox.AUDIO_DIR, exist_ok=True)
    os.makedirs(paginavox.TEXT_DIR, exist_ok=True)
    os.makedirs(paginavox.OUTPUT_DIR, exist_ok=True)
    os.makedirs(paginavox.PROFILE_DIR, exist_ok=True)


def split_lines_or_error(text: str) -> list[str]:
    """
    Découpe le texte en plusieurs lignes.
    Chaque ligne donnera un fichier audio.
    """
    lines = paginavox.split_text_lines(text or "")
    if not lines:
        raise gr.Error("Le texte est vide.")
    return lines


def safe_output_name(name: str, default: str) -> str:
    """
    Nettoie le nom du fichier de sortie pour éviter les caractères problématiques.
    """
    return paginavox.clean_output_name(name or "", default)


def profile_choices():
    """
    Récupère la liste des profils de clonage vocal existants.
    Ajoute aussi l'option pour créer un nouveau profil.
    """
    profiles = paginavox.list_voice_clone_profiles()

    choices = [("Créer un nouveau profil", NEW_PROFILE_VALUE)]
    choices.extend((profile["name"], profile["path"]) for profile in profiles)

    return choices


def refresh_profiles():
    """
    Rafraîchit la liste des profils vocaux.
    Fonction gardée au cas où tu veux remettre un bouton plus tard.
    """
    return gr.update(choices=profile_choices(), value=NEW_PROFILE_VALUE)


def save_uploaded_audio(uploaded_audio: str) -> str:
    """
    Sauvegarde l'audio de référence envoyé par l'utilisateur
    dans le dossier AUDIO_DIR.
    """
    if not uploaded_audio:
        raise gr.Error("Ajoute un audio de référence pour créer un nouveau profil.")

    ensure_dirs()

    ext = os.path.splitext(uploaded_audio)[1].lower() or ".wav"
    if ext not in paginavox.AUDIO_EXTENSIONS:
        raise gr.Error("Format audio non supporté. Utilise wav, mp3, flac, m4a ou ogg.")

    base = paginavox.clean_output_name(
        os.path.splitext(os.path.basename(uploaded_audio))[0],
        "reference"
    )

    destination = os.path.join(paginavox.AUDIO_DIR, f"{base}{ext}")

    # Si un fichier du même nom existe déjà, on ajoute un identifiant unique.
    if os.path.exists(destination):
        destination = os.path.join(
            paginavox.AUDIO_DIR,
            f"{base}_{uuid.uuid4().hex[:8]}{ext}"
        )

    shutil.copy2(uploaded_audio, destination)

    return destination


def create_profile_from_audio(
    uploaded_audio: str,
    profile_name: str,
    reference_text: str,
    language: str
):
    """
    Crée un nouveau profil vocal à partir d'un audio de référence.

    Si l'utilisateur donne une transcription, on l'utilise.
    Sinon, on lance la transcription automatique avec Whisper.
    """
    ref_audio = save_uploaded_audio(uploaded_audio)

    profile_base = safe_output_name(profile_name, "voice_profile")
    profile_path = os.path.join(paginavox.PROFILE_DIR, f"{profile_base}.pkl")

    # Si le profil existe déjà, on crée un nom unique.
    if os.path.exists(profile_path):
        profile_path = os.path.join(
            paginavox.PROFILE_DIR,
            f"{profile_base}_{uuid.uuid4().hex[:8]}.pkl"
        )

    ref_txt_path = paginavox.linked_text_for_audio(ref_audio)

    if reference_text and reference_text.strip():
        # Cas 1 : l'utilisateur donne la transcription manuellement.
        ref_text = paginavox.normalize_reference_text(reference_text)

        with open(ref_txt_path, "w", encoding="utf-8") as f:
            f.write(ref_text + "\n")
    else:
        # Cas 2 : pas de transcription donnée.
        # On utilise une transcription existante si elle existe.
        # Sinon, on lance Whisper.
        if not os.path.exists(ref_txt_path):
            ref_txt_path = paginavox.transcribe_audio(ref_audio, language, "small")

        ref_text = paginavox.normalize_reference_text(
            paginavox.read_text_file(ref_txt_path)
        )

    if not ref_text:
        raise gr.Error("La transcription de référence est vide.")

    # Création du prompt de clonage vocal.
    prompt_items = paginavox.create_voice_clone_prompt(ref_audio, ref_text)

    # Sauvegarde du profil dans un fichier .pkl
    with open(profile_path, "wb") as f:
        import pickle
        pickle.dump(prompt_items, f)

    return os.path.splitext(os.path.basename(profile_path))[0], prompt_items


def generated_result(generated: list[str], output_name: str, should_compile: bool):
    """
    Prépare le retour affiché dans Gradio après la génération audio.
    """
    compiled = None

    if should_compile and generated:
        compiled = paginavox.compile_audio_files(generated, output_name)

    preview = compiled or (generated[0] if generated else None)
    files = [compiled] if compiled else generated

    status = f"{len(generated)} fichier(s) créé(s) dans {paginavox.OUTPUT_DIR}"

    if compiled:
        status += f"\nFichier compilé : {compiled}"

    return status, preview, files


def generate_existing_voice(
    output_name: str,
    language_label: str,
    speaker: str,
    text: str,
    should_compile: bool
):
    """
    Génère une voix Qwen existante.
    """
    ensure_dirs()

    language = LANGUAGES[language_label]
    output_base = safe_output_name(output_name, "voix_qwen")
    lines = split_lines_or_error(text)

    generated = []

    for index, line in enumerate(lines, start=1):
        filename = f"{output_base}-{index:03d}.wav"
        output_path = os.path.join(paginavox.OUTPUT_DIR, filename)

        paginavox.generate_custom_voice_file(
            line,
            speaker,
            output_path,
            language
        )

        generated.append(output_path)

    return generated_result(generated, output_base, should_compile)


def generate_cloned_voice(
    output_name: str,
    language_label: str,
    profile_choice: str,
    uploaded_audio: str,
    profile_name: str,
    reference_text: str,
    text: str,
    should_compile: bool,
):
    """
    Génère une voix clonée.

    Deux possibilités :
    1. L'utilisateur choisit un profil existant.
    2. L'utilisateur crée un nouveau profil avec un audio de référence.
    """
    ensure_dirs()

    language = LANGUAGES[language_label]
    output_base = safe_output_name(output_name, "voix_clonee")
    lines = split_lines_or_error(text)

    if profile_choice == NEW_PROFILE_VALUE:
        _, voice_clone_prompt = create_profile_from_audio(
            uploaded_audio,
            profile_name,
            reference_text,
            language
        )
    else:
        voice_clone_prompt = paginavox.load_voice_clone_prompt(profile_choice)

    generated = []

    for index, line in enumerate(lines, start=1):
        filename = f"{output_base}-{index:03d}.wav"
        output_path = os.path.join(paginavox.OUTPUT_DIR, filename)

        paginavox.generate_voice_clone_file(
            line,
            voice_clone_prompt,
            output_path,
            language
        )

        generated.append(output_path)

    return generated_result(generated, output_base, should_compile)


def image_to_data_uri(image_path: str) -> str | None:
    """
    Convertit une image locale en data URI base64.

    Avantage :
    - pas de composant gr.Image
    - pas de bouton autour de l'image
    - pas de problème de chemin Windows dans le navigateur
    """
    if not os.path.exists(image_path):
        return None

    mime_type, _ = mimetypes.guess_type(image_path)
    mime_type = mime_type or "image/png"

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


def title_html() -> str:
    """
    Génère le titre HTML avec le logo si le fichier existe.
    """
    APP_TITLE = "PaginaVox"
    title = html.escape(APP_TITLE)
    logo_data_uri = image_to_data_uri(LOGO_PATH)

    if logo_data_uri:
        return f"""
        <div class="title-row">
            <img class="title-logo" src="{logo_data_uri}" alt="Logo PaginaVox">
            <h1 class="title-text">{title}</h1>
        </div>
        """

    return f"""
    <div class="title-row">
        <h1 class="title-text">{title}</h1>
    </div>
    """


def build_app():
    """
    Construit toute l'interface Gradio.
    """
    ensure_dirs()

    with gr.Blocks(
        title="PaginaVox"
    ) as demo:

        # Titre principal de l'application.
        # On utilise gr.HTML au lieu de gr.Image pour éviter que le logo
        # soit rendu dans un bouton cliquable.
        gr.HTML(title_html())

        with gr.Tabs():

            # ---------------------------------------------------------
            # Onglet 1 : génération avec une voix Qwen existante
            # ---------------------------------------------------------
            with gr.Tab(i18n("qwen_tab")):
                with gr.Row():
                    qwen_output_name = gr.Textbox(
                        label=i18n("output_name"),
                        value="test"
                    )

                    qwen_language = gr.Dropdown(
                        label=i18n("audio_language"),
                        choices=list(LANGUAGES),
                        value="Français"
                    )

                    qwen_voice = gr.Dropdown(
                        label=i18n("voice"),
                        choices=VOICE_CHOICES,
                        value=VOICE_CHOICES[0][1]
                    )

                qwen_text = gr.Textbox(
                    label=i18n("text_to_generate"),
                    lines=10,
                    placeholder=i18n("text_placeholder")
                )

                qwen_compile = gr.Checkbox(
                    label=i18n("compile"),
                    value=True
                )

                qwen_button = gr.Button(
                    i18n("generate"),
                    variant="primary"
                )

                qwen_status = gr.Textbox(
                    label=i18n("status"),
                    lines=4
                )

                qwen_preview = gr.Audio(
                    label=i18n("audio_preview"),
                    type="filepath"
                )

                qwen_files = gr.File(
                    label=i18n("generated_files"),
                    file_count="multiple"
                )

                qwen_button.click(
                    fn=generate_existing_voice,
                    inputs=[
                        qwen_output_name,
                        qwen_language,
                        qwen_voice,
                        qwen_text,
                        qwen_compile,
                    ],
                    outputs=[
                        qwen_status,
                        qwen_preview,
                        qwen_files,
                    ],
                )

            # ---------------------------------------------------------
            # Onglet 2 : clonage de voix
            # ---------------------------------------------------------
            with gr.Tab(i18n("clone_tab")):
                with gr.Row():
                    clone_output_name = gr.Textbox(
                        label=i18n("output_name"),
                        value="test"
                    )

                    clone_language = gr.Dropdown(
                        label=i18n("audio_language"),
                        choices=list(LANGUAGES),
                        value="Français"
                    )

                    clone_profile = gr.Dropdown(
                        label=i18n("profile"),
                        choices=profile_choices(),
                        value=NEW_PROFILE_VALUE
                    )

                # Volet fermé par défaut.
                # L'utilisateur peut l'ouvrir uniquement s'il veut créer
                # un nouveau profil vocal.
                with gr.Accordion(i18n("new_profile_panel"), open=False):
                    with gr.Row():
                        reference_audio = gr.Audio(
                            label=i18n("reference_audio"),
                            sources=["upload", "microphone"],
                            type="filepath"
                        )

                        new_profile_name = gr.Textbox(
                            label=i18n("new_profile_name"),
                            value="profil_1"
                        )

                    reference_text = gr.Textbox(
                        label=i18n("reference_text"),
                        lines=4,
                        placeholder=i18n("reference_text_placeholder"),
                    )

                clone_text = gr.Textbox(
                    label=i18n("text_to_generate"),
                    lines=10,
                    placeholder=i18n("text_placeholder")
                )

                clone_compile = gr.Checkbox(
                    label=i18n("compile"),
                    value=True
                )

                clone_button = gr.Button(
                    i18n("generate"),
                    variant="primary"
                )

                clone_status = gr.Textbox(
                    label=i18n("status"),
                    lines=5
                )

                clone_preview = gr.Audio(
                    label=i18n("audio_preview"),
                    type="filepath"
                )

                clone_files = gr.File(
                    label=i18n("generated_files"),
                    file_count="multiple"
                )

                clone_button.click(
                    fn=generate_cloned_voice,
                    inputs=[
                        clone_output_name,
                        clone_language,
                        clone_profile,
                        reference_audio,
                        new_profile_name,
                        reference_text,
                        clone_text,
                        clone_compile,
                    ],
                    outputs=[
                        clone_status,
                        clone_preview,
                        clone_files,
                    ],
                )

    return demo


if __name__ == "__main__":
    build_app().queue().launch(
        server_name="127.0.0.1",
        inbrowser=True,
        share=False,
        # On passe l'objet de traduction à Gradio.
        i18n=i18n,
        # Avec Gradio 6.x, theme et css doivent être passés à launch().
        theme=gr.themes.Soft(),
        css=CUSTOM_CSS,
        #footer_links=[],
    )
