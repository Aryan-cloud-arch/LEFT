#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║         TELEGRAM AUTO LEAVE GROUPS & CHANNELS                 ║
║  📱 Telegram: @MaiHuAryan                                     ║
║  💻 GitHub:   github.com/Aryan-cloud-arch/LEFT                ║
╚═══════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════
from telethon import TelegramClient                # Main Telegram client library
from telethon.tl.types import Channel, Chat        # To identify groups/channels
from telethon.tl.functions.channels import LeaveChannelRequest      # Leave supergroup/channel
from telethon.tl.functions.messages import DeleteChatUserRequest    # Leave basic group
import asyncio          # For async operations
import os               # For file operations, clear screen
import json             # For saving/loading config
from datetime import datetime   # For timestamps in logs


# ═══════════════════════════════════════════════════════════════
# COLORS FOR TERMINAL
# ═══════════════════════════════════════════════════════════════
class C:
    """
    Terminal color codes for beautiful output.
    Works on Termux, Linux, Mac. Windows may need colorama.
    """
    R = '\033[91m'      # Red - errors, warnings, channels
    G = '\033[92m'      # Green - success, groups
    Y = '\033[93m'      # Yellow - prompts, info
    B = '\033[94m'      # Blue - channels
    M = '\033[95m'      # Magenta - highlights
    C = '\033[96m'      # Cyan - borders, headers
    W = '\033[97m'      # White - normal text
    X = '\033[0m'       # Reset - clear formatting


# ═══════════════════════════════════════════════════════════════
# CONFIG FILE PATH
# ═══════════════════════════════════════════════════════════════
CONFIG_FILE = "config.json"     # Stores API_ID, API_HASH, PHONE for next time


# ═══════════════════════════════════════════════════════════════
# CONFIG FUNCTIONS - Save/Load credentials
# ═══════════════════════════════════════════════════════════════
def load_config():
    """
    Load saved config from config.json if exists.
    
    Returns:
        dict: {'api_id': ..., 'api_hash': ..., 'phone': ...} or empty dict
    """
    # Check if config file exists
    if os.path.exists(CONFIG_FILE):
        try:
            # Open and read JSON file
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            # If file is corrupted, return empty
            return {}
    return {}


def save_config(api_id, api_hash, phone):
    """
    Save credentials to config.json for next time.
    
    Args:
        api_id: Telegram API ID (integer)
        api_hash: Telegram API Hash (string)
        phone: Phone number with country code (string)
    """
    config = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone': phone
    }
    # Write to JSON file
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_credentials():
    """
    Get API credentials - either from saved config or ask user.
    
    Flow:
    1. Try to load from config.json
    2. If found, ask if user wants to use saved credentials
    3. If not found or user wants new, ask for input
    4. Save new credentials for next time
    
    Returns:
        tuple: (api_id, api_hash, phone)
    """
    # Try loading saved config
    config = load_config()
    
    # If config exists, ask if user wants to use it
    if config and config.get('api_id') and config.get('api_hash') and config.get('phone'):
        print(f"\n{C.G}📁 Found saved credentials:{C.X}")
        print(f"   {C.W}API ID: {C.Y}{config['api_id']}{C.X}")
        print(f"   {C.W}Phone:  {C.Y}{config['phone']}{C.X}")
        
        use_saved = input(f"\n{C.C}Use saved credentials? (y/n): {C.X}").strip().lower()
        
        if use_saved == 'y':
            return config['api_id'], config['api_hash'], config['phone']
    
    # Ask for new credentials
    print(f"\n{C.Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.X}")
    print(f"{C.W}Get API credentials from: {C.C}https://my.telegram.org{C.X}")
    print(f"{C.Y}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.X}\n")
    
    # Get API ID (must be integer)
    while True:
        try:
            api_id = int(input(f"{C.C}Enter API ID: {C.X}").strip())
            break
        except ValueError:
            print(f"{C.R}❌ API ID must be a number!{C.X}")
    
    # Get API Hash (string)
    api_hash = input(f"{C.C}Enter API HASH: {C.X}").strip()
    
    # Get Phone (with country code)
    phone = input(f"{C.C}Enter Phone (with +country code): {C.X}").strip()
    
    # Add + if user forgot
    if not phone.startswith('+'):
        phone = '+' + phone
    
    # Ask if user wants to save
    save = input(f"\n{C.Y}Save credentials for next time? (y/n): {C.X}").strip().lower()
    if save == 'y':
        save_config(api_id, api_hash, phone)
        print(f"{C.G}✅ Saved to {CONFIG_FILE}{C.X}")
    
    return api_id, api_hash, phone


