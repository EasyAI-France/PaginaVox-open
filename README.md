# PaginaVox Open

PaginaVox Open is a local command-line and Gradio application for generating speech with Qwen TTS.

It can:

- clone a voice from a reference audio file;
- use built-in Qwen voices;
- transcribe a reference audio file with Whisper when no transcript exists yet;
- generate one WAV file per non-empty text line;
- optionally merge generated WAV segments into one final audio file.

> French documentation is available in [README.fr.md](README.fr.md). The French help guide is [AIDE.md](AIDE.md).

## Requirements

- Windows or Linux.
- Python 3.12.
- NVIDIA GPU with CUDA support for Qwen TTS generation.
- Internet access on first install and first model download.

macOS is not currently supported for generation because the code loads Qwen models on `cuda:0`.

## Quick Start

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

The installer creates a local `env/` virtual environment and installs the required dependencies.

## Project Folders

- `audio/`: reference audio files for voice cloning.
- `txt/`: text files and generated Whisper transcripts.
- `output/`: generated WAV files.
- `profiles/`: cloned voice profiles.
- `gradio/`: local web interface.
- `Docker/`: NVIDIA Docker setup.
- `build/`: Windows executable build scripts.
- `Documents/`: user notices in DOCX format.
- `notebook/`: Colab notebook.

The runtime folders are ignored by Git except for their `.gitkeep` files.

## Command-Line Use

Run the script for your system, then choose:

1. the interface language;
2. the audio generation language;
3. the generation mode.

For voice cloning, place a reference audio file in `audio/`. If `txt/audio_name.txt` does not exist, PaginaVox automatically runs Whisper and creates the transcript.

Each non-empty text line becomes a separate audio file:

```text
output/example-001.wav
output/example-002.wav
output/example-003.wav
```

At the end, PaginaVox can merge the generated files into:

```text
output/example-compile.wav
```

## Gradio Interface

Start the local web interface:

Windows:

```powershell
.\gradio\run_gradio_windows.bat
```

Linux:

```bash
bash gradio/run_gradio_linux.sh
```

Then open the local URL printed by Gradio, usually:

```text
http://localhost:7860
```

## Windows Executable

To build a distributable Windows folder:

```powershell
.\install_env_windows.bat
.\build\build_windows_exe.bat
```

The folder to distribute is:

```text
dist/PaginaVox
```

See [build/BUILD_EXE_WINDOWS.md](build/BUILD_EXE_WINDOWS.md).

## Docker NVIDIA

The Docker setup is available in `Docker/`.

Windows:

```powershell
.\Docker\test_gpu.bat
.\Docker\build_windows.bat
.\Docker\run_windows.bat
```

Linux:

```bash
bash Docker/test_gpu.sh
bash Docker/build_linux_macos.sh
bash Docker/run_linux_macos.sh
```

See [Docker/README.md](Docker/README.md).

## Help

- English help: [HELP.md](HELP.md)
- French help: [AIDE.md](AIDE.md)
- Installation notes: [INSTALLATION.md](INSTALLATION.md)

## Repository Hygiene

Do not commit local runtime data:

- `env/`
- personal files in `audio/`
- generated files in `output/`
- private transcripts in `txt/`
- cloned voice profiles in `profiles/`
- model weights or caches

The `.gitignore` file is configured for this.

## License

Apache License 2.0. See [LICENSE](LICENSE).
