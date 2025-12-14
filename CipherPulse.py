#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║         CipherPulse ENCRYPTION TOOL v2.0 - AI POWERED                    ║
║              Kali Linux Edition | PROJECT                  		   ║
║                                                                          ║
║  Features:                                                               ║
║  ✓ Manual Encryption/Decryption with Custom Shift                        ║
║  ✓ Brute Force Decoder (All 26 Keys)                                     ║
║  ✓ AI-Powered Frequency Analysis                                         ║
║  ✓ Smart Auto Decoder with English Dictionary                            ║
║  ✓ Multiple Output Formats (Text, Bytes, Punched Tape)                   ║
║  ✓ Retro Terminal GUI                                                    ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import string
import threading
from collections import Counter
from typing import Dict, List, Tuple

class CaesarCipherTool:
    """AI-Powered Caesar Cipher Encryption/Decryption Tool"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 CipherPulse v2.0 - AI POWERED")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0e27")
        
        # Common English words for AI detection
        self.common_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'is', 'was', 'are', 'or', 'an',
            'as', 'if', 'my', 'we', 'your', 'all', 'can', 'her', 'what', 'so',
            'there', 'about', 'more', 'when', 'out', 'up', 'other', 'will', 'then'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the retro-style GUI"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define color scheme (Kali-inspired dark theme)
        bg_dark = "#0a0e27"
        bg_darker = "#050812"
        fg_green = "#00ff00"
        fg_cyan = "#00ffff"
        fg_white = "#ffffff"
        accent_color = "#1a1f3a"
        
        style.configure('Dark.TFrame', background=bg_dark)
        style.configure('Dark.TLabel', background=bg_dark, foreground=fg_green, font=('Courier', 10))
        style.configure('Title.TLabel', background=bg_dark, foreground=fg_cyan, font=('Courier', 12, 'bold'))
        style.configure('Dark.TButton', background=accent_color, foreground=fg_green, font=('Courier', 9))
        style.configure('Dark.TEntry', fieldbackground=bg_darker, foreground=fg_green, font=('Courier', 12, 'bold'))  # LARGER FONT
        style.configure('Large.TSpinbox', fieldbackground=bg_darker, foreground=fg_cyan, font=('Courier', 14, 'bold'), arrowcolor=fg_cyan)
        
        # Main frame
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame, fg_cyan)
        
        # Container for left and right panels
        content_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left panel - Input & Options
        left_panel = self.create_left_panel(content_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel - Output
        right_panel = self.create_right_panel(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    def create_header(self, parent, color):
        """Create retro header with ASCII art"""
        header_frame = ttk.Frame(parent, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=5)
        
        title_label = ttk.Label(
            header_frame,
            text="╔════════════════════════════════════════════════════╗\n" +
                 "║          🔐   CipherPulse v2.0                     ║\n" +
                 "║  AI-Powered | Kali Linux Edition | Caesar-Cipher   ║\n" +
                 "╚════════════════════════════════════════════════════╝",
            style='Title.TLabel',
            justify=tk.CENTER
        )
        title_label.pack()
        
    def create_left_panel(self, parent):
        """Create left panel with input controls"""
        left_frame = ttk.Frame(parent, style='Dark.TFrame')
        
        # Input section
        input_label = ttk.Label(left_frame, text="▶ TEXT INPUT", style='Title.TLabel')
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        # LARGER FONT FOR TEXT INPUT (14pt from 10pt)
        self.input_text = scrolledtext.ScrolledText(
            left_frame, height=8, width=50, bg="#050812", fg="#00ff00",
            font=('Courier', 14, 'bold'), insertbackground="#00ff00"  # INCREASED FROM 10 TO 14
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Shift value section - LARGER BOX AND FONT
        shift_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        shift_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(shift_frame, text="SHIFT VALUE (1-25):", style='Dark.TLabel').pack(side=tk.LEFT, padx=5)
        self.shift_var = tk.IntVar(value=3)
        # LARGER SPINBOX WITH BIGGER FONT (width=8 from 5, font 16pt)
        shift_spinbox = ttk.Spinbox(
            shift_frame, from_=1, to=25, textvariable=self.shift_var,
            width=8, font=('Courier', 16, 'bold')  # LARGER FONT AND WIDER BOX
        )
        shift_spinbox.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Operation buttons
        buttons_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            buttons_frame, text="🔒 ENCRYPT", 
            command=lambda: self.encrypt_text()
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(
            buttons_frame, text="🔓 DECRYPT", 
            command=lambda: self.decrypt_text()
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # AI Decryption section
        ai_label = ttk.Label(left_frame, text="▶ AI-POWERED DECRYPTION", style='Title.TLabel')
        ai_label.pack(anchor=tk.W, pady=(15, 5))
        
        ai_buttons_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        ai_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            ai_buttons_frame, text="🤖 BRUTE FORCE", 
            command=lambda: self.brute_force_decrypt()
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(
            ai_buttons_frame, text="🧠 FREQUENCY ANALYSIS", 
            command=lambda: self.frequency_analysis()
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(
            ai_buttons_frame, text="⚡ AUTO DECODER", 
            command=lambda: self.auto_decode()
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Output format section
        format_label = ttk.Label(left_frame, text="▶ OUTPUT FORMAT", style='Title.TLabel')
        format_label.pack(anchor=tk.W, pady=(15, 5))
        
        self.format_var = tk.StringVar(value="text")
        formats = [("TEXT", "text"), ("BYTES", "bytes"), ("PUNCHED TAPE", "tape")]
        
        format_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        format_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        for text, value in formats:
            ttk.Radiobutton(
                format_frame,
                text=text,
                variable=self.format_var,
                value=value
            ).pack(side=tk.LEFT, padx=10)
        
        # Control buttons
        control_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        control_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(control_frame, text="📋 CLEAR", command=self.clear_all).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(control_frame, text="💾 SAVE", command=self.save_output).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(control_frame, text="📂 LOAD", command=self.load_file).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        return left_frame
    
    def create_right_panel(self, parent):
        """Create right panel with output display"""
        right_frame = ttk.Frame(parent, style='Dark.TFrame')
        
        output_label = ttk.Label(right_frame, text="▶ OUTPUT RESULTS", style='Title.TLabel')
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        # LARGER FONT FOR OUTPUT RESULTS (12pt from 9pt)
        self.output_text = scrolledtext.ScrolledText(
            right_frame, height=15, width=50, bg="#050812", fg="#00ffff",
            font=('Courier', 10, 'bold'), insertbackground="#00ffff"  # INCREASED FROM 9 TO 12
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Copy button
        ttk.Button(right_frame, text="📋 COPY TO CLIPBOARD", command=self.copy_output).pack(fill=tk.X, pady=5)
        
        return right_frame
    
    # [Rest of the methods remain exactly the same - no changes needed]
    def encrypt_text(self):
        """Encrypt text using Caesar cipher"""
        text = self.input_text.get("1.0", tk.END).strip()
        shift = self.shift_var.get()
        
        if not text:
            messagebox.showwarning("Input Required", "Please enter text to encrypt!")
            return
        
        result = self._caesar_encrypt(text, shift)
        self.display_output(f"ENCRYPTED (Shift={shift}):\n{result}", result)
    
    def decrypt_text(self):
        """Decrypt text using Caesar cipher"""
        text = self.input_text.get("1.0", tk.END).strip()
        shift = self.shift_var.get()
        
        if not text:
            messagebox.showwarning("Input Required", "Please enter text to decrypt!")
            return
        
        result = self._caesar_decrypt(text, shift)
        self.display_output(f"DECRYPTED (Shift={shift}):\n{result}", result)
    
    def brute_force_decrypt(self):
        """Brute force all 26 possible shifts"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Input Required", "Please enter text to decrypt!")
            return
        
        output = "═" * 50 + "\n"
        output += "BRUTE FORCE DECRYPTION (All 26 Possible Shifts)\n"
        output += "═" * 50 + "\n\n"
        
        best_shift = 0
        best_score = 0
        best_text = ""
        
        for shift in range(26):
            decrypted = self._caesar_decrypt(text, shift)
            score = self._calculate_english_score(decrypted)
            
            output += f"[Shift {shift:2d}] {decrypted[:45]:<45} | Score: {score:3d}\n"
            
            if score > best_score:
                best_score = score
                best_shift = shift
                best_text = decrypted
        
        output += "\n" + "═" * 50 + "\n"
        output += f"✓ BEST MATCH: Shift {best_shift} (Score: {best_score})\n"
        output += "═" * 50 + "\n\n"
        output += f"RESULT:\n{best_text}"
        
        self.display_output(output, best_text)
    
    def frequency_analysis(self):
        """AI-powered frequency analysis for decryption"""
        text = self.input_text.get("1.0", tk.END).strip().upper()
        
        if not text:
            messagebox.showwarning("Input Required", "Please enter text!")
            return
        
        # Count letter frequencies
        letter_count = Counter(c for c in text if c.isalpha())
        total_letters = sum(letter_count.values())
        
        output = "═" * 60 + "\n"
        output += "AI FREQUENCY ANALYSIS REPORT\n"
        output += "═" * 60 + "\n\n"
        
        output += "LETTER FREQUENCIES:\n"
        output += "─" * 60 + "\n"
        
        for letter in "ETAOINSHRDLCUMWFGYPBVKJXQZ":
            if letter in letter_count:
                count = letter_count[letter]
                percent = (count / total_letters) * 100
                bar = "█" * int(percent / 2)
                output += f"[{letter}] {count:3d} ({percent:5.1f}%) {bar}\n"
        
        # Try to decode assuming E is the most common letter
        output += "\n" + "─" * 60 + "\n"
        output += "INTELLIGENT SHIFT ANALYSIS:\n"
        output += "─" * 60 + "\n"
        
        if letter_count:
            most_common_letter = letter_count.most_common(1)[0][0]
            shift = (ord(most_common_letter) - ord('E')) % 26
            decrypted = self._caesar_decrypt(text, shift)
            score = self._calculate_english_score(decrypted)
            
            output += f"Most common letter '{most_common_letter}' → Assume shift: {shift}\n"
            output += f"Confidence score: {score}%\n\n"
            output += f"DECODED TEXT:\n{decrypted}"
            
            self.display_output(output, decrypted)
        else:
            messagebox.showerror("Error", "No letters found in text!")
    
    def auto_decode(self):
        """Smart auto decoder using dictionary matching"""
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Input Required", "Please enter text to decrypt!")
            return
        
        output = "═" * 60 + "\n"
        output += "⚡ AUTO DECODER - SMART DICTIONARY MATCHING\n"
        output += "═" * 60 + "\n\n"
        
        best_shift = 0
        best_score = 0
        best_text = ""
        candidates = []
        
        # Test all shifts and score them
        for shift in range(26):
            decrypted = self._caesar_decrypt(text, shift)
            score = self._score_by_dictionary(decrypted)
            candidates.append((shift, decrypted, score))
            
            if score > best_score:
                best_score = score
                best_shift = shift
                best_text = decrypted
        
        # Sort by score
        candidates.sort(key=lambda x: x[2], reverse=True)
        
        output += "TOP 5 CANDIDATES:\n"
        output += "─" * 60 + "\n"
        for idx, (shift, text_candidate, score) in enumerate(candidates[:5], 1):
            output += f"{idx}. [Shift {shift}] Score: {score} | {text_candidate[:40]}\n"
        
        output += "\n" + "═" * 60 + "\n"
        output += f"✓ MOST LIKELY: Shift {best_shift} (Score: {best_score})\n"
        output += "═" * 60 + "\n\n"
        output += f"DECODED MESSAGE:\n{best_text}"
        
        self.display_output(output, best_text)
    
    def display_output(self, display_text: str, result_text: str):
        """Display output in selected format"""
        format_choice = self.format_var.get()
        
        if format_choice == "bytes":
            formatted = self._format_as_bytes(result_text)
        elif format_choice == "tape":
            formatted = self._format_as_punched_tape(result_text)
        else:  # text
            formatted = display_text
        
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", formatted)
        self.last_result = result_text
    
    def _format_as_bytes(self, text: str) -> str:
        """Format text as bytes representation"""
        output = "BYTES REPRESENTATION:\n"
        output += "═" * 60 + "\n\n"
        
        for i, char in enumerate(text):
            byte_val = ord(char)
            binary = format(byte_val, '08b')
            hex_val = format(byte_val, '02x')
            output += f"[{i:3d}] Char: '{char}' | ASCII: {byte_val:3d} | "
            output += f"HEX: {hex_val} | BIN: {binary}\n"
            
            if (i + 1) % 10 == 0:
                output += "\n"
        
        return output
    
    def _format_as_punched_tape(self, text: str) -> str:
        """Format text as punched tape visualization"""
        output = "PUNCHED TAPE VISUALIZATION:\n"
        output += "═" * 60 + "\n\n"
        
        for i, char in enumerate(text):
            byte_val = ord(char)
            binary = format(byte_val, '08b')
            
            output += f"[{binary}] "
            for bit in binary:
                output += "●" if bit == "1" else "○"
            output += f" | '{char}'\n"
        
        return output
    
    def _caesar_encrypt(self, text: str, shift: int) -> str:
        """Encrypt text using Caesar cipher"""
        result = ""
        for char in text:
            if char.isalpha():
                is_upper = char.isupper()
                char = char.upper()
                char_pos = ord(char) - ord('A')
                new_pos = (char_pos + shift) % 26
                new_char = chr(new_pos + ord('A'))
                result += new_char if is_upper else new_char.lower()
            else:
                result += char
        return result
    
    def _caesar_decrypt(self, text: str, shift: int) -> str:
        """Decrypt text using Caesar cipher"""
        return self._caesar_encrypt(text, 26 - shift)
    
    def _calculate_english_score(self, text: str) -> int:
        """Score text based on English language patterns"""
        text_upper = text.upper()
        score = 0
        
        # Check for common English letter frequencies
        common_letters = "ETAOINSHRDLCUMWFGYPBVKJ"
        for letter in common_letters:
            score += text_upper.count(letter) * (26 - common_letters.index(letter))
        
        return score
    
    def _score_by_dictionary(self, text: str) -> int:
        """Score text by counting common English words"""
        words = text.lower().split()
        score = 0
        
        for word in words:
            clean_word = ''.join(c for c in word if c.isalpha())
            if clean_word in self.common_words:
                score += len(clean_word)  # Weight by word length
        
        return score
    
    def copy_output(self):
        """Copy output to clipboard"""
        try:
            output = self.output_text.get("1.0", tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            messagebox.showinfo("Success", "Output copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Copy failed: {e}")
    
    def save_output(self):
        """Save output to file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(self.output_text.get("1.0", tk.END))
                messagebox.showinfo("Success", f"Saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")
    
    def load_file(self):
        """Load text from file"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'r') as f:
                    content = f.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Load failed: {e}")
    
    def clear_all(self):
        """Clear all fields"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)


def main():
    root = tk.Tk()
    app = CaesarCipherTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()
