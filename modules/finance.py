import json
from datetime import datetime

class FinanceModule:
    def __init__(self):
        # Data Anggaran Bajet 2026 (Contoh rujukan)
        self.annual_budgets = {
            "Malaysia": 393800000000, # RM 393.8 Bilion (Bajet 2026 est)
            "USA": 6900000000000,     # USD 6.9 Trilion
            "Global": 105000000000000  # USD 105 Trilion (Global GDP/Spend)
        }
        self.seconds_in_year = 31536000

    def calculate_live_spend(self):
        now = datetime.now()
        # Mengira berapa saat telah berlalu sejak awal tahun
        start_of_year = datetime(now.year, 1, 1)
        seconds_passed = (now - start_of_year).total_seconds()

        results = {}
        for country, budget in self.annual_budgets.items():
            spend_per_second = budget / self.seconds_in_year
            total_spent_so_far = seconds_passed * spend_per_second
            
            results[country] = {
                "spend_per_second": round(spend_per_second, 2),
                "total_spent_so_far": round(total_spent_so_far, 0),
                "currency": "MYR" if country == "Malaysia" else "USD"
            }
        return results

if __name__ == "__main__":
    fin = FinanceModule()
    print(json.dumps(fin.calculate_live_spend(), indent=4))
