import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import pyperclip
import webbrowser
from datetime import datetime

from hardware import HardwareDetector
from keygen import KeyGenerator
from sms import SMSSender, SMSConfig


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class HardwareKeyGeneratorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Advance Key Generator v2.0")
        self.root.geometry("960x720")
        self.root.minsize(800, 650)

        self.center_window()

        self.hw_detector = HardwareDetector()
        self.key_gen = KeyGenerator()
        self.sms_sender = SMSSender()

        self.hardware_info = {}
        self.generated_key = ""
        self.license_type = "Standard"

        self.setup_ui()

    def center_window(self):
        self.root.update_idletasks()
        w = 960
        h = 720
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def setup_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_main_content()
        self.create_status_bar()

    def create_header(self):
        header = ctk.CTkFrame(
            self.root, height=90, corner_radius=0, fg_color="#1a1a2e"
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(expand=True, fill="both", padx=30, pady=10)

        icon_label = ctk.CTkLabel(
            title_frame,
            text="\U0001F511",
            font=ctk.CTkFont(size=32),
            text_color="#e94560",
        )
        icon_label.pack(side="left", padx=(0, 15))

        text_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True)

        title = ctk.CTkLabel(
            text_frame,
            text="Advance Key Generator",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#ffffff",
            anchor="w",
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            text_frame,
            text="Hardware-based License Key Generation System",
            font=ctk.CTkFont(size=12),
            text_color="#8899aa",
            anchor="w",
        )
        subtitle.pack(anchor="w")

        self.lock_status = ctk.CTkLabel(
            title_frame,
            text="\U0001F512",
            font=ctk.CTkFont(size=24),
            text_color="#00ff88",
        )
        self.lock_status.pack(side="right", padx=(15, 0))

        self.time_label = ctk.CTkLabel(
            title_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#667788",
        )
        self.time_label.pack(side="right", padx=(0, 10))
        self.update_time()

    def update_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=now)
        self.root.after(1000, self.update_time)

    def create_main_content(self):
        content = ctk.CTkFrame(self.root, fg_color="#16213e", corner_radius=0)
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        self.create_sidebar(content)
        self.create_workspace(content)

    def create_sidebar(self, parent):
        sidebar = ctk.CTkFrame(
            parent, width=200, corner_radius=0, fg_color="#0f3460"
        )
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        nav_title = ctk.CTkLabel(
            sidebar,
            text="NAVIGATION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#667788",
        )
        nav_title.pack(anchor="w", padx=20, pady=(20, 10))

        nav_items = [
            ("\U0001F4CA  Dashboard", 0),
            ("\U0000FE0F  Generate Key", 1),
            ("\U0001F4E8  Send SMS", 2),
            ("\U00002699  Settings", 3),
            ("\U0001F4C4  About", 4),
        ]

        self.nav_buttons = []
        for text, idx in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                text_color="#aabbcc",
                hover_color="#1a1a4e",
                anchor="w",
                height=40,
                corner_radius=8,
                command=lambda i=idx: self.switch_view(i),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons.append(btn)

        self.nav_buttons[0].configure(fg_color="#1a1a4e", text_color="#ffffff")

        sidebar_bottom = ctk.CTkFrame(sidebar, fg_color="transparent")
        sidebar_bottom.pack(side="bottom", fill="x", padx=15, pady=15)

        version_label = ctk.CTkLabel(
            sidebar_bottom,
            text="v2.0.0",
            font=ctk.CTkFont(size=10),
            text_color="#445566",
        )
        version_label.pack()

    def create_workspace(self, parent):
        self.workspace = ctk.CTkFrame(parent, fg_color="#16213e", corner_radius=0)
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.workspace.grid_columnconfigure(0, weight=1)
        self.workspace.grid_rowconfigure(0, weight=1)

        self.views = []
        self.create_dashboard_view()
        self.create_keygen_view()
        self.create_sms_view()
        self.create_settings_view()
        self.create_about_view()

        for i, view in enumerate(self.views):
            if i == 0:
                view.grid(row=0, column=0, sticky="nsew")
            else:
                view.grid_remove()

    def switch_view(self, index):
        for i, view in enumerate(self.views):
            if i == index:
                view.grid()
            else:
                view.grid_remove()

        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.configure(fg_color="#1a1a4e", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color="#aabbcc")

    def create_dashboard_view(self):
        view = ctk.CTkFrame(self.workspace, fg_color="transparent")
        view.grid_columnconfigure(0, weight=1)
        self.views.append(view)

        dash_header = ctk.CTkLabel(
            view,
            text="System Dashboard",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
        )
        dash_header.pack(anchor="w", padx=10, pady=(10, 5))

        dash_sub = ctk.CTkLabel(
            view,
            text="Hardware Information Overview",
            font=ctk.CTkFont(size=12),
            text_color="#8899aa",
        )
        dash_sub.pack(anchor="w", padx=10, pady=(0, 20))

        self.dash_cards_frame = ctk.CTkScrollableFrame(
            view, fg_color="transparent"
        )
        self.dash_cards_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.dash_cards_frame.grid_columnconfigure(1, weight=1)

        self.refresh_dashboard()

    def refresh_dashboard(self):
        for widget in self.dash_cards_frame.winfo_children():
            widget.destroy()

        info_items = [
            ("Motherboard", "\U0001F4BB", "motherboard"),
            ("RAM Module", "\U0001F4BE", "ram"),
            ("Graphics Card", "\U0001F5B5", "vga"),
            ("Hard Disk", "\U0001F4C0", "hdd"),
            ("Windows Key", "\U0001F4CB", "windows_key"),
            ("Processor", "\U00002699", "cpu"),
            ("MAC Address", "\U0001F4F6", "mac"),
        ]

        row = 0
        col = 0
        for title, icon, key in info_items:
            card = self.create_info_card(
                self.dash_cards_frame, title, icon,
                self.hardware_info.get(key, "Not Detected"),
            )
            card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            col += 1
            if col > 1:
                col = 0
                row += 1

        self.dash_cards_frame.grid_columnconfigure(0, weight=1)
        self.dash_cards_frame.grid_columnconfigure(1, weight=1)

        refresh_btn = ctk.CTkButton(
            self.dash_cards_frame,
            text="\U0001F504  Refresh Hardware Info",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#e94560",
            hover_color="#c73e54",
            height=40,
            command=self.detect_hardware_threaded,
        )
        refresh_btn.grid(
            row=row + 1, column=0, columnspan=2,
            padx=20, pady=(20, 10), sticky="ew",
        )

    def create_info_card(self, parent, title, icon, value):
        card = ctk.CTkFrame(
            parent, fg_color="#1a1a3e", corner_radius=12,
            border_width=1, border_color="#2a2a5e",
        )
        card.grid_columnconfigure(0, weight=1)

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=28),
            text_color="#e94560",
        )
        icon_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color="#8899aa",
        )
        title_label.grid(row=1, column=0, padx=15, pady=(0, 2), sticky="w")

        value_label = ctk.CTkLabel(
            card,
            text=str(value)[:40] if value else "N/A",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff",
            wraplength=200,
        )
        value_label.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="w")

        return card

    def create_keygen_view(self):
        view = ctk.CTkFrame(self.workspace, fg_color="transparent")
        view.grid_columnconfigure(0, weight=1)
        view.grid_rowconfigure(1, weight=1)
        self.views.append(view)

        header = ctk.CTkLabel(
            view,
            text="License Key Generator",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
        )
        header.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        sub = ctk.CTkLabel(
            view,
            text="Generate unique hardware-locked license keys",
            font=ctk.CTkFont(size=12),
            text_color="#8899aa",
        )
        sub.grid(row=0, column=0, padx=10, pady=(25, 20), sticky="w")

        main_frame = ctk.CTkFrame(view, fg_color="#1a1a3e", corner_radius=15)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        license_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        license_frame.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="ew")
        license_frame.grid_columnconfigure(1, weight=1)

        type_label = ctk.CTkLabel(
            license_frame,
            text="License Type:",
            font=ctk.CTkFont(size=14),
            text_color="#aabbcc",
        )
        type_label.grid(row=0, column=0, padx=(0, 15), sticky="w")

        self.license_var = ctk.StringVar(value="Standard (16 char)")
        license_menu = ctk.CTkOptionMenu(
            license_frame,
            values=["Standard (16 char)", "Enterprise (25 char)", "Trial (8 char)"],
            variable=self.license_var,
            font=ctk.CTkFont(size=13),
            fg_color="#0f3460",
            button_color="#e94560",
            button_hover_color="#c73e54",
            dropdown_fg_color="#0f3460",
            width=220,
        )
        license_menu.grid(row=0, column=1, sticky="w")

        key_display_frame = ctk.CTkFrame(
            main_frame, fg_color="#0a0a2e", corner_radius=10,
            border_width=2, border_color="#2a2a6e",
        )
        key_display_frame.grid(
            row=1, column=0, padx=30, pady=(20, 10), sticky="ew",
        )
        key_display_frame.grid_columnconfigure(0, weight=1)

        self.key_display = ctk.CTkLabel(
            key_display_frame,
            text="XXXX-XXXX-XXXX-XXXX",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00ff88",
        )
        self.key_display.grid(row=0, column=0, padx=20, pady=25)

        self.key_status = ctk.CTkLabel(
            key_display_frame,
            text="Waiting to generate...",
            font=ctk.CTkFont(size=11),
            text_color="#667788",
        )
        self.key_status.grid(row=1, column=0, padx=20, pady=(0, 15))

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=30, pady=20, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        gen_btn = ctk.CTkButton(
            btn_frame,
            text="\U00002699  Generate Key",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#e94560",
            hover_color="#c73e54",
            height=45,
            corner_radius=10,
            command=self.generate_key_threaded,
        )
        gen_btn.grid(row=0, column=0, padx=5, sticky="ew")

        copy_btn = ctk.CTkButton(
            btn_frame,
            text="\U0001F4CB  Copy Key",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0f3460",
            hover_color="#1a4a7a",
            height=45,
            corner_radius=10,
            command=self.copy_key,
        )
        copy_btn.grid(row=0, column=1, padx=5, sticky="ew")

        save_btn = ctk.CTkButton(
            btn_frame,
            text="\U0001F4BE  Save to File",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0f3460",
            hover_color="#1a4a7a",
            height=45,
            corner_radius=10,
            command=self.save_key_to_file,
        )
        save_btn.grid(row=0, column=2, padx=5, sticky="ew")

        progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        progress_frame.grid(row=3, column=0, padx=30, pady=(0, 25), sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(
            progress_frame, height=6, corner_radius=3,
            fg_color="#0f3460", progress_color="#00ff88",
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew")
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color="#556677",
        )
        self.progress_label.grid(row=1, column=0, pady=(5, 0), sticky="ew")

    def create_sms_view(self):
        view = ctk.CTkFrame(self.workspace, fg_color="transparent")
        view.grid_columnconfigure(0, weight=1)
        self.views.append(view)

        header = ctk.CTkLabel(
            view,
            text="Send Key via SMS",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
        )
        header.pack(anchor="w", padx=10, pady=(10, 5))

        sub = ctk.CTkLabel(
            view,
            text="Send generated license key to any mobile number",
            font=ctk.CTkFont(size=12),
            text_color="#8899aa",
        )
        sub.pack(anchor="w", padx=10, pady=(0, 20))

        main_card = ctk.CTkFrame(
            view, fg_color="#1a1a3e", corner_radius=15,
            border_width=1, border_color="#2a2a5e",
        )
        main_card.pack(fill="both", expand=True, padx=20, pady=10)

        content = ctk.CTkFrame(main_card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        content.grid_columnconfigure(1, weight=1)

        row = 0
        ctk.CTkLabel(
            content,
            text="SMS Provider:",
            font=ctk.CTkFont(size=14),
            text_color="#aabbcc",
        ).grid(row=row, column=0, padx=(0, 15), pady=10, sticky="w")

        self.provider_var = ctk.StringVar(value="TextBelt")
        provider_menu = ctk.CTkOptionMenu(
            content,
            values=["TextBelt", "Fast2SMS"],
            variable=self.provider_var,
            font=ctk.CTkFont(size=13),
            fg_color="#0f3460",
            button_color="#e94560",
            button_hover_color="#c73e54",
            dropdown_fg_color="#0f3460",
            width=200,
            command=self.on_provider_change,
        )
        provider_menu.grid(row=row, column=1, padx=5, pady=10, sticky="w")

        row += 1
        self.api_key_label = ctk.CTkLabel(
            content,
            text="API Key:",
            font=ctk.CTkFont(size=14),
            text_color="#aabbcc",
        )
        self.api_key_label.grid(row=row, column=0, padx=(0, 15), pady=10, sticky="w")

        self.api_key_entry = ctk.CTkEntry(
            content,
            placeholder_text="Enter API key (if required)",
            font=ctk.CTkFont(size=13),
            fg_color="#0a0a2e",
            border_color="#2a2a5e",
            height=38,
        )
        self.api_key_entry.grid(row=row, column=1, padx=5, pady=10, sticky="ew")
        self.api_key_entry.configure(state="disabled")

        row += 1
        ctk.CTkLabel(
            content,
            text="Phone Number:",
            font=ctk.CTkFont(size=14),
            text_color="#aabbcc",
        ).grid(row=row, column=0, padx=(0, 15), pady=10, sticky="w")

        phone_frame = ctk.CTkFrame(content, fg_color="transparent")
        phone_frame.grid(row=row, column=1, padx=5, pady=10, sticky="ew")
        phone_frame.grid_columnconfigure(1, weight=1)

        code_label = ctk.CTkLabel(
            phone_frame,
            text="+91",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00ff88",
        )
        code_label.grid(row=0, column=0, padx=(0, 5))

        self.phone_entry = ctk.CTkEntry(
            phone_frame,
            placeholder_text="9876543210",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#0a0a2e",
            border_color="#2a2a5e",
            height=42,
        )
        self.phone_entry.grid(row=0, column=1, sticky="ew")

        row += 1
        ctk.CTkLabel(
            content,
            text="Message:",
            font=ctk.CTkFont(size=14),
            text_color="#aabbcc",
        ).grid(row=row, column=0, padx=(0, 15), pady=10, sticky="w")

        self.sms_message = ctk.CTkTextbox(
            content,
            height=100,
            font=ctk.CTkFont(size=13),
            fg_color="#0a0a2e",
            border_color="#2a2a5e",
            corner_radius=8,
        )
        self.sms_message.grid(row=row, column=1, padx=5, pady=10, sticky="ew")
        self.sms_message.insert(
            "1.0",
            "Your license key is: XXXX-XXXX-XXXX-XXXX\n\nGenerated by Advance Key Generator",
        )

        row += 1
        self.send_btn = ctk.CTkButton(
            content,
            text="\U0001F4E8  Send SMS",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#e94560",
            hover_color="#c73e54",
            height=45,
            corner_radius=10,
            command=self.send_sms_threaded,
        )
        self.send_btn.grid(
            row=row, column=0, columnspan=2, padx=5, pady=(25, 10), sticky="ew",
        )

        self.sms_status = ctk.CTkLabel(
            content,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#8899aa",
        )
        self.sms_status.grid(
            row=row + 1, column=0, columnspan=2, pady=(0, 10),
        )

    def create_settings_view(self):
        view = ctk.CTkFrame(self.workspace, fg_color="transparent")
        view.grid_columnconfigure(0, weight=1)
        self.views.append(view)

        header = ctk.CTkLabel(
            view,
            text="Settings",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff",
        )
        header.pack(anchor="w", padx=10, pady=(10, 20))

        card = ctk.CTkFrame(
            view, fg_color="#1a1a3e", corner_radius=15,
            border_width=1, border_color="#2a2a5e",
        )
        card.pack(fill="both", expand=True, padx=20, pady=10)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        content.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            content,
            text="Appearance:",
            font=ctk.CTkFont(size=14),
            text_color="#aabbcc",
        ).grid(row=0, column=0, padx=(0, 15), pady=10, sticky="w")

        theme_var = ctk.StringVar(value="Dark")
        theme_menu = ctk.CTkOptionMenu(
            content,
            values=["Dark", "Light", "System"],
            variable=theme_var,
            font=ctk.CTkFont(size=13),
            fg_color="#0f3460",
            button_color="#e94560",
            width=150,
            command=self.change_theme,
        )
        theme_menu.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(
            content,
            text="Color Theme:",
            font=ctk.CTkFont(size=14),
            text_color="#aabbcc",
        ).grid(row=1, column=0, padx=(0, 15), pady=10, sticky="w")

        color_var = ctk.StringVar(value="dark-blue")
        color_menu = ctk.CTkOptionMenu(
            content,
            values=["dark-blue", "blue", "green", "teal"],
            variable=color_var,
            font=ctk.CTkFont(size=13),
            fg_color="#0f3460",
            button_color="#e94560",
            width=150,
        )
        color_menu.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(
            content,
            text="Key Backup Directory:",
            font=ctk.CTkFont(size=14),
            text_color="#aabbcc",
        ).grid(row=2, column=0, padx=(0, 15), pady=10, sticky="w")

        dir_frame = ctk.CTkFrame(content, fg_color="transparent")
        dir_frame.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
        dir_frame.grid_columnconfigure(0, weight=1)

        self.dir_entry = ctk.CTkEntry(
            dir_frame,
            text="D:\\VsCode\\Advance_Key_Gen\\keys",
            font=ctk.CTkFont(size=12),
            fg_color="#0a0a2e",
            border_color="#2a2a5e",
            height=35,
        )
        self.dir_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        browse_btn = ctk.CTkButton(
            dir_frame,
            text="Browse",
            font=ctk.CTkFont(size=12),
            fg_color="#0f3460",
            hover_color="#1a4a7a",
            width=80,
            height=35,
            command=self.browse_directory,
        )
        browse_btn.grid(row=0, column=1)

    def create_about_view(self):
        view = ctk.CTkFrame(self.workspace, fg_color="transparent")
        view.grid_columnconfigure(0, weight=1)
        self.views.append(view)

        card = ctk.CTkFrame(
            view, fg_color="#1a1a3e", corner_radius=15,
            border_width=1, border_color="#2a2a5e",
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=40)

        ctk.CTkLabel(
            content,
            text="\U0001F511",
            font=ctk.CTkFont(size=64),
            text_color="#e94560",
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            content,
            text="Advance Key Generator",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff",
        ).pack()

        ctk.CTkLabel(
            content,
            text="Version 2.0.0",
            font=ctk.CTkFont(size=14),
            text_color="#8899aa",
        ).pack(pady=(5, 20))

        desc = (
            "A professional hardware-based license key generation system.\n"
            "Generates unique, secure keys based on your PC's hardware fingerprint.\n\n"
            "Hardware Sources:\n"
            "\U0001F4BB  Motherboard Serial Number\n"
            "\U0001F4BE  RAM Module Serial Number\n"
            "\U0001F5B5  Graphics Card Identifier\n"
            "\U0001F4C0  Hard Disk Serial Number\n"
            "\U0001F4CB  Windows Product Key\n"
            "\U00002699  CPU Processor ID\n"
            "\U0001F4F6  MAC Address"
        )

        ctk.CTkLabel(
            content,
            text=desc,
            font=ctk.CTkFont(size=13),
            text_color="#aabbcc",
            justify="center",
        ).pack(pady=10)

        ctk.CTkLabel(
            content,
            text="\u00A9 2024 Advance Key Generator. All rights reserved.",
            font=ctk.CTkFont(size=11),
            text_color="#556677",
        ).pack(pady=(30, 5))

    def on_provider_change(self, choice):
        if choice == "TextBelt":
            self.api_key_label.configure(text_color="#556677")
            self.api_key_entry.configure(state="disabled", placeholder_text="Not required for TextBelt")
        else:
            self.api_key_label.configure(text_color="#aabbcc")
            self.api_key_entry.configure(state="normal", placeholder_text="Enter your Fast2SMS API key")

    def detect_hardware_threaded(self):
        threading.Thread(target=self._detect_hardware, daemon=True).start()

    def _detect_hardware(self):
        try:
            self.root.after(0, lambda: self.set_status("Detecting hardware..."))
            self.hardware_info = self.hw_detector.get_all_info()
            self.root.after(0, self.refresh_dashboard)
            self.root.after(0, lambda: self.set_status("Hardware detected successfully"))
        except Exception as e:
            self.root.after(0, lambda: self.set_status(f"Error: {str(e)}"))

    def generate_key_threaded(self):
        threading.Thread(target=self._generate_key, daemon=True).start()

    def _generate_key(self):
        try:
            self.root.after(0, lambda: self.progress_bar.set(0.2))
            self.root.after(0, lambda: self.progress_label.configure(text="Detecting hardware..."))
            self.root.after(0, lambda: self.key_status.configure(text="Scanning hardware..."))

            if not self.hardware_info:
                self.hardware_info = self.hw_detector.get_all_info()

            self.root.after(0, lambda: self.progress_bar.set(0.5))
            self.root.after(0, lambda: self.progress_label.configure(text="Generating key..."))
            self.root.after(0, lambda: self.key_status.configure(text="Generating secure key..."))

            license_type = self.license_var.get()
            if "25" in license_type:
                key = self.key_gen.generate_activation_code(self.hardware_info)
            elif "8" in license_type:
                key = self.key_gen.generate_key(self.hardware_info, 8)
            else:
                key = self.key_gen.generate_license_key(self.hardware_info)

            self.generated_key = key

            self.root.after(0, lambda: self.progress_bar.set(1.0))
            self.root.after(0, lambda: self.key_display.configure(text=key))
            self.root.after(0, lambda: self.key_status.configure(
                text=f"\u2705 Key generated successfully | {license_type}",
            ))
            self.root.after(0, lambda: self.progress_label.configure(
                text="Key generated successfully!",
            ))

            sms_msg = self.sms_message.get("1.0", "end-1c")
            if "XXXX" in sms_msg or not sms_msg.strip():
                default_msg = (
                    f"Your license key is: {key}\n\n"
                    f"Generated by Advance Key Generator"
                )
                self.root.after(0, lambda: (
                    self.sms_message.delete("1.0", "end"),
                    self.sms_message.insert("1.0", default_msg),
                ))

            self.root.after(0, lambda: self.set_status("Key generated successfully"))

        except Exception as e:
            self.root.after(0, lambda: self.progress_bar.set(0))
            self.root.after(0, lambda: self.key_status.configure(
                text=f"\u274c Error: {str(e)[:50]}",
            ))
            self.root.after(0, lambda: self.progress_label.configure(text="Generation failed"))
            self.root.after(0, lambda: self.set_status(f"Error: {str(e)[:50]}"))

    def copy_key(self):
        if self.generated_key:
            pyperclip.copy(self.generated_key)
            self.set_status("Key copied to clipboard!")
            self.key_status.configure(text="\u2705 Key copied to clipboard")
        else:
            messagebox.showwarning("No Key", "Generate a key first!")

    def save_key_to_file(self):
        if not self.generated_key:
            messagebox.showwarning("No Key", "Generate a key first!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"license_key_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write("=" * 50 + "\n")
                    f.write("ADVANCE KEY GENERATOR - LICENSE KEY\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"License Key: {self.generated_key}\n")
                    f.write(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"License Type: {self.license_var.get()}\n\n")
                    f.write("-" * 50 + "\n")
                    f.write("Hardware Fingerprint:\n")
                    for k, v in self.hardware_info.items():
                        f.write(f"  {k}: {v}\n")
                    f.write("-" * 50 + "\n")
                self.set_status(f"Key saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def send_sms_threaded(self):
        threading.Thread(target=self._send_sms, daemon=True).start()

    def _send_sms(self):
        try:
            phone = self.phone_entry.get().strip()
            if not phone:
                self.root.after(0, lambda: self.sms_status.configure(
                    text="\u274c Please enter a phone number",
                    text_color="#e94560",
                ))
                return

            message = self.sms_message.get("1.0", "end-1c").strip()
            if not message:
                self.root.after(0, lambda: self.sms_status.configure(
                    text="\u274c Please enter a message",
                    text_color="#e94560",
                ))
                return

            if "XXXX" in message and self.generated_key:
                message = message.replace("XXXX-XXXX-XXXX-XXXX", self.generated_key)
                message = message.replace("XXXX-XXXX-XXXX", self.generated_key)
                message = message.replace("XXXX-XXXX", self.generated_key)
                message = message.replace("XXXX", self.generated_key)

            provider = self.provider_var.get()
            api_key = self.api_key_entry.get().strip()

            self.sms_sender.set_provider(provider, api_key)

            self.root.after(0, lambda: self.send_btn.configure(
                text="\U0001F4E4  Sending...", state="disabled",
            ))
            self.root.after(0, lambda: self.sms_status.configure(
                text="\U0001F504 Sending SMS...", text_color="#ffcc00",
            ))

            result = self.sms_sender.send_sms(phone, message)

            self.root.after(0, lambda: self.send_btn.configure(
                text="\U0001F4E8  Send SMS", state="normal",
            ))

            if result.get("success"):
                self.root.after(0, lambda: self.sms_status.configure(
                    text="\u2705 SMS sent successfully!", text_color="#00ff88",
                ))
                self.root.after(0, lambda: self.set_status(f"SMS sent to {phone}"))
            else:
                error = result.get("error", result.get("response", {}).get("error", "Unknown error"))
                self.root.after(0, lambda e=error: self.sms_status.configure(
                    text=f"\u274c Failed: {e}", text_color="#e94560",
                ))

        except Exception as e:
            self.root.after(0, lambda: self.send_btn.configure(
                text="\U0001F4E8  Send SMS", state="normal",
            ))
            self.root.after(0, lambda: self.sms_status.configure(
                text=f"\u274c Error: {str(e)[:60]}", text_color="#e94560",
            ))

    def change_theme(self, choice):
        mode = choice.lower()
        ctk.set_appearance_mode(mode)

    def browse_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, path)

    def create_status_bar(self):
        status_bar = ctk.CTkFrame(self.root, height=30, corner_radius=0, fg_color="#0a0a1e")
        status_bar.grid(row=2, column=0, sticky="ew")
        status_bar.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            status_bar,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color="#556677",
        )
        self.status_label.pack(side="left", padx=15)

        status_icon = ctk.CTkLabel(
            status_bar,
            text="\u25CF System Online",
            font=ctk.CTkFont(size=10),
            text_color="#00ff88",
        )
        status_icon.pack(side="right", padx=15)

    def set_status(self, message):
        self.status_label.configure(text=message)

    def run(self):
        threading.Thread(target=self._initial_detect, daemon=True).start()
        self.root.mainloop()

    def _initial_detect(self):
        self.root.after(0, lambda: self.set_status("Detecting hardware..."))
        try:
            self.hardware_info = self.hw_detector.get_all_info()
            self.root.after(0, self.refresh_dashboard)
            self.root.after(0, lambda: self.set_status("Ready - Hardware detected"))
        except Exception as e:
            self.root.after(0, lambda: self.set_status(f"Hardware detection: {str(e)[:40]}"))


if __name__ == "__main__":
    app = HardwareKeyGeneratorApp()
    app.run()
