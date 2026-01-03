#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#
#   ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗
#   ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
#      ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║
#      ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
#      ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
#      ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
#
#                    ██████╗██╗     ██╗███████╗███╗   ██╗████████╗
#                   ██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝
#                   ██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║   
#                   ██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║   
#                   ╚██████╗███████╗██║███████╗██║ ╚████║   ██║   
#                    ╚═════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   
#
#   Telegram Client Module - Handles all Telegram API operations
#
#   GitHub  : github.com/Aryan-cloud-arch/LEFT
#   Telegram: @MaiHuAryan
#
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import asyncio                                          # For async operations
import time                                              # For delays and timing
from telethon import TelegramClient                     # Main Telegram client
from telethon.tl.functions.channels import LeaveChannelRequest  # Leave supergroups/channels
from telethon.tl.functions.messages import DeleteChatUserRequest  # Leave basic groups
from telethon.tl.types import Channel, Chat, User        # Entity types
from telethon.errors import FloodWaitError, RPCError    # Error handling

# Import config
from config import (
    API_ID, 
    API_HASH, 
    PHONE_NUMBER, 
    SESSION_NAME,
    LEAVE_DELAY,
    BATCH_SIZE,
    BATCH_DELAY,
    LOG_FILE
)

# Import UI for messages
from ui import UI, Colors

# Import utils
from utils import append_to_log


