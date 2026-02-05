import time
import sys
from modules.worldometer_scraper import WorldometerScraper
from core.validator import DataValidator

def run_system_cycle():
    """Menjalankan satu kitaran penuh pemantauan DWL."""
    print("\n" + "="*50)
    print("🌍 DATABASE WORLD LOG (DWL) - SYSTEM START")
    print("="*50)

    # 1. Inisialisasi Komponen
    scraper = WorldometerScraper()
    validator = DataValidator()

    try:
        # 2. Langkah: Penarikan Data (Scraping)
        raw_data = scraper.fetch_data()
        
        if raw_data:
            # 3. Langkah: Pengesahan Data (Validation)
            validation_report = validator.validate_worldometer_data(raw_data)
            validator.log_validation(validation_report)

            if validation_report["is_valid"]:
                print("✅ STATUS: Data disahkan dan sedia untuk paparan Kiosk.")
            else:
                print("❌ STATUS: Data gagal pengesahan. Sila semak fail ralat.")
        else:
            print("⚠️ STATUS: Tiada data diterima dari modul scraper.")

    except Exception as e:
        print(f"❗ KRITIKAL: Kegagalan sistem pada kitaran ini - {str(e)}")

def main():
    # Menetapkan sela masa (interval) - Contoh: Setiap 1 jam (3600 saat)
    # Untuk tujuan demo, anda boleh set ke 60 saat.
    INTERVAL = 3600 

    print("🚀 DWL COMMAND CENTER SEDANG BERJALAN...")
    print(f"Kitaran automatik ditetapkan setiap {INTERVAL} saat.")
    
    try:
        while True:
            run_system_cycle()
            print(f"\n[INFO] Menunggu {INTERVAL} saat untuk kitaran seterusnya...")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Sistem dihentikan oleh pengguna. Menutup DWL.")
        sys.exit()

if __name__ == "__main__":
    main()
