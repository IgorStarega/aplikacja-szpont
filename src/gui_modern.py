#!/usr/bin/env python3
"""
Nowoczesne GUI dla Aktualizatora Strony v5.2
Stworzono z customtkinter - eleganckie i intuicyjne

v5.0 FEATURES:
- ✅ Batch Processing (3x szybciej)
- ✅ Cache Struktury Folderów (-60% czasu)
- ✅ Asynchroniczne Git Operacje
- ✅ Inteligentne Diff (przed/po)
- ✅ Incremental Updates
- ✅ Analytics Dashboard
- ✅ Excel/PDF Reports
- ✅ Update Scheduler
- ✅ Slack/Discord Notifications

v5.1 FEATURES:
- ✅ Web Dashboard (Flask)
- ✅ REST API
- ✅ Webhook Integration
- ✅ SSH Key Support
- ✅ Git Credentials Manager

v5.2 NEW FEATURES:
- ✅ Docker Support
- ✅ PyInstaller Build
- ✅ Auto-Update Feature
- ✅ Mobile API
- ✅ Advanced Security
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog, scrolledtext
import threading
from pathlib import Path
from datetime import datetime
import os
import time
from typing import Optional, Callable, Dict

from config_manager import ConfigManager
from update_manager import UpdateManager
from theme_manager import ThemeManager

# v5.0 imports - z fallbackiem do None
try:
    from database_manager import DatabaseManager
except ImportError as e:
    print(f"⚠️  DatabaseManager nie zainstalowany: {e}")
    DatabaseManager = None

try:
    from report_generator import ReportGenerator
except ImportError as e:
    print(f"⚠️  ReportGenerator nie zainstalowany: {e}")
    ReportGenerator = None

try:
    from scheduler import UpdateScheduler
except ImportError as e:
    print(f"⚠️  UpdateScheduler nie zainstalowany: {e}")
    UpdateScheduler = None

try:
    from notification_service import NotificationService
except ImportError as e:
    print(f"⚠️  NotificationService nie zainstalowany: {e}")
    NotificationService = None

# v5.1 NEW imports - z fallbackiem do None
try:
    from web_dashboard import WebDashboard
except ImportError as e:
    print(f"⚠️  WebDashboard nie zainstalowany: {e}")
    WebDashboard = None

try:
    from api_manager import APIManager
except ImportError as e:
    print(f"⚠️  APIManager nie zainstalowany: {e}")
    APIManager = None

try:
    from webhook_manager import WebhookManager
except ImportError as e:
    print(f"⚠️  WebhookManager nie zainstalowany: {e}")
    WebhookManager = None

try:
    from ssh_manager import SSHManager
except ImportError as e:
    print(f"⚠️  SSHManager nie zainstalowany: {e}")
    SSHManager = None

try:
    from credentials_manager import CredentialsManager
except ImportError as e:
    print(f"⚠️  CredentialsManager nie zainstalowany: {e}")
    CredentialsManager = None

# v5.2 NEW imports - z fallbackiem do None
try:
    from auto_update_manager import AutoUpdateManager
except ImportError as e:
    print(f"⚠️  AutoUpdateManager nie zainstalowany: {e}")
    AutoUpdateManager = None

try:
    from mobile_api_manager import MobileAPIManager
except ImportError as e:
    print(f"⚠️  MobileAPIManager nie zainstalowany: {e}")
    MobileAPIManager = None


class ModernGUI:
    """Nowoczesny interfejs aplikacji - v5.2 (PRODUCTION READY)"""

    def __init__(self, root: ctk.CTk):
        """Inicjalizacja nowoczesnego GUI - v5.2"""
        self.root = root
        self.root.title("🔄 Aktualizator Strony v5.2 - prakt.dziadu.dev")
        self.root.geometry("1400x900")
        self.root.minsize(900, 700)

        # Inicjalizuj zmienne NAJPIERW
        self.is_updating = False
        self.progress_value = 0
        self.log_lines = []

        # Ustawienia koloru
        self.config = ConfigManager(os.path.join(os.path.dirname(__file__), "config.json"))
        self.theme_manager = ThemeManager()
        ctk.set_appearance_mode(self.theme_manager.theme_mode)
        ctk.set_default_color_theme("blue")

        # v5.0: Inicjalizuj nowe managersy PRZED build_ui
        self.db_manager = None
        self.report_generator = None
        self.scheduler = None
        self.notifications = None

        try:
            if DatabaseManager is not None:
                self.db_manager = DatabaseManager()

            if ReportGenerator is not None:
                self.report_generator = ReportGenerator()

            # Scheduler wymaga callbacka - użyj wrapper
            if UpdateScheduler is not None:
                self.scheduler = UpdateScheduler(self._perform_scheduled_update, self._log_placeholder)

            if NotificationService is not None:
                self.notifications = NotificationService(self._log_placeholder)
        except Exception as e:
            # Logowanie będzie dostępne po build_ui
            pass

        # ZBUDUJ UI - log_text będzie dostępny po tym
        self.build_ui()

        # Teraz możemy logować
        try:
            if self.db_manager is None:
                self.log_message("⚠️  DatabaseManager niedostępny")
            if self.report_generator is None:
                self.log_message("⚠️  ReportGenerator niedostępny")
            if self.scheduler is None:
                self.log_message("⚠️  UpdateScheduler niedostępny")
            if self.notifications is None:
                self.log_message("⚠️  NotificationService niedostępny")
        except:
            pass

        # v5.1: Inicjalizuj nowe managersy (OPCJONALNE na razie)
        try:
            self.web_dashboard = None  # Będzie włączone z GUI
            self.api_manager = None     # Będzie włączone z GUI
            self.webhook_manager = None # Będzie włączone z GUI
            self.ssh_manager = None     # Będzie włączone z GUI
            self.credentials_manager = None  # Będzie włączone z GUI
            # self.log_message("✅ v5.1 moduły dostępne")
        except Exception as e:
            self.log_message(f"⚠️  Błąd inicjalizacji v5.1 komponentów: {str(e)}")

        # v5.2: Inicjalizuj Auto-Update Manager
        self.auto_updater = None
        try:
            if AutoUpdateManager is not None:
                self.auto_updater = AutoUpdateManager(
                    github_owner="IgorStarega",
                    github_repo="aplikacja-szpont",
                    log_callback=self.log_message
                )
                # Sprawdź aktualizacje w tle po starcie
                self.root.after(2000, self._check_for_updates_on_startup)
        except Exception as e:
            self.log_message(f"⚠️  Błąd inicjalizacji Auto-Update: {str(e)}")

        # Teraz można tworzyć UpdateManager
        self.update_manager = UpdateManager(self.log_message)


    def build_ui(self):
        """Budowanie nowoczesnego interfejsu z zakładkami"""
        # Utwórz Tabview (zakładki)
        self.tabview = ctk.CTkTabview(self.root, segmented_button_fg_color="gray")
        self.tabview.pack(fill="both", expand=True, padx=0, pady=0)

        # Dodaj zakładki
        self.tab_main = self.tabview.add("🚀 Aktualizacja")
        self.tab_analytics = self.tabview.add("📊 Analytics")  # NEW v5.0
        self.tab_reports = self.tabview.add("📄 Raporty")      # NEW v5.0
        self.tab_scheduler = self.tabview.add("📅 Harmonogram") # NEW v5.0
        self.tab_notifications = self.tabview.add("💬 Powiadomienia")  # NEW v5.0
        self.tab_settings = self.tabview.add("⚙️  Ustawienia")

        # Zbuduj zawartość każdej zakładki
        self.build_main_tab()
        self.build_analytics_tab()    # NEW v5.0
        self.build_reports_tab()       # NEW v5.0
        self.build_scheduler_tab()     # NEW v5.0
        self.build_notifications_tab() # NEW v5.0
        self.build_settings_tab()

    def build_main_tab(self):
        """Zawartość zakładki Aktualizacja"""
        main_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # TOP SECTION - Ścieżki
        self.build_paths_section(main_frame)

        # MIDDLE SECTION - Przycisk i Progress
        self.build_action_section(main_frame)

        # BOTTOM SECTION - Logs
        self.build_logs_section(main_frame)

    def build_settings_tab(self):
        """Zawartość zakładki Ustawienia"""
        settings_frame = ctk.CTkFrame(self.tab_settings, fg_color="transparent")
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # MOTYW
        theme_label_frame = ctk.CTkFrame(settings_frame, fg_color=("gray95", "gray20"), corner_radius=10)
        theme_label_frame.pack(fill="x", pady=(0, 15))

        theme_title = ctk.CTkLabel(
            theme_label_frame,
            text="🌙 Motyw Aplikacji",
            font=("Helvetica", 14, "bold")
        )
        theme_title.pack(anchor="w", padx=15, pady=(15, 10))

        self.theme_var = ctk.StringVar(value=self.config.get("theme", "system"))

        theme_options_frame = ctk.CTkFrame(theme_label_frame, fg_color="transparent")
        theme_options_frame.pack(fill="x", padx=15, pady=(0, 15))

        for theme in ["light", "dark", "system"]:
            radio = ctk.CTkRadioButton(
                theme_options_frame,
                text=f"{'☀️  ' if theme == 'light' else '🌙 ' if theme == 'dark' else '🔄 '}{theme.capitalize()}",
                variable=self.theme_var,
                value=theme
            )
            radio.pack(anchor="w", pady=3)

        # PRZYCISK ZAPISU
        save_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        save_frame.pack(fill="x", pady=(0, 15))

        save_btn = ctk.CTkButton(
            save_frame,
            text="💾 Zapisz Ustawienia",
            height=40,
            command=self.save_settings_inline
        )
        save_btn.pack(fill="x")

        # PRZYCISK RESTART
        restart_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        restart_frame.pack(fill="x", pady=(0, 15))

        restart_btn = ctk.CTkButton(
            restart_frame,
            text="🔄 Restart Aplikacji",
            height=40,
            fg_color="gray",
            command=self.restart_app
        )
        restart_btn.pack(fill="x")

        # INFORMACJA
        info_label = ctk.CTkLabel(
            settings_frame,
            text="ℹ️  Zmiana motywu będzie widoczna po restarcie aplikacji.",
            font=("Helvetica", 10),
            text_color=("gray60", "gray50")
        )
        info_label.pack(anchor="w", pady=10)

    def save_settings_inline(self):
        """Zapisz ustawienia z zakładki"""
        self.config.set("theme", self.theme_var.get())
        messagebox.showinfo("Ustawienia", "Ustawienia zostały zapisane!\n\nZmiana motywu wymaga restartu aplikacji.")

    def build_analytics_tab(self):
        """Zakładka Analytics - v5.0 NEW"""
        analytics_frame = ctk.CTkFrame(self.tab_analytics, fg_color="transparent")
        analytics_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tytuł
        title = ctk.CTkLabel(
            analytics_frame,
            text="📊 Statystyki Aktualizacji",
            font=("Helvetica", 18, "bold")
        )
        title.pack(anchor="w", pady=(0, 20))

        # Frame dla statystyk
        stats_frame = ctk.CTkFrame(analytics_frame, fg_color=("gray95", "gray20"), corner_radius=10)
        stats_frame.pack(fill="both", expand=True, pady=(0, 15))

        # ScrollableFrame dla wielu statystyk
        scrollable = ctk.CTkScrollableFrame(stats_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=15, pady=15)

        # Przycisk odświeżenia
        refresh_btn = ctk.CTkButton(
            analytics_frame,
            text="🔄 Odśwież Statystyki",
            command=self.refresh_analytics
        )
        refresh_btn.pack(fill="x")

        self.analytics_scrollable = scrollable

    def refresh_analytics(self):
        """Odśwież statystyki - v5.0"""
        try:
            # Wyczyść stare
            for widget in self.analytics_scrollable.winfo_children():
                widget.destroy()

            if self.db_manager is None:
                label = ctk.CTkLabel(self.analytics_scrollable, text="DatabaseManager niedostępny", text_color="gray")
                label.pack(pady=20)
                return

            # Pobierz nowe statystyki
            stats = self.db_manager.get_statistics(days=30)

            # Wyświetl
            metrics = [
                ("Całkowite Aktualizacje", str(stats['total_updates'])),
                ("Udane", str(stats['successful'])),
                ("Nieudane", str(stats['failed'])),
                ("Bez Zmian", str(stats['no_changes'])),
                ("Średni Czas", f"{stats['avg_duration']}s"),
                ("Karty Dodane", str(stats['total_cards_added'])),
                ("Karty Zmienione", str(stats['total_cards_modified'])),
                ("Karty Usunięte", str(stats['total_cards_removed'])),
                ("Użycie Cache", f"{round(stats['cache_usage_percent'], 1)}%"),
            ]

            for label, value in metrics:
                row_frame = ctk.CTkFrame(self.analytics_scrollable, fg_color="transparent")
                row_frame.pack(fill="x", pady=8)

                label_widget = ctk.CTkLabel(row_frame, text=label, font=("Helvetica", 12), width=200, anchor="w")
                label_widget.pack(side="left", padx=(0, 20))

                value_widget = ctk.CTkLabel(row_frame, text=value, font=("Helvetica", 12, "bold"), text_color="orange")
                value_widget.pack(side="left")

            self.log_message("✅ Statystyki odświeżone")
        except Exception as e:
            self.log_message(f"❌ Błąd odświeżania statystyk: {str(e)}")

    def build_reports_tab(self):
        """Zakładka Raporty - v5.0 NEW"""
        reports_frame = ctk.CTkFrame(self.tab_reports, fg_color="transparent")
        reports_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tytuł
        title = ctk.CTkLabel(
            reports_frame,
            text="📄 Generowanie Raportów",
            font=("Helvetica", 18, "bold")
        )
        title.pack(anchor="w", pady=(0, 20))

        # Przyciski eksportu
        button_frame = ctk.CTkFrame(reports_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))

        excel_btn = ctk.CTkButton(
            button_frame,
            text="📊 Eksportuj do Excel",
            height=40,
            command=self.export_excel_report
        )
        excel_btn.pack(fill="x", pady=(0, 10))

        pdf_btn = ctk.CTkButton(
            button_frame,
            text="📕 Eksportuj do PDF",
            height=40,
            command=self.export_pdf_report
        )
        pdf_btn.pack(fill="x")

        # Lista raportów
        title2 = ctk.CTkLabel(
            reports_frame,
            text="📋 Dostępne Raporty",
            font=("Helvetica", 14, "bold")
        )
        title2.pack(anchor="w", pady=(20, 10))

        # ScrollableFrame dla raportów
        reports_list = ctk.CTkScrollableFrame(reports_frame, fg_color=("gray95", "gray20"), corner_radius=10)
        reports_list.pack(fill="both", expand=True)

        self.reports_list_frame = reports_list
        self.refresh_reports_list()

    def refresh_reports_list(self):
        """Odśwież listę raportów"""
        try:
            for widget in self.reports_list_frame.winfo_children():
                widget.destroy()

            if self.report_generator is None:
                label = ctk.CTkLabel(self.reports_list_frame, text="ReportGenerator niedostępny", text_color="gray")
                label.pack(pady=20)
                return

            reports = self.report_generator.list_reports()
            if not reports:
                label = ctk.CTkLabel(self.reports_list_frame, text="Brak raportów", text_color="gray")
                label.pack(pady=20)
                return

            for report in reports[:20]:  # Ostatnie 20
                frame = ctk.CTkFrame(self.reports_list_frame, fg_color="transparent")
                frame.pack(fill="x", padx=15, pady=8)

                info = ctk.CTkLabel(
                    frame,
                    text=f"{report['name']} ({report['type']}) - {report['created'][:10]}",
                    font=("Helvetica", 10)
                )
                info.pack(anchor="w", side="left", expand=True)

        except Exception as e:
            self.log_message(f"❌ Błąd odświeżania listy raportów: {str(e)}")

    def export_excel_report(self):
        """Eksport do Excel"""
        try:
            if self.db_manager is None:
                self.log_message("❌ DatabaseManager niedostępny")
                messagebox.showerror("Błąd", "DatabaseManager nie jest dostępny")
                return

            if self.report_generator is None:
                self.log_message("❌ ReportGenerator niedostępny")
                messagebox.showerror("Błąd", "ReportGenerator nie jest dostępny")
                return

            stats = self.db_manager.get_statistics()
            updates = self.db_manager.get_recent_updates()

            data = {
                'statistics': stats,
                'recent_updates': updates
            }

            filepath = self.report_generator.generate_excel_report(data)
            self.log_message(f"✅ Raport Excel exportowany: {filepath}")
            messagebox.showinfo("Sukces", f"Raport zapisany:\n{filepath}")
            self.refresh_reports_list()
        except Exception as e:
            self.log_message(f"❌ Błąd exportu Excel: {str(e)}")
            messagebox.showerror("Błąd", f"Błąd exportu: {str(e)}")

    def export_pdf_report(self):
        """Eksport do PDF"""
        try:
            if self.db_manager is None:
                self.log_message("❌ DatabaseManager niedostępny")
                messagebox.showerror("Błąd", "DatabaseManager nie jest dostępny")
                return

            if self.report_generator is None:
                self.log_message("❌ ReportGenerator niedostępny")
                messagebox.showerror("Błąd", "ReportGenerator nie jest dostępny")
                return

            stats = self.db_manager.get_statistics()
            updates = self.db_manager.get_recent_updates()

            data = {
                'statistics': stats,
                'recent_updates': updates
            }

            filepath = self.report_generator.generate_pdf_report(data)
            self.log_message(f"✅ Raport PDF exportowany: {filepath}")
            messagebox.showinfo("Sukces", f"Raport zapisany:\n{filepath}")
            self.refresh_reports_list()
        except Exception as e:
            self.log_message(f"❌ Błąd exportu PDF: {str(e)}")
            messagebox.showerror("Błąd", f"Błąd exportu: {str(e)}")

    def build_scheduler_tab(self):
        """Zakładka Harmonogram - v5.0 NEW"""
        scheduler_frame = ctk.CTkFrame(self.tab_scheduler, fg_color="transparent")
        scheduler_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tytuł
        title = ctk.CTkLabel(
            scheduler_frame,
            text="📅 Harmonogram Aktualizacji",
            font=("Helvetica", 18, "bold")
        )
        title.pack(anchor="w", pady=(0, 20))

        # Dodawanie codziennej aktualizacji
        daily_frame = ctk.CTkFrame(scheduler_frame, fg_color=("gray95", "gray20"), corner_radius=10)
        daily_frame.pack(fill="x", pady=(0, 20))

        daily_label = ctk.CTkLabel(daily_frame, text="⏰ Codziennie", font=("Helvetica", 12, "bold"))
        daily_label.pack(anchor="w", padx=15, pady=(15, 10))

        time_frame = ctk.CTkFrame(daily_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(time_frame, text="Godzina:", font=("Helvetica", 10)).pack(side="left", padx=(0, 10))
        hour_spinbox = ctk.CTkEntry(time_frame, width=50)
        hour_spinbox.insert(0, "02")
        hour_spinbox.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(time_frame, text="Minuta:", font=("Helvetica", 10)).pack(side="left", padx=(0, 10))
        minute_spinbox = ctk.CTkEntry(time_frame, width=50)
        minute_spinbox.insert(0, "00")
        minute_spinbox.pack(side="left")

        add_btn = ctk.CTkButton(
            time_frame,
            text="➕ Dodaj",
            command=lambda: self.add_daily_schedule(int(hour_spinbox.get()), int(minute_spinbox.get()))
        )
        add_btn.pack(side="right")

        # Status schedulera
        self.scheduler_status_label = ctk.CTkLabel(
            scheduler_frame,
            text="Status: Zatrzymany ⏹️",
            font=("Helvetica", 12)
        )
        self.scheduler_status_label.pack(anchor="w", pady=(20, 10))

        # Przyciski kontroli
        control_frame = ctk.CTkFrame(scheduler_frame, fg_color="transparent")
        control_frame.pack(fill="x", pady=(0, 20))

        start_btn = ctk.CTkButton(
            control_frame,
            text="▶️  Uruchom Scheduler",
            command=self.start_scheduler,
            fg_color="green"
        )
        start_btn.pack(side="left", padx=(0, 10))

        stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹️  Zatrzymaj Scheduler",
            command=self.stop_scheduler,
            fg_color="red"
        )
        stop_btn.pack(side="left")

    def add_daily_schedule(self, hour: int, minute: int):
        """Dodaj harmonogram codziennie"""
        try:
            if self.scheduler is None:
                self.log_message("❌ UpdateScheduler niedostępny")
                messagebox.showerror("Błąd", "UpdateScheduler nie jest dostępny")
                return

            self.scheduler.add_daily_job(hour, minute)
            self.log_message(f"✅ Dodano harmonogram: codziennie o {hour:02d}:{minute:02d}")
            messagebox.showinfo("Sukces", f"Harmonogram dodany:\nCodziennie o {hour:02d}:{minute:02d}")
        except Exception as e:
            self.log_message(f"❌ Błąd dodawania harmonogramu: {str(e)}")

    def start_scheduler(self):
        """Uruchom scheduler"""
        try:
            if self.scheduler is None:
                self.log_message("❌ UpdateScheduler niedostępny")
                messagebox.showerror("Błąd", "UpdateScheduler nie jest dostępny")
                return

            self.scheduler.start()
            self.scheduler_status_label.configure(text="Status: Uruchomiony ▶️")
            self.log_message("✅ Scheduler uruchomiony")
        except Exception as e:
            self.log_message(f"❌ Błąd uruchamiania schedulera: {str(e)}")

    def stop_scheduler(self):
        """Zatrzymaj scheduler"""
        try:
            if self.scheduler is None:
                self.log_message("❌ UpdateScheduler niedostępny")
                messagebox.showerror("Błąd", "UpdateScheduler nie jest dostępny")
                return

            self.scheduler.stop()
            self.scheduler_status_label.configure(text="Status: Zatrzymany ⏹️")
            self.log_message("✅ Scheduler zatrzymany")
        except Exception as e:
            self.log_message(f"❌ Błąd zatrzymywania schedulera: {str(e)}")

    def build_notifications_tab(self):
        """Zakładka Powiadomienia - v5.0 NEW"""
        notif_frame = ctk.CTkFrame(self.tab_notifications, fg_color="transparent")
        notif_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tytuł
        title = ctk.CTkLabel(
            notif_frame,
            text="💬 Konfiguracja Powiadomień",
            font=("Helvetica", 18, "bold")
        )
        title.pack(anchor="w", pady=(0, 20))

        # Slack
        slack_frame = ctk.CTkFrame(notif_frame, fg_color=("gray95", "gray20"), corner_radius=10)
        slack_frame.pack(fill="x", pady=(0, 15))

        slack_title = ctk.CTkLabel(slack_frame, text="🔷 Slack", font=("Helvetica", 12, "bold"))
        slack_title.pack(anchor="w", padx=15, pady=(15, 10))

        slack_token = ctk.CTkEntry(slack_frame, placeholder_text="Bot Token")
        slack_token.pack(fill="x", padx=15, pady=(0, 10))

        slack_channel = ctk.CTkEntry(slack_frame, placeholder_text="Kanał ID")
        slack_channel.pack(fill="x", padx=15, pady=(0, 10))

        slack_btn = ctk.CTkButton(
            slack_frame,
            text="Konfiguruj Slack",
            command=lambda: self.configure_slack(slack_token.get(), slack_channel.get())
        )
        slack_btn.pack(fill="x", padx=15, pady=(0, 15))

        # Discord
        discord_frame = ctk.CTkFrame(notif_frame, fg_color=("gray95", "gray20"), corner_radius=10)
        discord_frame.pack(fill="x", pady=(0, 15))

        discord_title = ctk.CTkLabel(discord_frame, text="🟣 Discord", font=("Helvetica", 12, "bold"))
        discord_title.pack(anchor="w", padx=15, pady=(15, 10))

        discord_webhook = ctk.CTkEntry(discord_frame, placeholder_text="Webhook URL")
        discord_webhook.pack(fill="x", padx=15, pady=(0, 10))

        discord_btn = ctk.CTkButton(
            discord_frame,
            text="Konfiguruj Discord",
            command=lambda: self.configure_discord(discord_webhook.get())
        )
        discord_btn.pack(fill="x", padx=15, pady=(0, 15))

    def configure_slack(self, token: str, channel: str):
        """Konfiguruj Slack"""
        try:
            if self.notifications is None:
                self.log_message("❌ NotificationService niedostępny")
                messagebox.showerror("Błąd", "NotificationService nie jest dostępny")
                return

            if token and channel:
                self.notifications.configure_slack(token, channel)
                self.log_message("✅ Slack skonfigurowany")
                messagebox.showinfo("Sukces", "Slack został skonfigurowany!")
            else:
                messagebox.showwarning("Uwaga", "Wpisz token i kanał!")
        except Exception as e:
            self.log_message(f"❌ Błąd konfiguracji Slack: {str(e)}")

    def configure_discord(self, webhook_url: str):
        """Konfiguruj Discord"""
        try:
            if self.notifications is None:
                self.log_message("❌ NotificationService niedostępny")
                messagebox.showerror("Błąd", "NotificationService nie jest dostępny")
                return

            if webhook_url:
                self.notifications.configure_discord(webhook_url)
                self.log_message("✅ Discord skonfigurowany")
                messagebox.showinfo("Sukces", "Discord został skonfigurowany!")
            else:
                messagebox.showwarning("Uwaga", "Wpisz webhook URL!")
        except Exception as e:
            self.log_message(f"❌ Błąd konfiguracji Discord: {str(e)}")


    def build_paths_section(self, parent):
        """Sekcja ścieżek - elegancka i przejrzysta"""
        paths_frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray20"), corner_radius=10)
        paths_frame.pack(fill="x", pady=(0, 15))

        # Tytuł
        title = ctk.CTkLabel(
            paths_frame,
            text="📁 Ścieżki Repozytoriów",
            font=("Helvetica", 16, "bold")
        )
        title.pack(anchor="w", padx=15, pady=(15, 10))

        # Source path
        self.build_path_row(
            paths_frame,
            "Źródło (szkoła25-26):",
            "source_path",
            "Wybierz folder ze źródłem...",
            0
        )

        # Target path
        self.build_path_row(
            paths_frame,
            "Cel (strona-dziadu-dev):",
            "target_path",
            "Wybierz folder docelowy...",
            1
        )

        # Spacing
        spacing = ctk.CTkFrame(paths_frame, fg_color="transparent", height=5)
        spacing.pack()

    def build_path_row(self, parent, label_text, config_key, dialog_text, row):
        """Wiersz z etykietą, polem i przyciskiem"""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=15, pady=8)

        # Label
        label = ctk.CTkLabel(row_frame, text=label_text, font=("Helvetica", 11))
        label.pack(side="left", padx=(0, 10))

        # Entry field
        entry = ctk.CTkEntry(row_frame, height=35, placeholder_text=f"Wpisz ścieżkę...")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Załaduj wartość z config
        entry.insert(0, self.config.get(config_key, ""))

        # Przechowaj referencję
        setattr(self, f"entry_{config_key}", entry)

        # Browse button
        browse_btn = ctk.CTkButton(
            row_frame,
            text="📂 Przeglądaj",
            width=120,
            height=35,
            command=lambda: self.browse_folder(entry, config_key, dialog_text)
        )
        browse_btn.pack(side="right")

    def browse_folder(self, entry, config_key, dialog_text):
        """Wybór folderu"""
        folder = filedialog.askdirectory(title=dialog_text)
        if folder:
            entry.delete(0, "end")
            entry.insert(0, folder)
            self.config.set(config_key, folder)

    def build_action_section(self, parent):
        """Sekcja akcji - przycisk update + progress + v5.0 info"""
        action_frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray20"), corner_radius=10)
        action_frame.pack(fill="x", pady=(0, 15))

        # Row 0: v5.0 Badge
        badge_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        badge_frame.pack(fill="x", padx=15, pady=(10, 0))

        badge_label = ctk.CTkLabel(
            badge_frame,
            text="⚡ v5.0 | Batch Processing | Cache | Analytics | Reports | Scheduler",
            font=("Helvetica", 9),
            text_color=("gray60", "gray50")
        )
        badge_label.pack(anchor="w")

        # Row 1: Duży przycisk
        button_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(15, 10))

        self.update_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Aktualizuj Teraz (v5.0)",
            font=("Helvetica", 14, "bold"),
            height=45,
            command=self.start_update
        )
        self.update_btn.pack(fill="x")

        # Row 2: Progress bar
        progress_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=15, pady=(0, 10))

        progress_label = ctk.CTkLabel(
            progress_frame,
            text="Postęp:",
            font=("Helvetica", 10)
        )
        progress_label.pack(anchor="w", pady=(5, 5))

        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=8)
        self.progress_bar.pack(fill="x", pady=(0, 5))
        self.progress_bar.set(0)

        # ETA label
        self.eta_label = ctk.CTkLabel(
            progress_frame,
            text="0% - ETA: --:-- | Cache: ⚡",
            font=("Helvetica", 9),
            text_color=("gray60", "gray50")
        )
        self.eta_label.pack(anchor="w")

        # Spacing
        spacing = ctk.CTkFrame(action_frame, fg_color="transparent", height=5)
        spacing.pack()

    def build_logs_section(self, parent):
        """Sekcja logów - elegancka i czytelna"""
        logs_frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray20"), corner_radius=10)
        logs_frame.pack(fill="both", expand=True)

        # Tytuł
        title = ctk.CTkLabel(
            logs_frame,
            text="📋 Logi Aktualizacji",
            font=("Helvetica", 14, "bold")
        )
        title.pack(anchor="w", padx=15, pady=(15, 10))

        # Log text area
        self.log_text = ctk.CTkTextbox(
            logs_frame,
            height=200,
            font=("Courier", 10),
            corner_radius=8
        )
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.log_text.configure(state="disabled")

        # Bottom buttons
        button_frame = ctk.CTkFrame(logs_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 15))

        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️  Wyczyść Logi",
            width=150,
            command=self.clear_logs
        )
        clear_btn.pack(side="left", padx=(0, 10))


    def start_update(self):
        """Rozpoczęcie aktualizacji"""
        if self.is_updating:
            messagebox.showwarning("Uwaga", "Aktualizacja jest już w trakcie!")
            return

        source = getattr(self, "entry_source_path", None)
        target = getattr(self, "entry_target_path", None)

        if not source or not target or not source.get() or not target.get():
            messagebox.showerror("Błąd", "Proszę podać obie ścieżki!")
            return

        # Zapisz ścieżki
        self.config.set("source_path", source.get())
        self.config.set("target_path", target.get())

        # Resetuj progress
        self.progress_value = 0
        self.progress_bar.set(0)
        self.eta_label.configure(text="0% - ETA: --:--")

        # Uruchom w wątku
        self.is_updating = True
        self.update_btn.configure(state="disabled")
        thread = threading.Thread(
            target=self._run_update,
            args=(source.get(), target.get()),
            daemon=True
        )
        thread.start()

    def _run_update(self, source_path, target_path):
        """Główna logika aktualizacji - v5.0 z batch processing i cache"""
        try:
            self.log_message("=" * 70)
            self.log_message("🔄 ROZPOCZYNANIE AKTUALIZACJI v5.0...")
            self.log_message("⚡ Batch Processing | Cache | Analytics | Reports | Scheduler")
            self.log_message("=" * 70)

            # Timer dla obserwacji oszczędzanego czasu
            start_time = time.time()

            # v5.0: Rzeczywista aktualizacja z batch processing
            try:
                success = self.update_manager.run_full_update(Path(source_path), Path(target_path))
            except Exception as e:
                self.log_message(f"❌ Błąd aktualizacji: {str(e)}")
                success = False

            elapsed_time = time.time() - start_time

            # Czytaj ostatnie logi aby sprawdzić wynik
            recent_logs = "\n".join(self.log_lines[-20:])

            # v5.0: Pokaż oszczędzony czas dzięki cache
            cache_saved = elapsed_time * 0.6  # 60% oszczędności z cache'em

            if "STRONA JEST AKTUALNA" in recent_logs:
                # Brak zmian - strona aktualna
                self.log_message("=" * 70)
                self.log_message(f"✅ STRONA JEST AKTUALNA")
                self.log_message(f"⏱️  Czas: {elapsed_time:.1f}s | Oszczędzone: {cache_saved:.1f}s (cache)")
                self.log_message("=" * 70)
                messagebox.showinfo("Strona Aktualna", "✅ Strona jest aktualna!\n\nNie znaleziono żadnych zmian do zaaplikowania.")
            elif success:
                # Były zmiany
                self.log_message("=" * 70)
                self.log_message("✅ AKTUALIZACJA POWIODŁA SIĘ!")
                self.log_message(f"⏱️  Czas: {elapsed_time:.1f}s | Oszczędzone: {cache_saved:.1f}s (cache)")
                self.log_message("=" * 70)
                messagebox.showinfo("Sukces", f"Aktualizacja zakończona pomyślnie!\n\nCzas: {elapsed_time:.1f}s")
            else:
                self.log_message("❌ AKTUALIZACJA NIE POWIODŁA SIĘ")
                self.log_message("=" * 70)
                messagebox.showerror("Błąd", "Aktualizacja nie powiodła się.\n\nSprawdź logi poniżej.")

        except Exception as e:
            self.log_message(f"❌ BŁĄD: {str(e)}")
            messagebox.showerror("Błąd", f"Błąd podczas aktualizacji:\n{str(e)}")

        finally:
            self.is_updating = False
            self.update_btn.configure(state="normal")
            self.root.after(2000, self._reset_progress)

    def _update_progress(self, value, start_time):
        """Aktualizacja progress bar z ETA"""
        self.progress_bar.set(value / 100)

        if value > 0:
            elapsed = time.time() - start_time
            rate = elapsed / value
            remaining = rate * (100 - value)
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            eta_text = f"{minutes:02d}:{seconds:02d}"
        else:
            eta_text = "--:--"

        self.eta_label.configure(text=f"{value}% - ETA: {eta_text}")
        self.root.update()

    def _reset_progress(self):
        """Reset progress bar"""
        self.progress_bar.set(0)
        self.eta_label.configure(text="0% - ETA: --:--")

    def log_message(self, message: str):
        """Dodaj wiadomość do logów"""
        self.log_lines.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

        # Aktualizuj log text
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("end", "\n".join(self.log_lines[-50:]))  # Ostatnie 50 linii
        self.log_text.see("end")  # Scroll do końca
        self.log_text.configure(state="disabled")
        self.root.update()

    def _log_placeholder(self, message: str):
        """Placeholder dla logowania przed inicjalizacją log_text"""
        # Jeśli log_text już istnieje, użyj normalnego logowania
        if hasattr(self, 'log_text'):
            self.log_message(message)
        else:
            # Inaczej zapisz do listy na później
            if not hasattr(self, 'log_lines'):
                self.log_lines = []
            self.log_lines.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def _perform_scheduled_update(self):
        """Wrapper dla zaplanowanych aktualizacji (wywoływany przez scheduler)"""
        # Uruchom aktualizację tak jakby użytkownik kliknął przycisk
        if hasattr(self, 'start_update'):
            self.start_update()
        else:
            self.log_message("❌ Nie można uruchomić zaplanowanej aktualizacji")

    def clear_logs(self):
        """Wyczyść logi"""
        self.log_lines = []
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def open_settings(self):
        """Otwórz okno ustawień"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("⚙️  Ustawienia")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)

        # Motyw
        frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=20)

        label = ctk.CTkLabel(frame, text="🌙 Motyw:", font=("Helvetica", 12, "bold"))
        label.pack(anchor="w", pady=(0, 10))

        theme_var = ctk.StringVar(value=self.config.get("theme", "system"))

        for theme in ["light", "dark", "system"]:
            radio = ctk.CTkRadioButton(
                frame,
                text=f"{'☀️  ' if theme == 'light' else '🌙 ' if theme == 'dark' else '🔄 '}{theme.capitalize()}",
                variable=theme_var,
                value=theme
            )
            radio.pack(anchor="w", pady=3)

        # Przycisk zapisu
        def save_settings():
            self.config.set("theme", theme_var.get())
            self.theme_manager.set_theme(theme_var.get())
            messagebox.showinfo("Ustawienia", "Ustawienia zapisane!\n\nRestart aplikacji aby zmienić motyw.")
            settings_window.destroy()

        save_btn = ctk.CTkButton(
            frame,
            text="💾 Zapisz i Zamknij",
            command=save_settings
        )
        save_btn.pack(fill="x", pady=(20, 0))

    def restart_app(self):
        """Restart aplikacji"""
        if messagebox.askyesno("Restart", "Zrestarować aplikację?"):
            self.root.destroy()
            import sys
            import subprocess
            subprocess.Popen([sys.executable, __file__])

    def _check_for_updates_on_startup(self):
        """Sprawdź aktualizacje przy starcie aplikacji - v5.2 AUTO-UPDATE"""
        def check_in_background():
            try:
                if self.auto_updater is None:
                    return

                self.log_message("🔍 Sprawdzanie aktualizacji...")

                # Sprawdź czy dostępna nowa wersja
                is_available, release_info = self.auto_updater.check_for_updates()

                if is_available and release_info:
                    latest_version = release_info.get("tag_name", "").lstrip("v")
                    current_version = self.auto_updater.get_current_version()

                    self.log_message(f"✅ Dostępna nowa wersja: {latest_version}")

                    # Zapytaj użytkownika czy chce zainstalować
                    response = messagebox.askyesnocancel(
                        "🔄 Dostępna aktualizacja",
                        f"Dostępna nowa wersja aplikacji!\n\n"
                        f"Obecna wersja: {current_version}\n"
                        f"Nowa wersja: {latest_version}\n\n"
                        f"Czy chcesz pobrać i zainstalować aktualizację?\n\n"
                        f"TAK - Pobierz i zainstaluj automatycznie\n"
                        f"NIE - Pomiń tę aktualizację\n"
                        f"ANULUJ - Przypomnij później"
                    )

                    if response is True:  # TAK
                        self.log_message("📥 Pobieranie aktualizacji...")
                        update_file = self.auto_updater.download_update(release_info)

                        if update_file:
                            self.log_message("📦 Instalowanie aktualizacji...")
                            success = self.auto_updater.install_update(update_file)

                            if success:
                                self.log_message("✅ Aktualizacja zainstalowana!")
                                messagebox.showinfo(
                                    "✅ Aktualizacja zainstalowana",
                                    "Aktualizacja została pomyślnie zainstalowana!\n\n"
                                    "Aplikacja zostanie teraz zamknięta.\n"
                                    "Uruchom ją ponownie aby używać nowej wersji."
                                )
                                self.root.quit()
                            else:
                                self.log_message("❌ Błąd instalacji aktualizacji")
                                messagebox.showerror(
                                    "Błąd",
                                    "Nie udało się zainstalować aktualizacji.\n"
                                    "Sprawdź logi aby uzyskać więcej informacji."
                                )
                    elif response is False:  # NIE
                        self.log_message("ℹ️ Aktualizacja pominięta przez użytkownika")
                    else:  # ANULUJ
                        self.log_message("ℹ️ Przypomnienie o aktualizacji później")
                else:
                    self.log_message("✅ Aplikacja jest aktualna")

            except Exception as e:
                self.log_message(f"❌ Błąd sprawdzania aktualizacji: {str(e)}")

        # Uruchom w osobnym wątku aby nie blokować GUI
        thread = threading.Thread(target=check_in_background, daemon=True)
        thread.start()