# ═══════════════════════════════════════════════════════════════════════════════
#                           TELEGRAM CLIENT CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class TelegramLeaver:
    """
    Main class for handling Telegram operations.
    Manages connection, fetching dialogs, and leaving groups/channels.
    """
    
    def __init__(self):
        """
        Initialize the TelegramLeaver instance.
        Sets up the client and initializes counters.
        """
        
        # ─────────────────────────────────────────────────────────────────────
        # Create Telegram client instance
        # ─────────────────────────────────────────────────────────────────────
        
        # TelegramClient parameters:
        # - session: Name of the session file (stores login info)
        # - api_id: Your API ID from my.telegram.org
        # - api_hash: Your API hash from my.telegram.org
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        
        # ─────────────────────────────────────────────────────────────────────
        # Initialize counters for statistics
        # ─────────────────────────────────────────────────────────────────────
        
        self.left_count = 0      # Successfully left groups
        self.failed_count = 0    # Failed to leave
        self.skipped_count = 0   # Skipped (excluded)
        
        # ─────────────────────────────────────────────────────────────────────
        # Store dialogs
        # ─────────────────────────────────────────────────────────────────────
        
        self.all_dialogs = []    # List of all groups/channels
        
        # ─────────────────────────────────────────────────────────────────────
        # User info
        # ─────────────────────────────────────────────────────────────────────
        
        self.me = None           # Current user info
    
    # ═══════════════════════════════════════════════════════════════════════════
    #                           CONNECTION METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def connect(self):
        """
        Connect to Telegram and authenticate.
        Handles OTP verification if needed.
        
        Returns:
            bool: True if connected successfully, False otherwise
        """
        
        try:
            UI.show_loading("Connecting to Telegram")
            
            # ─────────────────────────────────────────────────────────────────
            # Start the client
            # ─────────────────────────────────────────────────────────────────
            
            # start() handles:
            # - Connecting to Telegram servers
            # - Authenticating with saved session or OTP
            # - phone parameter: Your phone number for login
            await self.client.start(phone=PHONE_NUMBER)
            
            # ─────────────────────────────────────────────────────────────────
            # Get current user info
            # ─────────────────────────────────────────────────────────────────
            
            self.me = await self.client.get_me()
            
            # ─────────────────────────────────────────────────────────────────
            # Display success message
            # ─────────────────────────────────────────────────────────────────
            
            # Build display name
            name = self.me.first_name or ""
            if self.me.last_name:
                name += f" {self.me.last_name}"
            
            username = f"@{self.me.username}" if self.me.username else "No username"
            
            print(f"""
{Colors.BRIGHT_CYAN}╭──────────────────────────────────────────────────────────────╮
│                    {Colors.BRIGHT_GREEN}✅ LOGIN SUCCESSFUL{Colors.BRIGHT_CYAN}                        │
├──────────────────────────────────────────────────────────────┤
│  {Colors.BRIGHT_WHITE}Name     : {Colors.BRIGHT_GREEN}{name:<47}{Colors.BRIGHT_CYAN}│
│  {Colors.BRIGHT_WHITE}Username : {Colors.BRIGHT_YELLOW}{username:<47}{Colors.BRIGHT_CYAN}│
│  {Colors.BRIGHT_WHITE}ID       : {Colors.WHITE}{self.me.id:<47}{Colors.BRIGHT_CYAN}│
╰──────────────────────────────────────────────────────────────╯
{Colors.RESET}""")
            
            return True
            
        except Exception as e:
            UI.show_error(f"Failed to connect: {str(e)}")
            return False
    
    async def disconnect(self):
        """
        Disconnect from Telegram.
        Should be called when done to clean up resources.
        """
        
        try:
            await self.client.disconnect()
            UI.show_info("Disconnected from Telegram")
        except Exception as e:
            UI.show_error(f"Error disconnecting: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    #                           FETCH DIALOGS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def fetch_all_dialogs(self):
        """
        Fetch all groups and channels the user is a member of.
        
        Returns:
            list: List of dialog dictionaries with info about each group/channel
        """
        
        UI.show_loading("Fetching all groups and channels")
        
        self.all_dialogs = []  # Reset the list
        count = 0
        
        try:
            # ─────────────────────────────────────────────────────────────────
            # Iterate through all dialogs
            # ─────────────────────────────────────────────────────────────────
            
            # iter_dialogs() yields all conversations:
            # - Private chats (we skip these)
            # - Groups (Chat objects)
            # - Supergroups (Channel with megagroup=True)
            # - Channels (Channel with megagroup=False)
            
            async for dialog in self.client.iter_dialogs():
                entity = dialog.entity
                
                # Skip private chats with users
                if isinstance(entity, User):
                    continue
                
                # ─────────────────────────────────────────────────────────────
                # Process Channel (supergroup or channel)
                # ─────────────────────────────────────────────────────────────
                
                if isinstance(entity, Channel):
                    count += 1
                    
                    # Determine if it's a group or channel
                    # megagroup = True means it's a supergroup
                    dialog_type = "group" if entity.megagroup else "channel"
                    
                    # Get member count (participants_count may not always be available)
                    members = entity.participants_count if hasattr(entity, 'participants_count') and entity.participants_count else "N/A"
                    
                    # Create dialog info dictionary
                    dialog_info = {
                        'id': entity.id,                         # Unique ID
                        'title': entity.title or "Unknown",      # Group/channel name
                        'type': dialog_type,                     # 'group' or 'channel'
                        'username': entity.username,             # @username if exists
                        'members': members,                      # Member count
                        'entity': entity,                        # Original entity object
                        'dialog': dialog                         # Original dialog object
                    }
                    
                    self.all_dialogs.append(dialog_info)
                
                # ─────────────────────────────────────────────────────────────
                # Process Chat (basic group)
                # ─────────────────────────────────────────────────────────────
                
                elif isinstance(entity, Chat):
                    count += 1
                    
                    dialog_info = {
                        'id': entity.id,
                        'title': entity.title or "Unknown",
                        'type': 'group',                         # Basic groups are always groups
                        'username': None,                        # Basic groups don't have usernames
                        'members': entity.participants_count if hasattr(entity, 'participants_count') else "N/A",
                        'entity': entity,
                        'dialog': dialog
                    }
                    
                    self.all_dialogs.append(dialog_info)
                
                # Print progress every 50 items
                if count % 50 == 0:
                    print(f"  {Colors.BRIGHT_WHITE}Found {count} groups/channels so far...{Colors.RESET}")
            
            # ─────────────────────────────────────────────────────────────────
            # Display summary
            # ─────────────────────────────────────────────────────────────────
            
            groups_count = sum(1 for d in self.all_dialogs if d['type'] == 'group')
            channels_count = sum(1 for d in self.all_dialogs if d['type'] == 'channel')
            
            print(f"""
{Colors.BRIGHT_CYAN}╭──────────────────────────────────────────────────────────────╮
│                   {Colors.BRIGHT_GREEN}📊 FETCH COMPLETE{Colors.BRIGHT_CYAN}                            │
├──────────────────────────────────────────────────────────────┤
│  {Colors.GROUP}🔶 Groups   : {groups_count:>6}{Colors.BRIGHT_CYAN}                                      │
│  {Colors.CHANNEL}🔷 Channels : {channels_count:>6}{Colors.BRIGHT_CYAN}                                      │
│  {Colors.BRIGHT_WHITE}📊 Total    : {len(self.all_dialogs):>6}{Colors.BRIGHT_CYAN}                                      │
╰──────────────────────────────────────────────────────────────╯
{Colors.RESET}""")
            
            return self.all_dialogs
            
        except Exception as e:
            UI.show_error(f"Error fetching dialogs: {e}")
            return []
    
    # ═══════════════════════════════════════════════════════════════════════════
    #                           LEAVE OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def leave_dialog(self, dialog_info):
        """
        Leave a single group or channel.
        
        Args:
            dialog_info: Dictionary containing dialog information
        
        Returns:
            tuple: (success: bool, message: str)
        """
        
        entity = dialog_info['entity']
        title = dialog_info['title']
        
        try:
            # ─────────────────────────────────────────────────────────────────
            # Leave based on entity type
            # ─────────────────────────────────────────────────────────────────
            
            if isinstance(entity, Channel):
                # For supergroups and channels, use LeaveChannelRequest
                await self.client(LeaveChannelRequest(entity))
            
            elif isinstance(entity, Chat):
                # For basic groups, use DeleteChatUserRequest
                # This removes ourselves from the group
                await self.client(DeleteChatUserRequest(
                    chat_id=entity.id,
                    user_id='me'
                ))
            
            # ─────────────────────────────────────────────────────────────────
            # Log success
            # ─────────────────────────────────────────────────────────────────
            
            self.left_count += 1
            append_to_log(LOG_FILE, f"LEFT: {title} (ID: {entity.id})")
            
            return True, f"Successfully left: {title}"
            
        except FloodWaitError as e:
            # ─────────────────────────────────────────────────────────────────
            # Handle rate limiting
            # ─────────────────────────────────────────────────────────────────
            
            # Telegram is asking us to wait
            wait_time = e.seconds
            UI.show_warning(f"Rate limited! Waiting {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            
            # Retry after waiting
            return await self.leave_dialog(dialog_info)
            
        except RPCError as e:
            # ─────────────────────────────────────────────────────────────────
            # Handle other Telegram errors
            # ─────────────────────────────────────────────────────────────────
            
            self.failed_count += 1
            error_msg = str(e)
            append_to_log(LOG_FILE, f"FAILED: {title} - Error: {error_msg}")
            
            return False, f"Failed to leave {title}: {error_msg}"
            
        except Exception as e:
            # ─────────────────────────────────────────────────────────────────
            # Handle unexpected errors
            # ─────────────────────────────────────────────────────────────────
            
            self.failed_count += 1
            error_msg = str(e)
            append_to_log(LOG_FILE, f"FAILED: {title} - Error: {error_msg}")
            
            return False, f"Unexpected error leaving {title}: {error_msg}"
    
    async def leave_multiple(self, dialogs_to_leave, callback=None):
        """
        Leave multiple groups/channels with progress tracking.
        
        Args:
            dialogs_to_leave: List of dialog dictionaries to leave
            callback: Optional callback function for progress updates
        
        Returns:
            dict: Statistics about the operation
        """
        
        total = len(dialogs_to_leave)
        start_time = time.time()
        
        print(f"\n{Colors.BRIGHT_CYAN}{'═' * 80}")
        print(f"{Colors.BRIGHT_YELLOW}  🚀 Starting to leave {total} groups/channels...")
        print(f"{Colors.BRIGHT_CYAN}{'═' * 80}{Colors.RESET}\n")
        
        for i, dialog_info in enumerate(dialogs_to_leave, 1):
            title = dialog_info['title']
            dialog_type = dialog_info['type']
            
            # ─────────────────────────────────────────────────────────────────
            # Leave the group/channel
            # ─────────────────────────────────────────────────────────────────
            
            success, message = await self.leave_dialog(dialog_info)
            
            # ─────────────────────────────────────────────────────────────────
            # Display progress
            # ─────────────────────────────────────────────────────────────────
            
            status = f"{Colors.BRIGHT_GREEN}✅" if success else f"{Colors.BRIGHT_RED}❌"
            UI.show_progress(i, total, title, status)
            print()  # New line after progress bar
            
            # ─────────────────────────────────────────────────────────────────
            # Rate limiting delays
            # ─────────────────────────────────────────────────────────────────
            
            # Delay between each leave
            await asyncio.sleep(LEAVE_DELAY)
            
            # Extra delay after each batch
            if i % BATCH_SIZE == 0 and i < total:
                print(f"\n{Colors.BRIGHT_YELLOW}  ⏳ Pausing {BATCH_DELAY}s after batch of {BATCH_SIZE}...{Colors.RESET}")
                await asyncio.sleep(BATCH_DELAY)
                print()
        
        # ─────────────────────────────────────────────────────────────────────
        # Calculate statistics
        # ─────────────────────────────────────────────────────────────────────
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        stats = {
            'total': total,
            'left': self.left_count,
            'failed': self.failed_count,
            'skipped': self.skipped_count,
            'time_taken': time_taken
        }
        
        return stats
    
    # ═══════════════════════════════════════════════════════════════════════════
    #                           UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def reset_counters(self):
        """Reset all counters to zero."""
        self.left_count = 0
        self.failed_count = 0
        self.skipped_count = 0
    
    def get_statistics(self):
        """
        Get current statistics.
        
        Returns:
            dict: Dictionary with current counts
        """
        
        groups_count = sum(1 for d in self.all_dialogs if d['type'] == 'group')
        channels_count = sum(1 for d in self.all_dialogs if d['type'] == 'channel')
        
        return {
            'total_groups': groups_count,
            'total_channels': channels_count,
            'total': len(self.all_dialogs),
            'left': self.left_count,
            'failed': self.failed_count,
            'skipped': self.skipped_count
        }


# ═══════════════════════════════════════════════════════════════════════════════
#                              TEST (if run directly)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("This module should be imported, not run directly.")
    print("Use main.py to run the application.")
