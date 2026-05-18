# PaginaVox Gradio Interface

This folder contains the local web interface for PaginaVox.

## Start on Windows

From the project root:

```powershell
.\gradio\run_gradio_windows.bat
```

## Start on Linux

```bash
bash gradio/run_gradio_linux.sh
```

The Gradio URL is usually:

```text
http://localhost:7860
```

## Features

- Text input for the content to generate.
- Audio language selection.
- Built-in Qwen voice selection.
- Generation from an existing cloned profile.
- New voice profile creation from reference audio.
- Automatic Whisper transcription when the reference text is empty.
- Optional WAV merge into one final file.

## Francais

Ce dossier contient l'interface web locale de PaginaVox.

Windows :

```powershell
.\gradio\run_gradio_windows.bat
```

Linux :

```bash
bash gradio/run_gradio_linux.sh
```
