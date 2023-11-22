import os
import shutil
from datetime import datetime

def create_backup_folder():
    backup_folder = "./backup"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"Backup folder '{backup_folder}' created.")

def backup_database():
    database_file = "/home/ubuntu/capstone-design/src/crawling/contract_addresses.db"
    backup_folder = "./backup"
    
    # Generate timestamp for the backup file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create backup file name with timestamp
    backup_file = f"contract_addresses.db_{timestamp}"
    
    # Full path to the backup file
    backup_path = os.path.join(backup_folder, backup_file)
    
    # Full path to the original database file
    database_path = os.path.join(os.getcwd(), database_file)
    
    try:
        # Copy the database file to the backup folder
        shutil.copy(database_path, backup_path)
        print(f"Backup created: {backup_path}")
    except Exception as e:
        print(f"Backup failed. Error: {e}")

if __name__ == "__main__":
    create_backup_folder()
    backup_database()
