#!/usr/bin/env bash
# Установка глобальных правил и скиллов Kimi Code через симлинки.
# Идемпотентно: можно запускать повторно.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIMI_DIR="$HOME/.kimi-code"
SKILLS_DIR="$HOME/.config/agents/skills"

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
