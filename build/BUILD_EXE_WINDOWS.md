# Build a Windows Executable

This guide explains how to create a distributable Windows version of PaginaVox.

## Expected Result

The build creates:

```text
dist/PaginaVox/PaginaVox.exe
```

Distribute the whole `dist/PaginaVox` folder, not only the `.exe` file.
The folder contains the executable, embedded Python files, Torch, Qwen TTS, and required libraries.

Users do not need to install Python or Conda.

## Build Machine Requirements

- Windows.
- Python 3.12.
- Internet access while installing dependencies.
- Enough disk space. Torch and AI dependencies can use several GB.

## Build

In PowerShell or CMD:

```powershell
.\install_env_windows.bat
.\build\build_windows_exe.bat
```

## Custom Icon

To replace the default executable icon, place an icon file here:

```text
build/icons/icon.ico
```

Then run:

```powershell
.\build\build_windows_exe.bat
```

The `.ico` file should ideally contain several sizes, for example 16x16, 32x32, 48x48, and 256x256.

When the build is complete, distribute this folder:

```text
dist/PaginaVox
```

You can compress it as a `.zip`.

## User Machine Requirements

- Windows 10 ou Windows 11 64 bits.
- NVIDIA CUDA-compatible GPU.
- Recent NVIDIA drivers.
- Internet access on first launch if Qwen/Whisper models are not already cached.

## First Launch

The user starts:

```text
PaginaVox.exe
```

These folders are created/used next to the executable:

- `audio/`
- `txt/`
- `output/`
- `profiles/`

## Important

The first launch can be slow because models may be downloaded from Hugging Face.

For a fully offline version, you must also prepare and distribute the Hugging Face model cache. That version will be much larger.

## Francais

Ce guide sert a fabriquer une version Windows distribuable de PaginaVox.

Le build cree `dist/PaginaVox/PaginaVox.exe`. Il faut distribuer tout le dossier `dist/PaginaVox`, pas seulement le fichier `.exe`.

Commandes :

```powershell
.\install_env_windows.bat
.\build\build_windows_exe.bat
```

Les utilisateurs n'ont pas besoin d'installer Python ou Conda, mais ils doivent avoir Windows 10/11 64 bits, une carte NVIDIA compatible CUDA, des pilotes NVIDIA recents, et une connexion internet au premier lancement si les modeles ne sont pas encore en cache.
