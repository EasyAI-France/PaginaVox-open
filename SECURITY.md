# Security Policy

## Supported Versions

The public repository tracks the latest version on the `main` branch.

## Reporting a Vulnerability

Please do not publish private audio, transcripts, voice profiles, API tokens, model caches, or credentials in issues or pull requests.

If you find a security issue, report it privately to the repository owner or maintainer through the available GitHub contact method.

## Sensitive Local Data

PaginaVox can create or use files that may contain personal data:

- reference audio in `audio/`;
- transcripts in `txt/`;
- generated voice profiles in `profiles/`;
- generated audio in `output/`;
- local model caches.

These files are ignored by Git and should stay local unless you intentionally choose to share them.

## Francais

Ne publie pas d'audios prives, de transcriptions privees, de profils de voix, de tokens, de caches de modeles ou d'identifiants dans les issues ou pull requests.

Si tu trouves une faille de securite, signale-la en prive au proprietaire ou mainteneur du depot via le moyen de contact disponible sur GitHub.
