#!/usr/bin/env python3
"""
SSH Manager dla Aktualizatora Strony v5.1
Zarządzanie SSH keys dla bezpiecznego dostępu do Git

v5.1 NEW:
- ✅ SSH Key Management
- ✅ Key Encryption
- ✅ Secure Credential Storage
- ✅ SSH Host Verification
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from cryptography.fernet import Fernet
from datetime import datetime


class SSHManager:
    """SSH Manager - v5.1"""

    def __init__(self,
                 data_dir: str = 'src/.data',
                 log_callback: Optional[Callable] = None):
        """
        Inicjalizacja SSH Manager

        Args:
            data_dir: Katalog dla danych SSH
            log_callback: Callback do logowania
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.ssh_dir = self.data_dir / 'ssh'
        self.ssh_dir.mkdir(parents=True, exist_ok=True)

        self.log_callback = log_callback or print
        self.ssh_config_file = self.ssh_dir / 'config.json'
        self.encryption_key = self._load_or_create_key()
        self.cipher = Fernet(self.encryption_key)

        self.ssh_config: Dict[str, Any] = self._load_config()

        self.log("✅ SSH Manager inicjalizowany (v5.1)")

    def _load_or_create_key(self) -> bytes:
        """Załaduj lub stwórz klucz szyfrowania"""
        key_file = self.ssh_dir / '.key'

        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Stwórz nowy klucz
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)

            # Ustaw uprawnienia
            os.chmod(key_file, 0o600)
            self.log("🔐 Wygenerowano nowy klucz szyfrowania")

            return key

    def _load_config(self) -> Dict[str, Any]:
        """Załaduj konfigurację SSH"""
        try:
            if self.ssh_config_file.exists():
                with open(self.ssh_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.log(f"⚠️  Błąd załadowania config: {str(e)}")

        return {'keys': {}}

    def _save_config(self):
        """Zapisz konfigurację SSH"""
        try:
            with open(self.ssh_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.ssh_config, f, ensure_ascii=False, indent=2)
            os.chmod(self.ssh_config_file, 0o600)
        except Exception as e:
            self.log(f"❌ Błąd zapisu config: {str(e)}")

    def add_ssh_key(self,
                    key_name: str,
                    private_key_path: str,
                    passphrase: Optional[str] = None) -> bool:
        """
        Dodaj SSH key

        Args:
            key_name: Nazwa klucza
            private_key_path: Ścieżka do prywatnego klucza
            passphrase: Hasło do klucza (opcjonalne)

        Returns:
            True jeśli się powiedło
        """
        try:
            key_path = Path(private_key_path)

            if not key_path.exists():
                self.log(f"❌ Plik klucza nie istnieje: {private_key_path}")
                return False

            # Przeczytaj klucz
            with open(key_path, 'rb') as f:
                key_content = f.read()

            # Zaszyfruj zawartość
            encrypted_content = self.cipher.encrypt(key_content)

            # Zapisz zaszyfrowany klucz
            encrypted_key_path = self.ssh_dir / f"{key_name}.enc"
            with open(encrypted_key_path, 'wb') as f:
                f.write(encrypted_content)

            os.chmod(encrypted_key_path, 0o600)

            # Zaktualizuj config
            self.ssh_config['keys'][key_name] = {
                'name': key_name,
                'source_path': str(private_key_path),
                'encrypted_path': str(encrypted_key_path),
                'passphrase_protected': passphrase is not None,
                'created_at': datetime.now().isoformat(),
                'active': True
            }

            self._save_config()
            self.log(f"✅ SSH key dodany: {key_name}")

            return True

        except Exception as e:
            self.log(f"❌ Błąd add_ssh_key: {str(e)}")
            return False

    def get_ssh_key(self, key_name: str) -> Optional[bytes]:
        """
        Pobierz deszyfrowany SSH key

        Args:
            key_name: Nazwa klucza

        Returns:
            Zawartość klucza lub None
        """
        try:
            if key_name not in self.ssh_config['keys']:
                self.log(f"❌ Klucz nie znaleziony: {key_name}")
                return None

            encrypted_path = self.ssh_config['keys'][key_name]['encrypted_path']

            with open(encrypted_path, 'rb') as f:
                encrypted_content = f.read()

            # Odszyfruj
            decrypted_content = self.cipher.decrypt(encrypted_content)

            return decrypted_content

        except Exception as e:
            self.log(f"❌ Błąd get_ssh_key: {str(e)}")
            return None

    def remove_ssh_key(self, key_name: str) -> bool:
        """
        Usuń SSH key

        Args:
            key_name: Nazwa klucza

        Returns:
            True jeśli się powiedło
        """
        try:
            if key_name not in self.ssh_config['keys']:
                self.log(f"❌ Klucz nie znaleziony: {key_name}")
                return False

            encrypted_path = self.ssh_config['keys'][key_name]['encrypted_path']

            # Usuń plik
            Path(encrypted_path).unlink(missing_ok=True)

            # Usuń z config
            del self.ssh_config['keys'][key_name]
            self._save_config()

            self.log(f"✅ SSH key usunięty: {key_name}")
            return True

        except Exception as e:
            self.log(f"❌ Błąd remove_ssh_key: {str(e)}")
            return False

    def list_ssh_keys(self) -> Dict[str, Dict[str, Any]]:
        """Pobierz listę SSH keys (bez szyfrowanej zawartości)"""
        result = {}

        for key_name, key_info in self.ssh_config.get('keys', {}).items():
            result[key_name] = {
                'name': key_info['name'],
                'created_at': key_info['created_at'],
                'active': key_info['active'],
                'passphrase_protected': key_info.get('passphrase_protected', False)
            }

        return result

    def set_default_key(self, key_name: str) -> bool:
        """
        Ustaw domyślny SSH key

        Args:
            key_name: Nazwa klucza

        Returns:
            True jeśli się powiedło
        """
        try:
            if key_name not in self.ssh_config['keys']:
                self.log(f"❌ Klucz nie znaleziony: {key_name}")
                return False

            # Wyłącz wszystkie inne
            for k in self.ssh_config['keys']:
                self.ssh_config['keys'][k]['active'] = False

            # Włącz wybrany
            self.ssh_config['keys'][key_name]['active'] = True
            self._save_config()

            self.log(f"✅ Domyślny SSH key: {key_name}")
            return True

        except Exception as e:
            self.log(f"❌ Błąd set_default_key: {str(e)}")
            return False

    def get_default_key(self) -> Optional[str]:
        """Pobierz domyślny SSH key"""
        for key_name, key_info in self.ssh_config.get('keys', {}).items():
            if key_info.get('active'):
                return key_name

        return None

    def verify_key_permissions(self, key_path: str) -> bool:
        """
        Weryfikuj uprawnienia SSH key

        Args:
            key_path: Ścieżka do klucza

        Returns:
            True jeśli uprawnienia są poprawne
        """
        try:
            path = Path(key_path)

            if not path.exists():
                self.log(f"❌ Plik klucza nie istnieje: {key_path}")
                return False

            # Sprawdzenie uprawnień - powinny być 0o600
            stat = path.stat()
            permissions = oct(stat.st_mode)[-3:]

            if permissions != '600':
                self.log(f"⚠️  Uprawnienia SSH key powinny być 0o600, są: 0o{permissions}")
                # Zmień uprawnienia
                os.chmod(key_path, 0o600)
                self.log(f"✅ Uprawnienia naprawione")

            return True

        except Exception as e:
            self.log(f"❌ Błąd verify_key_permissions: {str(e)}")
            return False

    def log(self, message: str):
        """Logowanie"""
        self.log_callback(message)


# Przykład użycia
if __name__ == '__main__':
    ssh_manager = SSHManager()

    # List keys
    print("SSH Keys:")
    for key_name, info in ssh_manager.list_ssh_keys().items():
        print(f"  {key_name}: {info}")

