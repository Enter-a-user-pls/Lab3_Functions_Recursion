
import time
import functools
from Student_Input import ABNORMAL_LIMIT, CRITICAL_COUNT
from telemetry import celsius_to_kelvin, is_abnormal

execution_log = []          # shared log written by the decorator and processors


def monitor(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        execution_log.append(f"[MONITOR] {func.__name__}() started")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except Exception as error:               # never terminate the program
            execution_log.append(f"[MONITOR] {func.__name__}() FAILED: {error}")
            raise
        elapsed = (time.perf_counter() - start) * 1000
        execution_log.append(
            f"[MONITOR] {func.__name__}() finished in {elapsed:.3f} ms "
            f"-> processed={result['processed']}"
        )
        return result
    return wrapper


def trace_abnormal(value, limit, depth=0, steps=None):
    
    if steps is None:
        steps = []
    excess = round(value - limit, 2)

    # ---- BASE CONDITION ----
    if excess <= 1.0:
        steps.append(f"depth {depth}: excess={excess} -> BASE reached, condition stabilised")
        return steps, depth

    # ---- RECURSIVE CASE ----
    steps.append(f"depth {depth}: excess={excess} -> reducing")
    return trace_abnormal(limit + excess / 2, limit, depth + 1, steps)


@monitor
def process_stream(classified_stream):
    """
    MAJOR PROCESSING FUNCTION (monitored by the decorator).
    Consumes the generator one reading at a time and returns a results dict.
    """
    results = {
        "processed": 0, "valid": 0, "invalid": 0,
        "invalid_details": [], "valid_samples": [],
        "abnormal": [], "kelvin_sample": [],
    }

    for status, index, sensor, payload in classified_stream:
        results["processed"] += 1

        if status == "invalid":
            results["invalid"] += 1
            results["invalid_details"].append(f"Reading #{index} [{sensor}] {payload}")
            execution_log.append(f"Reading #{index}: INVALID - handled without stopping")
            continue

        results["valid"] += 1
        if len(results["valid_samples"]) < 8:               # keep only a small sample
            results["valid_samples"].append((index, sensor, payload))
        if len(results["kelvin_sample"]) < 3:
            results["kelvin_sample"].append((index, payload, celsius_to_kelvin(payload)))

        if is_abnormal(payload, ABNORMAL_LIMIT):            # lambda filter
            steps, depth = trace_abnormal(payload, ABNORMAL_LIMIT)
            results["abnormal"].append(
                {"index": index, "sensor": sensor, "value": payload,
                 "steps": steps, "depth": depth}
            )
            execution_log.append(
                f"Reading #{index}: ABNORMAL {payload} on {sensor} "
                f"(recursive trace depth {depth})"
            )

    return results


def build_report(results):
    """Uses the returned results to compute the final diagnostic summary."""
    abnormal_count = len(results["abnormal"])
    if abnormal_count == 0:
        status = "NORMAL"
    elif abnormal_count < CRITICAL_COUNT:
        status = "WARNING"
    else:
        status = "CRITICAL"

    worst = max(results["abnormal"], key=lambda a: a["value"], default=None)
    return {
        "processed": results["processed"],
        "valid": results["valid"],
        "invalid": results["invalid"],
        "abnormal": abnormal_count,
        "status": status,
        "worst": worst,
    }