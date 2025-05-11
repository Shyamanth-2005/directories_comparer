

import os
import filecmp
from tqdm import tqdm
from datetime import datetime

def get_all_files(directory):
    """Recursively get all file paths relative to base directory."""
    file_list = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start=directory)
                file_list.append(rel_path)
    except Exception as e:
        print(f"Error reading files in directory '{directory}': {e}")
    return set(file_list)

def write_report(filepath, summary):
    try:
        with open(filepath, 'w',encoding='utf-8') as report:
            report.write(summary)
        print(f"\n📝 Report saved to: {filepath}")
    except Exception as e:
        print(f"Error writing report to file: {e}")

def compare_directories(dir_a, dir_b, report_filename="comparison_report.txt"):
    try:
        files_in_a = get_all_files(dir_a)
        files_in_b = get_all_files(dir_b)

        matched_paths = files_in_a & files_in_b
        missing_in_b = files_in_a - files_in_b
        extra_in_b = files_in_b - files_in_a

        identical_files = []
        different_files = []
        error_files = []
        print("\n🔍 Comparing file contents...\n")
        for rel_path in tqdm(sorted(matched_paths), desc="Comparing", unit="file"):
            try:
                file_a = os.path.join(dir_a, rel_path)
                file_b = os.path.join(dir_b, rel_path)

                if filecmp.cmp(file_a, file_b, shallow=False):
                    identical_files.append(rel_path)
                else:
                    different_files.append(rel_path)
            except Exception as e:
                print(f"Error comparing files {rel_path}: {e}")

        summary = []
        summary.append("--- 📊 COMPARISON REPORT ---")
        summary.append(f"Generated on: {datetime.now()}\n")
        summary.append(f"Directory A: {dir_a}")
        summary.append(f"Directory B: {dir_b}\n")
        summary.append(f"Total files in A           : {len(files_in_a)}")
        summary.append(f"Total files in B           : {len(files_in_b)}")
        summary.append(f"Matched file paths         : {len(matched_paths)}")
        summary.append(f"  └── Identical content    : {len(identical_files)}")
        summary.append(f"  └── Different content    : {len(different_files)}")
        summary.append(f"Missing in B (A-only)      : {len(missing_in_b)}")
        summary.append(f"Extra in B (Not in A)      : {len(extra_in_b)}\n")

        summary.append("✅ IDENTICAL FILES:")
        for file in sorted(identical_files):
            summary.append(f"  ✓ {file}")

        summary.append("\n❗DIFFERENT FILES (same path, different content):")
        for file in sorted(different_files):
            summary.append(f"  ⚠ {file}")

        summary.append("\n🚫 MISSING IN B (present in A):")
        for file in sorted(missing_in_b):
            summary.append(f"  ✗ {file}")

        summary.append("\n➕ EXTRA IN B (not in A):")
        for file in sorted(extra_in_b):
            summary.append(f"  + {file}")
        summary.append("\nERROR FILES (could not be compared):")
        if not error_files:
            summary.append("  None")
        else:
            for entry in sorted(error_files):
                summary.append(f"  ⚠ {entry}")

        report_text = '\n'.join(summary)
        write_report(report_filename, report_text)

    except Exception as e:
        print(f"An error occurred during comparison: {e}")

# Entry point
if __name__ == "__main__":
    try:
        dir_a = input("Enter path to Directory A (reference): ").strip()
        dir_b = input("Enter path to Directory B (to compare): ").strip()

        if not os.path.isdir(dir_a) or not os.path.isdir(dir_b):
            raise ValueError("One or both of the provided paths are not valid directories.")

        compare_directories(dir_a, dir_b)

    except Exception as e:
        print(f"Fatal error: {e}")
