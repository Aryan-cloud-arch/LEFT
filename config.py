#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#
#    ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗ 
#   ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝ 
#   ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
#   ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
#   ╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
#    ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝ 
#
#   Configuration File for Telegram Auto Leave Tool
#   
#   GitHub  : github.com/Aryan-cloud-arch/LEFT
#   Telegram: @MaiHuAryan
#
# ═══════════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                         TELEGRAM API CREDENTIALS                            │
# │                                                                             │
# │  How to get these:                                                          │
# │  1. Go to https://my.telegram.org/apps                                      │
# │  2. Login with your phone number                                            │
# │  3. Click on "API Development Tools"                                        │
# │  4. Create a new application (any name works)                               │
# │  5. Copy the API_ID (numbers) and API_HASH (alphanumeric string)            │
# │                                                                             │
# └─────────────────────────────────────────────────────────────────────────────┘

# Your API ID from my.telegram.org (This is a number)
# Example: API_ID = 12345678
API_ID = 12345678  # <-- Replace with your API ID

# Your API Hash from my.telegram.org (This is a string)
# Example: API_HASH = "abcdef1234567890abcdef1234567890"
API_HASH = "your_api_hash_here"  # <-- Replace with your API Hash

# Your phone number with country code
# Example: PHONE_NUMBER = "+919876543210"
PHONE_NUMBER = "+91XXXXXXXXXX"  # <-- Replace with your phone number


# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                              APP SETTINGS                                   │
# └─────────────────────────────────────────────────────────────────────────────┘

# Session name (file where login session is saved)
# This allows you to stay logged in without OTP every time
SESSION_NAME = "telegram_session"

# Delay between leaving each group (in seconds)
# Lower = Faster but higher risk of rate limit/ban
# Higher = Slower but safer
# Recommended: 2-3 seconds
LEAVE_DELAY = 2

# Extra delay after every N groups (to avoid flood wait)
# After leaving this many groups, script will pause extra
BATCH_SIZE = 10

# Extra pause duration after each batch (in seconds)
BATCH_DELAY = 10

# Number of groups to show per page
GROUPS_PER_PAGE = 100

# Log file path
LOG_FILE = "logs/left_groups.txt"


# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                            COLOR SETTINGS                                   │
# └─────────────────────────────────────────────────────────────────────────────┘

# Enable/Disable colored output
ENABLE_COLORS = True

# You can customize colors if needed (used in ui.py)
# Available: RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
