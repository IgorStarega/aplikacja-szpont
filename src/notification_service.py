#!/usr/bin/env python3
"""
Notification Service - v5.0 Feature
Integracje z Slack, Discord, Email

Funkcjonalność:
- ✅ Slack Integration - powiadomienia na Slack
- ✅ Discord Integration - powiadomienia na Discord
- ✅ Email Reports - wysyłanie raportów email
"""

from typing import Optional, Dict, Any, List
import json
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    raise ImportError("slack-sdk nie zainstalowany. Uruchom: pip install slack-sdk")

try:
    import discord
    from discord.ext import tasks
except ImportError:
    raise ImportError("discord.py nie zainstalowany. Uruchom: pip install discord.py")

try:
    import requests
except ImportError:
    raise ImportError("requests nie zainstalowany. Uruchom: pip install requests")


class NotificationService:
    """Service powiadomień - v5.0 Feature"""

    CONFIG_FILE = "src/.config/notifications.json"

    def __init__(self, log_callback=None):
        """Inicjalizacja service'u powiadomień"""
        self.log_callback = log_callback or print
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Załaduj konfigurację powiadomień"""
        config_path = Path(self.CONFIG_FILE)
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.log(f"⚠️  Błąd załadowania konfiguracji powiadomień: {str(e)}")

        return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Domyślna konfiguracja"""
        return {
            "slack": {
                "enabled": False,
                "token": "",
                "channel": ""
            },
            "discord": {
                "enabled": False,
                "webhook_url": ""
            },
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipients": []
            }
        }

    def log(self, message: str):
        """Logowanie wiadomości"""
        if self.log_callback:
            self.log_callback(f"[NOTIFICATIONS] {message}")

    def configure_slack(self, token: str, channel: str):
        """
        Konfiguruj Slack integration

        Args:
            token: Bot token z Slack API
            channel: ID kanału
        """
        self.config['slack'] = {
            'enabled': True,
            'token': token,
            'channel': channel
        }
        self._save_config()
        self.log("✅ Slack skonfigurowany")

    def configure_discord(self, webhook_url: str):
        """
        Konfiguruj Discord integration

        Args:
            webhook_url: Webhook URL z Discord
        """
        self.config['discord'] = {
            'enabled': True,
            'webhook_url': webhook_url
        }
        self._save_config()
        self.log("✅ Discord skonfigurowany")

    def configure_email(self, smtp_server: str, smtp_port: int, sender_email: str,
                       sender_password: str, recipients: List[str]):
        """
        Konfiguruj Email integration

        Args:
            smtp_server: Adres SMTP serwera
            smtp_port: Port SMTP
            sender_email: Email nadawcy
            sender_password: Hasło nadawcy
            recipients: Lista odbiorców
        """
        self.config['email'] = {
            'enabled': True,
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'sender_email': sender_email,
            'sender_password': sender_password,
            'recipients': recipients
        }
        self._save_config()
        self.log("✅ Email skonfigurowany")

    def _save_config(self):
        """Zapisz konfigurację"""
        config_path = Path(self.CONFIG_FILE)
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"⚠️  Błąd zapisu konfiguracji: {str(e)}")

    def send_slack_notification(self, message: str, color: str = "good"):
        """
        Wyślij powiadomienie na Slack

        Args:
            message: Wiadomość
            color: Kolor ('good', 'warning', 'danger')
        """
        if not self.config['slack']['enabled']:
            return False

        try:
            client = WebClient(token=self.config['slack']['token'])
            client.chat_postMessage(
                channel=self.config['slack']['channel'],
                attachments=[{
                    'color': color,
                    'text': message,
                    'mrkdwn_in': ['text']
                }]
            )
            self.log(f"✅ Powiadomienie Slack wysłane")
            return True
        except Exception as e:
            self.log(f"❌ Błąd wysyłania Slack: {str(e)}")
            return False

    def send_discord_notification(self, title: str, description: str, color: int = 0x00ff00):
        """
        Wyślij powiadomienie na Discord

        Args:
            title: Tytuł
            description: Opis
            color: Kolor jako hex int
        """
        if not self.config['discord']['enabled']:
            return False

        try:
            webhook_url = self.config['discord']['webhook_url']

            embed = {
                "title": title,
                "description": description,
                "color": color
            }

            data = {"embeds": [embed]}
            response = requests.post(webhook_url, json=data)

            if response.status_code == 204:
                self.log(f"✅ Powiadomienie Discord wysłane")
                return True
            else:
                self.log(f"⚠️  Discord zwrócił status: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Błąd wysyłania Discord: {str(e)}")
            return False

    def send_email_notification(self, subject: str, body: str, html: bool = False):
        """
        Wyślij raport email

        Args:
            subject: Temat
            body: Treść
            html: Czy HTML format
        """
        if not self.config['email']['enabled']:
            return False

        try:
            email_config = self.config['email']

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = email_config['sender_email']
            msg['To'] = ', '.join(email_config['recipients'])

            if html:
                part = MIMEText(body, 'html', 'utf-8')
            else:
                part = MIMEText(body, 'plain', 'utf-8')

            msg.attach(part)

            # Wysłanie
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)

            self.log(f"✅ Email wysłany do {len(email_config['recipients'])} odbiorców")
            return True
        except Exception as e:
            self.log(f"❌ Błąd wysyłania email: {str(e)}")
            return False

    def notify_update_success(self, summary: Dict[str, Any]):
        """
        Poinformuj o pomyślnej aktualizacji

        Args:
            summary: Podsumowanie zmian
        """
        message = f"""
✅ **Aktualizacja Strony Pomyślna**

📊 Podsumowanie:
- 📝 Karty dodane: {summary.get('added_count', 0)}
- 🔄 Karty zmienione: {summary.get('modified_count', 0)}
- 🗑️  Karty usunięte: {summary.get('removed_count', 0)}
- ⚡ Czas trwania: {summary.get('duration', 0)}s
- 💾 Cache użyty: {'Tak' if summary.get('cache_used') else 'Nie'}
"""

        # Wysłanie na wszystkie kanały
        self.send_slack_notification(message, color="good")
        self.send_discord_notification(
            "Aktualizacja Pomyślna",
            message,
            color=0x00ff00
        )

    def notify_update_failed(self, error: str):
        """
        Poinformuj o błędzie aktualizacji

        Args:
            error: Opis błędu
        """
        message = f"❌ **Błąd Aktualizacji**\n\n{error}"

        self.send_slack_notification(message, color="danger")
        self.send_discord_notification(
            "Błąd Aktualizacji",
            message,
            color=0xff0000
        )

