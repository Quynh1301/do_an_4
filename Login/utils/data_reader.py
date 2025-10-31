import csv

def read_csv_data(file_path):
    try:
        with open(file_path, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            print(f"Đọc file thành công với encoding: utf-8")
            print(f"Các cột trong file CSV: {reader.fieldnames}")
            return data
    except Exception as e:
        raise Exception(f"Lỗi khi đọc file CSV: {e}")
