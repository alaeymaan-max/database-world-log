import json
import os
from datetime import datetime

class DataValidator:
    def __init__(self):
        self.config_path = "core/config_api.json"
        self.thresholds = self._load_thresholds()

    def _load_thresholds(self):
        """Memuatkan had kriteria dari fail konfigurasi."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get("validation_rules", {})
        except Exception:
            # Had rujukan jika fail config tiada
            return {"population_min_threshold": 8000000000}

    def validate_worldometer_data(self, data):
        """Mengesahkan data dari Worldometer Scraper."""
        report = {
            "is_valid": True,
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }

        # 1. Semak struktur asas
        if not data or "metrics" not in data:
            report["is_valid"] = False
            report["errors"].append("Struktur data kosong atau rosak.")
            return report

        metrics = data["metrics"]

        # 2. Pengesahan Populasi (Mesti nombor & logik 2026)
        try:
            pop = int(metrics.get("current_population", 0))
            min_pop = self.thresholds.get("population_min_threshold", 8000000000)
            
            if pop < min_pop:
                report["is_valid"] = False
                report["errors"].append(f"Populasi dikesan bawah paras logik 2026: {pop}")
        except ValueError:
            report["is_valid"] = False
            report["errors"].append("Format data populasi bukan integer.")

        # 3. Semak jika ada nilai N/A yang kritikal
        critical_fields = ["current_population", "public_healthcare_spending"]
        for field in critical_fields:
            if metrics.get(field) == "N/A":
                report["is_valid"] = False
                report["errors"].append(f"Data kritikal '{field}' hilang (N/A).")

        return report

    def log_validation(self, report):
        """Menyimpan log pengesahan untuk rujukan sistem."""
        log_file = "data/logs/validation_history.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        status = "PASSED" if report["is_valid"] else "FAILED"
        log_entry = f"[{report['timestamp']}] STATUS: {status} | ERRORS: {report['errors']}\n"
        
        with open(log_file, 'a') as f:
            f.write(log_entry)
        
        if not report["is_valid"]:
            print(f"⚠️ VALIDATION ALERT: {report['errors']}")

if __name__ == "__main__":
    # Ujian pengesahan ringkas
    validator = DataValidator()
    sample_data = {
        "metrics": {
            "current_population": "8274102481",
            "public_healthcare_spending": "4500000"
        }
    }
    
    result = validator.validate_worldometer_data(sample_data)
    validator.log_validation(result)
    print(f"Validation Result: {'Lulus' if result['is_valid'] else 'Gagal'}")
