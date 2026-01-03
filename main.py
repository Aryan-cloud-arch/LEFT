#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║         TELEGRAM AUTO LEAVE GROUPS & CHANNELS                 ║
║                                                               ║
║  📱 Telegram: @MaiHuAryan                                     ║
║  💻 GitHub:   github.com/Aryan-cloud-arch/LEFT                ║
╚═══════════════════════════════════════════════════════════════╝
"""

from telethon import TelegramClient
from telethon.tl.types import Channel, Chat
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import DeleteChatUserRequest
import asyncio
import os
import re
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION - Edit these values
# ═══════════════════════════════════════════════════════════════
API_ID = 12345678              # Get from my.telegram.org
API_HASH = "your_api_hash"     # Get from my.telegram.org
PHONE = "+919876543210"        # Your phone with country code

# ═══════════════════════════════════════════════════════════════
# COLORS FOR TERMINAL
# ═══════════════════════════════════════════════════════════════
class C:
    R = '\033[91m'    # Red
    G = '\033[92m'    # Green
    Y = '\033[93m'    # Yellow
    B = '\033[94m'    # Blue
    M = '\033[95m'    # Magenta
    C = '\033[96m'    # Cyan
    W = '\033[97m'    # White
    X = '\033[0m'     # Reset
    BOLD = '\033[1m'

# ═══════════════════════════════════════════════════════════════
# RANGE PARSER - Handles all formats
# ═══════════════════════════════════════════════════════════════
def parse_range(input_str, max_val):
    """
    Parse range input like: 1-40, 1-40,45-50, 5,10,15, all
    Returns set of integers
    """
    if not input_str or input_str.lower() == 'none':
        return set()
    
    if input_str.lower() == 'all':
        return set(range(1, max_val + 1))
    
    result = set()
    parts = input_str.replace(' ', '').split(',')
    
    for part in parts:
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                if start <= end:
                    result.update(range(start, min(end, max_val) + 1))
            except:
                pass
        else:
            try:
                num = int(part)
                if 1 <= num <= max_val:
                    result.add(num)
            except:
                pass
    
    return result

# ═══════════════════════════════════════════════════════════════
# UI FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
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
║           {C.W}🚀 AUTO LEAVE GROUPS & CHANNELS 🚀{C.C}                  ║
╠═══════════════════════════════════════════════════════════════╣
║  {C.G}📱 Telegram: @MaiHuAryan{C.C}                                     ║
║  {C.B}💻 GitHub:   github.com/Aryan-cloud-arch/LEFT{C.C}                ║
╚═══════════════════════════════════════════════════════════════╝{C.X}
""")

def watermark():
    print(f"{C.C}─────────────────────────────────────────────────────────{C.X}")
    print(f"{C.Y}  📱 @MaiHuAryan  {C.W}│{C.B}  💻 github.com/Aryan-cloud-arch/LEFT{C.X}")
    print(f"{C.C}─────────────────────────────────────────────────────────{C.X}\n")

def menu():
    print(f"""
{C.C}╭────────────────────────────────────────╮
│{C.Y}            📋 MAIN MENU                {C.C}│
├────────────────────────────────────────┤
│  {C.G}[1]{C.W} 📋 View All Groups/Channels       {C.C}│
│  {C.G}[2]{C.W} 🚀 Leave by Range                 {C.C}│
│  {C.G}[3]{C.W} 🔍 Search & Leave                 {C.C}│
│  {C.G}[4]{C.W} ⚡ Leave ALL (Dangerous!)         {C.C}│
│  {C.G}[5]{C.W} ❌ Exit                           {C.C}│
╰────────────────────────────────────────╯{C.X}
""")
    watermark()

