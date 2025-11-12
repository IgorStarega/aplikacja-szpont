#!/usr/bin/env python3
"""
Credentials Manager dla Aktualizatora Strony v5.1
Bezpieczne przechowywanie Git credentials

v5.1 NEW:
- ✅ Git Credentials Storage
- ✅ Encrypted Password Storage
- ✅ Token Management
- ✅ Credential Rotation
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from functools import wraps
import time


class CredentialsManager:
    """Credentials Manager - v5.1"""

    def __init__(self,
                 data_dir: str = 'src/.data',
                 log_callback: Optional[Callable] = None):
        """
        Inicjalizacja Credentials Manager

        Args:
            data_dir: Katalog dla danych
            log_callback: Callback do logowania
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.creds_dir = self.data_dir / 'credentials'
        self.creds_dir.mkdir(parents=True, exist_ok=True)

        self.log_callback = log_callback or print
        self.creds_file = self.creds_dir / 'creds.json'

        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

        self.credentials: Dict[str, Any] = self._load_credentials()
        self.max_age_hours = 24  # Maksymalny wiek tokenu

        self.log("✅ Credentials Manager inicjalizowany (v5.1)")

    def _load_credentials(self) -> Dict[str, Any]:
        """Załaduj credentials"""
        try:
            if self.creds_file.exists():
                with open(self.creds_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.log(f"⚠️  Błąd załadowania credentials: {str(e)}")

        return {'git': {}, 'ssh': {}, 'tokens': {}}

    def _save_credentials(self):
        """Zapisz credentials"""
        try:
            with open(self.creds_file, 'w', encoding='utf-8') as f:
                json.dump(self.credentials, f, ensure_ascii=False, indent=2)

            # Ustaw uprawnienia
            self.creds_file.chmod(0o600)
            self.log("💾 Credentials zapisane")

        except Exception as e:
            self.log(f"❌ Błąd zapisu credentials: {str(e)}")

    def _encrypt(self, data: str) -> str:
        """Zaszyfruj dane"""
        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()

    def _decrypt(self, encrypted_data: str) -> str:
        """Odszyfruj dane"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            self.log(f"❌ Błąd deszyfrowania: {str(e)}")
            return ""

    # ==================== GIT CREDENTIALS ====================

    def store_git_credentials(self,
                             remote: str,
                             username: str,
                             password: str) -> bool:
        """
        Przechowaj Git credentials

        Args:
            remote: Git remote (np. github.com)
            username: Username
            password: Password lub token

        Returns:
            True jeśli się powiedło
        """
        try:
            encrypted_password = self._encrypt(password)

            self.credentials['git'][remote] = {
                'username': username,
                'password': encrypted_password,
                'created_at': datetime.now().isoformat(),
                'last_used': None
            }

            self._save_credentials()
            self.log(f"✅ Git credentials przechowywane: {remote}")
            return True

        except Exception as e:
            self.log(f"❌ Błąd store_git_credentials: {str(e)}")
            return False

    def get_git_credentials(self, remote: str) -> Optional[Dict[str, str]]:
        """
        Pobierz Git credentials

        Args:
            remote: Git remote

        Returns:
            Dict z username i password
        """
        try:
            if remote not in self.credentials['git']:
                self.log(f"⚠️  Credentials nie znalezione: {remote}")
                return None

            cred = self.credentials['git'][remote]

            # Odszyfruj hasło
            password = self._decrypt(cred['password'])

            # Zaktualizuj last_used
            cred['last_used'] = datetime.now().isoformat()
            self._save_credentials()

            return {
                'username': cred['username'],
                'password': password
            }

        except Exception as e:
            self.log(f"❌ Błąd get_git_credentials: {str(e)}")
            return None

    def remove_git_credentials(self, remote: str) -> bool:
        """Usuń Git credentials"""
        try:
            if remote in self.credentials['git']:
                del self.credentials['git'][remote]
                self._save_credentials()
                self.log(f"✅ Git credentials usunięte: {remote}")
                return True
            return False
        except Exception as e:
            self.log(f"❌ Błąd remove_git_credentials: {str(e)}")
            return False

    # ==================== TOKENS ====================

    def create_token(self,
                     name: str,
                     service: str,
                     value: str,
                     expires_in_hours: Optional[int] = None) -> str:
        """
        Stwórz token

        Args:
            name: Nazwa tokenu
            service: Serwis (slack, discord, github)
            value: Wartość tokenu
            expires_in_hours: Czas wygaśnięcia (opcjonalnie)

        Returns:
            Token ID
        """
        try:
            token_id = f"{service}_{name}_{int(time.time())}"
            encrypted_value = self._encrypt(value)

            created_at = datetime.now()
            expires_at = None

            if expires_in_hours:
                expires_at = (created_at + timedelta(hours=expires_in_hours)).isoformat()

            self.credentials['tokens'][token_id] = {
                'name': name,
                'service': service,
                'value': encrypted_value,
                'created_at': created_at.isoformat(),
                'expires_at': expires_at,
                'active': True
            }

            self._save_credentials()
            self.log(f"✅ Token stworzony: {token_id}")

            return token_id

        except Exception as e:
            self.log(f"❌ Błąd create_token: {str(e)}")
            raise

    def get_token(self, token_id: str) -> Optional[str]:
        """
        Pobierz token

        Args:
            token_id: ID tokenu

        Returns:
            Wartość tokenu
        """
        try:
            if token_id not in self.credentials['tokens']:
                return None

            token = self.credentials['tokens'][token_id]

            # Sprawdzenie wygaśnięcia
            if token['expires_at']:
                expires_at = datetime.fromisoformat(token['expires_at'])
                if datetime.now() > expires_at:
                    self.log(f"⚠️  Token wygasł: {token_id}")
                    token['active'] = False
                    self._save_credentials()
                    return None

            # Odszyfruj wartość
            return self._decrypt(token['value'])

        except Exception as e:
            self.log(f"❌ Błąd get_token: {str(e)}")
            return None

    def list_tokens(self, service: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Pobierz listę tokenów

        Args:
            service: Opcjonalnie filtruj po serwisie

        Returns:
            Dict z tokenami (bez wartości)
        """
        result = {}

        for token_id, token_info in self.credentials['tokens'].items():
            if service and token_info['service'] != service:
                continue

            result[token_id] = {
                'name': token_info['name'],
                'service': token_info['service'],
                'created_at': token_info['created_at'],
                'expires_at': token_info['expires_at'],
                'active': token_info['active']
            }

        return result

    def revoke_token(self, token_id: str) -> bool:
        """Odwołaj token"""
        try:
            if token_id in self.credentials['tokens']:
                self.credentials['tokens'][token_id]['active'] = False
                self._save_credentials()
                self.log(f"✅ Token odwołany: {token_id}")
                return True
            return False
        except Exception as e:
            self.log(f"❌ Błąd revoke_token: {str(e)}")
            return False

    # ==================== CREDENTIAL ROTATION ====================

    def rotate_credentials(self, remote: str, new_password: str) -> bool:
        """
        Zmień credentials

        Args:
            remote: Git remote
            new_password: Nowe hasło

        Returns:
            True jeśli się powiedło
        """
        try:
            if remote not in self.credentials['git']:
                return False

            old_password = self.credentials['git'][remote]['password']
            self.credentials['git'][remote]['password'] = self._encrypt(new_password)
            self.credentials['git'][remote]['rotated_at'] = datetime.now().isoformat()

            self._save_credentials()
            self.log(f"✅ Credentials zmienione: {remote}")

            return True

        except Exception as e:
            self.log(f"❌ Błąd rotate_credentials: {str(e)}")
            return False

    # ==================== CLEANUP ====================

    def cleanup_expired_tokens(self) -> int:
        """Oczyść wygasłe tokeny"""
        try:
            removed = 0
            expired_tokens = []

            for token_id, token_info in self.credentials['tokens'].items():
                if token_info['expires_at']:
                    expires_at = datetime.fromisoformat(token_info['expires_at'])
                    if datetime.now() > expires_at:
                        expired_tokens.append(token_id)

            for token_id in expired_tokens:
                del self.credentials['tokens'][token_id]
                removed += 1

            if removed > 0:
                self._save_credentials()
                self.log(f"🧹 Wyczyszczono {removed} wygasłych tokenów")

            return removed

        except Exception as e:
            self.log(f"❌ Błąd cleanup_expired_tokens: {str(e)}")
            return 0

    def log(self, message: str):
        """Logowanie"""
        self.log_callback(message)


# Przykład użycia
if __name__ == '__main__':
    creds = CredentialsManager()

    # Store credentials
    creds.store_git_credentials(
        remote='github.com',
        username='user',
        password='token'
    )

    # Get credentials
    creds_data = creds.get_git_credentials('github.com')
    print(f"Git credentials: {creds_data}")

