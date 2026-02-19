"""
Milestone 4: Multi-Sensor Integration (25 points)
===================================================

This milestone verifies that the student has:
1. Created a multi-sensor script combining AHT20 and VCNL4200
2. Imported the VCNL4200 library correctly
3. Created a VCNL4200 sensor object
4. Read proximity and lux values

These tests analyze code structure using AST/regex.
Actual hardware testing is done locally via validate_pi.py.
"""

import os
import ast
import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper: Get repository root
# ---------------------------------------------------------------------------
def get_repo_root():
    """Find the repository root by looking for .github folder."""
    current = Path(__file__).parent.parent
    if (current / ".github").exists():
        return current
    return current


REPO_ROOT = get_repo_root()


# ---------------------------------------------------------------------------
# Test 4.1: VCNL4200 Library Import (7 points)
# ---------------------------------------------------------------------------
def test_vcnl4200_import():
    """
    Verify that the multi-sensor script imports the VCNL4200 library.

    Expected: import adafruit_vcnl4200

    Suggestion: Add this import:
        import adafruit_vcnl4200
    """
    script_path = REPO_ROOT / "multi_capteurs.py"

    if not script_path.exists():
        pytest.skip("multi_capteurs.py not found")

    content = script_path.read_text()

    has_import = any([
        "adafruit_vcnl4200" in content,
        "from adafruit_vcnl4200" in content,
    ])

    if not has_import:
        pytest.fail(
            f"\n\n"
            f"Expected: VCNL4200 library import\n"
            f"Actual: No adafruit_vcnl4200 import found\n\n"
            f"Suggestion: Add this import in multi_capteurs.py:\n"
            f"  import adafruit_vcnl4200\n"
            f"\n"
            f"The VCNL4200 is a proximity and ambient light sensor at address 0x51.\n"
        )


# ---------------------------------------------------------------------------
# Test 4.2: VCNL4200 Sensor Object Creation (7 points)
# ---------------------------------------------------------------------------
def test_vcnl4200_sensor_creation():
    """
    Verify that the script creates a VCNL4200 sensor object.

    Expected: Adafruit_VCNL4200 sensor initialization

    Suggestion: Create sensor with:
        vcnl = adafruit_vcnl4200.Adafruit_VCNL4200(i2c)
    """
    script_path = REPO_ROOT / "multi_capteurs.py"

    if not script_path.exists():
        pytest.skip("multi_capteurs.py not found")

    content = script_path.read_text()

    has_sensor = any([
        "Adafruit_VCNL4200(" in content,
        "adafruit_vcnl4200." in content and "i2c" in content.lower(),
    ])

    if not has_sensor:
        pytest.fail(
            f"\n\n"
            f"Expected: VCNL4200 sensor object creation\n"
            f"Actual: No VCNL4200 sensor initialization found\n\n"
            f"Suggestion: Create the sensor object:\n"
            f"  import adafruit_vcnl4200\n"
            f"  vcnl = adafruit_vcnl4200.Adafruit_VCNL4200(i2c)\n"
            f"\n"
            f"The VCNL4200 shares the same I2C bus as the AHT20.\n"
        )


# ---------------------------------------------------------------------------
# Test 4.3: Proximity Reading (5 points)
# ---------------------------------------------------------------------------
def test_proximity_reading():
    """
    Verify that the script reads proximity from the VCNL4200 sensor.

    Expected: Code that accesses .proximity

    Suggestion: Read proximity with:
        proximity = vcnl.proximity
    """
    script_path = REPO_ROOT / "multi_capteurs.py"

    if not script_path.exists():
        pytest.skip("multi_capteurs.py not found")

    content = script_path.read_text()

    has_proximity = ".proximity" in content

    if not has_proximity:
        pytest.fail(
            f"\n\n"
            f"Expected: Proximity reading from VCNL4200\n"
            f"Actual: No .proximity access found\n\n"
            f"Suggestion: Read proximity like this:\n"
            f"  proximity = vcnl.proximity\n"
            f"  print(f\"Proximite: {{proximity}}\")\n"
            f"\n"
            f"The .proximity property returns a raw integer count.\n"
            f"Higher values mean closer objects.\n"
        )


# ---------------------------------------------------------------------------
# Test 4.4: Lux Reading (6 points)
# ---------------------------------------------------------------------------
def test_lux_reading():
    """
    Verify that the script reads ambient light (lux) from the VCNL4200.

    Expected: Code that accesses .lux

    Suggestion: Read ambient light with:
        lux = vcnl.lux
    """
    script_path = REPO_ROOT / "multi_capteurs.py"

    if not script_path.exists():
        pytest.skip("multi_capteurs.py not found")

    content = script_path.read_text()

    has_lux = ".lux" in content

    if not has_lux:
        pytest.fail(
            f"\n\n"
            f"Expected: Ambient light (lux) reading from VCNL4200\n"
            f"Actual: No .lux access found\n\n"
            f"Suggestion: Read ambient light like this:\n"
            f"  lux = vcnl.lux\n"
            f"  print(f\"Lumiere: {{lux:.1f}} lux\")\n"
        )


# ---------------------------------------------------------------------------
# Test 4.5: Shared I2C Bus with AHT20 (Bonus verification)
# ---------------------------------------------------------------------------
def test_shared_i2c_bus():
    """
    Verify that both AHT20 and VCNL4200 are used in the same script.

    Expected: Both adafruit_ahtx0 and adafruit_vcnl4200 imports

    Suggestion: A multi-sensor script should import both libraries:
        import adafruit_ahtx0
        import adafruit_vcnl4200
    """
    script_path = REPO_ROOT / "multi_capteurs.py"

    if not script_path.exists():
        pytest.skip("multi_capteurs.py not found")

    content = script_path.read_text()

    has_aht = "adafruit_ahtx0" in content
    has_vcnl = "adafruit_vcnl4200" in content

    if not (has_aht and has_vcnl):
        pytest.skip(
            "Both AHT20 and VCNL4200 imports recommended for multi-sensor script.\n"
            "The multi_capteurs.py script should combine both sensors on shared I2C bus."
        )
