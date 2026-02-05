import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

class WorldometerScraper:
    def __init__(self):
        self.url = "https://www.worldometers.info/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.log_path = "data/logs/worldometer_live.json"

    def fetch_data(self):
        """Menarik data terkini dari Worldometer."""
        print(f"[{datetime.now()}] Memulakan imbasan Worldometer...")
        
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Mencari elemen-elemen rts-counter (Real Time Statistics)
            # Nota: ID ini berdasarkan struktur Worldometer 2026
            data = {
                "timestamp": datetime.now().isoformat(),
                "status": "VALIDATED",
                "metrics": {
                    "current_population": self._get_counter(soup, "current_population"),
                    "births_today": self._get_counter(soup, "births_today"),
                    "deaths_today": self._get_counter(soup, "deaths_today"),
                    "public_healthcare_spending": self._get_counter(soup, "health_spending"),
                    "public_education_spending": self._get_counter(soup, "edu_spending"),
                    "military_spending_today": self._get_counter(soup, "mil_spending"),
                    "co2_emissions_tons": self._get_counter(soup, "co2_emissions"),
                    "forest_loss_hectares": self._get_counter(soup, "forest_loss")
                }
            }

            self._save_to_json(data)
            print(f"[{datetime.now()}] Data berjaya dikemas kini.")
            return data

        except Exception as e:
            print(f"❗ RALAT: Gagal menarik data - {str(e)}")
            return None

    def _get_counter(self, soup, rel_name):
        """Mengekstrak teks dari span berdasarkan atribut 'rel'."""
        element = soup.find("span", {"rel": rel_name})
        if element:
            # Membersihkan koma dan simbol untuk tujuan pengiraan (validation)
            clean_val = element.text.strip().replace(",", "")
            return clean_val
        return "N/A"

    def _save_to_json(self, data):
        """Menyimpan hasil ke dalam folder data/logs/."""
        # Memastikan folder wujud
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        with open(self.log_path, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    # Jalankan ujian skrip
    scraper = WorldometerScraper()
    result = scraper.fetch_data()
    if result:
        print("\n--- LIVE DATA SUMMARY 2026 ---")
        for key, value in result['metrics'].items():
            print(f"{key.replace('_', ' ').title()}: {value}")
