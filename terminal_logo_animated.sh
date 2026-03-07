#!/bin/bash
# Animated Terminal Logo with Typing Effect

# Color codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m'

# Get terminal dimensions
TERM_WIDTH=$(tput cols)
TERM_HEIGHT=$(tput lines)

# Clear screen and hide cursor
clear
tput civis

# Function to center text
center_text() {
    local text="$1"
    local text_length=${#text}
    local padding=$(( (TERM_WIDTH - text_length) / 2 ))
    printf "%*s" $padding ""
    echo "$text"
}

# Move cursor to center of screen
start_line=$(( (TERM_HEIGHT - 10) / 2 ))
tput cup $start_line 0

# Typing effect function
type_line() {
    local line="$1"
    local delay="${2:-0.005}"
    local text_length=${#line}
    local padding=$(( (TERM_WIDTH - text_length) / 2 ))

    printf "%*s" $padding ""
    for (( i=0; i<${#line}; i++ )); do
        echo -n "${line:$i:1}"
        sleep "$delay"
    done
    echo ""
}

# ASCII Art Lines
logo_lines=(
    "    _   _           _           _ _     _    "
    "   | \ | |         | |         (_) |   | |   "
    "   |  \| | __ _ ___| |__   ___ _| | __| |__  "
    "   | . \` |/ _\` / __| '_ \ / _ \ | |/ /| '_ \ "
    "   | |\  | (_| \__ \ | | |  __/ |   < | | | |"
    "   |_| \_|\__,_|___/_| |_|\___|_|_|\_\|_| |_|"
)

# Type each line with effect
for line in "${logo_lines[@]}"; do
    type_line "$line" 0.003
done

echo ""

# Create separator with animation
SEPARATOR_WIDTH=$((TERM_WIDTH - 4))
separator_padding=$(( (TERM_WIDTH - SEPARATOR_WIDTH) / 2 ))

# Animate separator from center outward
printf "%*s" $separator_padding ""
for (( i=0; i<SEPARATOR_WIDTH; i++ )); do
    echo -en "${CYAN}━${NC}"
    sleep 0.002
done
echo ""

# Fade in subtitle
sleep 0.2
echo -e "${GREEN}$(center_text "Ruby | Python Developer | AI/ML Engineer")${NC}"

# Animate bottom separator
printf "%*s" $separator_padding ""
for (( i=0; i<SEPARATOR_WIDTH; i++ )); do
    echo -en "${CYAN}━${NC}"
    sleep 0.002
done
echo ""

echo ""

# Show cursor again
tput cnorm
