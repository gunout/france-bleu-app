<div align="center">

# 🎙️ Gunout Player — Édition France Bleu / ICI

**Lecteur audio & vidéo tout-en-un pour les 44 radios France Bleu et les flux ICI Matin**

[![Repo](https://img.shields.io/badge/GitHub-gunout%2Ffrance--bleu--app-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/gunout/france-bleu-app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6%2B-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![mpv](https://img.shields.io/badge/mpv-0.35%2B-691F69?style=for-the-badge&logo=mpv&logoColor=white)](https://mpv.io/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2025%2B-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)]()

[Fonctionnalités](#-fonctionnalités) · [Installation](#-installation) · [Utilisation](#-utilisation) · [FAQ](#-faq)

</div>

---

## 📖 À propos

**Gunout Player — Édition France Bleu / ICI** est un lecteur multimédia de bureau conçu pour écouter les **44 radios locales France Bleu** (désormais **ICI**) et regarder les **matinales filmées** diffusées simultanément sur les chaînes régionales **France 3**, ainsi que le direct de **France Info TV** via YouTube.

Interface sombre et minimaliste, intégration native de `mpv` via `libmpv`, support complet des flux **Icecast**, **HLS (M3U8)** et **YouTube** grâce à `yt-dlp`.

> ⚠️ **Note** : Depuis janvier 2025, France Bleu est devenue **ICI**. Les flux Icecast conservent toutefois l'ancien préfixe `fb...` (ex. `fbalsace-midfi.mp3`) et restent parfaitement fonctionnels.

---

## ✨ Fonctionnalités

### 🎧 Audio
- **44 radios France Bleu** — tous les flux Icecast officiels de Radio France
- Lecture stable en direct (MP3 / AAC)
- Volume réglable, mute, pause, stop

### 📺 Vidéo
- **12 flux ICI Matin** — matinales filmées via France 3 régions (HLS)
- **France Info TV** — direct YouTube intégré nativement
- Support HLS (`.m3u8`) et YouTube (via `yt-dlp`)
- Rendu OpenGL natif via `wid` — pas de surcoût CPU

### 🎨 Interface
- Fenêtre frameless avec coins arrondis
- **Visualiseur audio bleu France Bleu** (32 barres animées)
- Thème sombre avec accent bleu (`#3d7bd9`)
- **Barre de recherche** temps réel
- **Filtres RADIOS / TV / TOUT**
- Auto-hide des contrôles après 3,5 s d'inactivité
- Repli de fenêtre (mode mini 70 px)
- Resize par les bords, déplacement par glisser

### ⚙️ Technique
- Intégration native `libmpv` (vidéo) + `mpv` audio-only
- `yt-dlp` pour YouTube (avec mise à jour en un clic)
- Aucune dépendance à `ffmpeg` pour l'audio
- Compatible Linux, macOS, Windows

---

## 📦 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/gunout/france-bleu-app.git
cd france-bleu-app
```

### 2. Prérequis système

#### 🐧 Debian / Ubuntu / Linux Mint

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
                    libmpv2 mpv libqt6opengl6 \
                    wget curl
```

#### 🐧 Fedora

```bash
sudo dnf install -y python3 python3-pip mpv mpv-libs qt6-qtbase
```

#### 🐧 Arch / Manjaro

```bash
sudo pacman -S python python-pip mpv qt6-base
```

#### 🍎 macOS

```bash
brew install python mpv
```

#### 🪟 Windows

1. Installez [Python 3.10+](https://www.python.org/downloads/)
2. Téléchargez [libmpv](https://sourceforge.net/projects/mpv-player-windows/files/libmpv/) et placez `libmpv-2.dll` dans le dossier du projet
3. Installez [yt-dlp](https://github.com/yt-dlp/yt-dlp/releases) et ajoutez-le au `PATH`

### 3. Installer `yt-dlp` (version récente obligatoire)

> ⚠️ **Important** : `yt-dlp` installé via `apt` est souvent obsolète. YouTube change régulièrement son API. Utilisez le **binaire officiel** :

```bash
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
     -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

Vérifiez :

```bash
yt-dlp --version
# → 2025.xx.xx ou plus récent
```

### 4. Installer les dépendances Python

```bash
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate.bat        # Windows

pip install -r requirements.txt
```

### 5. Fichier `requirements.txt`

```txt
PyQt6>=6.6.0
PyQt6-Qt6>=6.6.0
PyQt6-sip>=13.6.0
python-mpv>=1.0.4
yt-dlp>=2025.1.0
```

---

## 🚀 Utilisation

### Lancement

```bash
python3 fr.py
```

### Comportement au démarrage

1. La fenêtre s'affiche avec le visualiseur bleu.
2. Après **1 seconde**, **France Info TV** se lance automatiquement.
3. Vous pouvez ensuite :
   - Cliquer sur **RADIOS** pour filtrer les 44 radios France Bleu
   - Cliquer sur **TV** pour filtrer les flux vidéo (ICI Matin + France Info)
   - Cliquer sur **TOUT** pour tout afficher
   - Double-cliquer sur une station pour la lancer

### Raccourcis

| Action | Méthode |
|---|---|
| Lancer une station | Double-clic |
| Pause / Reprendre | Bouton ▶/⏸ |
| Arrêter | Bouton ⏹ |
| Muet | Bouton 🔊 |
| Régler le volume | Curseur |
| Replier les contrôles | Bouton ⌄ |
| Replier la fenêtre | Bouton ⌃ (en haut à droite) |
| Déplacer la fenêtre | Glisser n'importe où |
| Redimensionner | Tirer sur les bords |

---

## 📸 Aperçu

### 🎵 Mode Audio — Visualiseur bleu France Bleu

```
┌─────────────────────────────────────────────────┐
│  FRANCE BLEU   [RADIOS] [TV] [TOUT] [INFO]  ─ ×│
│  by gleaphe — Édition France Bleu / ICI         │
│                                                 │
│    ▁▃▅▇█▇▅▃▁▃▅▇█▇▅▃▁▃▅▇█▇▅▃▁▃▅▇█▇▅▃▁         │
│           FRANCE BLEU PARIS                     │
│              EN DIRECT                          │
│  ▶ ⏹  EN DIRECT                    🔊 ▬▬▬ 80  ⌄│
│                                                 │
│  🔍 RECHERCHER UNE STATION...                   │
│  44 RADIOS FRANCE BLEU / ICI                    │
│  📻  France Bleu Alsace                         │
│  📻  France Bleu Armorique                      │
│  ...                                            │
└─────────────────────────────────────────────────┘
```

### 📺 Mode Vidéo — ICI Matin / France Info

```
┌─────────────────────────────────────────────────┐
│  FRANCE BLEU   [RADIOS] [TV] [TOUT] [INFO]  ─ ×│
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │
│  │        ▶ ICI MATIN — FRANCE INFO TV       │ │
│  │              [EN DIRECT]                  │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│  ▶ ⏹  EN DIRECT                    🔊 ▬▬▬ 80  ⌄│
│                                                 │
│  🔍 RECHERCHER UNE STATION...                   │
│  13 FLUX TV (ICI MATIN + FRANCE INFO)           │
│  📺  ICI Matin — France 3 Alsace                │
│  📺  France Info — Direct YouTube               │
└─────────────────────────────────────────────────┘
```

---

## 🗂️ Structure du projet

```
france-bleu-app/
├── fr.py               # Application principale
├── logo.png            # Logo (optionnel, remplacé par texte si absent)
├── requirements.txt    # Dépendances Python
├── LICENSE             # Licence MIT
└── README.md           # Ce fichier
```

---

## 🛠️ Dépannage

### ❌ Erreur `Precondition check failed` ou `No video formats found`

**Cause** : `yt-dlp` est trop vieux pour l'API YouTube actuelle.

**Solution** :

```bash
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
     -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
hash -r
yt-dlp --version   # doit être ≥ 2025
```

### ❌ Erreur `qt.qpa.theme.gnome: dbus reply error`

**Cause** : votre système n'a pas le portail XDG `org.freedesktop.portal.Settings` (fréquent sous GNOME minimal ou WSL).

**Solution** : ce message est **inoffensif**, il n'empêche pas le fonctionnement. Pour le masquer :

```bash
export QT_QPA_PLATFORMTHEME=
```

Ou installez :

```bash
sudo apt install xdg-desktop-portal xdg-desktop-portal-gnome
```

### ❌ Aucun son sur les radios

**Vérifiez** :
1. Que `mpv` est installé : `mpv --version`
2. Que `pulseaudio` ou `pipewire` tourne : `pactl info`
3. Que le volume système n'est pas à zéro

### ❌ La vidéo YouTube ne démarre pas

Testez en ligne de commande :

```bash
yt-dlp --get-url https://www.youtube.com/watch?v=NG7ZX42nZKc
```

- Si une URL s'affiche → le player fonctionnera.
- Si erreur → mettez `yt-dlp` à jour (voir ci-dessus).

### ❌ Les flux ICI Matin ne s'affichent pas

Les flux France 3 diffusent la matinale **uniquement de 7h à 9h en semaine**. En dehors, c'est la programmation régionale habituelle.

Ils sont également **géo-restreints** — hors de France métropolitaine, certains flux peuvent être bloqués.

---

## ❓ FAQ

**Q : Pourquoi certains flux ne fonctionnent pas ?**
R : Les flux France 3 (ICI Matin) sont communautaires et peuvent changer. Les flux France Bleu (Icecast) sont officiels et stables.

**Q : Puis-je ajouter mes propres stations ?**
R : Oui, modifiez les listes `FRANCE_BLEU_AUDIO` ou `FRANCE_3_VIDEO` au début de `fr.py`.

**Q : Le player fonctionne-t-il sous Windows ?**
R : Oui, à condition d'installer `libmpv-2.dll` et `yt-dlp` dans le `PATH`.

**Q : Comment mettre à jour yt-dlp facilement ?**
R : Ajoutez un alias dans votre `.bashrc` :

```bash
alias update-ytdlp='sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp && sudo chmod a+rx /usr/local/bin/yt-dlp && hash -r && yt-dlp --version'
```

**Q : Puis-je désactiver le lancement automatique de France Info ?**
R : Oui, dans `showEvent`, commentez la ligne `QTimer.singleShot(1000, self._autostart_france_info)`.

---

## 🧰 Stack technique

| Composant | Rôle |
|---|---|
| **Python 3.10+** | Langage principal |
| **PyQt6** | Interface graphique |
| **python-mpv** | Binding Python pour `libmpv` |
| **libmpv** | Moteur de lecture audio/vidéo |
| **yt-dlp** | Résolution des flux YouTube |
| **Qt6 OpenGL** | Rendu vidéo natif (via `wid`) |

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commit (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Push (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une Pull Request

---

## 📜 Licence

Distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.

---

## 👤 Auteur

**gleaphe** / **gunout**

- 🐙 GitHub : [@gunout](https://github.com/gunout)
- 📦 Dépôt : [france-bleu-app](https://github.com/gunout/france-bleu-app)


---

## 🙏 Remerciements

- [Radio France](https://www.radiofrance.fr/) pour les flux Icecast France Bleu
- [France Télévisions](https://www.france.tv/) pour les flux ICI Matin
- [mpv](https://mpv.io/) et [yt-dlp](https://github.com/yt-dlp/yt-dlp) pour la lecture multimédia

---

<div align="center">

**⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile ! ⭐**

*Fait avec ❤️ à La Réunion*

</div>
