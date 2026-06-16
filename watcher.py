import time
import os
import psutil

def wait_and_sync():
    print("Waiting for run_missing_teams.py to finish...")
    while True:
        is_running = False
        for p in psutil.process_iter(['cmdline']):
            try:
                cmdline = p.info.get('cmdline')
                if cmdline and 'run_missing_teams.py' in ' '.join(cmdline):
                    is_running = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        if not is_running:
            break
            
        time.sleep(10)
        
    print("Scraping finished. Running sync...")
    os.system("python sync_scraped_teams.py")

if __name__ == "__main__":
    wait_and_sync()
