#!/bin/bash
# Matrix-style Terminal Logo Animation

# Color codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
MATRIX_GREEN='\033[1;32m'
DIM='\033[2m'
NC='\033[0m'

# Get terminal dimensions
TERM_WIDTH=$(tput cols)
TERM_HEIGHT=$(tput lines)

# Clear screen and hide cursor
clear
tput civis

# ASCII Logo
logo_lines=(
    "    _   _           _           _ _     _    "
    "   | \ | |         | |         (_) |   | |   "
    "   |  \| | __ _ ___| |__   ___ _| | __| |__  "
    "   | . \` |/ _\` / __| '_ \ / _ \ | |/ /| '_ \ "
    "   | |\  | (_| \__ \ | | |  __/ |   < | | | |"
    "   |_| \_|\__,_|___/_| |_|\___|_|_|\_\|_| |_|"
)

# Function to center text
center_text() {
    local text="$1"
    local text_length=${#text}
    local padding=$(( (TERM_WIDTH - text_length) / 2 ))
    printf "%*s" $padding ""
    echo "$text"
}

# Calculate starting position
start_line=$(( (TERM_HEIGHT - 10) / 2 ))

# Matrix rain effect (brief)
for rain in {1..15}; do
    tput cup $((start_line - 2)) 0
    for line in "${logo_lines[@]}"; do
        text_length=${#line}
        padding=$(( (TERM_WIDTH - text_length) / 2 ))
        printf "%*s" $padding ""

        for (( i=0; i<${#line}; i++ )); do
            if [ $((RANDOM % 3)) -eq 0 ]; then
                echo -en "${MATRIX_GREEN}${DIM}$((RANDOM % 10))${NC}"
            else
                echo -n " "
            fi
        done
        echo ""
    done
    sleep 0.05
done

# Clear and reveal actual logo with fade effect
clear
tput cup $start_line 0

# Reveal logo line by line with color
for line in "${logo_lines[@]}"; do
    echo -e "${GREEN}$(center_text "$line")${NC}"
    sleep 0.1
done

echo ""

# Create separator
SEPARATOR_WIDTH=$((TERM_WIDTH - 4))
separator=$(printf '━%.0s' $(seq 1 $SEPARATOR_WIDTH))
separator_padding=$(( (TERM_WIDTH - SEPARATOR_WIDTH) / 2 ))

printf "%*s" $separator_padding ""
echo -e "${CYAN}${separator}${NC}"

sleep 0.15
center_text "Ruby | Python Developer | AI/ML Engineer"

printf "%*s" $separator_padding ""
echo -e "${CYAN}${separator}${NC}"

echo ""

# Show cursor
tput cnorm
