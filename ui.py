#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#
#   ██╗   ██╗██╗    ██████╗ ██████╗ ███╗   ███╗██████╗  ██████╗ ███╗   ██╗███████╗███╗   ██╗████████╗███████╗
#   ██║   ██║██║   ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔═══██╗████╗  ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
#   ██║   ██║██║   ██║     ██║   ██║██╔████╔██║██████╔╝██║   ██║██╔██╗ ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
#   ██║   ██║██║   ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║   ██║██║╚██╗██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
#   ╚██████╔╝██║   ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ╚██████╔╝██║ ╚████║███████╗██║ ╚████║   ██║   ███████║
#    ╚═════╝ ╚═╝    ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
#
#   Beautiful UI Components for Telegram Auto Leave Tool
#
#   GitHub  : github.com/Aryan-cloud-arch/LEFT
#   Telegram: @MaiHuAryan
#
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import os                      # For terminal operations (clear screen, get size)
import sys                     # For system operations (stdout flush)
from colorama import Fore      # For colored text (RED, GREEN, etc.)
from colorama import Back      # For background colors
from colorama import Style     # For text styles (BRIGHT, DIM, RESET)
from colorama import init      # For initializing colorama

# ─────────────────────────────────────────────────────────────────────────────
# INITIALIZE COLORAMA
# ─────────────────────────────────────────────────────────────────────────────

# Initialize colorama for cross-platform color support
# autoreset=True means colors reset after each print statement
init(autoreset=True)


# ═══════════════════════════════════════════════════════════════════════════════
#                              COLOR SHORTCUTS
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    """
    Color shortcuts for easy access throughout the application.
    Using class instead of individual variables for better organization.
    """
    
    # ─────────────────────────────────────────────────────────────────────────
    # BASIC COLORS
    # ─────────────────────────────────────────────────────────────────────────
    
    RED = Fore.RED                    # For errors, warnings, items to be deleted
    GREEN = Fore.GREEN                # For success messages, items to keep
    YELLOW = Fore.YELLOW              # For warnings, highlights
    BLUE = Fore.BLUE                  # For information, general text
    MAGENTA = Fore.MAGENTA            # For special highlights
    CYAN = Fore.CYAN                  # For headers, important info
    WHITE = Fore.WHITE                # For normal text
    
    # ─────────────────────────────────────────────────────────────────────────
    # BRIGHT/BOLD COLORS (more visible)
    # ─────────────────────────────────────────────────────────────────────────
    
    BRIGHT_RED = Fore.RED + Style.BRIGHT
    BRIGHT_GREEN = Fore.GREEN + Style.BRIGHT
    BRIGHT_YELLOW = Fore.YELLOW + Style.BRIGHT
    BRIGHT_BLUE = Fore.BLUE + Style.BRIGHT
    BRIGHT_MAGENTA = Fore.MAGENTA + Style.BRIGHT
    BRIGHT_CYAN = Fore.CYAN + Style.BRIGHT
    BRIGHT_WHITE = Fore.WHITE + Style.BRIGHT
    
    # ─────────────────────────────────────────────────────────────────────────
    # SPECIAL PURPOSE COLORS
    # ─────────────────────────────────────────────────────────────────────────
    
    GROUP = Fore.YELLOW + Style.BRIGHT      # Color for groups
    CHANNEL = Fore.MAGENTA + Style.BRIGHT   # Color for channels
    SUCCESS = Fore.GREEN + Style.BRIGHT     # For success messages
    ERROR = Fore.RED + Style.BRIGHT         # For error messages
    WARNING = Fore.YELLOW + Style.BRIGHT    # For warning messages
    INFO = Fore.CYAN + Style.BRIGHT         # For info messages
    HEADER = Fore.CYAN + Style.BRIGHT       # For headers
    
    # ─────────────────────────────────────────────────────────────────────────
    # RESET
    # ─────────────────────────────────────────────────────────────────────────
    
    RESET = Style.RESET_ALL                 # Reset all formatting


