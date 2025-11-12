#!/usr/bin/env python3
"""
Webhook Manager dla Aktualizatora Strony v5.1
Zarządzanie GitHub webhooks i wywoływaniem aktualizacji

v5.1 NEW:
- ✅ GitHub Webhook Integration
- ✅ Push Event Handling
- ✅ Automatic Update Triggering
- ✅ Webhook Verification
"""

import json
import hashlib
import hmac
from typing import Dict, Any, Callable, Optional, List
from datetime import datetime
from pathlib import Path
import threading
import requests


class WebhookManager:
    """Webhook Manager - v5.1"""

    def __init__(self,
                 update_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None,
                 secret: Optional[str] = None):
        """
        Inicjalizacja Webhook Manager

        Args:
            update_callback: Callback do uruchomienia aktualizacji
            log_callback: Callback do logowania
            secret: Secret do weryfikacji GitHub webhooks
        """
        self.update_callback = update_callback
        self.log_callback = log_callback or print
        self.secret = secret or 'webhook-secret-v5.1'
        self.webhooks: List[Dict[str, Any]] = []
        self.webhook_history: List[Dict[str, Any]] = []
        self.max_history = 100

        self.log("✅ Webhook Manager inicjalizowany (v5.1)")

    def verify_github_webhook(self, payload_bytes: bytes, signature: str) -> bool:
        """
        Weryfikuj GitHub webhook signature

        Args:
            payload_bytes: Treść payloadu
            signature: Signature z nagłówka X-Hub-Signature-256

        Returns:
            True jeśli signature jest valid
        """
        try:
            # GitHub używa format: sha256=<hash>
            if not signature.startswith('sha256='):
                self.log("⚠️  Nieznany format signature")
                return False

            expected_signature = signature.split('sha256=')[1]

            # Oblicz HMAC-SHA256
            computed_signature = hmac.new(
                self.secret.encode(),
                payload_bytes,
                hashlib.sha256
            ).hexdigest()

            # Porównaj signatures
            is_valid = hmac.compare_digest(expected_signature, computed_signature)

            if is_valid:
                self.log("✅ Webhook signature verified")
            else:
                self.log("❌ Webhook signature invalid")

            return is_valid

        except Exception as e:
            self.log(f"❌ Błąd verify_github_webhook: {str(e)}")
            return False

    def handle_github_webhook(self, payload: Dict[str, Any]) -> bool:
        """
        Obsłuż GitHub webhook payload

        Args:
            payload: GitHub webhook payload

        Returns:
            True jeśli webhook został przetworzony
        """
        try:
            event_type = payload.get('action', 'unknown')

            # Sprawdź event type
            if 'push' in str(payload):
                self.log(f"📤 GitHub push event: {event_type}")

                # Pobierz informacje
                repo_name = payload.get('repository', {}).get('name', 'unknown')
                pusher = payload.get('pusher', {}).get('name', 'unknown')
                commits = len(payload.get('commits', []))

                self.log(f"  📦 Repo: {repo_name}")
                self.log(f"  👤 Pusher: {pusher}")
                self.log(f"  📝 Commits: {commits}")

                # Uruchom aktualizację
                if self.update_callback:
                    threading.Thread(
                        target=self._trigger_update_async,
                        args=(repo_name,),
                        daemon=True
                    ).start()

                # Zapisz w historii
                self._add_to_history({
                    'type': 'github_push',
                    'repo': repo_name,
                    'pusher': pusher,
                    'commits': commits,
                    'status': 'triggered'
                })

                return True

            # Inne event types
            self.log(f"ℹ️  GitHub event: {event_type}")

            self._add_to_history({
                'type': event_type,
                'status': 'received'
            })

            return True

        except Exception as e:
            self.log(f"❌ Błąd handle_github_webhook: {str(e)}")
            self._add_to_history({
                'type': 'error',
                'error': str(e),
                'status': 'failed'
            })
            return False

    def _trigger_update_async(self, repo_name: str):
        """Uruchom aktualizację w tle"""
        try:
            self.log(f"🔄 Triggering update dla: {repo_name}")
            if self.update_callback:
                self.update_callback()
        except Exception as e:
            self.log(f"❌ Błąd async update: {str(e)}")

    def register_webhook(self, url: str, events: List[str]) -> str:
        """
        Zarejestruj webhook

        Args:
            url: URL webhoka
            events: Lista eventów do nasłuchiwania

        Returns:
            Webhook ID
        """
        try:
            webhook_id = hashlib.md5(
                f"{url}{datetime.now().isoformat()}".encode()
            ).hexdigest()

            webhook = {
                'id': webhook_id,
                'url': url,
                'events': events,
                'created_at': datetime.now().isoformat(),
                'active': True
            }

            self.webhooks.append(webhook)
            self.log(f"✅ Webhook zarejestrowany: {webhook_id}")
            self.log(f"   URL: {url}")
            self.log(f"   Events: {', '.join(events)}")

            return webhook_id

        except Exception as e:
            self.log(f"❌ Błąd register_webhook: {str(e)}")
            raise

    def unregister_webhook(self, webhook_id: str) -> bool:
        """
        Wyrejestruj webhook

        Args:
            webhook_id: ID webhoka

        Returns:
            True jeśli się powiedło
        """
        try:
            self.webhooks = [w for w in self.webhooks if w['id'] != webhook_id]
            self.log(f"✅ Webhook usunięty: {webhook_id}")
            return True
        except Exception as e:
            self.log(f"❌ Błąd unregister_webhook: {str(e)}")
            return False

    def get_webhooks(self) -> List[Dict[str, Any]]:
        """Pobierz listę webhooks"""
        return self.webhooks

    def _add_to_history(self, entry: Dict[str, Any]):
        """Dodaj wpis do historii"""
        entry['timestamp'] = datetime.now().isoformat()
        self.webhook_history.append(entry)

        # Zachowaj tylko ostatnie N wpisów
        if len(self.webhook_history) > self.max_history:
            self.webhook_history = self.webhook_history[-self.max_history:]

    def get_history(self) -> List[Dict[str, Any]]:
        """Pobierz historię webhooks"""
        return self.webhook_history

    def send_outgoing_webhook(self, url: str, payload: Dict[str, Any]) -> bool:
        """
        Wyślij outgoing webhook do innego serwera

        Args:
            url: URL docelowy
            payload: Dane do wysłania

        Returns:
            True jeśli się powiedło
        """
        try:
            self.log(f"📤 Wysyłanie webhook do: {url}")

            response = requests.post(
                url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                self.log(f"✅ Webhook wysłany pomyślnie")
                return True
            else:
                self.log(f"⚠️  Webhook response: {response.status_code}")
                return False

        except Exception as e:
            self.log(f"❌ Błąd send_outgoing_webhook: {str(e)}")
            return False

    def save_webhooks(self, filepath: str = 'src/.data/webhooks.json'):
        """Zapisz webhooks do pliku"""
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.webhooks, f, ensure_ascii=False, indent=2)

            self.log(f"💾 Webhooks zapisane: {filepath}")
        except Exception as e:
            self.log(f"❌ Błąd save_webhooks: {str(e)}")

    def load_webhooks(self, filepath: str = 'src/.data/webhooks.json'):
        """Załaduj webhooks z pliku"""
        try:
            path = Path(filepath)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    self.webhooks = json.load(f)
                self.log(f"✅ Webhooks załadowane: {len(self.webhooks)} webhooks")
        except Exception as e:
            self.log(f"❌ Błąd load_webhooks: {str(e)}")

    def log(self, message: str):
        """Logowanie"""
        self.log_callback(message)


# Przykład użycia
if __name__ == '__main__':
    webhook_manager = WebhookManager()

    # Zarejestruj webhook
    webhook_id = webhook_manager.register_webhook(
        url='http://example.com/webhook',
        events=['push', 'pull_request']
    )

    print(f"Webhook ID: {webhook_id}")
    print(f"Webhooks: {webhook_manager.get_webhooks()}")

