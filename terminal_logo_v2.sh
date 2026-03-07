#!/bin/bash
# Terminal startup logo for Nasheikh's machine (Dynamic Centered Version)

# Color codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Get terminal width
TERM_WIDTH=$(tput cols)

# Function to center text
center_text() {
    local text="$1"
    local text_length=${#text}
    local padding=$(( (TERM_WIDTH - text_length) / 2 ))
    printf "%*s" $padding ""
    echo "$text"
}

# Function to center colored text
center_colored() {
    local text="$1"
    # Strip color codes to calculate actual text length
    local clean_text=$(echo -e "$text" | sed 's/\x1b\[[0-9;]*m//g')
    local text_length=${#clean_text}
    local padding=$(( (TERM_WIDTH - text_length) / 2 ))
    printf "%*s" $padding ""
    echo -e "$text"
}

# ASCII Art Logo (width: 50 characters)
ASCII_LOGO=(
    "    _   _           _           _ _     _    "
    "   | \ | |         | |         (_) |   | |   "
    "   |  \| | __ _ ___| |__   ___ _| | __| |__  "
    "   | . \` |/ _\` / __| '_ \ / _ \ | |/ /| '_ \ "
    "   | |\  | (_| \__ \ | | |  __/ |   < | | | |"
    "   |_| \_|\__,_|___/_| |_|\___|_|_|\_\|_| |_|"
)

# Print centered ASCII art
for line in "${ASCII_LOGO[@]}"; do
    center_text "$line"
done

# Create dynamic separator line (window width - 4)
SEPARATOR_WIDTH=$((TERM_WIDTH - 4))
separator=$(printf '━%.0s' $(seq 1 $SEPARATOR_WIDTH))

# Calculate padding for centering separator
separator_padding=$(( (TERM_WIDTH - SEPARATOR_WIDTH) / 2 ))

# Print centered separator and subtitle
printf "%*s" $separator_padding ""
echo -e "${CYAN}${separator}${NC}"
center_colored "${GREEN}Ruby ${NC}|${GREEN} Python Developer ${NC}|${YELLOW} AI/ML Engineer${NC}"
printf "%*s" $separator_padding ""
echo -e "${CYAN}${separator}${NC}"
echo ""
