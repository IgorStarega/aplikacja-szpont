#!/usr/bin/env python3
"""
Database Manager - v5.0 Feature
SQLite Historia Aktualizacji + Analytics

Funkcjonalność:
- ✅ Przechowywanie historii aktualizacji w SQLite
- ✅ Analityka zmian (trendy, statystyki)
- ✅ Szybkie zapytania do bazy
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

Base = declarative_base()


class UpdateHistory(Base):
    """Model historii aktualizacji"""
    __tablename__ = 'update_history'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    status = Column(String)  # 'success', 'failed', 'no_changes'
    duration_seconds = Column(Integer)
    folders_updated = Column(JSON)  # Lista zmienonych folderów
    added_count = Column(Integer, default=0)
    modified_count = Column(Integer, default=0)
    removed_count = Column(Integer, default=0)
    cache_used = Column(Boolean, default=False)
    error_message = Column(String, nullable=True)

    def __repr__(self):
        return f"<UpdateHistory({self.timestamp}, {self.status})>"


class DatabaseManager:
    """Manager bazy danych - v5.0 Feature"""

    DB_FILE = "src/.data/updates.db"

    def __init__(self, db_path: str = DB_FILE):
        """Inicjalizacja database manager'a"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)

        # Utwórz połączenie
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

    def add_update_record(self, status: str, duration: int, folders: List[str],
                         added: int = 0, modified: int = 0, removed: int = 0,
                         cache_used: bool = False, error: Optional[str] = None) -> int:
        """
        Dodaj wpis do historii aktualizacji

        Args:
            status: 'success', 'failed', 'no_changes'
            duration: Czas trwania w sekundach
            folders: Lista zaktualizowanych folderów
            added: Liczba dodanych kart
            modified: Liczba zmodyfikowanych kart
            removed: Liczba usunętych kart
            cache_used: Czy użyto cache'a
            error: Komunikat błędu (jeśli status = 'failed')

        Returns:
            ID nowego rekordu
        """
        session = self.Session()
        try:
            record = UpdateHistory(
                status=status,
                duration_seconds=duration,
                folders_updated=folders,
                added_count=added,
                modified_count=modified,
                removed_count=removed,
                cache_used=cache_used,
                error_message=error
            )
            session.add(record)
            session.commit()
            record_id = record.id
            session.close()
            return record_id
        except Exception as e:
            session.rollback()
            session.close()
            raise e

    def get_recent_updates(self, days: int = 7, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Pobierz ostatnie aktualizacje

        Args:
            days: Liczba dni do przejrzenia
            limit: Maksymalna liczba wyników

        Returns:
            Lista słowników z danymi aktualizacji
        """
        session = self.Session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            records = session.query(UpdateHistory)\
                .filter(UpdateHistory.timestamp >= cutoff_date)\
                .order_by(UpdateHistory.timestamp.desc())\
                .limit(limit)\
                .all()

            result = []
            for record in records:
                result.append({
                    'id': record.id,
                    'timestamp': record.timestamp.isoformat(),
                    'status': record.status,
                    'duration': record.duration_seconds,
                    'folders': record.folders_updated,
                    'added': record.added_count,
                    'modified': record.modified_count,
                    'removed': record.removed_count,
                    'cache_used': record.cache_used,
                    'error': record.error_message
                })
            return result
        finally:
            session.close()

    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """
        Oblicz statystyki z ostatnich N dni

        Args:
            days: Liczba dni do przeanalizowania

        Returns:
            Słownik ze statystykami
        """
        session = self.Session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            records = session.query(UpdateHistory)\
                .filter(UpdateHistory.timestamp >= cutoff_date)\
                .all()

            if not records:
                return {
                    'total_updates': 0,
                    'successful': 0,
                    'failed': 0,
                    'no_changes': 0,
                    'total_cards_added': 0,
                    'total_cards_modified': 0,
                    'total_cards_removed': 0,
                    'avg_duration': 0,
                    'cache_usage_percent': 0
                }

            stats = {
                'total_updates': len(records),
                'successful': len([r for r in records if r.status == 'success']),
                'failed': len([r for r in records if r.status == 'failed']),
                'no_changes': len([r for r in records if r.status == 'no_changes']),
                'total_cards_added': sum(r.added_count for r in records),
                'total_cards_modified': sum(r.modified_count for r in records),
                'total_cards_removed': sum(r.removed_count for r in records),
                'avg_duration': sum(r.duration_seconds for r in records) // len(records) if records else 0,
                'cache_usage_percent': (len([r for r in records if r.cache_used]) / len(records) * 100) if records else 0
            }
            return stats
        finally:
            session.close()

    def get_folder_statistics(self, days: int = 30) -> Dict[str, int]:
        """
        Statystyki per folder

        Args:
            days: Liczba dni do przeanalizowania

        Returns:
            Słownik z liczbą aktualizacji per folder
        """
        session = self.Session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            records = session.query(UpdateHistory)\
                .filter(UpdateHistory.timestamp >= cutoff_date)\
                .all()

            folder_stats = {}
            for record in records:
                if record.folders_updated:
                    for folder in record.folders_updated:
                        folder_stats[folder] = folder_stats.get(folder, 0) + 1

            return folder_stats
        finally:
            session.close()

    def cleanup_old_records(self, days: int = 90) -> int:
        """
        Usuń stare rekordy z bazy

        Args:
            days: Usuń rekordy starsze niż N dni

        Returns:
            Liczba usuniętych rekordów
        """
        session = self.Session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            deleted = session.query(UpdateHistory)\
                .filter(UpdateHistory.timestamp < cutoff_date)\
                .delete()
            session.commit()
            return deleted
        finally:
            session.close()