# ═══════════════════════════════════════════════════════════════
# RANGE PARSER - Handles all input formats
# ═══════════════════════════════════════════════════════════════
def parse_range(input_str, max_val):
    """
    Parse range input in multiple formats.
    
    Supported formats:
        - "1-40"        → Returns {1, 2, 3, ..., 40}
        - "1-40,50-60"  → Returns {1, 2, ..., 40, 50, 51, ..., 60}
        - "5,10,15"     → Returns {5, 10, 15}
        - "1-10,15,20"  → Returns {1, 2, ..., 10, 15, 20}
        - "all"         → Returns {1, 2, ..., max_val}
        - "none" or ""  → Returns empty set
    
    Args:
        input_str: User input string
        max_val: Maximum allowed value (total items count)
    
    Returns:
        set: Set of selected indices (1-based)
    """
    # Handle empty or none input
    if not input_str or input_str.lower() == 'none':
        return set()
    
    # Handle "all" - select everything
    if input_str.lower() == 'all':
        return set(range(1, max_val + 1))
    
    result = set()
    
    # Remove spaces and split by comma
    # Example: "1-40, 50-60" → ["1-40", "50-60"]
    parts = input_str.replace(' ', '').split(',')
    
    for part in parts:
        # Check if it's a range (contains -)
        if '-' in part:
            try:
                # Split by - and get start, end
                # Example: "1-40" → start=1, end=40
                start, end = map(int, part.split('-'))
                
                # Only add if start <= end (valid range)
                if start <= end:
                    # Add all numbers from start to min(end, max_val)
                    # min() ensures we don't exceed max_val
                    result.update(range(start, min(end, max_val) + 1))
            except:
                # Invalid format, skip this part
                pass
        else:
            # Single number
            try:
                num = int(part)
                # Only add if within valid range
                if 1 <= num <= max_val:
                    result.add(num)
            except:
                # Invalid number, skip
                pass
    
    return result


# ═══════════════════════════════════════════════════════════════
# UI FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def clear():
    """Clear terminal screen. Works on Windows (cls) and Unix (clear)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    """Display the main banner with ASCII art and watermark."""
    clear()
    print(f"""{C.C}
