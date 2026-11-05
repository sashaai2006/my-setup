#!/usr/bin/env bash
# Установка глобальных правил и скиллов Kimi Code через симлинки.
# Идемпотентно: можно запускать повторно.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIMI_DIR="$HOME/.kimi-code"
SKILLS_DIR="$HOME/.config/agents/skills"

usage() {
  cat <<'EOF'
Usage: install.sh [options]

  --skills-dir PATH   Куда ставить скиллы (по умолчанию: ~/.config/agents/skills)
  --agents            Сокращение для --skills-dir ~/.agents/skills
  -h, --help          Показать справку
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --skills-dir)
      [ $# -ge 2 ] || { echo "error: --skills-dir требует путь" >&2; exit 1; }
      SKILLS_DIR="$2"
      shift 2
      ;;
    --agents)
      SKILLS_DIR="$HOME/.agents/skills"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: неизвестный аргумент: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

mkdir -p "$KIMI_DIR" "$SKILLS_DIR"

# Глобальные правила: существующий файл переименуем в .bak
if [ -f "$KIMI_DIR/AGENTS.md" ] && [ ! -L "$KIMI_DIR/AGENTS.md" ]; then
  mv "$KIMI_DIR/AGENTS.md" "$KIMI_DIR/AGENTS.md.bak"
  echo "backup: $KIMI_DIR/AGENTS.md -> AGENTS.md.bak"
fi
ln -sfn "$REPO_DIR/kimi-code/AGENTS.md" "$KIMI_DIR/AGENTS.md"
echo "linked: $KIMI_DIR/AGENTS.md"

# Скиллы: симлинк для каждого скилла; существующие не-ссылки бэкапим
for skill_dir in "$REPO_DIR"/skills/*/; do
  name="$(basename "$skill_dir")"
  target="$SKILLS_DIR/$name"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    mv "$target" "$target.bak"
    echo "backup: $target -> $target.bak"
  fi
  ln -sfn "$skill_dir" "$target"
  echo "linked: $target"
done

echo "done."
