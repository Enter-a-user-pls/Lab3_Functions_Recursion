"""Entry point: wires the modules together and prints the assessment output."""

from Student_Input import LAST_NAME, SEED_NUM, FAVORITE_ARTIST, STREAM_LENGTH
from telemetry import build_student_seed, telemetry_stream, valid_readings
from diagnostics import process_stream, build_report, execution_log


def main():
    # Run the pipeline: generator -> generator -> monitored processor
    stream = telemetry_stream()
    classified = valid_readings(stream)
    results = process_stream(classified)
    report = build_report(results)

    print("Student-Specific Inputs:")
    print(f"  LAST_NAME       = {LAST_NAME}")
    print(f"  SEED_NUM        = {SEED_NUM}")
    print(f"  FAVORITE_ARTIST = {FAVORITE_ARTIST}")
    print(f"  Derived seed    = {build_student_seed(LAST_NAME, SEED_NUM, FAVORITE_ARTIST)}")
    print()

    print("Generated Telemetry Data:")
    print(f"  Stream length: {STREAM_LENGTH} readings")
    for index, sensor, value in results["valid_samples"]:
        print(f"  #{index:<3} {sensor}  {value}")
    print()

    print("Valid/Invalid Results:")
    print(f"  Valid readings  : {report['valid']}")
    print(f"  Invalid readings: {report['invalid']}")
    for detail in results["invalid_details"]:
        print(f"    - {detail}")
    print()

    print("Processed Results:")
    print(f"  Total processed: {report['processed']}")
    print("  Lambda transform (Celsius -> Kelvin) samples:")
    for index, c, k in results["kelvin_sample"]:
        print(f"    #{index}: {c} C = {k} K")
    print()

    print("Recursive Analysis:")
    if not results["abnormal"]:
        print("  No abnormal conditions detected.")
    for item in results["abnormal"]:
        print(f"  Reading #{item['index']} [{item['sensor']}] value={item['value']}")
        for step in item["steps"]:
            print(f"      {step}")
    print()

    print("Final Diagnostic Summary:")
    print(f"  Processed readings   : {report['processed']}")
    print(f"  Valid readings       : {report['valid']}")
    print(f"  Invalid readings     : {report['invalid']}")
    print(f"  Abnormal conditions  : {report['abnormal']}")
    if report["worst"]:
        w = report["worst"]
        print(f"  Worst reading        : #{w['index']} [{w['sensor']}] = {w['value']}")
    print(f"  Overall equipment status: {report['status']}")
    print()

    print("Execution Log:")
    for entry in execution_log:
        print(f"  {entry}")
    print()

    print("Final Output:")
    print(
        f"  Equipment status {report['status']}: {report['processed']} readings processed "
        f"({report['valid']} valid, {report['invalid']} invalid), "
        f"{report['abnormal']} abnormal condition(s) detected."
    )


if __name__ == "__main__":
    main()