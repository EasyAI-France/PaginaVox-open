# Aide PaginaVox Open

## 1. Installer

Windows :

```powershell
.\install_env_windows.bat
```

Linux :

```bash
bash install_env_linux.sh
```

Le script cree un environnement virtuel local `env/` dans le dossier du projet.

## 2. Lancer

Windows :

```powershell
.\run_windows.bat
```

Linux :

```bash
bash run_linux.sh
```

## 3. Cloner une voix

1. Place ton audio de reference dans `audio/`.
2. Lance PaginaVox.
3. Choisis le mode de clonage depuis un audio.
4. Choisis ton fichier audio.
5. Donne un nom au nouveau profil.

Si `txt/nom_audio.txt` n'existe pas, Whisper se lance automatiquement et cree la transcription.

Le profil cree est sauvegarde dans `profiles/`.

## 4. Generer avec une voix Qwen existante

1. Lance PaginaVox.
2. Choisis le mode voix Qwen existante.
3. Choisis une voix dans la liste.
4. Choisis un fichier texte ou saisis le texte a la main.

## 5. Textes et fichiers audio

Chaque ligne non vide devient un fichier WAV separe.

Exemple avec le nom de sortie `test` :

```text
output/test-001.wav
output/test-002.wav
output/test-003.wav
```

A la fin, PaginaVox peut compiler les fichiers dans :

```text
output/test-compile.wav
```

## 6. Problemes courants

### `No module named 'torch'`

L'environnement Python n'est pas installe ou pas active. Relance le script d'installation de ton systeme.

### Environnement Python casse ou obsolete

Supprime ou recree `env/` avec le script d'installation :

```powershell
.\install_env_windows.bat
```

### Whisper ne trouve pas de texte

Verifie que l'audio est clair et que la langue choisie correspond bien a l'audio.

### CUDA ou carte graphique

La generation Qwen utilise actuellement `cuda:0`. Il faut une carte NVIDIA compatible CUDA avec des pilotes recents.

## 7. Avant de publier sur GitHub

Ne publie pas :

- le dossier `env/` ;
- tes audios personnels dans `audio/` ;
- les sorties dans `output/` ;
- les profils `.pkl` dans `profiles/` ;
- les transcriptions privees dans `txt/` ;
- les poids ou caches de modeles.

Le fichier `.gitignore` est prepare pour cela.

## 8. Interface Gradio

L'interface Gradio permet d'utiliser PaginaVox avec des zones de saisie au lieu des questions en terminal.

Windows :

```powershell
.\gradio\run_gradio_windows.bat
```

Linux :

```bash
bash gradio/run_gradio_linux.sh
```

Elle propose :

- une zone de texte ;
- le choix de la langue audio ;
- le choix de la voix Qwen ;
- le clonage depuis un profil existant ;
- la creation d'un nouveau profil depuis un audio de reference ;
- la transcription Whisper automatique si le texte de reference est vide ;
- la compilation optionnelle en un seul WAV.

## 9. Creer un executable Windows

Sur le PC qui fabrique l'application :

```powershell
.\install_env_windows.bat
.\build\build_windows_exe.bat
```

Le dossier a distribuer sera :

```text
dist/PaginaVox
```

Les utilisateurs lancent ensuite :

```text
PaginaVox.exe
```

Ils n'ont pas besoin d'installer Python ou Conda, mais ils doivent avoir une carte NVIDIA compatible et des pilotes NVIDIA recents.

Voir [build/BUILD_EXE_WINDOWS.md](build/BUILD_EXE_WINDOWS.md).

## 10. Docker NVIDIA

Les fichiers Docker sont dans le dossier `Docker/`.

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

L'interface Gradio sera disponible sur :

```text
http://localhost:7860
```

Voir [Docker/README.md](Docker/README.md).
