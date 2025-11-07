#!/usr/bin/env python3
"""
Update Scheduler - v5.0 Feature
Harmonogram aktualizacji (Scheduler)

Funkcjonalność:
- ✅ Uruchamianie aktualizacji o określonym czasie
- ✅ Powtarzane aktualizacje (codziennie, co tydzień, itp.)
- ✅ Logging harmonogramu
"""

import schedule
import threading
import time
from datetime import datetime, timedelta
from typing import Callable, Dict, Any, Optional, List
from pathlib import Path
import json
import logging


class UpdateScheduler:
    """Scheduler aktualizacji - v5.0 Feature"""

    CONFIG_FILE = "src/.config/schedule.json"

    def __init__(self, update_callback: Callable, log_callback: Callable = None):
        """
        Inicjalizacja schedulera

        Args:
            update_callback: Funkcja do wywołania dla aktualizacji
            log_callback: Funkcja do logowania (opcjonalnie)
        """
        self.update_callback = update_callback
        self.log_callback = log_callback or print

        self.scheduler = schedule.Scheduler()
        self.is_running = False
        self.scheduler_thread = None
        self.scheduled_jobs: Dict[str, Any] = {}

        self._load_schedule_config()

    def _load_schedule_config(self):
        """Załaduj konfigurację harmonogramu"""
        config_path = Path(self.CONFIG_FILE)
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    self.log(f"📅 Konfiguracja harmonogramu załadowana")
                    return
        except Exception as e:
            self.log(f"⚠️  Błąd załadowania harmonogramu: {str(e)}")

        self.config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Domyślna konfiguracja"""
        return {
            "enabled": False,
            "jobs": []
        }

    def _save_schedule_config(self):
        """Zapisz konfigurację harmonogramu"""
        config_path = Path(self.CONFIG_FILE)
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.log(f"📅 Konfiguracja harmonogramu zapisana")
        except Exception as e:
            self.log(f"⚠️  Błąd zapisu harmonogramu: {str(e)}")

    def log(self, message: str):
        """Logowanie wiadomości"""
        if self.log_callback:
            self.log_callback(f"[SCHEDULER] {message}")

    def add_daily_job(self, hour: int, minute: int = 0, job_name: str = "daily_update"):
        """
        Dodaj codzienną aktualizację

        Args:
            hour: Godzina (0-23)
            minute: Minuta (0-59)
            job_name: Nazwa zadania
        """
        time_str = f"{hour:02d}:{minute:02d}"

        job = self.scheduler.every().day.at(time_str).do(self._run_scheduled_update, job_name)
        self.scheduled_jobs[job_name] = {
            'type': 'daily',
            'time': time_str,
            'next_run': job.next_run.isoformat() if job.next_run else None
        }

        self.log(f"📅 Dodano codzienne aktualizacje o {time_str}")

        # Zapisz konfigurację
        self.config["jobs"].append({
            "name": job_name,
            "type": "daily",
            "time": time_str
        })
        self._save_schedule_config()

    def add_interval_job(self, interval: int, interval_type: str, job_name: str = "interval_update"):
        """
        Dodaj aktualizację co określony interwał

        Args:
            interval: Liczba jednostek (np. 6)
            interval_type: 'hours', 'minutes', 'seconds'
            job_name: Nazwa zadania
        """
        if interval_type == 'hours':
            job = self.scheduler.every(interval).hours.do(self._run_scheduled_update, job_name)
        elif interval_type == 'minutes':
            job = self.scheduler.every(interval).minutes.do(self._run_scheduled_update, job_name)
        elif interval_type == 'seconds':
            job = self.scheduler.every(interval).seconds.do(self._run_scheduled_update, job_name)
        else:
            self.log(f"❌ Nieznany typ interwału: {interval_type}")
            return

        self.scheduled_jobs[job_name] = {
            'type': 'interval',
            'interval': f"{interval} {interval_type}",
            'next_run': job.next_run.isoformat() if job.next_run else None
        }

        self.log(f"📅 Dodano aktualizacje co {interval} {interval_type}")

        # Zapisz konfigurację
        self.config["jobs"].append({
            "name": job_name,
            "type": "interval",
            "interval": interval,
            "interval_type": interval_type
        })
        self._save_schedule_config()

    def _run_scheduled_update(self, job_name: str):
        """Uruchom zaplanowaną aktualizację"""
        self.log(f"⏰ Uruchamianie zaplanowanej aktualizacji: {job_name}")
        try:
            self.update_callback()
            self.log(f"✅ Zaplanowana aktualizacja ({job_name}) zakończona pomyślnie")
        except Exception as e:
            self.log(f"❌ Błąd w zaplanowanej aktualizacji ({job_name}): {str(e)}")

    def start(self):
        """Uruchom scheduler"""
        if self.is_running:
            self.log("⚠️  Scheduler już uruchomiony")
            return

        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        self.log(f"🚀 Scheduler uruchomiony ({len(self.scheduled_jobs)} zadań)")

    def _run_scheduler(self):
        """Główna pętla schedulera"""
        while self.is_running:
            self.scheduler.run_pending()
            time.sleep(1)

    def stop(self):
        """Zatrzymaj scheduler"""
        if not self.is_running:
            self.log("⚠️  Scheduler już zatrzymany")
            return

        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=2)
        self.log("⏹️  Scheduler zatrzymany")

    def clear_jobs(self):
        """Wyczyść wszystkie zadania"""
        self.scheduler.clear()
        self.scheduled_jobs.clear()
        self.config["jobs"] = []
        self._save_schedule_config()
        self.log("🗑️  Wszystkie zadania usunięte")

    def get_next_run_time(self) -> Optional[str]:
        """Pobierz czas następnego uruchomienia"""
        if self.scheduler.jobs:
            return self.scheduler.idle_seconds

        return None

    def get_jobs_info(self) -> List[Dict[str, Any]]:
        """Pobierz informacje o zaplanowanych zadaniach"""
        jobs_info = []
        for job in self.scheduler.jobs:
            jobs_info.append({
                'name': str(job.job_func),
                'next_run': job.next_run.isoformat() if job.next_run else None,
                'at_time': job.at_time if hasattr(job, 'at_time') else None
            })
        return jobs_info

