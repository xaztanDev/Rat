# ═══════════════════════════════════════════════════════════════
#   CREDIT : XaztanDEV
# ═══════════════════════════════════════════════════════════════

from jnius import autoclass
from android import AndroidService

def start_service():
    try:
        service = AndroidService('System Update', 'running')
        service.start('service started')
        return service
    except Exception as e:
        print(f"Service error: {e}")
        return None

if __name__ == "__main__":
    import main
    main.start()