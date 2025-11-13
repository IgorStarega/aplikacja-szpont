#!/usr/bin/env python3
"""
Mobile API Manager - v5.2 Feature
REST API dla aplikacji mobilnej

Funkcjonalność:
- ✅ Endpoints dla aplikacji mobilnej
- ✅ Autoryzacja API Key
- ✅ Status aktualizacji
- ✅ Zdalne uruchamianie aktualizacji
- ✅ Historia i statystyki
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Callable, Optional
from functools import wraps
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
import json


class MobileAPIManager:
    """Manager API dla aplikacji mobilnej - v5.2 Feature"""

    API_KEYS_FILE = "src/.config/api_keys.json"
    DEFAULT_PORT = 8080

    def __init__(self,
                 update_callback: Callable = None,
                 status_callback: Callable = None,
                 log_callback: Callable = None):
        """
        Inicjalizacja Mobile API Manager

        Args:
            update_callback: Funkcja do uruchamiania aktualizacji
            status_callback: Funkcja do pobierania statusu
            log_callback: Funkcja do logowania
        """
        self.update_callback = update_callback
        self.status_callback = status_callback
        self.log_callback = log_callback or print

        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS dla aplikacji mobilnej

        self.api_keys = self._load_api_keys()
        self._setup_routes()

    def log(self, message: str):
        """Logowanie wiadomości"""
        if self.log_callback:
            self.log_callback(f"[MOBILE-API] {message}")

    def _load_api_keys(self) -> Dict[str, Dict]:
        """Załaduj klucze API"""
        api_keys_path = Path(self.API_KEYS_FILE)
        try:
            if api_keys_path.exists():
                with open(api_keys_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}

    def _save_api_keys(self):
        """Zapisz klucze API"""
        api_keys_path = Path(self.API_KEYS_FILE)
        try:
            api_keys_path.parent.mkdir(parents=True, exist_ok=True)
            with open(api_keys_path, 'w', encoding='utf-8') as f:
                json.dump(self.api_keys, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Błąd zapisu kluczy API: {e}")

    def generate_api_key(self, name: str = "mobile_app") -> str:
        """
        Generuj nowy klucz API

        Args:
            name: Nazwa klucza (np. "mobile_app", "web_client")

        Returns:
            Nowy klucz API
        """
        api_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        self.api_keys[key_hash] = {
            "name": name,
            "created": datetime.now().isoformat(),
            "last_used": None,
            "requests_count": 0
        }

        self._save_api_keys()
        self.log(f"✅ Wygenerowano nowy klucz API: {name}")
        return api_key

    def revoke_api_key(self, api_key: str) -> bool:
        """
        Unieważnij klucz API

        Args:
            api_key: Klucz do unieważnienia

        Returns:
            True jeśli sukces
        """
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        if key_hash in self.api_keys:
            del self.api_keys[key_hash]
            self._save_api_keys()
            self.log(f"✅ Unieważniono klucz API")
            return True
        return False

    def require_api_key(self, f):
        """Dekorator wymagający klucza API"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')

            if not api_key:
                return jsonify({
                    'error': 'Missing API key',
                    'message': 'Provide X-API-Key header'
                }), 401

            key_hash = hashlib.sha256(api_key.encode()).hexdigest()

            if key_hash not in self.api_keys:
                return jsonify({
                    'error': 'Invalid API key',
                    'message': 'API key not recognized'
                }), 401

            # Zaktualizuj statystyki
            self.api_keys[key_hash]['last_used'] = datetime.now().isoformat()
            self.api_keys[key_hash]['requests_count'] += 1
            self._save_api_keys()

            return f(*args, **kwargs)

        return decorated_function

    def _setup_routes(self):
        """Konfiguruj endpointy API"""

        @self.app.route('/api/v1/health', methods=['GET'])
        def health():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'version': '5.2.0',
                'timestamp': datetime.now().isoformat()
            })

        @self.app.route('/api/v1/status', methods=['GET'])
        @self.require_api_key
        def status():
            """Pobierz status aplikacji"""
            try:
                if self.status_callback:
                    status_data = self.status_callback()
                else:
                    status_data = {
                        'status': 'unknown',
                        'message': 'Status callback not configured'
                    }

                return jsonify({
                    'success': True,
                    'data': status_data,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/v1/update', methods=['POST'])
        @self.require_api_key
        def trigger_update():
            """Uruchom aktualizację"""
            try:
                if not self.update_callback:
                    return jsonify({
                        'success': False,
                        'error': 'Update callback not configured'
                    }), 500

                # Uruchom aktualizację w tle
                import threading
                thread = threading.Thread(target=self.update_callback, daemon=True)
                thread.start()

                return jsonify({
                    'success': True,
                    'message': 'Update started',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/v1/history', methods=['GET'])
        @self.require_api_key
        def get_history():
            """Pobierz historię aktualizacji"""
            try:
                # Limit z query params
                limit = request.args.get('limit', 10, type=int)

                # Tutaj można zintegrować z DatabaseManager
                history = []  # Placeholder

                return jsonify({
                    'success': True,
                    'data': {
                        'history': history,
                        'count': len(history)
                    },
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/v1/stats', methods=['GET'])
        @self.require_api_key
        def get_statistics():
            """Pobierz statystyki"""
            try:
                # Tutaj można zintegrować z DatabaseManager
                stats = {
                    'total_updates': 0,
                    'successful': 0,
                    'failed': 0,
                    'last_update': None
                }

                return jsonify({
                    'success': True,
                    'data': stats,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        @self.app.route('/api/v1/config', methods=['GET'])
        @self.require_api_key
        def get_config():
            """Pobierz konfigurację (bezpieczną)"""
            try:
                # Zwróć tylko bezpieczne dane konfiguracji
                safe_config = {
                    'version': '5.2.0',
                    'features': [
                        'batch_processing',
                        'caching',
                        'async_git',
                        'analytics',
                        'reports',
                        'scheduler',
                        'notifications',
                        'web_dashboard',
                        'api',
                        'webhooks',
                        'auto_update',
                        'mobile_api'
                    ]
                }

                return jsonify({
                    'success': True,
                    'data': safe_config,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

    def start(self, host: str = '0.0.0.0', port: int = None, debug: bool = False):
        """
        Uruchom API server

        Args:
            host: Host (domyślnie 0.0.0.0 dla dostępu z sieci)
            port: Port (domyślnie 8080)
            debug: Tryb debug
        """
        if port is None:
            port = self.DEFAULT_PORT

        self.log(f"🚀 Uruchamianie Mobile API na {host}:{port}")
        self.app.run(host=host, port=port, debug=debug, threaded=True)

    def start_background(self, host: str = '0.0.0.0', port: int = None):
        """
        Uruchom API server w tle

        Args:
            host: Host
            port: Port
        """
        import threading

        if port is None:
            port = self.DEFAULT_PORT

        thread = threading.Thread(
            target=self.start,
            args=(host, port, False),
            daemon=True
        )
        thread.start()

        self.log(f"✅ Mobile API uruchomione w tle na {host}:{port}")

