import os
import subprocess
import webbrowser
import psutil
import random
import platform
import speech_recognition as sr
from datetime import datetime
from googleapiclient.discovery import build
import threading
import queue
import keyboard

class ArciaAI:
    def __init__(self):
        self.response = {
            "greeting": ["Hello, I'm Arcia your text based assisstant! How can I assist you today?"],
            "thank_you": ["You're welcome! Is there anything else I can help you with?"],
            "exit": ["Exiting the AI program. See you next time!"],
            "bantuan": ["Perintah yang tersedia:\n"
                        "- Buka aplikasi [nama aplikasi]\n"
                        "- Buka website [URL]\n"
                        "- Mainkan video [judul video] di YouTube\n"
                        "- Mainkan video [judul video] dari channel [channel] di youtube\n"
                        "- Pantau sistem (CPU, RAM, Disk)\n"
                        "- Keluar (untuk keluar dari program)\n"
                        "- Halo, Hai, Selamat Pagi, Selamat Siang, Selamat Sore, Selamat Malam (untuk menyapa)\n"
                        "- Terima kasih (untuk mengucapkan terima kasih)\n"]
        }
        # flags and communication
        self.command_queue = queue.Queue()
        self.text_mode = threading.Event()   # when set -> text mode active
        self.stop_event = threading.Event()  # when set -> shutdown all threads
        self.mic_ok = threading.Event()
        self.mic_ok.set()
    
    def parse_command(self, command: str):
        command = command.lower()
        # allow explicit mode switching via speech/text
        if command.strip() in ["mode text", "mode teks", "text mode", "teks mode"]:
            self.text_mode.set()
            return "Beralih ke MODE TEXT. Ketik perintah Anda."
        if command.strip() in ["mode voice", "voice mode", "mode suara"]:
            self.text_mode.clear()
            return "Beralih ke MODE VOICE. Mendengarkan..."
        # Simple command parsing
        if "buka aplikasi" in command:
            app_name = command.split("buka aplikasi", 1)[-1].strip()
            return self.open_app(app_name)
        elif "buka web" in command:
            url = command.split("buka web ")[-1].strip()
            return self.open_website(url)
        if "mainkan video" in command and "youtube" in command:
            if "dari channel" in command:  # Check if channel is specified
                parts = command.split("dari channel")
                video_part = parts[0].replace("mainkan video", "").strip()
                channel_part = parts[1].replace("di youtube", "").strip()
                return self.play_youtube_video(video_part, channel_part)
            else:
                query = command.split("mainkan video")[-1].replace("di youtube", "").strip()
                return self.play_youtube_video(query)
        elif "pantau sistem" in command or "monitor sistem" in command:
            return self.monitor_system()
        elif "keluar" in command or "exit" in command or "quit" in command:
            self.stop_event.set()
            return random.choice(self.response["exit"])
        elif any(word in command for word in ["halo", "hai", "selamat pagi", "selamat siang", "selamat sore", "selamat malam"]):
            return random.choice(self.response["greeting"])
        elif "bantuan" in command or "help" in command:
            return random.choice(self.response["bantuan"])
        elif "terima kasih" in command:
            return random.choice(self.response["thank_you"])
        else:
            return "Perintah tidak dikenali. Coba ketik 'bantuan'."
    
    #Listen for commands to open applications or websites
    def voice_listener_thread(self):
        r = sr.Recognizer()
        while not self.stop_event.is_set():
            if self.text_mode.is_set():
                # don't touch mic while in text mode; wait until mode changes
                threading.Event().wait(0.5)
                continue
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    print("Voice listener: aktif, mendengarkan perintah...")
                    while not self.stop_event.is_set() and not self.text_mode.is_set():
                        try:
                            audio = r.listen(source, phrase_time_limit=6)
                            try:
                                text = r.recognize_google(audio, language="id-ID").lower().strip()
                            except sr.UnknownValueError:
                                continue
                            except sr.RequestError as e:
                                print(f"Voice listener: RequestError {e}. Switching to text mode.")
                                self.mic_ok.clear()
                                self.text_mode.set()
                                break

                            # if in text mode, only honor voice->voice-mode command
                            if self.text_mode.is_set():
                                if text in ["mode voice", "voice mode", "mode suara"]:
                                    self.command_queue.put(text)
                                continue

                            # push recognized voice command
                            self.command_queue.put(text)

                        except OSError as e:
                            # hardware/stream error -> switch to text mode and wait before retry
                            print(f"Voice listener: microphone error: {e}. Switching to text mode.")
                            self.mic_ok.clear()
                            self.text_mode.set()
                            break
            except Exception as e:
                # Could not open microphone (device missing/disconnected) -> go to text mode and wait
                print(f"Voice listener gagal start atau device hilang: {e}. Memaksa mode text sementara.")
                self.mic_ok.clear()
                self.text_mode.set()
                # avoid busy-loop: sleep a bit before retrying
                threading.Event().wait(2)
        # exit thread
        print("Voice listener: terminated.")
                
    def open_app(self, app_name: str):
        app_paths = {
            "7zip": "C:\\Program Files\\7-Zip\\7zFM.exe",
            "notepad": "C:\\Windows\\System32\\notepad.exe",
            "calculator": "C:\\Windows\\System32\\calc.exe",
            "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "steam": "C:\\Program Files (x86)\\Steam\\steam.exe",
            "file explorer": "C:\\Windows\\explorer.exe",
            #"whatsapp": "C:\\Users\\Public\\Desktop\\WhatsApp.lnk",
            "task manager": "C:\\Windows\\System32\\taskmgr.exe",
            #"settings": "C:\\Windows\\System32\\ms-settings:app",
            "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
            "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
            "rainmeter": "D:\\Wallpaper & Utility\\Rainmeter\\Rainmeter.exe",
            "zoom": "C:\\Program Files\\Zoom\\bin\\Zoom.exe",
            "camera": "C:\\Windows\\System32\\Camera.exe",
            "vs code": "C:\\Program Files\\Microsoft VS Code\\Code.exe",
            "clock": "C:\\Windows\\System32\\Clock.exe",
            "calendar": "C:\\Windows\\System32\\Calendar.exe",
            "copilot": "C:\\Program Files\\Microsoft\\Copilot\\Copilot.exe",
            "vlc media player": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
            "notepad++": "C:\\Program Files\\Notepad++\\notepad++.exe",
            "microsoft edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "microsoft teams": "C:\\Users\\arman\\AppData\\Local\\Microsoft\\Teams\\Update.exe",
            "grass": "D:\\Grass\\Grass.exe",
            "mining": "D:\\Uprock\\Uprock.exe",
            "BlueStacks": "D:\\Games\\BlueStacks\\BlueStacks.exe",
            "cmd": "C:\\Windows\\System32\\cmd.exe",
            "epic games": "C:\\Program Files\\Epic Games\\Launcher\\Portal\\Binaries\\Win64\\EpicGamesLauncher.exe",
            "drive": "C:\\Program Files\\Google\\Drive File Stream\\GoogleDriveFS.exe",
            "Honkai Impact": "D:\\games\\Honkai Impact 3rd\\HonkaiImpact3.exe",
            "GeforceNow": "C:\\Program Files\\NVIDIA Corporation\\NVIDIA GeForce NOW\\GeForceNOW.exe",
            "microsoft store": "C:\\Windows\\System32\\WinStore.App.exe",
            "osu": "D:\\games\\osu\\osu!.exe",
            "osulazer": "C:\\Users\\arman\\AppData\\Local\\osulazer\\current\\osu!.exe",
            "winrar": "C:\\Program Files\\WinRAR\\WinRAR.exe",
            "vpn": "C:\\Program Files\\Proton\\VPN\\ProtonVPN.Launcher.exe",
        }
        if app_name in app_paths:
            subprocess.Popen(app_paths[app_name])
            return f"Membuka aplikasi {app_name}."
        else:
            return f"Aplikasi {app_name} tidak ditemukan. Pastikan nama aplikasi benar."
    
    def open_website(self, url: str):
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        url = url.replace(" ", "")
        try:
            webbrowser.open(url)
            return f"Membuka website {url}"      
        except Exception as e:
            return f"Gagal membuka website {url}. Error: {str(e)}"
    
    def play_youtube_video(self, query: str, channel: str = None):
        
        API_KEY = "AIzaSyD8vjBett9APr_xbNbj24b8sunZ8I2RpSg"
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        try:
            if channel:
                full_query = f"{query} channel {channel}"
            else:
                full_query = query
            
            search_response = youtube.search().list(
                q=full_query,
                part='snippet',
                maxResults=1,
                type='video'
            ).execute()
            
            if search_response["items"]:
                video_id = search_response["items"][0]["id"]["videoId"]
                video_title = search_response["items"][0]["snippet"]["title"]
                video_url = f"https://www.youtube.com/watch?v={video_id}&autoplay=1"

                # Membuka URL di browser default
                print(f"Memutar video: {video_title}")
                webbrowser.open(video_url)
                return f"Memutar video '{video_title}' di YouTube..."
            else:
                return f"Tidak ditemukan video dengan judul '{full_query}'."

        except Exception as e:
            return f"Gagal memutar video di YouTube. Error: {str(e)}"    
    
    def monitor_system(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        info_header = "Berikut adalah informasi sistem saat ini:\n"
        system_info = {
            "CPU Usage": f"{cpu_usage}%",
            "Memory Usage": f"{memory_info.percent}%",
            "Disk Usage": f"{disk_info.percent}%"
        }
        return info_header + "\n".join([f"{key}: {value}" for key, value in system_info.items()])

#Main loop
if __name__ == "__main__":
    ai = ArciaAI()
    print("Arcia is ready. Type/Speech 'bantuan/Help' for available commands.")
    print(f"{ai.response['greeting'][0]}\n")
    
    try:
        keyboard.add_hotkey('ctrl+shift+t', lambda: (ai.text_mode.set(), print("Hotkey: MODE TEXT aktif")))
        keyboard.add_hotkey('ctrl+shift+o', lambda: (ai.text_mode.clear(), print("Hotkey: MODE VOICE aktif")))
    except Exception as e:
        print(f"Hotkey tidak terpasang: {e}. Anda masih bisa mengetik 'mode text' atau ucap 'mode text' jika mic aktif.")

    # start voice listener thread
    listener_thread = threading.Thread(target=ai.voice_listener_thread, daemon=True)
    listener_thread.start()

    try:
        while not ai.stop_event.is_set():
            # if there is a queued voice command, process it
            try:
                voice_cmd = ai.command_queue.get(timeout=0.5)
            except queue.Empty:
                voice_cmd = None

            if voice_cmd:
                print(f"Anda (voice): {voice_cmd}")
                resp = ai.parse_command(voice_cmd)
                print(f"Arcia: {resp}")
                if ai.stop_event.is_set():
                    break
                continue

            # if in text mode, accept keyboard input (blocking until user types)
            if ai.text_mode.is_set():
                try:
                    cmd = input("Anda (text): ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("Interupsi. Keluar.")
                    ai.stop_event.set()
                    break

                if not cmd:
                    continue
                # allow typing to switch back
                if cmd.lower() in ["mode voice", "voice mode", "mode suara"]:
                    ai.text_mode.clear()
                    print("Arcia: Beralih ke MODE VOICE.")
                    continue

                # process typed command
                resp = ai.parse_command(cmd)
                print(f"Arcia: {resp}")
                if ai.stop_event.is_set():
                    break

            else:
                # not in text mode and no voice command -> short sleep to avoid busy loop
                threading.Event().wait(0.2)

    except KeyboardInterrupt:
        ai.stop_event.set()

    # cleanup
    ai.stop_event.set()
    print("Arcia: shutting down...")
    listener_thread.join(timeout=2)
    print("Arcia: exited.")