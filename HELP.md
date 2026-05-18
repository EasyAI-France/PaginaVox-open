# PaginaVox Open Help

## 1. Install

Windows:

```powershell
.\install_env_windows.bat
```

Linux:

```bash
bash install_env_linux.sh
```

The installer creates a local `env/` virtual environment in the project folder.

## 2. Start

Windows:

```powershell
.\run_windows.bat
```

Linux:

```bash
bash run_linux.sh
```

## 3. Clone a Voice

1. Put a reference audio file in `audio/`.
2. Start PaginaVox.
3. Choose `Clone a voice from an audio file`.
4. Select the audio file.
5. Give the new profile a name.

If `txt/audio_name.txt` does not exist, Whisper runs automatically and creates the transcript.

The generated profile is saved in `profiles/`.

## 4. Generate with a Built-In Qwen Voice

1. Start PaginaVox.
2. Choose the built-in Qwen voice mode.
3. Select a voice from the list.
4. Select a text file or enter text manually.

## 5. Text and Audio Files

Each non-empty line becomes a separate WAV file.

Example with output name `test`:

```text
output/test-001.wav
output/test-002.wav
output/test-003.wav
```

At the end, PaginaVox can merge the files into:

```text
output/test-compile.wav
```

## 6. Common Issues

### `No module named 'torch'`

The Python environment is missing or not activated. Run the installer again for your operating system.

### Broken or obsolete Python environment

Delete or recreate `env/` with the installer:

```powershell
.\install_env_windows.bat
```

### Whisper cannot find the text

Check that the audio is clear and that the selected language matches the reference audio.

### CUDA or GPU errors

Qwen generation currently uses `cuda:0`. Use a compatible NVIDIA GPU with recent drivers.

## 7. Before Publishing to GitHub

Do not publish:

- `env/`;
- personal audio files in `audio/`;
- generated audio files in `output/`;
- `.pkl` profiles in `profiles/`;
- private transcripts in `txt/`;
- downloaded model weights or caches.

The `.gitignore` file is configured for this.

## 8. Gradio Interface

The Gradio interface provides form fields instead of terminal prompts.

Windows:

```powershell
.\gradio\run_gradio_windows.bat
```

Linux:

```bash
bash gradio/run_gradio_linux.sh
```

It includes:

- a text input area;
- audio language selection;
- built-in Qwen voice selection;
- generation from an existing voice profile;
- creation of a new profile from reference audio;
- automatic Whisper transcription when reference text is empty;
- optional merge into one WAV file.

## 9. Build a Windows Executable

On the build machine:

```powershell
.\install_env_windows.bat
.\build\build_windows_exe.bat
```

The distributable folder is:

```text
dist/PaginaVox
```

Users then run:

```text
PaginaVox.exe
```

They do not need Python or Conda installed, but they need a compatible NVIDIA GPU and recent NVIDIA drivers.

See [build/BUILD_EXE_WINDOWS.md](build/BUILD_EXE_WINDOWS.md).

## 10. Docker NVIDIA

Docker files are in `Docker/`.

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

The Gradio interface will be available at:

```text
http://localhost:7860
```

See [Docker/README.md](Docker/README.md).
