import csv
import re
"""
This class is responsible for read and get values for csv file 
"""
class DataReader:
    @staticmethod
    def extract_reg_numbers(file_path):
        """Extracts vehicle registration numbers from a given file."""
        with open(file_path, 'r') as file:
            content = file.read()
        pattern = r'\b[A-Z]{2}[0-9]{2}\s?[A-Z]{3}\b'  # UK vehicle registration format
        return re.findall(pattern, content)

    @staticmethod
    def load_expected_values(file_path):
        """Reads expected car values from the output file."""
        expected_values = {}
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                reg_number = row["VARIANT_REG"].strip()
                expected_values[reg_number] = {"MAKE_MODEL":row["MAKE_MODEL"].strip(), "YEAR":row["YEAR"].strip()}
        return expected_values
