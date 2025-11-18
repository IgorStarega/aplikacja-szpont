"""
Visualization Manager dla Aktualizatora Strony v5.3.0
Interaktywne wykresy i wizualizacje

Funkcje:
- Wykresy trendów aktualizacji
- Heatmapy aktywności
- Interaktywne dashboardy (plotly)
- Export wykresów (PNG/PDF)
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json


class VisualizationManager:
    """Zarządzanie wizualizacjami i wykresami"""

    def __init__(self, database_manager=None):
        """
        Inicjalizacja Visualization Manager

        Args:
            database_manager: Opcjonalny DatabaseManager dla danych
        """
        self.db_manager = database_manager
        self.cache_path = Path.cwd() / "cache" / "visualizations"
        self.cache_path.mkdir(parents=True, exist_ok=True)

    def generate_trend_chart(
        self,
        days: int = 30,
        output_path: Path = None,
        use_plotly: bool = False
    ) -> Optional[str]:
        """
        Generuj wykres trendów aktualizacji

        Args:
            days: Ile dni wstecz
            output_path: Gdzie zapisać (opcjonalnie)
            use_plotly: Użyj plotly zamiast matplotlib

        Returns:
            Ścieżka do wygenerowanego wykresu
        """
        if not self.db_manager:
            print("⚠️  Brak połączenia z bazą danych")
            return None

        # Pobierz dane
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Symulacja danych (w rzeczywistości z bazy)
        dates = []
        counts = []

        for i in range(days):
            date = start_date + timedelta(days=i)
            dates.append(date.strftime("%Y-%m-%d"))
            # W rzeczywistości: zapytanie do DB
            counts.append(i % 5 + 1)  # Symulacja

        if use_plotly:
            return self._create_plotly_line_chart(dates, counts, output_path)
        else:
            return self._create_matplotlib_line_chart(dates, counts, output_path)

    def _create_matplotlib_line_chart(
        self,
        dates: List[str],
        values: List[int],
        output_path: Path = None
    ) -> str:
        """Stwórz wykres liniowy (matplotlib)"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            from matplotlib.figure import Figure

            fig, ax = plt.subplots(figsize=(12, 6))

            # Konwertuj daty
            date_objects = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

            # Plot
            ax.plot(date_objects, values, marker='o', linewidth=2,
                   color='#1f77b4', label='Aktualizacje')

            # Formatowanie
            ax.set_xlabel('Data', fontsize=12)
            ax.set_ylabel('Liczba aktualizacji', fontsize=12)
            ax.set_title('Trend aktualizacji w czasie', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()

            # Format osi X
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate()

            # Zapisz
            if not output_path:
                output_path = self.cache_path / f"trend_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return str(output_path)

        except ImportError:
            print("⚠️  Matplotlib nie zainstalowane")
            return None
        except Exception as e:
            print(f"❌ Błąd tworzenia wykresu: {e}")
            return None

    def _create_plotly_line_chart(
        self,
        dates: List[str],
        values: List[int],
        output_path: Path = None
    ) -> str:
        """Stwórz interaktywny wykres (plotly)"""
        try:
            import plotly.graph_objs as go
            import plotly.io as pio

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=dates,
                y=values,
                mode='lines+markers',
                name='Aktualizacje',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=8)
            ))

            fig.update_layout(
                title='Trend aktualizacji w czasie',
                xaxis_title='Data',
                yaxis_title='Liczba aktualizacji',
                hovermode='x unified',
                template='plotly_white'
            )

            # Zapisz
            if not output_path:
                output_path = self.cache_path / f"trend_interactive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

            pio.write_html(fig, str(output_path))

            return str(output_path)

        except ImportError:
            print("⚠️  Plotly nie zainstalowane")
            return None
        except Exception as e:
            print(f"❌ Błąd tworzenia wykresu: {e}")
            return None

    def generate_heatmap(
        self,
        days: int = 30,
        output_path: Path = None
    ) -> Optional[str]:
        """
        Generuj heatmapę aktywności (dni x godziny)

        Args:
            days: Ile dni wstecz
            output_path: Gdzie zapisać

        Returns:
            Ścieżka do wykresu
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np

            # Symulacja danych (7 dni x 24 godziny)
            data = np.random.randint(0, 10, size=(7, 24))

            fig, ax = plt.subplots(figsize=(14, 6))

            im = ax.imshow(data, cmap='YlOrRd', aspect='auto')

            # Etykiety
            days_labels = ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob', 'Niedz']
            hours_labels = [f'{h:02d}:00' for h in range(24)]

            ax.set_xticks(range(24))
            ax.set_yticks(range(7))
            ax.set_xticklabels(hours_labels, rotation=45)
            ax.set_yticklabels(days_labels)

            ax.set_xlabel('Godzina', fontsize=12)
            ax.set_ylabel('Dzień tygodnia', fontsize=12)
            ax.set_title('Heatmapa aktywności', fontsize=14, fontweight='bold')

            # Colorbar
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label('Liczba aktualizacji', rotation=270, labelpad=20)

            # Zapisz
            if not output_path:
                output_path = self.cache_path / f"heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return str(output_path)

        except ImportError:
            print("⚠️  Matplotlib/numpy nie zainstalowane")
            return None
        except Exception as e:
            print(f"❌ Błąd tworzenia heatmapy: {e}")
            return None

    def generate_pie_chart(
        self,
        data: Dict[str, int],
        title: str = "Rozkład",
        output_path: Path = None
    ) -> Optional[str]:
        """
        Generuj wykres kołowy

        Args:
            data: Dict z danymi (kategoria -> wartość)
            title: Tytuł wykresu
            output_path: Gdzie zapisać

        Returns:
            Ścieżka do wykresu
        """
        try:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(10, 8))

            labels = list(data.keys())
            sizes = list(data.values())
            colors = plt.cm.Set3(range(len(labels)))

            # Explode pierwszy segment
            explode = [0.1] + [0] * (len(labels) - 1)

            ax.pie(
                sizes,
                explode=explode,
                labels=labels,
                colors=colors,
                autopct='%1.1f%%',
                shadow=True,
                startangle=90
            )

            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.axis('equal')

            # Zapisz
            if not output_path:
                output_path = self.cache_path / f"pie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return str(output_path)

        except ImportError:
            print("⚠️  Matplotlib nie zainstalowane")
            return None
        except Exception as e:
            print(f"❌ Błąd tworzenia wykresu kołowego: {e}")
            return None

    def generate_bar_chart(
        self,
        categories: List[str],
        values: List[int],
        title: str = "Statystyki",
        output_path: Path = None
    ) -> Optional[str]:
        """
        Generuj wykres słupkowy

        Args:
            categories: Lista kategorii
            values: Lista wartości
            title: Tytuł
            output_path: Gdzie zapisać

        Returns:
            Ścieżka do wykresu
        """
        try:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(12, 6))

            bars = ax.bar(categories, values, color='#1f77b4', alpha=0.7)

            # Dodaj wartości na słupkach
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{int(height)}',
                    ha='center',
                    va='bottom'
                )

            ax.set_xlabel('Kategoria', fontsize=12)
            ax.set_ylabel('Wartość', fontsize=12)
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')

            # Obróć etykiety jeśli długie
            plt.xticks(rotation=45, ha='right')

            # Zapisz
            if not output_path:
                output_path = self.cache_path / f"bar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return str(output_path)

        except ImportError:
            print("⚠️  Matplotlib nie zainstalowane")
            return None
        except Exception as e:
            print(f"❌ Błąd tworzenia wykresu słupkowego: {e}")
            return None

    def clear_cache(self):
        """Wyczyść cache wykresów"""
        for file in self.cache_path.glob("*.png"):
            file.unlink()
        for file in self.cache_path.glob("*.html"):
            file.unlink()
        print("✅ Cache wykresów wyczyszczony")


# ===== PRZYKŁAD UŻYCIA =====
if __name__ == "__main__":
    # Inicjalizacja
    vm = VisualizationManager()

    # Wykres trendów (matplotlib)
    print("📊 Generuję wykres trendów (matplotlib)...")
    path1 = vm.generate_trend_chart(days=30, use_plotly=False)
    if path1:
        print(f"✅ Wykres zapisany: {path1}")

    # Heatmapa
    print("\n🔥 Generuję heatmapę aktywności...")
    path2 = vm.generate_heatmap()
    if path2:
        print(f"✅ Heatmapa zapisana: {path2}")

    # Wykres kołowy
    print("\n🥧 Generuję wykres kołowy...")
    data = {
        "HTML": 45,
        "CSS": 25,
        "JavaScript": 20,
        "Obrazy": 10
    }
    path3 = vm.generate_pie_chart(data, title="Rozkład typów plików")
    if path3:
        print(f"✅ Wykres kołowy zapisany: {path3}")

    # Wykres słupkowy
    print("\n📊 Generuję wykres słupkowy...")
    categories = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj"]
    values = [12, 19, 15, 22, 18]
    path4 = vm.generate_bar_chart(categories, values, title="Aktualizacje per miesiąc")
    if path4:
        print(f"✅ Wykres słupkowy zapisany: {path4}")

    print("\n✨ Wszystkie wykresy wygenerowane!")

