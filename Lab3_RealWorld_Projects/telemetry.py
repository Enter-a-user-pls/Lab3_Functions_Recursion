
import random
from Student_Input import (LAST_NAME, SEED_NUM, FAVORITE_ARTIST, STREAM_LENGTH,
                    SENSOR_COUNT, VALID_MIN, VALID_MAX)


def build_student_seed(last_name, seed_num, favorite_artist):
    name_value = sum(ord(ch) for ch in last_name.lower() if ch.isalpha())
    artist_value = sum(ord(ch) for ch in favorite_artist.lower() if ch.isalpha())
    return (name_value * 31) + (artist_value * 17) + (seed_num * 101)


def telemetry_stream(length=STREAM_LENGTH):
    
    rng = random.Random(build_student_seed(LAST_NAME, SEED_NUM, FAVORITE_ARTIST))
    corrupt_samples = [None, "ERR", "N/A", "###", ""]

    for i in range(1, length + 1):
        sensor_id = f"S{rng.randint(1, SENSOR_COUNT)}"
        roll = rng.random()

        if roll < 0.15:                      # ~15% corrupted transmissions
            value = rng.choice(corrupt_samples)
        elif roll < 0.25:                    # ~10% out-of-range values
            value = round(rng.choice([-1, 1]) * rng.uniform(160, 300), 2)
        elif roll < 0.45:                    # ~20% high (abnormal) readings
            value = round(rng.uniform(100.5, 145), 2)
        else:                                # ~55% normal readings
            value = round(rng.uniform(20, 95), 2)

        yield (i, sensor_id, value)


def validate_reading(raw_value):
    
    number = float(raw_value)                # may raise ValueError / TypeError
    if number != number:                     # NaN check
        raise ValueError("NaN is not a valid measurement")
    if not (VALID_MIN <= number <= VALID_MAX):
        raise ValueError(f"value {number} outside range [{VALID_MIN}, {VALID_MAX}]")
    return number


# LAMBDA 
celsius_to_kelvin = lambda c: round(c + 273.15, 2)     # transform
is_abnormal = lambda value, limit: value > limit        # filter condition


def valid_readings(stream):
    
    for index, sensor, raw in stream:
        try:
            value = validate_reading(raw)
            yield ("valid", index, sensor, value)
        except (ValueError, TypeError) as error:
            yield ("invalid", index, sensor, f"{type(error).__name__}: {error} (raw={raw!r})")