# ═══════════════════════════════════════════════════════════════
# MAIN APP CLASS
# ═══════════════════════════════════════════════════════════════
class App:
    def __init__(self):
        self.client = TelegramClient('session', API_ID, API_HASH)
        self.dialogs = []
        self.stats = {'success': 0, 'failed': 0}
    
    async def connect(self):
        """Connect to Telegram"""
        print(f"{C.Y}⏳ Connecting to Telegram...{C.X}")
        await self.client.start(phone=PHONE)
        me = await self.client.get_me()
        print(f"{C.G}✅ Logged in: {me.first_name} (@{me.username}){C.X}\n")
    
    async def fetch_dialogs(self):
        """Fetch all groups and channels"""
        print(f"{C.Y}⏳ Fetching groups/channels...{C.X}")
        self.dialogs = []
        idx = 0
        
        async for dialog in self.client.iter_dialogs():
            entity = dialog.entity
            
            if isinstance(entity, Channel):
                idx += 1
                dtype = 'channel' if not entity.megagroup else 'group'
                self.dialogs.append({
                    'idx': idx,
                    'id': entity.id,
                    'title': dialog.title or "Unknown",
                    'type': dtype,
                    'username': getattr(entity, 'username', None),
                    'entity': entity
                })
            elif isinstance(entity, Chat):
                idx += 1
                self.dialogs.append({
                    'idx': idx,
                    'id': entity.id,
                    'title': dialog.title or "Unknown",
                    'type': 'group',
                    'username': None,
                    'entity': entity
                })
        
        groups = sum(1 for d in self.dialogs if d['type'] == 'group')
        channels = len(self.dialogs) - groups
        
        print(f"{C.G}✅ Found: {C.Y}{len(self.dialogs)}{C.G} total "
              f"({C.G}{groups} groups{C.W}, {C.B}{channels} channels{C.G}){C.X}\n")
    
    async def leave(self, dialog):
        """Leave a single group/channel"""
        try:
            entity = dialog['entity']
            if isinstance(entity, Channel):
                await self.client(LeaveChannelRequest(entity))
            else:
                await self.client(DeleteChatUserRequest(entity.id, 'me'))
            return True
        except Exception as e:
            return False
    
    def show_dialogs(self, page=1, page_size=100):
        """Display dialogs with pagination"""
        total = len(self.dialogs)
        total_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = min(start + page_size, total)
        
        clear()
        watermark()
        print(f"{C.C}╔═══ Page {page}/{total_pages} ═══ [{start+1}-{end}] of {total} ═══╗{C.X}\n")
        
        for d in self.dialogs[start:end]:
            color = C.G if d['type'] == 'group' else C.B
            icon = '👥' if d['type'] == 'group' else '📢'
            username = f" (@{d['username']})" if d['username'] else ""
            print(f"{C.W}[{d['idx']:3}] {color}{icon} {d['title'][:40]}{C.Y}{username}{C.X}")
        
        print(f"\n{C.C}╚═══════════════════════════════════════════════════════════╝{C.X}")
        print(f"{C.Y}[N]ext [P]rev [G]oto page [Q]uit{C.X}")
        
        return total_pages
    
    async def view_all(self):
        """View all dialogs with pagination"""
        if not self.dialogs:
            print(f"{C.R}❌ No dialogs found!{C.X}")
            return
        
        page = 1
        while True:
            total_pages = self.show_dialogs(page)
            
            cmd = input(f"\n{C.C}Enter command: {C.X}").lower().strip()
            
            if cmd == 'n' and page < total_pages:
                page += 1
            elif cmd == 'p' and page > 1:
                page -= 1
            elif cmd.startswith('g'):
                try:
                    p = int(cmd[1:].strip() or input("Page number: "))
                    if 1 <= p <= total_pages:
                        page = p
                except:
                    pass
            elif cmd == 'q':
                break
    
    async def leave_by_range(self):
        """Main feature: Leave by range with exclusions"""
        if not self.dialogs:
            print(f"{C.R}❌ No dialogs found!{C.X}")
            return
        
        # Show quick view option
        view = input(f"{C.Y}View list first? (y/n): {C.X}").lower()
        if view == 'y':
            await self.view_all()
        
        clear()
        watermark()
        print(f"{C.G}Total: {len(self.dialogs)} groups/channels{C.X}\n")
        
        # Range help
        print(f"{C.C}Range formats:{C.X}")
        print(f"  {C.W}• 1-40       → Select 1 to 40")
        print(f"  • 1-40,50-60 → Multiple ranges")
        print(f"  • 5,10,15    → Specific numbers")
        print(f"  • all        → Select all{C.X}\n")
        
        # Get range
        range_input = input(f"{C.Y}Enter range [1-{len(self.dialogs)}]: {C.X}").strip()
        selected = parse_range(range_input, len(self.dialogs))
        
        if not selected:
            print(f"{C.R}❌ No valid selection!{C.X}")
            return
        
        print(f"{C.G}✅ Selected: {len(selected)} items{C.X}\n")
        
        # Exclusions
        print(f"{C.C}Exclude formats:{C.X}")
        print(f"  {C.W}• 7-9 or 7,8,9  → Exclude these")
        print(f"  • search        → Search by name")
        print(f"  • none          → No exclusions{C.X}\n")
        
        exclude_input = input(f"{C.Y}Exclude (or 'none'/'search'): {C.X}").strip().lower()
        excluded = set()
        
        if exclude_input == 'search':
            # Search exclusion
            while True:
                term = input(f"{C.Y}Search term (or 'done'): {C.X}").strip()
                if term.lower() == 'done':
                    break
                
                matches = [(d['idx'], d['title']) for d in self.dialogs 
                          if d['idx'] in selected and term.lower() in d['title'].lower()]
                
                if matches:
                    print(f"\n{C.G}Found {len(matches)} matches:{C.X}")
                    for idx, title in matches:
                        print(f"  {C.W}[{idx}] {title}{C.X}")
                    
                    exc = input(f"{C.Y}Exclude which? (indices or 'all'): {C.X}").strip()
                    if exc.lower() == 'all':
                        excluded.update(idx for idx, _ in matches)
                    else:
                        excluded.update(parse_range(exc, len(self.dialogs)))
                else:
                    print(f"{C.R}No matches found{C.X}")
        
        elif exclude_input != 'none':
            excluded = parse_range(exclude_input, len(self.dialogs))
        
        excluded = excluded.intersection(selected)
        final = selected - excluded
        
        if not final:
            print(f"{C.R}❌ Nothing to leave after exclusions!{C.X}")
            return
        
        # Preview
        clear()
        watermark()
        
        to_leave = [d for d in self.dialogs if d['idx'] in final]
        to_keep = [d for d in self.dialogs if d['idx'] in excluded]
        
        print(f"""
{C.R}╔═══════════════════════════════╗  {C.G}╔═══════════════════════════════╗
║   ❌ TO BE LEFT ({len(to_leave):3})          ║  ║   ✅ TO KEEP ({len(to_keep):3})             ║
╠═══════════════════════════════╣  ╠═══════════════════════════════╣{C.X}""")
        
        max_show = max(len(to_leave), len(to_keep), 10)
        for i in range(min(max_show, 15)):
            left_item = f"{to_leave[i]['idx']}. {to_leave[i]['title'][:20]}" if i < len(to_leave) else ""
            keep_item = f"{to_keep[i]['idx']}. {to_keep[i]['title'][:20]}" if i < len(to_keep) else ""
            print(f"{C.R}║ {left_item:<29} ║  {C.G}║ {keep_item:<29} ║{C.X}")
        
        if len(to_leave) > 15:
            print(f"{C.R}║  ... and {len(to_leave)-15} more{' '*14}║  {C.G}║{' '*31}║{C.X}")
        
        print(f"{C.R}╚═══════════════════════════════╝  {C.G}╚═══════════════════════════════╝{C.X}\n")
        
        # Confirm
        print(f"{C.R}⚠️  WARNING: {len(to_leave)} groups/channels will be LEFT!{C.X}")
        confirm = input(f"{C.Y}Type 'CONFIRM' to proceed: {C.X}").strip()
        
        if confirm != 'CONFIRM':
            print(f"{C.Y}Cancelled.{C.X}")
            return
        
        # Execute
        await self._execute_leave(to_leave)
    
    async def leave_by_search(self):
        """Search and leave"""
        term = input(f"{C.Y}Search term: {C.X}").strip()
        if not term:
            return
        
        matches = [d for d in self.dialogs if term.lower() in d['title'].lower()]
        
        if not matches:
            print(f"{C.R}No matches found!{C.X}")
            return
        
        print(f"\n{C.G}Found {len(matches)} matches:{C.X}")
        for d in matches:
            color = C.G if d['type'] == 'group' else C.B
            print(f"  {C.W}[{d['idx']}] {color}{d['title']}{C.X}")
        
        choice = input(f"\n{C.Y}Select to leave (range/all/cancel): {C.X}").strip()
        
        if choice.lower() == 'cancel':
            return
        
        if choice.lower() == 'all':
            to_leave = matches
        else:
            indices = parse_range(choice, len(self.dialogs))
            match_indices = {d['idx'] for d in matches}
            valid = indices.intersection(match_indices)
            to_leave = [d for d in matches if d['idx'] in valid]
        
        if not to_leave:
            print(f"{C.R}Nothing selected!{C.X}")
            return
        
        confirm = input(f"{C.R}Leave {len(to_leave)} items? (CONFIRM): {C.X}").strip()
        if confirm == 'CONFIRM':
            await self._execute_leave(to_leave)
    
    async def leave_all(self):
        """Leave ALL - Dangerous"""
        print(f"{C.R}")
        print("╔═══════════════════════════════════════════════════════╗")
        print("║             ⚠️  DANGER ZONE ⚠️                         ║")
        print(f"║   This will leave ALL {len(self.dialogs)} groups/channels!           ║")
        print("╚═══════════════════════════════════════════════════════╝")
        print(f"{C.X}")
        
        c1 = input(f"{C.Y}Type 'I UNDERSTAND': {C.X}").strip()
        if c1 != 'I UNDERSTAND':
            return
        
        c2 = input(f"{C.Y}Type 'LEAVE ALL': {C.X}").strip()
        if c2 != 'LEAVE ALL':
            return
        
        await self._execute_leave(self.dialogs)
    
    async def _execute_leave(self, dialogs):
        """Execute leaving with progress"""
        total = len(dialogs)
        self.stats = {'success': 0, 'failed': 0}
        start_time = datetime.now()
        
        print(f"\n{C.Y}⏳ Leaving {total} groups/channels...{C.X}\n")
        
        for i, d in enumerate(dialogs, 1):
            result = await self.leave(d)
            
            if result:
                self.stats['success'] += 1
                print(f"{C.G}✅ [{i}/{total}] Left: {d['title'][:40]}{C.X}")
            else:
                self.stats['failed'] += 1
                print(f"{C.R}❌ [{i}/{total}] Failed: {d['title'][:40]}{C.X}")
            
            # Progress bar
            pct = int(i / total * 30)
            bar = f"[{'█' * pct}{'░' * (30-pct)}] {i}/{total}"
            print(f"{C.C}{bar}{C.X}")
            
            # Rate limiting
            await asyncio.sleep(2)
            if i % 10 == 0:
                print(f"{C.Y}⏳ Pausing 10s...{C.X}")
                await asyncio.sleep(10)
        
        # Summary
        duration = datetime.now() - start_time
        print(f"""
{C.C}╔═══════════════════════════════════════════════════════╗
║                    📊 SUMMARY                          ║
╠═══════════════════════════════════════════════════════╣
║  {C.G}✅ Success: {self.stats['success']:<5}{C.C}                                  ║
║  {C.R}❌ Failed:  {self.stats['failed']:<5}{C.C}                                  ║
║  {C.Y}⏱️  Time:    {str(duration).split('.')[0]:<10}{C.C}                          ║
╚═══════════════════════════════════════════════════════╝{C.X}
""")
        watermark()
        
        # Export log
        self._export_log(dialogs)
    
    def _export_log(self, dialogs):
        """Export to log file"""
        os.makedirs('logs', exist_ok=True)
        filename = f"logs/left_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("TELEGRAM AUTO LEAVE LOG\n")
            f.write(f"@MaiHuAryan | github.com/Aryan-cloud-arch/LEFT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Success: {self.stats['success']}\n")
            f.write(f"Failed: {self.stats['failed']}\n\n")
            f.write("Groups/Channels:\n")
            for d in dialogs:
                f.write(f"[{d['idx']}] {d['title']} ({d['type']})\n")
        
        print(f"{C.G}📄 Log saved: {filename}{C.X}")
    
    async def run(self):
        """Main loop"""
        try:
            banner()
            await self.connect()
            await self.fetch_dialogs()
            
            while True:
                menu()
                choice = input(f"{C.C}Enter choice [1-5]: {C.X}").strip()
                
                if choice == '1':
                    await self.view_all()
                elif choice == '2':
                    await self.leave_by_range()
                elif choice == '3':
                    await self.leave_by_search()
                elif choice == '4':
                    await self.leave_all()
                elif choice == '5':
                    print(f"\n{C.G}👋 Bye! @MaiHuAryan{C.X}\n")
                    break
                else:
                    print(f"{C.R}Invalid choice!{C.X}")
                
                input(f"\n{C.Y}Press Enter to continue...{C.X}")
                
        except KeyboardInterrupt:
            print(f"\n{C.Y}Cancelled by user.{C.X}")
        finally:
            await self.client.disconnect()

# ═══════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    asyncio.run(app.run())