╔═══════════════════════════════════════════════════════════════╗
║  {C.Y}████████╗{C.G}███████╗{C.B}██╗     {C.M}███████╗{C.R} ██████╗ {C.C}██████╗ {C.W}█████╗ {C.Y}███╗   ███╗{C.C}  ║
║  {C.Y}╚══██╔══╝{C.G}██╔════╝{C.B}██║     {C.M}██╔════╝{C.R}██╔════╝ {C.C}██╔══██╗{C.W}██╔══██╗{C.Y}████╗ ████║{C.C}  ║
║  {C.Y}   ██║   {C.G}█████╗  {C.B}██║     {C.M}█████╗  {C.R}██║  ███╗{C.C}██████╔╝{C.W}███████║{C.Y}██╔████╔██║{C.C}  ║
║  {C.Y}   ██║   {C.G}██╔══╝  {C.B}██║     {C.M}██╔══╝  {C.R}██║   ██║{C.C}██╔══██╗{C.W}██╔══██║{C.Y}██║╚██╔╝██║{C.C}  ║
║  {C.Y}   ██║   {C.G}███████╗{C.B}███████╗{C.M}███████╗{C.R}╚██████╔╝{C.C}██║  ██║{C.W}██║  ██║{C.Y}██║ ╚═╝ ██║{C.C}  ║
║  {C.Y}   ╚═╝   {C.G}╚══════╝{C.B}╚══════╝{C.M}╚══════╝{C.R} ╚═════╝ {C.C}╚═╝  ╚═╝{C.W}╚═╝  ╚═╝{C.Y}╚═╝     ╚═╝{C.C}  ║
║                                                               ║
║              {C.W}🚀 AUTO LEAVE GROUPS & CHANNELS 🚀{C.C}               ║
╠═══════════════════════════════════════════════════════════════╣
║  {C.G}📱 Telegram: @MaiHuAryan{C.C}                                     ║
║  {C.B}💻 GitHub:   github.com/Aryan-cloud-arch/LEFT{C.C}                ║
╚═══════════════════════════════════════════════════════════════╝{C.X}
""")


def watermark():
    """Display small watermark footer."""
    print(f"{C.C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.X}")
    print(f"{C.Y}  📱 @MaiHuAryan  {C.W}│{C.B}  💻 github.com/Aryan-cloud-arch/LEFT{C.X}")
    print(f"{C.C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.X}\n")


def menu():
    """Display main menu options."""
    print(f"""
{C.C}╭──────────────────────────────────────────╮
│{C.Y}              📋 MAIN MENU                {C.C}│
├──────────────────────────────────────────┤
│  {C.G}[1]{C.W} 📋 View All Groups/Channels         {C.C}│
│  {C.G}[2]{C.W} 🚀 Leave by Range Selection         {C.C}│
│  {C.G}[3]{C.W} 🔍 Search & Leave by Name           {C.C}│
│  {C.G}[4]{C.W} ⚡ Leave ALL (Dangerous!)           {C.C}│
│  {C.G}[5]{C.W} ❌ Exit                             {C.C}│
╰──────────────────────────────────────────╯{C.X}
""")
    watermark()


# ═══════════════════════════════════════════════════════════════
# MAIN APP CLASS
# ═══════════════════════════════════════════════════════════════
class App:
    """
    Main application class that handles all operations.
    
    Attributes:
        client: TelegramClient instance for API calls
        dialogs: List of all fetched groups/channels
        stats: Dictionary tracking success/failed counts
    """
    
    def __init__(self, api_id, api_hash, phone):
        """
        Initialize app with Telegram credentials.
        
        Args:
            api_id: Telegram API ID from my.telegram.org
            api_hash: Telegram API Hash from my.telegram.org
            phone: Phone number with country code (+91...)
        """
        # Create Telegram client
        # 'session' = session file name (saves login for next time)
        self.client = TelegramClient('session', api_id, api_hash)
        
        # Store phone for login
        self.phone = phone
        
        # Will store all groups/channels after fetching
        self.dialogs = []
        
        # Statistics tracker
        self.stats = {
            'success': 0,   # Successfully left
            'failed': 0     # Failed to leave
        }
    
    
    async def connect(self):
        """
        Connect to Telegram and authenticate.
        
        First run: Will send OTP to your Telegram app
        Next runs: Uses saved session (no OTP needed)
        """
        print(f"{C.Y}⏳ Connecting to Telegram...{C.X}")
        
        # Start client with phone number
        # This handles OTP automatically
        await self.client.start(phone=self.phone)
        
        # Get logged in user info
        me = await self.client.get_me()
        
        # Show success message
        print(f"{C.G}✅ Logged in: {me.first_name} (@{me.username}){C.X}\n")
    
    
    async def fetch_dialogs(self):
        """
        Fetch all groups and channels from Telegram.
        
        This method:
        1. Iterates through all dialogs (chats)
        2. Filters only groups and channels (skips private chats)
        3. Stores them in self.dialogs with metadata
        
        Dialog structure:
        {
            'idx': 1,              # Display index (1-based)
            'id': 123456789,       # Telegram chat ID
            'title': "Group Name", # Group/channel name
            'type': 'group',       # 'group' or 'channel'
            'username': 'grp_uname', # @username if exists
            'entity': <object>     # Raw Telegram entity for API calls
        }
        """
        print(f"{C.Y}⏳ Fetching groups/channels...{C.X}")
        
        # Reset dialogs list
        self.dialogs = []
        idx = 0     # Counter for display index
        
        # Iterate through ALL dialogs
        async for dialog in self.client.iter_dialogs():
            entity = dialog.entity
            
            # Check if it's a Channel (supergroup or channel)
            if isinstance(entity, Channel):
                idx += 1
                
                # megagroup = True means it's a supergroup (group)
                # megagroup = False means it's a channel
                dtype = 'channel' if not entity.megagroup else 'group'
                
                self.dialogs.append({
                    'idx': idx,
                    'id': entity.id,
                    'title': dialog.title or "Unknown",
                    'type': dtype,
                    'username': getattr(entity, 'username', None),
                    'entity': entity
                })
            
            # Check if it's a basic Chat (old-style group)
            elif isinstance(entity, Chat):
                idx += 1
                
                self.dialogs.append({
                    'idx': idx,
                    'id': entity.id,
                    'title': dialog.title or "Unknown",
                    'type': 'group',
                    'username': None,   # Basic groups don't have usernames
                    'entity': entity
                })
        
        # Count groups and channels separately
        groups = sum(1 for d in self.dialogs if d['type'] == 'group')
        channels = len(self.dialogs) - groups
        
        # Show summary with colors (green for groups, blue for channels)
        print(f"{C.G}✅ Found: {C.Y}{len(self.dialogs)}{C.G} total "
              f"({C.G}{groups} groups{C.W}, {C.B}{channels} channels{C.G}){C.X}\n")
    
    
    async def leave(self, dialog):
        """
        Leave a single group or channel.
        
        Args:
            dialog: Dialog dict with 'entity' key
        
        Returns:
            bool: True if success, False if failed
        
        Uses different API calls for:
        - Channel/Supergroup: LeaveChannelRequest
        - Basic Group: DeleteChatUserRequest
        """
        try:
            entity = dialog['entity']
            
            if isinstance(entity, Channel):
                # For channels and supergroups
                await self.client(LeaveChannelRequest(entity))
            else:
                # For basic groups
                # 'me' = current user
                await self.client(DeleteChatUserRequest(entity.id, 'me'))
            
            return True
        
        except Exception as e:
            # Log error for debugging (optional)
            # print(f"Error: {e}")
            return False
    
    
    def show_dialogs(self, page=1, page_size=100):
        """
        Display dialogs with pagination (100 per page).
        
        Args:
            page: Current page number (1-based)
            page_size: Items per page (default 100)
        
        Returns:
            int: Total number of pages
        
        Colors:
        - Groups: Green 👥
        - Channels: Blue 📢
        """
        total = len(self.dialogs)
        
        # Calculate total pages (ceiling division)
        total_pages = (total + page_size - 1) // page_size
        
        # Calculate start/end indices for current page
        start = (page - 1) * page_size
        end = min(start + page_size, total)
        
        # Clear and show header
        clear()
        watermark()
        print(f"{C.C}╔═══ Page {page}/{total_pages} ═══ Showing [{start+1}-{end}] of {total} ═══╗{C.X}\n")
        
        # Display each dialog on current page
        for d in self.dialogs[start:end]:
            # Green for groups, Blue for channels
            color = C.G if d['type'] == 'group' else C.B
            icon = '👥' if d['type'] == 'group' else '📢'
            
            # Show username if exists
            username = f" (@{d['username']})" if d['username'] else ""
            
            # Format: [  1] 👥 Group Name (@username)
            # [:40] limits title to 40 chars to avoid overflow
            print(f"{C.W}[{d['idx']:3}] {color}{icon} {d['title'][:40]}{C.Y}{username}{C.X}")
        
        # Footer
        print(f"\n{C.C}╚═══════════════════════════════════════════════════════════╝{C.X}")
        print(f"{C.Y}[N]ext  [P]rev  [F]irst  [L]ast  [G]oto page  [Q]uit{C.X}")
        
        return total_pages
    
    
    async def view_all(self):
        """
        Interactive paginated view of all groups/channels.
        
        Navigation:
        - N: Next page
        - P: Previous page
        - F: First page
        - L: Last page
        - G: Go to specific page (g5 or g 5)
        - Q: Quit/back to menu
        """
        if not self.dialogs:
            print(f"{C.R}❌ No dialogs found! Fetch first.{C.X}")
            return
        
        page = 1    # Start at page 1
        
        while True:
            # Display current page and get total pages
            total_pages = self.show_dialogs(page)
            
            # Get navigation command
            cmd = input(f"\n{C.C}Enter command: {C.X}").lower().strip()
            
            if cmd == 'n' and page < total_pages:
                # Next page (if not last)
                page += 1
            
            elif cmd == 'p' and page > 1:
                # Previous page (if not first)
                page -= 1
            
            elif cmd == 'f':
                # First page
                page = 1
            
            elif cmd == 'l':
                # Last page
                page = total_pages
            
            elif cmd.startswith('g'):
                # Goto page: "g5" or "g 5"
                try:
                    p = int(cmd[1:].strip() or input(f"{C.Y}Page number: {C.X}"))
                    if 1 <= p <= total_pages:
                        page = p
                    else:
                        print(f"{C.R}Invalid page! (1-{total_pages}){C.X}")
                except:
                    print(f"{C.R}Invalid page number!{C.X}")
            
            elif cmd == 'q':
                # Quit pagination view
                break
    
    
    async def leave_by_range(self):
        """
        Main feature: Leave groups by range selection with exclusions.
        
        Flow:
        1. Optionally view list first
        2. Enter range to select (1-40, 1-40,50-60, 5,10,15, all)
        3. Enter exclusions (7-9, search, none)
        4. If search: search by name and select
        5. Show side-by-side preview
        6. Confirm
        7. Execute leaving
        8. Export log
        """
        if not self.dialogs:
            print(f"{C.R}❌ No dialogs found!{C.X}")
            return
        
        # ─────────────────────────────────────────────────
        # STEP 1: Offer to view list first
        # ─────────────────────────────────────────────────
        view = input(f"{C.Y}View list first? (y/n): {C.X}").lower().strip()
        if view == 'y':
            await self.view_all()
        
        clear()
        watermark()
        print(f"{C.G}Total: {len(self.dialogs)} groups/channels{C.X}\n")
        
        # ─────────────────────────────────────────────────
        # STEP 2: Show range format help
        # ─────────────────────────────────────────────────
        print(f"{C.C}┌─────────────────────────────────────────────┐")
        print(f"│  {C.Y}RANGE FORMATS:{C.C}                              │")
        print(f"│  {C.W}• 1-40         → Select 1 to 40{C.C}             │")
        print(f"│  {C.W}• 1-40,50-60   → Multiple ranges{C.C}            │")
        print(f"│  {C.W}• 5,10,15,20   → Specific numbers{C.C}           │")
        print(f"│  {C.W}• 1-50,55,60   → Range + numbers{C.C}            │")
        print(f"│  {C.W}• all          → Select all{C.C}                 │")
        print(f"└─────────────────────────────────────────────┘{C.X}\n")
        
        # ─────────────────────────────────────────────────
        # STEP 3: Get range selection
        # ─────────────────────────────────────────────────
        range_input = input(f"{C.C}Enter range [1-{len(self.dialogs)}]: {C.X}").strip()
        selected = parse_range(range_input, len(self.dialogs))
        
        if not selected:
            print(f"{C.R}❌ No valid selection!{C.X}")
            return
        
        print(f"{C.G}✅ Selected: {len(selected)} items{C.X}\n")
        
        # ─────────────────────────────────────────────────
        # STEP 4: Show exclusion format help
        # ─────────────────────────────────────────────────
        print(f"{C.C}┌─────────────────────────────────────────────┐")
        print(f"│  {C.Y}EXCLUSION FORMATS:{C.C}                          │")
        print(f"│  {C.W}• 7-9          → Exclude 7, 8, 9{C.C}            │")
        print(f"│  {C.W}• 7,8,9        → Exclude 7, 8, 9{C.C}            │")
        print(f"│  {C.W}• search       → Search by name{C.C}             │")
        print(f"│  {C.W}• none         → No exclusions{C.C}              │")
        print(f"└─────────────────────────────────────────────┘{C.X}\n")
        
        # ─────────────────────────────────────────────────
        # STEP 5: Get exclusions
        # ─────────────────────────────────────────────────
        exclude_input = input(f"{C.C}Exclude (or 'none'/'search'): {C.X}").strip().lower()
        excluded = set()
        
        if exclude_input == 'search':
            # ─────────────────────────────────────────────
            # SEARCH EXCLUSION MODE
            # ─────────────────────────────────────────────
            while True:
                term = input(f"\n{C.Y}Search term (or 'done'): {C.X}").strip()
                
                if term.lower() == 'done':
                    break
                
                if not term:
                    continue
                
                # Search in selected dialogs only
                matches = []
                for d in self.dialogs:
                    # Only search in selected items
                    if d['idx'] in selected:
                        # Case-insensitive search in title
                        if term.lower() in d['title'].lower():
                            matches.append(d)
                
                if matches:
                    print(f"\n{C.G}Found {len(matches)} matches:{C.X}")
                    for d in matches:
                        color = C.G if d['type'] == 'group' else C.B
                        print(f"  {C.W}[{d['idx']}] {color}{d['title']}{C.X}")
                    
                    exc = input(f"\n{C.Y}Exclude which? (indices or 'all' or 'none'): {C.X}").strip()
                    
                    if exc.lower() == 'all':
                        # Exclude all matches
                        for d in matches:
                            excluded.add(d['idx'])
                        print(f"{C.G}✅ Excluded {len(matches)} items{C.X}")
                    
                    elif exc.lower() != 'none':
                        # Parse and add to excluded
                        new_exc = parse_range(exc, len(self.dialogs))
                        # Only add if they're in matches
                        match_idx = {d['idx'] for d in matches}
                        valid = new_exc.intersection(match_idx)
                        excluded.update(valid)
                        print(f"{C.G}✅ Excluded {len(valid)} items{C.X}")
                else:
                    print(f"{C.R}No matches found for '{term}'{C.X}")
            
            print(f"\n{C.G}Total excluded: {len(excluded)}{C.X}")
        
        elif exclude_input != 'none' and exclude_input:
            # Parse exclusion range
            excluded = parse_range(exclude_input, len(self.dialogs))
        
        # Only keep exclusions that are in selected range
        excluded = excluded.intersection(selected)
        
        # ─────────────────────────────────────────────────
        # STEP 6: Calculate final list
        # ─────────────────────────────────────────────────
        final = selected - excluded
        
        if not final:
            print(f"{C.R}❌ Nothing to leave after exclusions!{C.X}")
            return
        
        # ─────────────────────────────────────────────────
        # STEP 7: Side-by-side preview
        # ─────────────────────────────────────────────────
        clear()
        watermark()
        
        # Get actual dialog objects
        to_leave = [d for d in self.dialogs if d['idx'] in final]
        to_keep = [d for d in self.dialogs if d['idx'] in excluded]
        
        # Header
        print(f"""
{C.R}╔═══════════════════════════════╗  {C.G}╔═══════════════════════════════╗
║   ❌ TO BE LEFT ({len(to_leave):3})          ║  ║   ✅ TO KEEP ({len(to_keep):3})             ║
╠═══════════════════════════════╣  ╠═══════════════════════════════╣{C.X}""")
        
        # Calculate max rows to show
        max_show = max(len(to_leave), len(to_keep))
        max_show = min(max_show, 15)    # Limit to 15 rows
        
        # Show items side by side
        for i in range(max_show):
            # Left side (to leave)
            if i < len(to_leave):
                left = f"{to_leave[i]['idx']}. {to_leave[i]['title'][:22]}"
            else:
                left = ""
            
            # Right side (to keep)
            if i < len(to_keep):
                right = f"{to_keep[i]['idx']}. {to_keep[i]['title'][:22]}"
            else:
                right = ""
            
            print(f"{C.R}║ {left:<29} ║  {C.G}║ {right:<29} ║{C.X}")
        
        # Show "and X more" if list is long
        if len(to_leave) > 15:
            print(f"{C.R}║  ... and {len(to_leave)-15} more{' '*14}║  {C.G}║{' '*31}║{C.X}")
        
        # Footer
        print(f"{C.R}╚═══════════════════════════════╝  {C.G}╚═══════════════════════════════╝{C.X}\n")
        
        # ─────────────────────────────────────────────────
        # STEP 8: Confirmation
        # ─────────────────────────────────────────────────
        print(f"{C.R}⚠️  WARNING: {len(to_leave)} groups/channels will be LEFT!{C.X}")
        print(f"{C.W}Type {C.Y}CONFIRM{C.W} to proceed or anything else to cancel.{C.X}\n")
        
        confirm = input(f"{C.C}➤ {C.X}").strip()
        
        if confirm != 'CONFIRM':
            print(f"{C.Y}Cancelled.{C.X}")
            return
        
        # ─────────────────────────────────────────────────
        # STEP 9: Execute leaving
        # ─────────────────────────────────────────────────
        await self._execute_leave(to_leave)
    
    
    async def leave_by_search(self):
        """
        Search for groups/channels by name and leave selected ones.
        
        Flow:
        1. Enter search term
        2. Show matches
        3. Select which to leave (range, all, cancel)
        4. Confirm
        5. Execute
        """
        # Get search term
        term = input(f"{C.Y}🔍 Search term: {C.X}").strip()
        
        if not term:
            print(f"{C.R}Search term cannot be empty!{C.X}")
            return
        
        # Search in all dialogs (case-insensitive)
        matches = []
        for d in self.dialogs:
            if term.lower() in d['title'].lower():
                matches.append(d)
            # Also search in username if exists
            elif d['username'] and term.lower() in d['username'].lower():
                matches.append(d)
        
        if not matches:
            print(f"{C.R}No matches found for '{term}'!{C.X}")
            return
        
        # Show matches
        print(f"\n{C.G}Found {len(matches)} matches:{C.X}\n")
        
        for d in matches:
            color = C.G if d['type'] == 'group' else C.B
            icon = '👥' if d['type'] == 'group' else '📢'
            username = f" (@{d['username']})" if d['username'] else ""
            print(f"  {C.W}[{d['idx']}] {color}{icon} {d['title']}{C.Y}{username}{C.X}")
        
        # Get selection
        print(f"\n{C.C}Enter indices to LEAVE:{C.X}")
        print(f"{C.W}  • Range/numbers (1-5, 2,4,6)")
        print(f"  • 'all' to leave all matches")
        print(f"  • 'cancel' to abort{C.X}\n")
        
        choice = input(f"{C.C}➤ {C.X}").strip()
        
        if choice.lower() == 'cancel':
            print(f"{C.Y}Cancelled.{C.X}")
            return
        
        # Determine which to leave
        to_leave = []
        
        if choice.lower() == 'all':
            to_leave = matches
        else:
            indices = parse_range(choice, len(self.dialogs))
            # Only include if in matches
            match_idx = {d['idx'] for d in matches}
            valid = indices.intersection(match_idx)
            to_leave = [d for d in matches if d['idx'] in valid]
        
        if not to_leave:
            print(f"{C.R}Nothing selected!{C.X}")
            return
        
        # Confirm
        print(f"\n{C.R}⚠️  Leave {len(to_leave)} items?{C.X}")
        confirm = input(f"{C.Y}Type CONFIRM: {C.X}").strip()
        
        if confirm == 'CONFIRM':
            await self._execute_leave(to_leave)
        else:
            print(f"{C.Y}Cancelled.{C.X}")
    
    
    async def leave_all(self):
        """
        Leave ALL groups and channels.
        
        This is dangerous! Requires double confirmation:
        1. Type "I UNDERSTAND"
        2. Type "LEAVE ALL"
        """
        # Show danger warning box
        print(f"""{C.R}
