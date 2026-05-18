# PaginaVox NVIDIA Docker

This folder contains the files required to build and run PaginaVox in Docker with an NVIDIA GPU.

## Requirements

- Docker Desktop with WSL2 backend on Windows, or Docker Engine on Linux.
- Recent NVIDIA driver.
- Working NVIDIA GPU support in Docker.
- Internet access for the first image build and first model download.

## Test Docker GPU Access

Windows:

```powershell
.\Docker\test_gpu.bat
```

Linux:

```bash
bash Docker/test_gpu.sh
```

The command should print `nvidia-smi`.

## Build the Image

Windows:

```powershell
.\Docker\build_windows.bat
```

Linux:

```bash
bash Docker/build_linux_macos.sh
```

## Start PaginaVox Gradio

Windows:

```powershell
.\Docker\run_windows.bat
```

Linux:

```bash
bash Docker/run_linux_macos.sh
```

Then open:

```text
http://localhost:7860
```

## Start Command-Line Mode in Docker

```bash
docker compose -f Docker/docker-compose.yml run --rm paginavox python3 main.py
```

## Volumes

These local folders are mounted in the container:

- `audio/`
- `txt/`
- `output/`
- `profiles/`

The Hugging Face cache is stored in the Docker volume `paginavox-hf-cache`.

## macOS Note

Docker Desktop on macOS does not provide NVIDIA CUDA GPU access. This Docker setup is intended for Windows with WSL2/Docker Desktop or Linux with NVIDIA Container Toolkit.

## Francais

Ce dossier contient les fichiers pour construire et lancer PaginaVox dans Docker avec GPU NVIDIA.

### Prerequis

- Docker Desktop avec backend WSL2 sur Windows, ou Docker Engine sur Linux.
- Pilote NVIDIA recent.
- Support GPU Docker fonctionnel.
- Connexion internet au premier build et au premier lancement des modeles.

### Tester le GPU Docker

Windows :

```powershell
.\Docker\test_gpu.bat
```

Linux :

```bash
bash Docker/test_gpu.sh
```

La commande doit afficher `nvidia-smi`.

### Construire l'image

Windows :

```powershell
.\Docker\build_windows.bat
```

Linux :

```bash
bash Docker/build_linux_macos.sh
```

### Lancer PaginaVox Gradio

Windows :

```powershell
.\Docker\run_windows.bat
```

Linux :

```bash
bash Docker/run_linux_macos.sh
```

Ouvre ensuite :

```text
http://localhost:7860
```

## Useful Sources

- Docker GPU Desktop Windows: https://docs.docker.com/desktop/features/gpu/
- Docker Compose GPU: https://docs.docker.com/compose/gpu-support/
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/
