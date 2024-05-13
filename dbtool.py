import streamlit as st
import shutil
import os
import datetime
import time

def create_record(record):
    try:
        with open("file.txt", 'a') as file:
            file.write(','.join(record) + '\n')
        st.success("Record created successfully.")
    except FileNotFoundError:
        st.error(f"Error: File 'file.txt' not found.")

def read_records():
    try:
        with open("file.txt", 'r') as file:
            records = [line.strip().split(',') for line in file]

        st.subheader("Records:")
        for record in records:
            st.write(record)
    except FileNotFoundError:
        st.error(f"Error: File 'file.txt' not found.")

def update_record(old_record, new_record):
    try:
        with open("file.txt", 'r') as file:
            lines = file.readlines()
        updated_lines = [','.join(new_record) + '\n' if old_record in line else line for line in lines]
        with open("file.txt", 'w') as file:
            file.writelines(updated_lines)
        st.success("Record updated successfully.")
    except FileNotFoundError:
        st.error(f"Error: File 'file.txt' not found.")

def delete_record(record):
    try:
        record_str = ','.join(record)

        with open("file.txt", 'r') as file:
            lines = file.readlines()
        updated_lines = [line for line in lines if record_str not in line]
        with open("file.txt", 'w') as file:
            file.writelines(updated_lines)
        st.success("Record deleted successfully.")
    except FileNotFoundError:
        st.error(f"Error: File 'file.txt' not found.")

def backup_file(backup_time):
    try:
        if not os.path.exists("backup"):
            os.makedirs("backup")

        file_name, file_extension = os.path.splitext("file.txt")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file_name = f"{file_name}_{timestamp}{file_extension}"
        backup_file_path = os.path.join("backup", backup_file_name)

        current_time = datetime.datetime.now().strftime("%H:%M")
        time_difference = (datetime.datetime.strptime(backup_time, "%H:%M") - datetime.datetime.strptime(current_time, "%H:%M")).total_seconds()

        time.sleep(time_difference)

        shutil.copy2("file.txt", backup_file_path)
        st.success(f"File backed up to: {backup_file_path}")
    except FileNotFoundError:
        st.error(f"Error: Source file 'file.txt' not found.")

def restore_backup(backup_file_name):
    try:
        backup_file_path = os.path.join("backup", backup_file_name)
        shutil.copy2(backup_file_path, "file.txt")
        st.success(f"Backup file '{backup_file_name}' restored successfully.")
    except FileNotFoundError:
        st.error(f"Error: Backup file '{backup_file_name}' not found.")

def monitor_backups():
    while True:
        files = os.listdir("backup")
        if len(files) == 0:
            st.warning("Backup Pending...")
        else:
            st.subheader("Backup Status:")
            for file in files:
                st.write(f"Backup file: {file}")
            st.success("Backup Completed")
        time.sleep(5)

def main():
    st.title("Record Management App")

    menu_options = ["Create Record", "Read Records", "Update Record", "Delete Record", "Backup File", "Restore Backup", "Monitor Backup Status", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu_options)

    if choice == "Create Record":
        st.subheader("Create Record")
        record = st.text_input("Enter record (id,name,data):")
        if st.button("Create"):
            create_record(record.split(','))

    elif choice == "Read Records":
        st.subheader("Read Records")
        read_records()

    elif choice == "Update Record":
        st.subheader("Update Record")
        old_record = st.text_input("Enter record ID to update:")
        new_record = st.text_input("Enter new record (id,name,data):")
        if st.button("Update"):
            update_record(old_record, new_record.split(','))

    elif choice == "Delete Record":
        st.subheader("Delete Record")
        record = st.text_input("Enter record (id,name,data) to delete:")
        if st.button("Delete"):
            delete_record(record.split(','))

    elif choice == "Backup File":
        st.subheader("Backup File")
        backup_time = st.text_input("Enter backup time (HH:MM):")
        if st.button("Backup"):
            backup_file(backup_time)

    elif choice == "Restore Backup":
        st.subheader("Restore Backup")
        backup_file_name = st.text_input("Enter the backup file name to restore:")
        if st.button("Restore"):
            restore_backup(backup_file_name)

    elif choice == "Monitor Backup Status":
        st.subheader("Monitor Backup Status")
        monitor_backups()

    elif choice == "Exit":
        st.write("Exiting program.")

if __name__ == "__main__":
    main()
