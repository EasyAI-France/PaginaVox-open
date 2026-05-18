# PaginaVox Open

PaginaVox Open est une application locale en ligne de commande et avec interface Gradio pour generer de la parole avec Qwen TTS.

Elle permet :

- de cloner une voix depuis un audio de reference ;
- d'utiliser les voix Qwen integrees ;
- de transcrire automatiquement un audio de reference avec Whisper si aucun texte n'existe encore ;
- de generer un fichier WAV par ligne de texte non vide ;
- de compiler les segments WAV generes dans un seul fichier final.

> English documentation is available in [README.md](README.md). The English help guide is [HELP.md](HELP.md).

## Prerequis

- Windows ou Linux.
- Python 3.12.
- Carte NVIDIA compatible CUDA pour la generation Qwen TTS.
- Connexion internet au premier lancement et au premier telechargement des modeles.

macOS n'est pas pris en charge pour la generation actuellement, car le code charge les modeles Qwen sur `cuda:0`.

## Installation rapide

### Windows

```powershell
.\install_env_windows.bat
.\run_windows.bat
```

### Linux

```bash
bash install_env_linux.sh
bash run_linux.sh
```

Le script d'installation cree un environnement virtuel local `env/` et installe les dependances.

## Dossiers du projet

- `audio/` : audios de reference pour le clonage.
- `txt/` : textes a lire et transcriptions Whisper.
- `output/` : fichiers WAV generes.
- `profiles/` : profils de voix clones.
- `gradio/` : interface web locale.
- `Docker/` : configuration Docker NVIDIA.
- `build/` : scripts de build executable Windows.
- `Documents/` : notices utilisateur au format DOCX.
- `notebook/` : notebook Colab.

Les dossiers d'execution sont ignores par Git, sauf leurs fichiers `.gitkeep`.

## Utilisation en ligne de commande

Lance le script adapte a ton systeme, puis choisis :

1. la langue de l'interface ;
2. la langue de generation audio ;
3. le mode de generation.

Pour le clonage de voix, place un audio dans `audio/`. Si `txt/nom_audio.txt` n'existe pas, PaginaVox lance Whisper automatiquement et cree la transcription.

Chaque ligne non vide devient un fichier audio :

```text
output/exemple-001.wav
output/exemple-002.wav
output/exemple-003.wav
```

A la fin, PaginaVox peut compiler les segments dans :

```text
output/exemple-compile.wav
```

## Interface Gradio

Lance l'interface web locale :

Windows :

```powershell
.\gradio\run_gradio_windows.bat
```

Linux :

```bash
bash gradio/run_gradio_linux.sh
```

Ouvre ensuite l'URL locale affichee par Gradio, generalement :

```text
http://localhost:7860
```

## Executable Windows

Pour creer un dossier distribuable Windows :

```powershell
.\install_env_windows.bat
.\build\build_windows_exe.bat
```

Le dossier a distribuer est :

```text
dist/PaginaVox
```

Voir [build/BUILD_EXE_WINDOWS.md](build/BUILD_EXE_WINDOWS.md).

## Docker NVIDIA

Les fichiers Docker sont disponibles dans `Docker/`.

Windows :

```powershell
.\Docker\test_gpu.bat
.\Docker\build_windows.bat
.\Docker\run_windows.bat
```

Linux :

```bash
bash Docker/test_gpu.sh
bash Docker/build_linux_macos.sh
bash Docker/run_linux_macos.sh
```

Voir [Docker/README.md](Docker/README.md).

## Aide

- Aide en francais : [AIDE.md](AIDE.md)
- Help in English: [HELP.md](HELP.md)
- Notes d'installation : [INSTALLATION.md](INSTALLATION.md)

## Hygiene du depot

Ne publie pas les donnees locales :

- `env/`
- les fichiers personnels dans `audio/`
- les fichiers generes dans `output/`
- les transcriptions privees dans `txt/`
- les profils de voix clones dans `profiles/`
- les poids ou caches de modeles

Le fichier `.gitignore` est prepare pour cela.

## Licence

Apache License 2.0. Voir [LICENSE](LICENSE).
