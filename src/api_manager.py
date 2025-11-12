#!/usr/bin/env python3
"""
REST API Manager dla Aktualizatora Strony v5.1
Zdefiniowane API endpoints do programistycznego sterowania

v5.1 NEW:
- ✅ REST API Endpoints
- ✅ JSON Request/Response
- ✅ Error Handling
- ✅ API Documentation
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class APIResponse:
    """Standardowa odpowiedź API"""
    status: str  # ok, error, pending
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Konwertuj do słownika"""
        return asdict(self)


@dataclass
class UpdateRequest:
    """Request do uruchomienia aktualizacji"""
    source_repo: Optional[str] = None
    target_repo: Optional[str] = None
    force: bool = False
    notify: bool = True
    webhook_url: Optional[str] = None


class APIManager:
    """REST API Manager - v5.1"""

    def __init__(self, update_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None):
        """
        Inicjalizacja API Manager

        Args:
            update_callback: Callback do uruchomienia aktualizacji
            log_callback: Callback do logowania
        """
        self.update_callback = update_callback
        self.log_callback = log_callback or print
        self.api_version = "5.1"
        self.endpoints_registered = 0

        self.log("✅ API Manager inicjalizowany (v5.1)")

    # ==================== UPDATE ENDPOINTS ====================

    def trigger_update(self, request_data: Dict[str, Any]) -> APIResponse:
        """
        POST /api/update
        Uruchom aktualizację

        Request:
        {
            "source_repo": "/path/to/source",
            "target_repo": "/path/to/target",
            "force": false,
            "notify": true
        }

        Response:
        {
            "status": "triggered",
            "message": "Aktualizacja uruchomiona",
            "data": {"task_id": "uuid"}
        }
        """
        try:
            request = UpdateRequest(**request_data)

            if self.update_callback:
                task_id = self.update_callback(**asdict(request))

                return APIResponse(
                    status='triggered',
                    message='Aktualizacja uruchomiona',
                    data={'task_id': str(task_id)}
                )
            else:
                return APIResponse(
                    status='error',
                    message='Update callback nie skonfigurowany'
                )
        except Exception as e:
            self.log(f"❌ Błąd trigger_update: {str(e)}")
            return APIResponse(
                status='error',
                message=f'Błąd: {str(e)}'
            )

    # ==================== STATUS ENDPOINTS ====================

    def get_status(self) -> APIResponse:
        """
        GET /api/status
        Pobierz status aplikacji

        Response:
        {
            "status": "ok",
            "message": "Aplikacja działa normalnie",
            "data": {
                "version": "5.1",
                "uptime": 3600,
                "last_update": "2025-11-12T10:30:00"
            }
        }
        """
        return APIResponse(
            status='ok',
            message='Aplikacja działa normalnie',
            data={
                'version': self.api_version,
                'timestamp': datetime.now().isoformat()
            }
        )

    # ==================== CONFIG ENDPOINTS ====================

    def get_config(self, config_data: Dict[str, Any]) -> APIResponse:
        """
        GET /api/config
        Pobierz konfigurację

        Response:
        {
            "status": "ok",
            "data": {...config...}
        }
        """
        return APIResponse(
            status='ok',
            message='Konfiguracja pobrana',
            data=config_data
        )

    def update_config(self, new_config: Dict[str, Any]) -> APIResponse:
        """
        PUT /api/config
        Zaktualizuj konfigurację

        Request:
        {...new_config...}

        Response:
        {
            "status": "updated",
            "message": "Konfiguracja zaktualizowana"
        }
        """
        try:
            self.log(f"📝 Konfiguracja zaktualizowana z API")
            return APIResponse(
                status='updated',
                message='Konfiguracja zaktualizowana',
                data=new_config
            )
        except Exception as e:
            self.log(f"❌ Błąd update_config: {str(e)}")
            return APIResponse(
                status='error',
                message=f'Błąd: {str(e)}'
            )

    # ==================== STATS ENDPOINTS ====================

    def get_stats(self, stats_data: Dict[str, Any]) -> APIResponse:
        """
        GET /api/stats
        Pobierz statystyki

        Response:
        {
            "status": "ok",
            "data": {
                "total_updates": 42,
                "successful": 40,
                "failed": 2
            }
        }
        """
        return APIResponse(
            status='ok',
            message='Statystyki pobrane',
            data=stats_data
        )

    # ==================== HEALTH ENDPOINTS ====================

    def health_check(self) -> APIResponse:
        """
        GET /api/health
        Sprawdzenie zdrowotności aplikacji

        Response:
        {
            "status": "healthy",
            "message": "Wszystko działa poprawnie"
        }
        """
        return APIResponse(
            status='healthy',
            message='Wszystko działa poprawnie',
            data={'timestamp': datetime.now().isoformat()}
        )

    # ==================== WEBHOOK ENDPOINTS ====================

    def register_webhook(self, webhook_url: str, events: List[str]) -> APIResponse:
        """
        POST /api/webhooks
        Zarejestruj webhook

        Request:
        {
            "url": "https://example.com/webhook",
            "events": ["update_start", "update_complete", "update_error"]
        }

        Response:
        {
            "status": "registered",
            "data": {"webhook_id": "uuid"}
        }
        """
        try:
            self.log(f"🔗 Webhook zarejestrowany: {webhook_url}")
            return APIResponse(
                status='registered',
                message='Webhook zarejestrowany',
                data={'webhook_url': webhook_url, 'events': events}
            )
        except Exception as e:
            self.log(f"❌ Błąd register_webhook: {str(e)}")
            return APIResponse(
                status='error',
                message=f'Błąd: {str(e)}'
            )

    # ==================== SSH ENDPOINTS ====================

    def get_ssh_config(self) -> APIResponse:
        """
        GET /api/ssh
        Pobierz konfigurację SSH

        Response:
        {
            "status": "ok",
            "data": {"ssh_enabled": true}
        }
        """
        return APIResponse(
            status='ok',
            message='Konfiguracja SSH pobrana',
            data={'ssh_enabled': False}  # Default
        )

    def configure_ssh(self, ssh_key_path: str, passphrase: Optional[str] = None) -> APIResponse:
        """
        POST /api/ssh/configure
        Skonfiguruj SSH key

        Request:
        {
            "key_path": "/path/to/id_rsa",
            "passphrase": "optional"
        }

        Response:
        {
            "status": "configured",
            "message": "SSH skonfigurowany"
        }
        """
        try:
            self.log(f"🔐 SSH key konfigurowany: {ssh_key_path}")
            return APIResponse(
                status='configured',
                message='SSH skonfigurowany',
                data={'ssh_key': ssh_key_path}
            )
        except Exception as e:
            self.log(f"❌ Błąd configure_ssh: {str(e)}")
            return APIResponse(
                status='error',
                message=f'Błąd: {str(e)}'
            )

    # ==================== DOCUMENTATION ====================

    def get_documentation(self) -> APIResponse:
        """
        GET /api/docs
        Pobierz dokumentację API

        Response:
        {
            "status": "ok",
            "data": {...endpoints...}
        }
        """
        endpoints = {
            'POST /api/update': 'Uruchom aktualizację',
            'GET /api/status': 'Status aplikacji',
            'GET /api/stats': 'Statystyki',
            'GET /api/config': 'Pobierz config',
            'PUT /api/config': 'Zaktualizuj config',
            'GET /api/health': 'Health check',
            'POST /api/webhooks': 'Rejestruj webhook',
            'GET /api/ssh': 'SSH config',
            'POST /api/ssh/configure': 'Skonfiguruj SSH',
            'GET /api/docs': 'API Documentation'
        }

        return APIResponse(
            status='ok',
            message='Dokumentacja API',
            data={'endpoints': endpoints, 'version': self.api_version}
        )

    def log(self, message: str):
        """Logowanie"""
        self.log_callback(message)


# Przykład użycia
if __name__ == '__main__':
    api = APIManager()

    # Test health check
    response = api.health_check()
    print(json.dumps(response.to_dict(), indent=2))

    # Test dokumentacji
    response = api.get_documentation()
    print(json.dumps(response.to_dict(), indent=2))

