#!/usr/bin/env bash
# ============================================================
#  Gunout Player — Édition France Bleu / ICI
#  Script d'installation automatique
#  Dépôt : https://github.com/gunout/france-bleu-app
# ============================================================

set -euo pipefail

# ----- Couleurs -----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ----- Bannière -----
banner() {
    echo -e "${BLUE}${BOLD}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║   🎙️  GUNOUT PLAYER — Édition France Bleu / ICI      ║"
    echo "║                                                       ║"
    echo "║   Installation automatique                            ║"
    echo "║   https://github.com/gunout/france-bleu-app           ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ----- Fonctions utilitaires -----
info()    { echo -e "${CYAN}[INFO]${NC} $*"; }
success() { echo -e "${GREEN}[✓]${NC} $*"; }
warn()    { echo -e "${YELLOW}[!]${NC} $*"; }
error()   { echo -e "${RED}[✗]${NC} $*" >&2; }
die()     { error "$*"; exit 1; }

# ----- Détection OS -----
detect_os() {
    case "$(uname -s)" in
        Linux*)   OS="linux" ;;
        Darwin*)  OS="macos" ;;
        *)        OS="unknown" ;;
    esac

    if [ "$OS" = "linux" ]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            DISTRO="${ID:-unknown}"
        else
            DISTRO="unknown"
        fi
    fi
}

# ----- Vérification des privilèges sudo -----
check_sudo() {
    if ! command -v sudo >/dev/null 2>&1; then
        warn "sudo n'est pas installé. Les étapes nécessitant les droits root échoueront."
        SUDO=""
    else
        SUDO="sudo"
    fi
}

# ============================================================
#  1. Installer les dépendances système
# ============================================================
install_system_deps() {
    info "Installation des dépendances système..."

    case "$OS" in
        linux)
            case "$DISTRO" in
                ubuntu|debian|linuxmint|pop|zorin)
                    $SUDO apt update
                    $SUDO apt install -y \
                        python3 python3-pip python3-venv \
                        libmpv2 mpv libqt6opengl6 \
                        wget curl
                    ;;
                fedora|rhel|centos)
                    $SUDO dnf install -y \
                        python3 python3-pip \
                        mpv mpv-libs qt6-qtbase \
                        wget curl
                    ;;
                arch|manjaro|endeavouros)
                    $SUDO pacman -Sy --noconfirm \
                        python python-pip \
                        mpv qt6-base \
                        wget curl
                    ;;
                *)
                    warn "Distribution Linux non reconnue : $DISTRO"
                    warn "Installez manuellement : python3, pip, mpv, libmpv, Qt6."
                    ;;
            esac
            ;;
        macos)
            if ! command -v brew >/dev/null 2>&1; then
                die "Homebrew n'est pas installé. Installez-le : https://brew.sh/"
            fi
            brew install python mpv wget
            ;;
        *)
            die "Système d'exploitation non supporté : $(uname -s)"
            ;;
    esac

    success "Dépendances système installées."
}

# ============================================================
#  2. Installer yt-dlp (version récente, binaire officiel)
# ============================================================
install_ytdlp() {
    info "Installation de yt-dlp (binaire officiel)..."

    local ytdlp_version
    ytdlp_version="$(yt-dlp --version 2>/dev/null || echo "absent")"

    if [ "$ytdlp_version" = "absent" ]; then
        warn "yt-dlp n'est pas installé. Installation..."
    else
        info "Version actuelle : $ytdlp_version"
        info "Mise à jour vers la dernière version..."
    fi

    if [ "$OS" = "macos" ]; then
        # Sur macOS, on utilise brew ou pip
        if command -v brew >/dev/null 2>&1; then
            brew upgrade yt-dlp 2>/dev/null || brew install yt-dlp
        else
            python3 -m pip install --upgrade --user yt-dlp
        fi
    else
        # Linux : binaire officiel dans /usr/local/bin
        $SUDO wget -q --show-progress \
            https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
            -O /usr/local/bin/yt-dlp
        $SUDO chmod a+rx /usr/local/bin/yt-dlp
        hash -r 2>/dev/null || true
    fi

    local new_version
    new_version="$(yt-dlp --version 2>/dev/null || echo "inconnu")"
    success "yt-dlp installé : $new_version"
}

# ============================================================
#  3. Créer l'environnement virtuel Python
# ============================================================
setup_venv() {
    info "Création de l'environnement virtuel Python (.venv)..."

    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        success "Environnement virtuel créé."
    else
        info "L'environnement virtuel existe déjà."
    fi

    # Activation
    # shellcheck disable=SC1091
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    elif [ -f ".venv/Scripts/activate" ]; then
        source .venv/Scripts/activate
    else
        die "Impossible d'activer l'environnement virtuel."
    fi

    python -m pip install --upgrade pip
    success "pip mis à jour."
}

# ============================================================
#  4. Installer les dépendances Python
# ============================================================
install_python_deps() {
    info "Installation des dépendances Python..."

    if [ ! -f "requirements.txt" ]; then
        warn "requirements.txt introuvable. Création..."
        cat > requirements.txt <<'EOF'
PyQt6>=6.6.0
PyQt6-Qt6>=6.6.0
PyQt6-sip>=13.6.0
python-mpv>=1.0.4
yt-dlp>=2025.1.0
EOF
        success "requirements.txt créé."
    fi

    pip install -r requirements.txt
    success "Dépendances Python installées."
}

# ============================================================
#  5. Vérifications finales
# ============================================================
verify() {
    info "Vérification de l'installation..."

    local ok=0

    if command -v mpv >/dev/null 2>&1; then
        success "mpv : $(mpv --version | head -1)"
    else
        error "mpv introuvable."
        ok=1
    fi

    if command -v yt-dlp >/dev/null 2>&1; then
        success "yt-dlp : $(yt-dlp --version)"
    else
        error "yt-dlp introuvable."
        ok=1
    fi

    if python -c "import PyQt6" 2>/dev/null; then
        success "PyQt6 : installé"
    else
        error "PyQt6 introuvable."
        ok=1
    fi

    if python -c "import mpv" 2>/dev/null; then
        success "python-mpv : installé"
    else
        error "python-mpv introuvable."
        ok=1
    fi

    if [ $ok -eq 0 ]; then
        success "Toutes les dépendances sont présentes."
    else
        warn "Certaines dépendances manquent. Vérifiez les messages ci-dessus."
    fi
}

# ============================================================
#  6. Lancer l'application (optionnel)
# ============================================================
launch_prompt() {
    echo
    echo -e "${BOLD}Voulez-vous lancer Gunout Player maintenant ? (o/N)${NC}"
    read -r answer
    case "$answer" in
        [oOyY]*)
            if [ -f "fr.py" ]; then
                info "Lancement de fr.py..."
                python fr.py
            else
                die "fr.py introuvable dans le dossier courant."
            fi
            ;;
        *)
            info "Lancement annulé."
            ;;
    esac
}

# ============================================================
#  MAIN
# ============================================================
main() {
    banner
    detect_os
    check_sudo

    info "Système détecté : $OS${DISTRO:+ ($DISTRO)}"
    echo

    install_system_deps
    echo
    install_ytdlp
    echo
    setup_venv
    echo
    install_python_deps
    echo
    verify

    echo
    echo -e "${GREEN}${BOLD}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║              ✓  INSTALLATION TERMINÉE  ✓              ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${BOLD}Pour lancer le player :${NC}"
    echo -e "  ${CYAN}source .venv/bin/activate${NC}"
    echo -e "  ${CYAN}python fr.py${NC}"
    echo

    launch_prompt
}

main "$@"
