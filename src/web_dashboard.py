#!/usr/bin/env python3
"""
Web Dashboard dla Aktualizatora Strony v5.1
Flask-based web panel do zarządzania aplikacją z przeglądarki

v5.1 NEW:
- ✅ Flask Web Server
- ✅ Real-time WebSocket Updates
- ✅ REST API Endpoints
- ✅ Responsive Web UI
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from pathlib import Path
from typing import Dict, Any, Callable, Optional
from datetime import datetime
import threading
from logging import getLogger

logger = getLogger(__name__)


class WebDashboard:
    """Web Dashboard Server - v5.1"""

    def __init__(self,
                 host: str = "127.0.0.1",
                 port: int = 5000,
                 update_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None):
        """
        Inicjalizacja Web Dashboard

        Args:
            host: Host do nasłuchiwania
            port: Port do nasłuchiwania
            update_callback: Callback dla aktualizacji
            log_callback: Callback dla logowania
        """
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'aktualizator-strony-secret-v5.1'
        CORS(self.app)

        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.host = host
        self.port = port
        self.update_callback = update_callback
        self.log_callback = log_callback or print
        self.is_running = False
        self.server_thread = None

        # Statystyki
        self.stats = {
            'total_updates': 0,
            'successful_updates': 0,
            'failed_updates': 0,
            'no_changes_updates': 0,
            'total_cards_added': 0,
            'total_cards_removed': 0,
            'total_execution_time': 0.0
        }

        self._setup_routes()
        self._setup_websocket_handlers()

        self.log("✅ Web Dashboard inicjalizowany (v5.1)")

    def _setup_routes(self):
        """Konfiguracja Flask routes"""

        @self.app.route('/')
        def index():
            """Główna strona"""
            return jsonify({
                'status': 'ok',
                'version': '5.1',
                'message': 'Aktualizator Strony Web Dashboard',
                'endpoints': {
                    'GET /api/stats': 'Pobierz statystyki',
                    'GET /api/status': 'Status aplikacji',
                    'POST /api/update': 'Uruchom aktualizację',
                    'GET /api/config': 'Pobierz konfigurację',
                    'POST /api/config': 'Zaktualizuj konfigurację',
                    'WebSocket': 'Połączenie WebSocket na /'
                }
            })

        @self.app.route('/api/stats')
        def get_stats():
            """Pobierz statystyki"""
            return jsonify(self.stats)

        @self.app.route('/api/status')
        def get_status():
            """Status aplikacji"""
            return jsonify({
                'running': self.is_running,
                'timestamp': datetime.now().isoformat(),
                'version': '5.1'
            })

        @self.app.route('/api/update', methods=['POST'])
        def trigger_update():
            """Uruchom aktualizację"""
            try:
                data = request.get_json()

                if self.update_callback:
                    threading.Thread(
                        target=self.update_callback,
                        kwargs=data or {},
                        daemon=True
                    ).start()

                    return jsonify({
                        'status': 'triggered',
                        'message': 'Aktualizacja uruchomiona'
                    }), 202
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Update callback nie skonfigurowany'
                    }), 500

            except Exception as e:
                self.log(f"❌ Błąd trigger update: {str(e)}")
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 500

        @self.app.route('/api/config', methods=['GET'])
        def get_config():
            """Pobierz konfigurację"""
            try:
                config_path = Path('config.json')
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    return jsonify(config)
                return jsonify({}), 404
            except Exception as e:
                self.log(f"❌ Błąd get_config: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/config', methods=['POST'])
        def update_config():
            """Zaktualizuj konfigurację"""
            try:
                data = request.get_json()
                config_path = Path('config.json')

                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                self.log("✅ Konfiguracja zaktualizowana z API")
                self.socketio.emit('config_updated', data, broadcast=True)

                return jsonify({
                    'status': 'updated',
                    'message': 'Konfiguracja zaktualizowana'
                })
            except Exception as e:
                self.log(f"❌ Błąd update_config: {str(e)}")
                return jsonify({'error': str(e)}), 500

    def _setup_websocket_handlers(self):
        """Konfiguracja WebSocket handlers"""

        @self.socketio.on('connect')
        def handle_connect():
            """Klient się połączył"""
            self.log("✅ Klient połączony do Web Dashboard")
            emit('connected', {'data': 'Połączono z dashboardem'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Klient się rozłączył"""
            self.log("❌ Klient rozłączony z Web Dashboard")

        @self.socketio.on('request_stats')
        def handle_request_stats():
            """Klient żąda statystyk"""
            emit('stats_update', self.stats, broadcast=True)

    def start(self):
        """Uruchom Web Dashboard"""
        if self.is_running:
            self.log("⚠️  Web Dashboard już uruchomiony")
            return

        self.is_running = True
        self.server_thread = threading.Thread(
            target=lambda: self.socketio.run(
                self.app,
                host=self.host,
                port=self.port,
                debug=False
            ),
            daemon=True
        )
        self.server_thread.start()
        self.log(f"🚀 Web Dashboard uruchomiony: http://{self.host}:{self.port}")

    def stop(self):
        """Zatrzymaj Web Dashboard"""
        if not self.is_running:
            return

        self.is_running = False
        self.log("⏹️  Web Dashboard zatrzymany")

    def broadcast_update(self, data: Dict[str, Any]):
        """Wyślij update do wszystkich połączonych klientów"""
        if self.is_running:
            self.socketio.emit('update_progress', data, broadcast=True)

    def broadcast_log(self, message: str):
        """Wyślij log do wszystkich klientów"""
        if self.is_running:
            self.socketio.emit('log_message', {
                'timestamp': datetime.now().isoformat(),
                'message': message
            }, broadcast=True)

    def update_stats(self, stats: Dict[str, Any]):
        """Zaktualizuj statystyki"""
        self.stats.update(stats)
        self.broadcast_update({'stats': self.stats})

    def log(self, message: str):
        """Logowanie"""
        self.log_callback(message)


# Przykład użycia
if __name__ == '__main__':
    dashboard = WebDashboard()
    dashboard.start()

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        dashboard.stop()

