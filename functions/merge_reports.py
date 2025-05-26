import os
import glob
from datetime import datetime
from robot.api import ExecutionResult
import sys
import argparse

def parse_robot_timestamp(timestamp_str):
    """Convert Robot Framework timestamp string to datetime object"""
    if not timestamp_str:
        return None
    try:
        clean_ts = timestamp_str.split('.')[0]
        return datetime.strptime(clean_ts, '%Y%m%d %H:%M:%S')
    except (ValueError, AttributeError) as e:
        print(f"Warning: Failed to parse timestamp '{timestamp_str}': {str(e)}")
        return None

def find_results_directories(base_pattern='test-results-'):
    """Find all directories matching the base pattern"""
    return [d for d in glob.glob(f"{base_pattern}*") if os.path.isdir(d)]

def find_robot_results(directory):
    """Find all robot output files in a directory"""
    patterns = ['output.xml', '*.xml', '**/output.xml', '**/*.xml']
    found_files = set()
    
    for pattern in patterns:
        for filepath in glob.glob(os.path.join(directory, pattern), recursive=True):
            if os.path.isfile(filepath):
                try:
                    # Quick validation that it's a robot file
                    ExecutionResult(filepath)
                    found_files.add(os.path.abspath(filepath))
                except:
                    continue
    return sorted(found_files)

def merge_reports(results_dirs, output_dir):
    """Merge all Robot Framework reports"""
    all_files = []
    for directory in results_dirs:
        files = find_robot_results(directory)
        if files:
            print(f"Found {len(files)} result files in {directory}:")
            for f in files:
                print(f"  - {f}")
            all_files.extend(files)
        else:
            print(f"Warning: No valid Robot files found in {directory}")
    
    if not all_files:
        print("Error: No valid result files found in any directory")
        return False
    
    start_times = []
    end_times = []
    valid_files = []

    for xml_file in all_files:
        try:
            result = ExecutionResult(xml_file)
            if hasattr(result.suite, 'starttime') and hasattr(result.suite, 'endtime'):
                start_dt = parse_robot_timestamp(result.suite.starttime)
                end_dt = parse_robot_timestamp(result.suite.endtime)
                if start_dt and end_dt:
                    start_times.append(start_dt)
                    end_times.append(end_dt)
                    valid_files.append(xml_file)
        except Exception as e:
            print(f"Warning: Error processing {xml_file}: {str(e)}")

    if not valid_files:
        print("Error: No files with valid timestamps found")
        return False

    start_time = min(start_times).strftime('%Y%m%d %H:%M:%S')
    end_time = max(end_times).strftime('%Y%m%d %H:%M:%S')

    os.makedirs(output_dir, exist_ok=True)
    output_base = os.path.join(output_dir, "")

    cmd = (
        f'rebot '
        f'--starttime "{start_time}" '
        f'--endtime "{end_time}" '
        f'--output {output_base}output.xml '
        f'--log {output_base}log.html '
        f'--report {output_base}report.html '
        f'{" ".join(valid_files)}'
    )

    print("\nExecuting merge command:")
    print(cmd)
    if os.system(cmd) != 0:
        print("Error: rebot command failed")
        return False

    print("\nSuccessfully created:")
    print(f"- {output_base}output.xml")
    print(f"- {output_base}log.html")
    print(f"- {output_base}report.html")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge Robot Framework results")
    parser.add_argument("--output-dir", type=str, default="merged-results", help="Directory to write merged results into")
    args = parser.parse_args()

    print("Robot Framework Report Merger")
    print("=" * 50)

    # Find all matching directories
    results_dirs = find_results_directories()
    
    if not results_dirs:
        print("No test-results-* directories found")
        sys.exit(1)
    
    print(f"Found {len(results_dirs)} results directories:")
    for d in results_dirs:
        print(f"- {d}")
    
    output_path = args.output_dir
    if not merge_reports(results_dirs, output_path):
        sys.exit(1)