# ═══════════════════════════════════════════════════════════════════════════════
#                                UI CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class UI:
    """
    Main UI class containing all display functions.
    Handles banners, menus, progress bars, and all visual elements.
    """
    
    # ─────────────────────────────────────────────────────────────────────────
    # CLASS VARIABLES
    # ─────────────────────────────────────────────────────────────────────────
    
    # Watermark information
    TELEGRAM_HANDLE = "@MaiHuAryan"
    GITHUB_REPO = "github.com/Aryan-cloud-arch/LEFT"
    
    # Box drawing characters for beautiful borders
    BOX_HORIZONTAL = "═"
    BOX_VERTICAL = "║"
    BOX_TOP_LEFT = "╔"
    BOX_TOP_RIGHT = "╗"
    BOX_BOTTOM_LEFT = "╚"
    BOX_BOTTOM_RIGHT = "╝"
    BOX_T_LEFT = "╠"
    BOX_T_RIGHT = "╣"
    
    # Rounded box characters
    ROUND_TOP_LEFT = "╭"
    ROUND_TOP_RIGHT = "╮"
    ROUND_BOTTOM_LEFT = "╰"
    ROUND_BOTTOM_RIGHT = "╯"
    ROUND_HORIZONTAL = "─"
    ROUND_VERTICAL = "│"
    
    # ─────────────────────────────────────────────────────────────────────────
    # UTILITY METHODS
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def clear_screen():
        """
        Clear the terminal screen.
        Works on both Windows (cls) and Unix/Linux/Mac (clear).
        """
        # os.name is 'nt' on Windows, 'posix' on Unix/Linux/Mac
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def get_terminal_width():
        """
        Get the current terminal width in characters.
        Returns default of 80 if unable to determine.
        """
        try:
            # os.get_terminal_size() returns (columns, rows)
            return os.get_terminal_size().columns
        except OSError:
            # If terminal size can't be determined, use default
            return 80
    
    @staticmethod
    def center_text(text, width=None):
        """
        Center a text string within the given width.
        
        Args:
            text: The text to center
            width: The total width (default: terminal width)
        
        Returns:
            Centered string with padding
        """
        # Use terminal width if not specified
        if width is None:
            width = UI.get_terminal_width()
        
        # Calculate padding and return centered text
        return text.center(width)
    
    # ─────────────────────────────────────────────────────────────────────────
    # MAIN BANNER
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_banner():
        """
        Display the main application banner with ASCII art.
        This is shown when the application starts.
        """
        
        # Clear screen first for clean display
        UI.clear_screen()
        
        # Get terminal width for proper centering
        width = UI.get_terminal_width()
        
        # Define the ASCII art banner
        # Using raw strings (r"") to avoid escape character issues
        banner = rf"""
{Colors.BRIGHT_CYAN}
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║  {Colors.BRIGHT_RED}████████╗{Colors.BRIGHT_WHITE}███████╗{Colors.BRIGHT_CYAN}██╗     {Colors.BRIGHT_GREEN}███████╗{Colors.BRIGHT_YELLOW} ██████╗ {Colors.BRIGHT_MAGENTA}██████╗  {Colors.BRIGHT_BLUE} █████╗ {Colors.BRIGHT_RED}███╗   ███╗{Colors.BRIGHT_CYAN}  ║
║  {Colors.BRIGHT_RED}╚══██╔══╝{Colors.BRIGHT_WHITE}██╔════╝{Colors.BRIGHT_CYAN}██║     {Colors.BRIGHT_GREEN}██╔════╝{Colors.BRIGHT_YELLOW}██╔════╝ {Colors.BRIGHT_MAGENTA}██╔══██╗ {Colors.BRIGHT_BLUE}██╔══██╗{Colors.BRIGHT_RED}████╗ ████║{Colors.BRIGHT_CYAN}  ║
║  {Colors.BRIGHT_RED}   ██║   {Colors.BRIGHT_WHITE}█████╗  {Colors.BRIGHT_CYAN}██║     {Colors.BRIGHT_GREEN}█████╗  {Colors.BRIGHT_YELLOW}██║  ███╗{Colors.BRIGHT_MAGENTA}██████╔╝ {Colors.BRIGHT_BLUE}███████║{Colors.BRIGHT_RED}██╔████╔██║{Colors.BRIGHT_CYAN}  ║
║  {Colors.BRIGHT_RED}   ██║   {Colors.BRIGHT_WHITE}██╔══╝  {Colors.BRIGHT_CYAN}██║     {Colors.BRIGHT_GREEN}██╔══╝  {Colors.BRIGHT_YELLOW}██║   ██║{Colors.BRIGHT_MAGENTA}██╔══██╗ {Colors.BRIGHT_BLUE}██╔══██║{Colors.BRIGHT_RED}██║╚██╔╝██║{Colors.BRIGHT_CYAN}  ║
║  {Colors.BRIGHT_RED}   ██║   {Colors.BRIGHT_WHITE}███████╗{Colors.BRIGHT_CYAN}███████╗{Colors.BRIGHT_GREEN}███████╗{Colors.BRIGHT_YELLOW}╚██████╔╝{Colors.BRIGHT_MAGENTA}██║  ██║ {Colors.BRIGHT_BLUE}██║  ██║{Colors.BRIGHT_RED}██║ ╚═╝ ██║{Colors.BRIGHT_CYAN}  ║
║  {Colors.BRIGHT_RED}   ╚═╝   {Colors.BRIGHT_WHITE}╚══════╝{Colors.BRIGHT_CYAN}╚══════╝{Colors.BRIGHT_GREEN}╚══════╝{Colors.BRIGHT_YELLOW} ╚═════╝ {Colors.BRIGHT_MAGENTA}╚═╝  ╚═╝ {Colors.BRIGHT_BLUE}╚═╝  ╚═╝{Colors.BRIGHT_RED}╚═╝     ╚═╝{Colors.BRIGHT_CYAN}  ║
║                                                                                   ║
║             {Colors.BRIGHT_YELLOW}🚀 AUTO LEAVE GROUPS & CHANNELS TOOL 🚀{Colors.BRIGHT_CYAN}                          ║
║                                                                                   ║
║  {Colors.ROUND_TOP_LEFT}{Colors.ROUND_HORIZONTAL * 75}{Colors.ROUND_TOP_RIGHT}  ║
║  {Colors.ROUND_VERTICAL}  {Colors.BRIGHT_WHITE}Developed by : {Colors.BRIGHT_GREEN}{UI.TELEGRAM_HANDLE:<20}{Colors.BRIGHT_WHITE}                                       {Colors.BRIGHT_CYAN}{Colors.ROUND_VERTICAL}  ║
║  {Colors.ROUND_VERTICAL}  {Colors.BRIGHT_WHITE}GitHub       : {Colors.BRIGHT_BLUE}{UI.GITHUB_REPO:<40}{Colors.BRIGHT_WHITE}              {Colors.BRIGHT_CYAN}{Colors.ROUND_VERTICAL}  ║
║  {Colors.ROUND_BOTTOM_LEFT}{Colors.ROUND_HORIZONTAL * 75}{Colors.ROUND_BOTTOM_RIGHT}  ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
        
        # Print the banner
        print(banner)
    
    # ─────────────────────────────────────────────────────────────────────────
    # MAIN MENU
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_main_menu():
        """
        Display the main menu with all options.
        Returns the user's choice as a string.
        """
        
        menu = f"""
{Colors.BRIGHT_CYAN}╭──────────────────────────────────────────────────────────────╮
│                     {Colors.BRIGHT_YELLOW}🏠 MAIN MENU{Colors.BRIGHT_CYAN}                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   {Colors.BRIGHT_WHITE}[1] {Colors.BRIGHT_GREEN}📋 View All Groups & Channels{Colors.BRIGHT_CYAN}                       │
│   {Colors.BRIGHT_WHITE}[2] {Colors.BRIGHT_YELLOW}🚀 Leave by Range Selection{Colors.BRIGHT_CYAN}                         │
│   {Colors.BRIGHT_WHITE}[3] {Colors.BRIGHT_MAGENTA}🔍 Search & Leave by Name{Colors.BRIGHT_CYAN}                           │
│   {Colors.BRIGHT_WHITE}[4] {Colors.BRIGHT_RED}⚡ Leave ALL (Dangerous!){Colors.BRIGHT_CYAN}                           │
│   {Colors.BRIGHT_WHITE}[5] {Colors.BRIGHT_BLUE}📊 View Statistics{Colors.BRIGHT_CYAN}                                  │
│   {Colors.BRIGHT_WHITE}[6] {Colors.WHITE}⚙️  Settings{Colors.BRIGHT_CYAN}                                         │
│   {Colors.BRIGHT_WHITE}[7] {Colors.RED}❌ Exit{Colors.BRIGHT_CYAN}                                              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  {Colors.BRIGHT_WHITE}Telegram: {Colors.BRIGHT_GREEN}{UI.TELEGRAM_HANDLE:<15} {Colors.BRIGHT_WHITE}│ GitHub: {Colors.BRIGHT_BLUE}Aryan-cloud-arch{Colors.BRIGHT_CYAN}  │
╰──────────────────────────────────────────────────────────────╯
{Colors.RESET}"""
        
        print(menu)
        
        # Get user input with styled prompt
        choice = input(f"{Colors.BRIGHT_YELLOW}  ➤ Enter your choice [1-7]: {Colors.BRIGHT_WHITE}")
        
        return choice
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY GROUP LIST
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_group_list(dialogs, page=1, per_page=100):
        """
        Display a paginated list of groups and channels.
        
        Args:
            dialogs: List of dialog objects (groups/channels)
            page: Current page number (1-indexed)
            per_page: Number of items per page
        
        Returns:
            None (just displays)
        """
        
        # Calculate pagination
        total_items = len(dialogs)                           # Total number of items
        total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
        start_idx = (page - 1) * per_page                    # Starting index for current page
        end_idx = min(start_idx + per_page, total_items)     # Ending index for current page
        
        # Header
        print(f"""
{Colors.BRIGHT_CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗
║              {Colors.BRIGHT_YELLOW}📋 ALL GROUPS & CHANNELS (Page {page}/{total_pages}){Colors.BRIGHT_CYAN}                          ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  {Colors.BRIGHT_WHITE}Total: {Colors.BRIGHT_GREEN}{total_items} items{Colors.BRIGHT_WHITE}  │  {Colors.GROUP}🔶 Group{Colors.BRIGHT_WHITE}  │  {Colors.CHANNEL}🔷 Channel{Colors.BRIGHT_CYAN}                            ║
╠═══════════════════════════════════════════════════════════════════════════════╣""")
        
        # Display each item
        for i in range(start_idx, end_idx):
            dialog = dialogs[i]
            
            # Get dialog info
            idx = i + 1                                      # 1-indexed number
            title = dialog['title'][:45]                     # Truncate long names
            dialog_type = dialog['type']                     # 'group' or 'channel'
            members = dialog.get('members', 'N/A')           # Member count if available
            
            # Choose color based on type
            if dialog_type == 'group':
                type_icon = "🔶"
                type_color = Colors.GROUP
            else:
                type_icon = "🔷"
                type_color = Colors.CHANNEL
            
            # Format and print the row
            print(f"║  {Colors.BRIGHT_WHITE}{idx:>4}. {type_color}{type_icon} {title:<45}{Colors.BRIGHT_CYAN} │ {Colors.WHITE}Members: {members:<8}{Colors.BRIGHT_CYAN}║")
        
        # Footer
        print(f"""╠═══════════════════════════════════════════════════════════════════════════════╣
║  {Colors.BRIGHT_WHITE}[N] Next Page  [P] Previous Page  [Q] Back to Menu  [S] Select Range{Colors.BRIGHT_CYAN}        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  {Colors.BRIGHT_WHITE}Telegram: {Colors.BRIGHT_GREEN}{UI.TELEGRAM_HANDLE}{Colors.BRIGHT_WHITE}        │        GitHub: {Colors.BRIGHT_BLUE}{UI.GITHUB_REPO}{Colors.BRIGHT_CYAN}  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}""")
        
        return total_pages
    
    # ─────────────────────────────────────────────────────────────────────────
    # RANGE INPUT PROMPT
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_range_input_help():
        """
        Display help text for range input format.
        Shows all supported formats with examples.
        """
        
        help_text = f"""
{Colors.BRIGHT_CYAN}╭──────────────────────────────────────────────────────────────────────────────╮
│                        {Colors.BRIGHT_YELLOW}📝 RANGE INPUT FORMATS{Colors.BRIGHT_CYAN}                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   {Colors.BRIGHT_WHITE}Format          │  Example        │  Selects{Colors.BRIGHT_CYAN}                           │
│   {Colors.BRIGHT_GREEN}────────────────│─────────────────│──────────────────────────────{Colors.BRIGHT_CYAN}     │
│   {Colors.BRIGHT_WHITE}Single Range    │  {Colors.BRIGHT_YELLOW}1-40{Colors.BRIGHT_WHITE}            │  Groups 1 to 40{Colors.BRIGHT_CYAN}                    │
│   {Colors.BRIGHT_WHITE}Multiple Ranges │  {Colors.BRIGHT_YELLOW}1-40,50-60{Colors.BRIGHT_WHITE}      │  Groups 1-40 AND 50-60{Colors.BRIGHT_CYAN}             │
│   {Colors.BRIGHT_WHITE}Individual      │  {Colors.BRIGHT_YELLOW}5,10,15,20{Colors.BRIGHT_WHITE}      │  Only groups 5, 10, 15, 20{Colors.BRIGHT_CYAN}         │
│   {Colors.BRIGHT_WHITE}Mixed           │  {Colors.BRIGHT_YELLOW}1-40,55,60-70{Colors.BRIGHT_WHITE}   │  Groups 1-40, 55, and 60-70{Colors.BRIGHT_CYAN}        │
│   {Colors.BRIGHT_WHITE}All             │  {Colors.BRIGHT_YELLOW}all{Colors.BRIGHT_WHITE}             │  All groups{Colors.BRIGHT_CYAN}                        │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
{Colors.RESET}"""
        
        print(help_text)
    
    @staticmethod
    def show_exclude_input_help():
        """
        Display help text for exclude input format.
        """
        
        help_text = f"""
{Colors.BRIGHT_CYAN}╭──────────────────────────────────────────────────────────────────────────────╮
│                      {Colors.BRIGHT_YELLOW}🛡️ EXCLUDE INPUT FORMATS{Colors.BRIGHT_CYAN}                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   {Colors.BRIGHT_WHITE}Format          │  Example        │  Keeps (Won't Leave){Colors.BRIGHT_CYAN}               │
│   {Colors.BRIGHT_GREEN}────────────────│─────────────────│──────────────────────────────{Colors.BRIGHT_CYAN}     │
│   {Colors.BRIGHT_WHITE}Range           │  {Colors.BRIGHT_GREEN}7-9{Colors.BRIGHT_WHITE}             │  Groups 7, 8, 9{Colors.BRIGHT_CYAN}                    │
│   {Colors.BRIGHT_WHITE}Individual      │  {Colors.BRIGHT_GREEN}7,8,9{Colors.BRIGHT_WHITE}           │  Groups 7, 8, 9{Colors.BRIGHT_CYAN}                    │
│   {Colors.BRIGHT_WHITE}Mixed           │  {Colors.BRIGHT_GREEN}5-10,15,20{Colors.BRIGHT_WHITE}      │  Groups 5-10, 15, and 20{Colors.BRIGHT_CYAN}           │
│   {Colors.BRIGHT_WHITE}By Name         │  {Colors.BRIGHT_GREEN}name:family{Colors.BRIGHT_WHITE}     │  Groups with "family" in name{Colors.BRIGHT_CYAN}      │
│   {Colors.BRIGHT_WHITE}None            │  {Colors.BRIGHT_GREEN}none{Colors.BRIGHT_WHITE}            │  Don't exclude any{Colors.BRIGHT_CYAN}                 │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
{Colors.RESET}"""
        
        print(help_text)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SIDE BY SIDE PREVIEW
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_side_by_side_preview(to_leave, to_keep, page=1, per_page=20):
        """
        Display side-by-side preview of groups to leave vs keep.
        
        Args:
            to_leave: List of dialogs that will be left
            to_keep: List of dialogs that will be kept
            page: Current page number
            per_page: Items per page (per column)
        """
        
        # Calculate totals
        total_leave = len(to_leave)
        total_keep = len(to_keep)
        
        # Calculate pagination
        total_pages = max(
            (total_leave + per_page - 1) // per_page,
            (total_keep + per_page - 1) // per_page
        )
        if total_pages == 0:
            total_pages = 1
        
        start_idx = (page - 1) * per_page
        
        # Header
        print(f"""
{Colors.BRIGHT_CYAN}╔════════════════════════════════════════════════════════════════════════════════════════╗
║                              {Colors.BRIGHT_YELLOW}📋 FINAL PREVIEW (Page {page}/{total_pages}){Colors.BRIGHT_CYAN}                                  ║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                        ║
║   {Colors.BRIGHT_RED}┌────────────────────────────────────────┐{Colors.BRIGHT_CYAN}   {Colors.BRIGHT_GREEN}┌────────────────────────────────────────┐{Colors.BRIGHT_CYAN}   ║
║   {Colors.BRIGHT_RED}│   ❌ TO BE LEFT ({total_leave:>4} groups){" " * (18 - len(str(total_leave)))}│{Colors.BRIGHT_CYAN}   {Colors.BRIGHT_GREEN}│   ✅ TO KEEP ({total_keep:>4} groups){" " * (20 - len(str(total_keep)))}│{Colors.BRIGHT_CYAN}   ║
║   {Colors.BRIGHT_RED}├────────────────────────────────────────┤{Colors.BRIGHT_CYAN}   {Colors.BRIGHT_GREEN}├────────────────────────────────────────┤{Colors.BRIGHT_CYAN}   ║""")
        
        # Display items side by side
        for i in range(per_page):
            left_idx = start_idx + i
            right_idx = start_idx + i
            
            # Left column (to leave)
            if left_idx < total_leave:
                left_item = to_leave[left_idx]
                left_num = left_item['original_index']
                left_title = left_item['title'][:30]
                left_type = "🔶" if left_item['type'] == 'group' else "🔷"
                left_text = f"{left_num:>4}. {left_type} {left_title:<30}"
            else:
                left_text = " " * 38
            
            # Right column (to keep)
            if right_idx < total_keep:
                right_item = to_keep[right_idx]
                right_num = right_item['original_index']
                right_title = right_item['title'][:30]
                right_type = "🔶" if right_item['type'] == 'group' else "🔷"
                right_text = f"{right_num:>4}. {right_type} {right_title:<30}"
            else:
                right_text = " " * 38
            
            # Print row
            print(f"║   {Colors.BRIGHT_RED}│ {Colors.WHITE}{left_text}{Colors.BRIGHT_RED}│{Colors.BRIGHT_CYAN}   {Colors.BRIGHT_GREEN}│ {Colors.WHITE}{right_text}{Colors.BRIGHT_GREEN}│{Colors.BRIGHT_CYAN}   ║")
        
        # Footer
        print(f"""║   {Colors.BRIGHT_RED}└────────────────────────────────────────┘{Colors.BRIGHT_CYAN}   {Colors.BRIGHT_GREEN}└────────────────────────────────────────┘{Colors.BRIGHT_CYAN}   ║
║                                                                                        ║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║   {Colors.BRIGHT_YELLOW}⚠️  Summary: {Colors.BRIGHT_RED}{total_leave} groups will be LEFT{Colors.BRIGHT_WHITE} │ {Colors.BRIGHT_GREEN}{total_keep} groups will be KEPT{Colors.BRIGHT_CYAN}                         ║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║   {Colors.BRIGHT_WHITE}[N] Next Page   [P] Previous Page   [C] CONFIRM   [X] Cancel{Colors.BRIGHT_CYAN}                       ║
╠════════════════════════════════════════════════════════════════════════════════════════╣
║   {Colors.BRIGHT_WHITE}Telegram: {Colors.BRIGHT_GREEN}{UI.TELEGRAM_HANDLE}{Colors.BRIGHT_WHITE}              │              GitHub: {Colors.BRIGHT_BLUE}{UI.GITHUB_REPO}{Colors.BRIGHT_CYAN}     ║
╚════════════════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}""")
        
        return total_pages
    
    # ─────────────────────────────────────────────────────────────────────────
    # PROGRESS BAR
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_progress(current, total, title="", status=""):
        """
        Display a progress bar with percentage.
        
        Args:
            current: Current progress value
            total: Total value
            title: Title of current item being processed
            status: Status icon (✅ or ❌)
        """
        
        # Calculate percentage
        if total > 0:
            percentage = (current / total) * 100
        else:
            percentage = 0
        
        # Create progress bar (40 characters wide)
        bar_width = 40
        filled = int(bar_width * current / total) if total > 0 else 0
        empty = bar_width - filled
        
        # Progress bar characters
        bar = f"{Colors.BRIGHT_GREEN}{'█' * filled}{Colors.WHITE}{'░' * empty}"
        
        # Truncate title if too long
        title_display = title[:35] + "..." if len(title) > 35 else title
        
        # Print progress (use \r to overwrite line)
        print(f"\r{Colors.BRIGHT_CYAN}║ {status} {Colors.WHITE}[{bar}{Colors.WHITE}] {Colors.BRIGHT_YELLOW}{percentage:>5.1f}%{Colors.WHITE} ({current}/{total}) {Colors.BRIGHT_WHITE}{title_display:<40}{Colors.RESET}", end="", flush=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUMMARY DISPLAY
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_summary(left_count, failed_count, skipped_count, time_taken):
        """
        Display final summary after operation completes.
        
        Args:
            left_count: Number of groups successfully left
            failed_count: Number of failed attempts
            skipped_count: Number of skipped groups
            time_taken: Time taken in seconds
        """
        
        # Format time
        minutes = int(time_taken // 60)
        seconds = int(time_taken % 60)
        time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
        
        summary = f"""

