# Installation

This guide explains how to install and run PaginaVox Open locally.

## English

### Runtime Folders

- `audio/`: reference audio files for voice cloning.
- `txt/`: text files and Whisper transcripts.
- `output/`: generated WAV files.
- `profiles/`: cloned voice profiles.
- `env/`: local Python virtual environment created by the install scripts.

Each non-empty line in a text file becomes one audio file:

```text
name-001.wav
name-002.wav
name-003.wav
```

### Recommended Install: Local `env`

This installation stays inside the project folder and does not modify the system Python.

#### Windows

1. Install Python 3.12.
2. Open PowerShell in the project folder.
3. Run:

```powershell
.\install_env_windows.bat
```

4. Start PaginaVox:

```powershell
.\run_windows.bat
```

#### Linux

1. Install Python 3.12 and `venv`.
2. Open a terminal in the project folder.
3. Run:

```bash
bash install_env_linux.sh
```

4. Start PaginaVox:

```bash
bash run_linux.sh
```

### Conda Option

```bash
conda env create -f environment.yml
conda activate paginavox-command
python main.py
```

### GPU Note

Qwen generation currently loads models on `cuda:0`, so an NVIDIA CUDA GPU is required.

## Francais

### Dossiers

- `audio/` : audios de reference pour le clonage de voix.
- `txt/` : fichiers `.txt` a lire et transcriptions Whisper.
- `output/` : fichiers `.wav` generes.
- `profiles/` : profils de voix clones.
- `env/` : environnement Python local cree par les scripts d'installation.

Chaque ligne non vide d'un fichier `.txt` devient un fichier audio :

```text
nom-001.wav
nom-002.wav
nom-003.wav
```

### Installation recommandee : environnement local `env`

Cette installation reste dans le dossier du projet. Elle ne modifie pas le Python systeme.

#### Windows

1. Installe Python 3.12.
2. Ouvre PowerShell dans le dossier du projet.
3. Lance :

```powershell
.\install_env_windows.bat
```

4. Lance PaginaVox :

```powershell
.\run_windows.bat
```

#### Linux

1. Installe Python 3.12 et `venv`.
2. Ouvre un terminal dans le dossier du projet.
3. Lance :

```bash
bash install_env_linux.sh
```

4. Lance PaginaVox :

```bash
bash run_linux.sh
```

### Option Conda

```bash
conda env create -f environment.yml
conda activate paginavox-command
python main.py
```

### Note GPU

La generation Qwen charge actuellement les modeles sur `cuda:0`, donc une carte NVIDIA compatible CUDA est requise.