╔═══════════════════════════════════════════════════════════╗
║                   ⚠️  DANGER ZONE ⚠️                       ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║   This will leave {C.Y}ALL {len(self.dialogs)} groups/channels!{C.R}           ║
║                                                           ║
║   This action {C.W}CANNOT{C.R} be undone!                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{C.X}
""")
        
        # First confirmation
        c1 = input(f"{C.Y}Type 'I UNDERSTAND' to continue: {C.X}").strip()
        if c1 != 'I UNDERSTAND':
            print(f"{C.G}Phew! Cancelled.{C.X}")
            return
        
        # Second confirmation
        c2 = input(f"{C.R}Type 'LEAVE ALL' to confirm: {C.X}").strip()
        if c2 != 'LEAVE ALL':
            print(f"{C.G}Cancelled.{C.X}")
            return
        
        # Execute
        await self._execute_leave(self.dialogs)
    
    
    async def _execute_leave(self, dialogs):
        """
        Execute the leaving operation with progress tracking.
        
        Args:
            dialogs: List of dialog dicts to leave
        
        Features:
        - Progress bar
        - Success/failure tracking
        - Rate limiting (2s between each, 10s every 10)
        - Summary at end
        - Export to log file
        """
        total = len(dialogs)
        self.stats = {'success': 0, 'failed': 0}
        start_time = datetime.now()
        
        print(f"\n{C.Y}⏳ Leaving {total} groups/channels...{C.X}")
        print(f"{C.C}{'─' * 55}{C.X}\n")
        
        for i, d in enumerate(dialogs, 1):
            # Attempt to leave
            result = await self.leave(d)
            
            # Different colors for groups and channels
            type_color = C.G if d['type'] == 'group' else C.B
            
            if result:
                self.stats['success'] += 1
                print(f"{C.G}✅ [{i}/{total}] Left: {type_color}{d['title'][:40]}{C.X}")
            else:
                self.stats['failed'] += 1
                print(f"{C.R}❌ [{i}/{total}] Failed: {type_color}{d['title'][:40]}{C.X}")
            
            # Progress bar
            pct = int(i / total * 30)   # 30 chars wide
            bar = '█' * pct + '░' * (30 - pct)
            percent = int(i / total * 100)
            print(f"{C.C}  [{bar}] {percent}% ({i}/{total}){C.X}\n")
            
            # Rate limiting to avoid Telegram ban
            await asyncio.sleep(2)  # 2 seconds between each
            
            # Extra pause every 10 leaves
            if i % 10 == 0 and i < total:
                print(f"{C.Y}  ⏳ Pausing 10s to avoid rate limit...{C.X}\n")
                await asyncio.sleep(10)
        
        # Calculate duration
        duration = datetime.now() - start_time
        duration_str = str(duration).split('.')[0]  # Remove microseconds
        
        # Show summary
        print(f"""
{C.C}╔═══════════════════════════════════════════════════════════╗
║                      📊 SUMMARY                            ║
╠═══════════════════════════════════════════════════════════╣
║  {C.G}✅ Successfully Left: {self.stats['success']:<5}{C.C}                          ║
║  {C.R}❌ Failed:            {self.stats['failed']:<5}{C.C}                          ║
║  {C.Y}⏱️  Time Taken:        {duration_str:<15}{C.C}                ║
╚═══════════════════════════════════════════════════════════╝{C.X}
""")
        watermark()
        
        # Export to log file
        self._export_log(dialogs)
    
    
    def _export_log(self, dialogs):
        """
        Export list of processed groups to a log file.
        
        Creates logs/ folder if not exists.
        Filename: left_YYYYMMDD_HHMMSS.txt
        
        Log contains:
        - Timestamp
        - Statistics
        - List of all processed groups
        """
        # Create logs folder if not exists
        os.makedirs('logs', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"logs/left_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write("=" * 55 + "\n")
                f.write("TELEGRAM AUTO LEAVE - LOG FILE\n")
                f.write("=" * 55 + "\n")
                f.write(f"Telegram: @MaiHuAryan\n")
                f.write(f"GitHub:   github.com/Aryan-cloud-arch/LEFT\n")
                f.write("=" * 55 + "\n\n")
                
                # Stats
                f.write(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Processed: {len(dialogs)}\n")
                f.write(f"Success: {self.stats['success']}\n")
                f.write(f"Failed: {self.stats['failed']}\n\n")
                
                # List
                f.write("-" * 55 + "\n")
                f.write("GROUPS/CHANNELS:\n")
                f.write("-" * 55 + "\n")
                
                for d in dialogs:
                    type_icon = "[G]" if d['type'] == 'group' else "[C]"
                    username = f" @{d['username']}" if d['username'] else ""
                    f.write(f"{d['idx']:3}. {type_icon} {d['title']}{username}\n")
                
                f.write("\n" + "=" * 55 + "\n")
                f.write("END OF LOG\n")
                f.write("=" * 55 + "\n")
            
            print(f"{C.G}📄 Log saved: {filename}{C.X}\n")
        
        except Exception as e:
            print(f"{C.R}❌ Failed to save log: {e}{C.X}\n")
    
    
    async def run(self):
        """
        Main application loop.
        
        Flow:
        1. Show banner
        2. Connect to Telegram
        3. Fetch all groups/channels
        4. Show menu
        5. Handle user choice
        6. Loop until exit
        """
        try:
            # Show banner
            banner()
            
            # Connect to Telegram
            await self.connect()
            
            # Fetch all groups and channels
            await self.fetch_dialogs()
            
            # Main menu loop
            while True:
                menu()
                
                choice = input(f"{C.C}Enter choice [1-5]: {C.X}").strip()
                
                if choice == '1':
                    # View all with pagination
                    await self.view_all()
                
                elif choice == '2':
                    # Leave by range selection
                    await self.leave_by_range()
                
                elif choice == '3':
                    # Search and leave
                    await self.leave_by_search()
                
                elif choice == '4':
                    # Leave ALL (dangerous)
                    await self.leave_all()
                
                elif choice == '5':
                    # Exit
                    print(f"\n{C.G}👋 Goodbye! - @MaiHuAryan{C.X}\n")
                    break
                
                else:
                    print(f"{C.R}❌ Invalid choice! Enter 1-5{C.X}")
                
                # Pause before showing menu again
                input(f"\n{C.Y}Press Enter to continue...{C.X}")
        
        except KeyboardInterrupt:
            # Handle Ctrl+C
            print(f"\n\n{C.Y}⚠️  Cancelled by user (Ctrl+C){C.X}")
        
        except Exception as e:
            # Handle any unexpected error
            print(f"\n{C.R}❌ Error: {e}{C.X}")
        
        finally:
            # Always disconnect properly
            await self.client.disconnect()


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Show banner first
    banner()
    
    # Get credentials (from saved or ask user)
    api_id, api_hash, phone = get_credentials()
    
    # Create app instance
    app = App(api_id, api_hash, phone)
    
    # Run the app
    asyncio.run(app.run())