{Colors.BRIGHT_CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗
║                           {Colors.BRIGHT_YELLOW}📊 OPERATION SUMMARY{Colors.BRIGHT_CYAN}                              ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   {Colors.BRIGHT_GREEN}✅ Successfully Left  : {left_count:>6} groups{Colors.BRIGHT_CYAN}                                     ║
║   {Colors.BRIGHT_YELLOW}⏭️  Skipped (Excluded) : {skipped_count:>6} groups{Colors.BRIGHT_CYAN}                                     ║
║   {Colors.BRIGHT_RED}❌ Failed             : {failed_count:>6} groups{Colors.BRIGHT_CYAN}                                     ║
║   {Colors.BRIGHT_WHITE}⏱️  Time Taken         : {time_str:>10}{Colors.BRIGHT_CYAN}                                     ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║   {Colors.BRIGHT_WHITE}📄 Log saved to: logs/left_groups.txt{Colors.BRIGHT_CYAN}                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║   {Colors.BRIGHT_WHITE}Telegram: {Colors.BRIGHT_GREEN}{UI.TELEGRAM_HANDLE}{Colors.BRIGHT_WHITE}              │              GitHub: {Colors.BRIGHT_BLUE}{UI.GITHUB_REPO}{Colors.BRIGHT_CYAN}     ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
        
        print(summary)
    
    # ─────────────────────────────────────────────────────────────────────────
    # MESSAGE DISPLAYS
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_success(message):
        """Display a success message."""
        print(f"\n{Colors.BRIGHT_GREEN}  ✅ {message}{Colors.RESET}")
    
    @staticmethod
    def show_error(message):
        """Display an error message."""
        print(f"\n{Colors.BRIGHT_RED}  ❌ {message}{Colors.RESET}")
    
    @staticmethod
    def show_warning(message):
        """Display a warning message."""
        print(f"\n{Colors.BRIGHT_YELLOW}  ⚠️  {message}{Colors.RESET}")
    
    @staticmethod
    def show_info(message):
        """Display an info message."""
        print(f"\n{Colors.BRIGHT_CYAN}  ℹ️  {message}{Colors.RESET}")
    
    @staticmethod
    def get_input(prompt):
        """Get user input with styled prompt."""
        return input(f"\n{Colors.BRIGHT_YELLOW}  ➤ {prompt}: {Colors.BRIGHT_WHITE}")
    
    @staticmethod
    def confirm(message):
        """
        Ask for confirmation.
        Returns True if user confirms, False otherwise.
        """
        response = input(f"\n{Colors.BRIGHT_YELLOW}  ➤ {message} (yes/no): {Colors.BRIGHT_WHITE}")
        return response.lower() in ['yes', 'y']
    
    # ─────────────────────────────────────────────────────────────────────────
    # LOADING ANIMATION
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_loading(message):
        """Display a loading message."""
        print(f"\n{Colors.BRIGHT_CYAN}  ⏳ {message}...{Colors.RESET}")
    
    # ─────────────────────────────────────────────────────────────────────────
    # FOOTER/WATERMARK
    # ─────────────────────────────────────────────────────────────────────────
    
    @staticmethod
    def show_footer():
        """Display footer with watermark."""
        footer = f"""
{Colors.BRIGHT_CYAN}────────────────────────────────────────────────────────────────────────────────
  {Colors.BRIGHT_WHITE}Developed by: {Colors.BRIGHT_GREEN}{UI.TELEGRAM_HANDLE}{Colors.BRIGHT_WHITE}  │  GitHub: {Colors.BRIGHT_BLUE}{UI.GITHUB_REPO}
{Colors.BRIGHT_CYAN}────────────────────────────────────────────────────────────────────────────────
{Colors.RESET}"""
        print(footer)


# ═══════════════════════════════════════════════════════════════════════════════
#                              TEST UI (if run directly)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Test the UI components
    UI.show_banner()
    UI.show_main_menu()
