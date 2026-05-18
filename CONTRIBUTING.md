# Contributing

Thanks for helping improve PaginaVox Open.

## Development Setup

Use Python 3.12.

Windows:

```powershell
.\install_env_windows.bat
.\run_windows.bat
```

Linux:

```bash
bash install_env_linux.sh
bash run_linux.sh
```

## Before Opening a Pull Request

- Keep generated files out of Git: `env/`, `audio/`, `txt/`, `output/`, `profiles/`, `dist/`, model caches, and voice profiles.
- Do not commit personal audio, private transcripts, or `.pkl` voice profiles.
- Update English and French documentation when changing user-facing behavior.
- Prefer small, focused changes.
- Test the command-line path when changing `main.py`.
- Test the Gradio path when changing `gradio/app.py`.

## Francais

Merci de contribuer a PaginaVox Open.

Avant d'ouvrir une pull request :

- ne publie pas `env/`, `audio/`, `txt/`, `output/`, `profiles/`, `dist/`, les caches de modeles ou les profils de voix ;
- ne commit pas d'audios personnels, de transcriptions privees ou de profils `.pkl` ;
- mets a jour la documentation anglaise et francaise si le comportement utilisateur change ;
- garde les changements petits et clairement limites ;
- teste la ligne de commande si tu modifies `main.py` ;
- teste l'interface Gradio si tu modifies `gradio/app.py`.
