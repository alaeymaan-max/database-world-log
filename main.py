import time
import sys
import json
import os
from datetime import datetime
from modules.worldometer_scraper import WorldometerScraper
from modules.finance import FinanceModule
from core.validator import DataValidator

def run_system_cycle():
    """Menjalankan satu kitaran penuh pemantauan DWL termasuk Kewangan."""
    print("\n" + "="*50)
    print(f"🌍 DWL SYSTEM CYCLE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    # 1. Inisialisasi Komponen
    scraper = WorldometerScraper()
    finance = FinanceModule()
    validator = DataValidator()
    log_path = "data/logs/worldometer_live.json"

    try:
        # 2. Langkah: Penarikan Data (Worldometer)
        print("[1/3] Menarik data statistik dunia...")
        raw_data = scraper.fetch_data()
        
        if raw_data:
            # 3. Langkah: Penarikan Data (Kewangan/Malaysia)
            print("[2/3] Mengira statistik kewangan & bajet live...")
            finance_data = finance.calculate_live_spend()
            raw_data["finance"] = finance_data

            # 4. Langkah: Pengesahan Data
            print("[3/3] Menjalankan validasi integriti data...")
            validation_report = validator.validate_worldometer_data(raw_data)
            validator.log_validation(validation_report)

            if validation_report["is_valid"]:
                # Simpan data akhir yang telah digabungkan
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, 'w') as f:
                    json.dump(raw_data, f, indent=4)
                print("✅ STATUS: Sinkronisasi Berjaya. Fail JSON dikemaskini.")
            else:
                print(f"❌ STATUS: Data tidak sah - {validation_report['errors']}")
        else:
            print("⚠️ STATUS: Gagal menarik data utama dari Scraper.")

    except Exception as e:
        print(f"❗ KRITIKAL: Kegagalan sistem pada kitaran ini - {str(e)}")

def main():
    # Untuk GitHub Actions, kita biasanya mahu ia jalan SEKALI sahaja setiap jam.
    # Jika anda guna di PC sendiri (WSL), anda boleh kekalkan gelung (loop) ini.
    
    # Check jika dijalankan di GitHub Actions
    IS_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'
    
    if IS_GITHUB:
        run_system_cycle()
        print("\n🚀 Kitaran GitHub Actions selesai.")
    else:
        INTERVAL = 60 # Sela masa 60 saat untuk mod lokal
        print("🚀 DWL COMMAND CENTER: MOD LOKAL AKTIF")
        try:
            while True:
                run_system_cycle()
                print(f"\n[INFO] Menunggu {INTERVAL} saat untuk kitaran seterusnya...")
                time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print("\n🛑 Sistem dihentikan. Menutup DWL.")
            sys.exit()

if __name__ == "__main__":
    main()
