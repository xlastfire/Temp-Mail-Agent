#!/usr/bin/env python3
"""
📧 TempMail123 Terminal Agent
A complete CLI tool for managing temporary email addresses
"""

import requests
import json
import time
import os
import sys
from datetime import datetime
from typing import Optional, Dict, List

# ==========================================
# GIT CONFIGURATION
# ==========================================
GIT_USERNAME = "xlastfire"
GIT_REPO = "https://github.com/xlastfire/Temp-Mail-Agent"
# ==========================================

# ANSI Color Codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Foreground Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright Foreground Colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

# Clear Console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Print colored text
def print_color(text: str, color: str = Colors.RESET, bold: bool = False):
    bold_code = Colors.BOLD if bold else ""
    print(f"{bold_code}{color}{text}{Colors.RESET}")

# Print header with Git Name
def print_header():
    clear_console()
    
    # Calculate padding for perfect centering (68 is the inner width)
    git_line = f"By @{GIT_USERNAME}"
    left_pad = (68 - len(git_line)) // 2
    right_pad = 68 - len(git_line) - left_pad
    
    print_color("╔" + "═" * 68 + "╗", Colors.BRIGHT_CYAN)
    print_color("║" + " " * 19 + "📧 TempMail123 Terminal Agent" + " " * 19 + "║", Colors.BRIGHT_CYAN, bold=True)
    print_color("║" + " " * left_pad + git_line + " " * right_pad + "║", Colors.BRIGHT_MAGENTA, bold=True)
    print_color("╚" + "═" * 68 + "╝", Colors.BRIGHT_CYAN)
    print()

# Print separator
def print_separator(char: str = "─", length: int = 70):
    print_color(char * length, Colors.DIM)

# TempMail API Client
class TempMailClient:
    def __init__(self):
        self.base_url = "https://api.tempmail123.com/v1"
        self.mailbox_id: Optional[str] = None
        self.mailbox_address: Optional[str] = None
        self.mailbox_token: Optional[str] = None
        self.expires_at: Optional[str] = None
        self.session = requests.Session()
        
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://tempmail123.com",
            "priority": "u=1, i",
            "referer": "https://tempmail123.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        }
    
    def create_mailbox(self) -> Dict:
        """Create a new 10-minute temporary mailbox"""
        url = f"{self.base_url}/mailboxes"
        
        json_data = {"expiresIn": "10m"}
        
        try:
            response = self.session.post(url, headers=self.headers, json=json_data, timeout=30)
            
            if response.status_code in[200, 201]:
                data = response.json()
                if data.get('data'):
                    self.mailbox_id = data['data'].get('id')
                    self.mailbox_address = data['data'].get('address')
                    self.mailbox_token = data['data'].get('token')
                    self.expires_at = data['data'].get('expiresAt')
                    return {'success': True, 'data': data['data']}
            
            return {'success': False, 'error': f"Status: {response.status_code}", 'raw': response.text}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_messages(self) -> Dict:
        """Get all messages for the current mailbox"""
        if not self.mailbox_id or not self.mailbox_token:
            return {'success': False, 'error': 'No mailbox created'}
        
        url = f"{self.base_url}/mailboxes/{self.mailbox_id}/messages"
        headers = self.headers.copy()
        headers['x-mailbox-token'] = self.mailbox_token
        
        try:
            response = self.session.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {'success': True, 'data': data.get('data', {})}
            
            return {'success': False, 'error': f"Status: {response.status_code}", 'raw': response.text}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_message_details(self, message_id: str) -> Dict:
        """Get full details of a specific message"""
        if not self.mailbox_id or not self.mailbox_token:
            return {'success': False, 'error': 'No mailbox created'}
        
        url = f"{self.base_url}/mailboxes/{self.mailbox_id}/messages/{message_id}"
        headers = self.headers.copy()
        headers['x-mailbox-token'] = self.mailbox_token
        
        try:
            response = self.session.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {'success': True, 'data': data.get('data', {})}
            
            return {'success': False, 'error': f"Status: {response.status_code}", 'raw': response.text}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_mailbox(self) -> Dict:
        """Delete the current mailbox"""
        if not self.mailbox_id or not self.mailbox_token:
            return {'success': False, 'error': 'No mailbox created'}
        
        url = f"{self.base_url}/mailboxes/{self.mailbox_id}"
        headers = self.headers.copy()
        headers['x-mailbox-token'] = self.mailbox_token
        
        try:
            response = self.session.delete(url, headers=headers, timeout=30)
            
            if response.status_code in[200, 204]:
                self._reset_mailbox()
                return {'success': True}
            
            return {'success': False, 'error': f"Status: {response.status_code}", 'raw': response.text}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _reset_mailbox(self):
        """Reset mailbox credentials"""
        self.mailbox_id = None
        self.mailbox_address = None
        self.mailbox_token = None
        self.expires_at = None
    
    def is_mailbox_active(self) -> bool:
        """Check if mailbox is active"""
        return bool(self.mailbox_id and self.mailbox_token)
    
    def get_time_remaining(self) -> str:
        """Get time remaining until expiry"""
        if not self.expires_at:
            return "Unknown"
        
        try:
            expires = datetime.fromisoformat(self.expires_at.replace('Z', '+00:00'))
            now = datetime.now(expires.tzinfo)
            remaining = expires - now
            
            if remaining.total_seconds() <= 0:
                return "Expired"
            
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            return f"{minutes}m {seconds}s"
        except:
            return "Unknown"

