# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-ahtx0", "adafruit-blinka"]
# ///
"""
Local Hardware Validation for Formatif F3
==========================================

Run this script ON YOUR RASPBERRY PI to validate hardware setup.
It creates marker files that GitHub Actions will verify.

Usage:
    python3 validate_pi.py

The script will:
1. Verify I2C communication
2. Test AHT20 sensor (temperature + humidity)
3. Verify your aht20_sensor.py script
4. Create marker files for GitHub Actions

After running successfully, commit and push the .test_markers/ folder.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Terminal Colors
# ---------------------------------------------------------------------------
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def success(msg):
    print(f"{Colors.GREEN}[PASS] {msg}{Colors.END}")


def fail(msg):
    print(f"{Colors.RED}[FAIL] {msg}{Colors.END}")


def warn(msg):
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.END}")


def info(msg):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.END}")


def header(msg):
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f" {msg}")
    print(f"{'='*60}{Colors.END}\n")


# ---------------------------------------------------------------------------
# Marker Management
# ---------------------------------------------------------------------------
MARKERS_DIR = Path(__file__).parent / ".test_markers"


def create_marker(name, content):
    """Create a marker file for GitHub Actions verification."""
    MARKERS_DIR.mkdir(exist_ok=True)
    marker_path = MARKERS_DIR / f"{name}.txt"
    timestamp = datetime.now().isoformat()
    marker_path.write_text(f"Verified: {timestamp}\n{content}\n")
    info(f"Marker created: {marker_path.name}")


# ---------------------------------------------------------------------------
# Test: I2C Communication
# ---------------------------------------------------------------------------
def check_i2c():
    """Verify I2C is enabled and working."""
    header("I2C COMMUNICATION")

    try:
        import board
        i2c = board.I2C()
        success("I2C bus initialized")
        return i2c
    except Exception as e:
        fail(f"I2C initialization failed: {e}")
        print("\n  Enable I2C on Raspberry Pi:")
        print("    sudo raspi-config > Interface Options > I2C > Enable")
        print("    sudo reboot")
        return None


# ---------------------------------------------------------------------------
# Test: AHT20 Sensor
# ---------------------------------------------------------------------------
def check_aht20(i2c):
    """Test AHT20 sensor reading."""
    header("AHT20 SENSOR TEST")

    if i2c is None:
        fail("Cannot test AHT20 - I2C not available")
        return False

    try:
        import adafruit_ahtx0

        sensor = adafruit_ahtx0.AHTx0(i2c)
        info("AHT20 found at address 0x38")

        # Read values
        temp = sensor.temperature
        humidity = sensor.relative_humidity

        success(f"Temperature: {temp:.1f} C")
        success(f"Humidity: {humidity:.1f} %RH")

        create_marker("aht20_verified", f"T={temp:.1f}C H={humidity:.1f}%RH")
        return True

    except ImportError:
        fail("adafruit_ahtx0 not installed")
        print("\n  Install with:")
        print("    pip install adafruit-circuitpython-ahtx0")
        return False
    except Exception as e:
        fail(f"AHT20 error: {e}")
        print("\n  Check connections:")
        print("    - VCC to 3.3V (NOT 5V!)")
        print("    - GND to GND")
        print("    - SCL to GPIO 3 (Pin 5)")
        print("    - SDA to GPIO 2 (Pin 3)")
        print("\n  Run i2cdetect to verify:")
        print("    sudo i2cdetect -y 1")
        print("    You should see 38 for the AHT20")
        return False


# ---------------------------------------------------------------------------
# Test: Script Validation
# ---------------------------------------------------------------------------
def check_aht20_script():
    """Verify aht20_sensor.py script."""
    header("SCRIPT VALIDATION")

    script_path = Path(__file__).parent / "aht20_sensor.py"

    if not script_path.exists():
        fail("aht20_sensor.py not found")
        print("\n  Create your aht20_sensor.py script in the same folder.")
        return False

    success("aht20_sensor.py exists")

    # Check syntax
    try:
        with open(script_path) as f:
            compile(f.read(), script_path, 'exec')
        success("Python syntax is valid")
    except SyntaxError as e:
        fail(f"Syntax error on line {e.lineno}: {e.msg}")
        return False

    # Check required content
    content = script_path.read_text()
    checks = [
        ("import board", "board import"),
        ("adafruit_ahtx0", "adafruit_ahtx0 import"),
    ]

    all_present = True
    for pattern, desc in checks:
        if pattern in content:
            success(f"Found: {desc}")
        else:
            fail(f"Missing: {desc}")
            all_present = False

    # Check for retry logic
    has_retry = any([
        "retry" in content.lower(),
        "MAX_RETRIES" in content,
        "max_retries" in content,
        "range(3)" in content,
        "range(5)" in content,
    ])

    if has_retry:
        success("Found: retry logic pattern")
    else:
        warn("Retry logic not detected (recommended for robustness)")

    if all_present:
        create_marker("aht20_script_verified", "Script structure valid")

    return all_present


# ---------------------------------------------------------------------------
# Test: VCNL4200 Sensor (Optional - Multi-Sensor Exercise)
# ---------------------------------------------------------------------------
def check_vcnl4200(i2c):
    """Test VCNL4200 sensor reading (non-blocking, for multi-sensor exercise)."""
    header("VCNL4200 SENSOR CHECK (OPTIONAL)")

    if i2c is None:
        warn("Cannot test VCNL4200 - I2C not available")
        return None

    # Check if VCNL4200 is detected at 0x51 via i2cdetect
    try:
        result = subprocess.run(
            ["i2cdetect", "-y", "1"],
            capture_output=True, text=True, timeout=5
        )
        if "51" not in result.stdout:
            warn("VCNL4200 not detected at address 0x51")
            info("The VCNL4200 is only needed for the multi-sensor exercise (Milestone 4)")
            info("Connect via STEMMA QT daisy-chain and run i2cdetect -y 1")
            return None
    except Exception:
        warn("Could not run i2cdetect to check for VCNL4200")
        return None

    try:
        import adafruit_vcnl4200

        vcnl = adafruit_vcnl4200.Adafruit_VCNL4200(i2c)
        info("VCNL4200 found at address 0x51")

        proximity = vcnl.proximity
        lux = vcnl.lux

        success(f"Proximite: {proximity}")
        success(f"Lumiere: {lux:.1f} lux")

        create_marker("vcnl4200_verified", f"Proximity={proximity} Lux={lux:.1f}")
        return True

    except ImportError:
        warn("adafruit_vcnl4200 not installed")
        info("Install with: pip install adafruit-circuitpython-vcnl4200")
        return None
    except Exception as e:
        warn(f"VCNL4200 error: {e}")
        info("Check STEMMA QT daisy-chain connection")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"\n{Colors.BOLD}Formatif F3 - Local Hardware Validation{Colors.END}")
    print(f"{'='*60}\n")

    results = {}

    # Run all checks
    i2c = check_i2c()
    results["I2C"] = i2c is not None
    results["AHT20"] = check_aht20(i2c)
    results["Script"] = check_aht20_script()

    # Optional VCNL4200 check (non-blocking)
    vcnl_result = check_vcnl4200(i2c)

    # Summary
    header("FINAL RESULTS")

    all_required_passed = results["I2C"] and results["AHT20"] and results["Script"]

    for test, passed in results.items():
        if passed:
            success(f"{test}: OK")
        else:
            fail(f"{test}: FAILED")

    # VCNL4200 is optional (shown separately)
    if vcnl_result is True:
        success("VCNL4200: OK (multi-sensor ready)")
    elif vcnl_result is None:
        warn("VCNL4200: Not detected (optional for Milestone 4)")
    else:
        warn("VCNL4200: Error (optional for Milestone 4)")

    print()

    if all_required_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("=" * 60)
        print(" ALL REQUIRED TESTS PASSED!")
        print("=" * 60)
        print(f"{Colors.END}")

        create_marker("all_tests_passed", "All required validations completed")

        print("\nNext steps:")
        print("  git add .test_markers/")
        print("  git commit -m \"feat: validation locale completee\"")
        print("  git push")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}")
        print("=" * 60)
        print(" SOME TESTS FAILED - Fix issues and run again")
        print("=" * 60)
        print(f"{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