# Main Agent Class
class TempMailAgent:
    def __init__(self):
        self.client = TempMailClient()
        self.running = True
        self.auto_refresh = False
        self.refresh_interval = 5
    
    def show_status(self):
        """Display current mailbox status"""
        print_separator("─")
        print_color("📊 MAILBOX STATUS", Colors.BRIGHT_BLUE, bold=True)
        print_separator("─")
        
        if self.client.is_mailbox_active():
            print_color(f"  📧 Address     : {Colors.BRIGHT_GREEN}{self.client.mailbox_address}{Colors.RESET}")
            print_color(f"  🔑 Token       : {Colors.DIM}{self.client.mailbox_token[:20]}...{Colors.RESET}")
            print_color(f"  ⏰ Expires In  : {Colors.BRIGHT_YELLOW}{self.client.get_time_remaining()}{Colors.RESET}")
            print_color(f"  ✅ Status      : {Colors.BRIGHT_GREEN}Active{Colors.RESET}")
        else:
            print_color(f"  ❌ No active mailbox", Colors.BRIGHT_RED)
            print_color(f"  💡 Create one with option 1", Colors.DIM)
        
        print()
    
    def show_messages(self, messages_data: Dict):
        """Display messages in a formatted way"""
        print_separator("─")
        print_color("📬 INBOX", Colors.BRIGHT_MAGENTA, bold=True)
        print_separator("─")
        
        items = messages_data.get('items',[])
        count = messages_data.get('count', 0)
        
        if not items:
            print_color("  📭 No messages yet...", Colors.DIM)
            print()
            return
        
        print_color(f"  Total Messages: {count}", Colors.BRIGHT_CYAN)
        print()
        
        for idx, msg in enumerate(items, 1):
            status = "📗" if msg.get('isRead') else "📙"
            print_color(f"  [{idx}] {status} {msg.get('subject', 'No Subject')}", Colors.WHITE)
            print_color(f"      From: {msg.get('fromName', 'Unknown')} <{msg.get('fromAddress', 'Unknown')}>", Colors.DIM)
            print_color(f"      Time: {msg.get('receivedAt', 'Unknown')[:19]}", Colors.DIM)
            print_color(f"      Preview: {msg.get('preview', '')[:50]}...", Colors.CYAN)
            print()
    
    def show_message_detail(self, message: Dict):
        """Display full message details"""
        print_separator("═")
        print_color("📄 MESSAGE DETAILS", Colors.BRIGHT_GREEN, bold=True)
        print_separator("═")
        
        print_color(f"  📧 From    : {message.get('fromName', 'Unknown')} <{message.get('fromAddress', 'Unknown')}>", Colors.WHITE)
        print_color(f"  📨 To      : {message.get('to', 'Unknown')}", Colors.WHITE)
        print_color(f"  📝 Subject : {message.get('subject', 'No Subject')}", Colors.BRIGHT_YELLOW, bold=True)
        print_color(f"  ⏰ Received: {message.get('receivedAt', 'Unknown')[:19]}", Colors.DIM)
        print_color(f"  📖 Status  : {'Read' if message.get('isRead') else 'Unread'}", Colors.CYAN)
        
        print()
        print_separator("─")
        print_color("  MESSAGE BODY:", Colors.BRIGHT_BLUE, bold=True)
        print_separator("─")
        
        # Show text body
        text_body = message.get('text', message.get('html', 'No content'))
        # Clean up the text
        text_body = text_body.replace('\\r\\n', '\n').replace('\\n', '\n')
        
        for line in text_body.split('\n'):
            print_color(f"  {line}", Colors.WHITE)
        
        print()
    
    def create_mailbox_menu(self):
        """Create a new mailbox"""
        print_header()
        print_color("🆕 CREATE NEW MAILBOX", Colors.BRIGHT_GREEN, bold=True)
        print()
        
        print_color("  Generating a new 10-minute temporary mailbox...", Colors.DIM)
        print()
        
        result = self.client.create_mailbox()
        
        if result['success']:
            data = result['data']
            print_color("  ✅ Mailbox created successfully!", Colors.BRIGHT_GREEN, bold=True)
            print()
            print_color(f"  📧 Email: {data.get('address')}", Colors.BRIGHT_CYAN)
            print_color(f"  ⏰ Expires: {data.get('expiresAt', 'Unknown')[:19]}", Colors.YELLOW)
            print()
            input("  Press Enter to continue...")
        else:
            print_color(f"  ❌ Error: {result.get('error', 'Unknown')}", Colors.BRIGHT_RED)
            input("  Press Enter to continue...")
    
    def inbox_menu(self):
        """Menu to view inbox"""
        while True:
            print_header()
            self.show_status()
            
            result = self.client.get_messages()
            
            if result['success']:
                self.show_messages(result['data'])
            else:
                print_color(f"  ❌ Error: {result.get('error', 'Unknown')}", Colors.BRIGHT_RED)
            
            print_separator("─")
            print("  [1] Refresh")
            print("[2] Read Message")
            print("  [3] Toggle Auto-Refresh")
            print("[0] Back")
            print()
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                continue
            elif choice == '2':
                self.read_message_menu(result.get('data', {}))
            elif choice == '3':
                self.auto_refresh = not self.auto_refresh
                status = "ON" if self.auto_refresh else "OFF"
                print_color(f"  Auto-refresh turned {status}", Colors.BRIGHT_CYAN)
                time.sleep(1)
    
    def read_message_menu(self, messages_data: Dict):
        """Menu to read a specific message"""
        items = messages_data.get('items',[])
        
        if not items:
            print_color("  No messages to read!", Colors.BRIGHT_RED)
            time.sleep(1)
            return
        
        print()
        msg_num = input("  Enter message number to read: ").strip()
        
        try:
            idx = int(msg_num) - 1
            if 0 <= idx < len(items):
                msg_id = items[idx].get('id')
                
                print()
                print_color("  Loading message...", Colors.DIM)
                
                result = self.client.get_message_details(msg_id)
                
                if result['success']:
                    self.show_message_detail(result['data'])
                    input("  Press Enter to continue...")
                else:
                    print_color(f"  ❌ Error: {result.get('error', 'Unknown')}", Colors.BRIGHT_RED)
                    time.sleep(1)
            else:
                print_color("  Invalid message number!", Colors.BRIGHT_RED)
                time.sleep(1)
        except ValueError:
            print_color("  Invalid input!", Colors.BRIGHT_RED)
            time.sleep(1)
    
    def settings_menu(self):
        """Settings menu"""
        while True:
            print_header()
            print_color("⚙️  SETTINGS", Colors.BRIGHT_YELLOW, bold=True)
            print()
            
            print(f"  Auto-Refresh: {'ON' if self.auto_refresh else 'OFF'}")
            print(f"  Refresh Interval: {self.refresh_interval}s")
            print()
            
            print("  [1] Toggle Auto-Refresh")
            print("  [2] Change Refresh Interval")
            print("  [0] Back")
            print()
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.auto_refresh = not self.auto_refresh
                status = "ON" if self.auto_refresh else "OFF"
                print_color(f"  Auto-refresh turned {status}", Colors.BRIGHT_CYAN)
                time.sleep(1)
            elif choice == '2':
                try:
                    interval = int(input("  Enter refresh interval (seconds): ").strip())
                    if 1 <= interval <= 60:
                        self.refresh_interval = interval
                        print_color("  Interval updated!", Colors.BRIGHT_GREEN)
                    else:
                        print_color("  Please enter 1-60 seconds", Colors.BRIGHT_RED)
                    time.sleep(1)
                except ValueError:
                    print_color("  Invalid input!", Colors.BRIGHT_RED)
                    time.sleep(1)
    
    def main_menu(self):
        """Main application menu"""
        while self.running:
            print_header()
            self.show_status()
            
            print_separator("═")
            print_color("  MAIN MENU", Colors.BRIGHT_WHITE, bold=True)
            print_separator("═")
            print()
            print("[1] 🆕 Create New Mailbox")
            print("  [2] 📬 View Inbox")
            print("  [3] ⚙️  Settings")
            print("  [4] 🔄 Quick Refresh")
            print("  [5] 🗑️  Delete Mailbox")
            print("[6] ℹ️  About")
            print("  [0] 🚪 Exit")
            print()
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                print()
                print_color("  Goodbye! 👋", Colors.BRIGHT_CYAN, bold=True)
                print()
                self.running = False
            elif choice == '1':
                self.create_mailbox_menu()
            elif choice == '2':
                if not self.client.is_mailbox_active():
                    print_color("  ❌ Please create a mailbox first!", Colors.BRIGHT_RED)
                    time.sleep(1.5)
                else:
                    self.inbox_menu()
            elif choice == '3':
                self.settings_menu()
            elif choice == '4':
                print_header()
                print_color("  Refreshing...", Colors.DIM)
                result = self.client.get_messages()
                if result['success']:
                    self.show_messages(result['data'])
                else:
                    print_color(f"  ❌ Error: {result.get('error', 'Unknown')}", Colors.BRIGHT_RED)
                input("  Press Enter to continue...")
            elif choice == '5':
                if self.client.is_mailbox_active():
                    confirm = input("  Are you sure? (y/n): ").strip().lower()
                    if confirm == 'y':
                        result = self.client.delete_mailbox()
                        if result['success']:
                            print_color("  ✅ Mailbox deleted!", Colors.BRIGHT_GREEN)
                        else:
                            print_color(f"  ❌ Error: {result.get('error', 'Unknown')}", Colors.BRIGHT_RED)
                        time.sleep(1)
                else:
                    print_color("  No active mailbox to delete!", Colors.BRIGHT_RED)
                    time.sleep(1)
            elif choice == '6':
                self.show_about()
    
    def show_about(self):
        """Show about information"""
        print_header()
        print_color("ℹ️  ABOUT", Colors.BRIGHT_MAGENTA, bold=True)
        print_separator("═")
        print()
        print_color("  TempMail123 Terminal Agent", Colors.BRIGHT_CYAN, bold=True)
        print(f"  Developer : @{GIT_USERNAME}")
        print(f"  GitHub    : {GIT_REPO}")
        print()
        print("  Version   : 1.0.0")
        print("  API       : tempmail123.com")
        print()
        print("  Features:")
        print_color("    ✓ Automatically create 10m temporary email addresses", Colors.BRIGHT_GREEN)
        print_color("    ✓ Receive and read emails", Colors.BRIGHT_GREEN)
        print_color("    ✓ Auto-refresh inbox", Colors.BRIGHT_GREEN)
        print_color("    ✓ Beautiful colored terminal UI", Colors.BRIGHT_GREEN)
        print()
        print("  Created with Python & Requests")
        print()
        print_separator("─")
        input("  Press Enter to continue...")

# Auto-refresh thread (optional enhancement)
def auto_refresh_loop(agent: TempMailAgent):
    """Background auto-refresh"""
    while agent.running and agent.auto_refresh:
        time.sleep(agent.refresh_interval)
        if agent.client.is_mailbox_active():
            agent.client.get_messages()

# Main Entry Point
def main():
    print_color("\n🚀 Starting TempMail123 Terminal Agent...", Colors.BRIGHT_GREEN, bold=True)
    time.sleep(1)
    
    agent = TempMailAgent()
    
    try:
        agent.main_menu()
    except KeyboardInterrupt:
        print()
        print_color("\n  Interrupted by user. Goodbye! 👋", Colors.BRIGHT_YELLOW)
        print()
    except Exception as e:
        print_color(f"\n  ❌ Unexpected error: {e}", Colors.BRIGHT_RED)
        print()

if __name__ == "__main__":
    main()
