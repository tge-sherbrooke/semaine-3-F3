"""
Milestone 3: Retry Logic and Quality (40 points)
=================================================

This milestone verifies that the student has:
1. Implemented retry logic for I2C errors (consistent with DHT22 pattern)
2. Proper error handling
3. Code quality and structure

IMPORTANT: The retry pattern is consistent with Week 2 DHT22 approach.
While I2C is more reliable than one-wire, errors can still occur
(loose connections, bus conflicts). Professional code handles these.
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
# Test 3.1: Retry Logic Implementation (15 points)
# ---------------------------------------------------------------------------
def test_retry_logic_exists():
    """
    CRITICAL: Verify that AHT20 code includes retry logic.

    Expected: A loop with try/except that retries on error

    WHY THIS MATTERS:
    While I2C is more reliable than DHT22's one-wire protocol,
    errors CAN occur (loose connections, bus conflicts, timing issues).
    Professional code ALWAYS includes error handling. This pattern
    is consistent with Week 2's DHT22 retry approach.

    Suggestion: Implement retry like this:
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            try:
                temperature = sensor.temperature
                humidity = sensor.relative_humidity
                break
            except Exception as e:
                print(f"Retry {attempt + 1}/{MAX_RETRIES}: {e}")
                time.sleep(1)
    """
    script_path = REPO_ROOT / "aht20_sensor.py"

    if not script_path.exists():
        pytest.skip("aht20_sensor.py not found")

    content = script_path.read_text()

    # Check for retry patterns
    has_loop = any([
        "for " in content and "range(" in content,
        "while " in content,
    ])

    has_try_except = "try:" in content and "except" in content

    has_retry_indicator = any([
        "retry" in content.lower(),
        "attempt" in content.lower(),
        "tentative" in content.lower(),  # French
        "essai" in content.lower(),  # French
        "max_" in content.lower(),
        "MAX_" in content,
        "range(3)" in content,
        "range(5)" in content,
    ])

    # We need: loop + try/except + some retry indicator
    if not (has_loop and has_try_except and has_retry_indicator):
        pytest.fail(
            f"\n\n"
            f"IMPORTANT: Retry logic not detected!\n\n"
            f"Expected: Loop with try/except to handle I2C read errors\n"
            f"Actual: Found loop={has_loop}, try/except={has_try_except}, "
            f"retry indicator={has_retry_indicator}\n\n"
            f"WHY THIS MATTERS:\n"
            f"  While I2C is more reliable than DHT22, errors CAN occur:\n"
            f"  - Loose connections\n"
            f"  - I2C bus conflicts with multiple devices\n"
            f"  - Timing issues during initialization\n"
            f"  Professional code ALWAYS handles these cases.\n\n"
            f"Suggestion: Implement retry pattern (consistent with DHT22):\n"
            f"  MAX_RETRIES = 3\n"
            f"  for attempt in range(MAX_RETRIES):\n"
            f"      try:\n"
            f"          temperature = sensor.temperature\n"
            f"          humidity = sensor.relative_humidity\n"
            f"          break  # Success!\n"
            f"      except Exception as e:\n"
            f"          print(f\"Retry {{attempt + 1}}/{{MAX_RETRIES}}: {{e}}\")\n"
            f"          time.sleep(1)\n"
        )


# ---------------------------------------------------------------------------
# Test 3.2: MAX_RETRIES Constant Defined (5 points)
# ---------------------------------------------------------------------------
def test_max_retries_constant():
    """
    Verify that a MAX_RETRIES constant is defined.

    Expected: MAX_RETRIES = 3 (or similar)

    Suggestion: Define retry limit at top of script:
        MAX_RETRIES = 3
    """
    script_path = REPO_ROOT / "aht20_sensor.py"

    if not script_path.exists():
        pytest.skip("aht20_sensor.py not found")

    content = script_path.read_text()

    has_max_retries = any([
        re.search(r'MAX_RETRIES\s*=\s*\d+', content),
        re.search(r'max_retries\s*=\s*\d+', content),
        re.search(r'NB_TENTATIVES\s*=\s*\d+', content),  # French
        re.search(r'RETRY_COUNT\s*=\s*\d+', content),
    ])

    if not has_max_retries:
        pytest.fail(
            f"\n\n"
            f"Expected: MAX_RETRIES constant defined\n"
            f"Actual: No retry limit constant found\n\n"
            f"Suggestion: Define retry limit at top of script:\n"
            f"  MAX_RETRIES = 3  # Nombre de tentatives de lecture\n"
            f"\n"
            f"Using a constant makes the code clearer and easier to maintain.\n"
        )


# ---------------------------------------------------------------------------
# Test 3.3: Error Handling Quality (10 points)
# ---------------------------------------------------------------------------
def test_error_handling_quality():
    """
    Verify that error handling is properly implemented.

    Expected: try/except with specific exception handling (not bare except)

    Suggestion: Use specific exceptions:
        except RuntimeError as e:
        OR
        except Exception as e:
    NOT:
        except:  # Bad! Catches everything including KeyboardInterrupt
    """
    script_path = REPO_ROOT / "aht20_sensor.py"

    if not script_path.exists():
        pytest.skip("aht20_sensor.py not found")

    content = script_path.read_text()

    # Check for bare except (bad practice)
    has_bare_except = re.search(r'except\s*:', content)

    if has_bare_except:
        pytest.fail(
            f"\n\n"
            f"Expected: Specific exception handling (except Exception as e:)\n"
            f"Actual: Bare 'except:' found (bad practice)\n\n"
            f"Suggestion: Always catch specific exceptions:\n"
            f"  GOOD:  except RuntimeError as e:\n"
            f"  GOOD:  except Exception as e:\n"
            f"  BAD:   except:  # Catches KeyboardInterrupt too!\n"
            f"\n"
            f"Bare except catches EVERYTHING, including Ctrl+C, making\n"
            f"your program hard to stop.\n"
        )

    # Check for proper exception handling
    has_proper_except = any([
        "except RuntimeError" in content,
        "except Exception" in content,
        "except OSError" in content,
        "except IOError" in content,
    ])

    if not has_proper_except:
        pytest.fail(
            f"\n\n"
            f"Expected: Specific exception handling\n"
            f"Actual: No proper exception handling found\n\n"
            f"Suggestion: Handle I2C-related exceptions:\n"
            f"  try:\n"
            f"      temperature = sensor.temperature\n"
            f"  except RuntimeError as e:\n"
            f"      print(f\"Erreur I2C: {{e}}\")\n"
        )


# ---------------------------------------------------------------------------
# Test 3.4: Main Guard Present (5 points)
# ---------------------------------------------------------------------------
def test_main_guard():
    """
    Verify that the script has a main() function or __name__ guard.

    Expected: if __name__ == "__main__" pattern

    Suggestion: Structure your code:
        def main():
            # Your code here

        if __name__ == "__main__":
            main()
    """
    script_path = REPO_ROOT / "aht20_sensor.py"

    if not script_path.exists():
        pytest.skip("aht20_sensor.py not found")

    content = script_path.read_text()

    has_guard = '__name__' in content and '__main__' in content

    if not has_guard:
        pytest.fail(
            f"\n\n"
            f"Expected: __name__ == \"__main__\" guard\n"
            f"Actual: No main guard found\n\n"
            f"Suggestion: Add at the end of your script:\n"
            f"  if __name__ == \"__main__\":\n"
            f"      main()\n"
            f"\n"
            f"This allows your script to be imported as a module\n"
            f"without running automatically.\n"
        )


# ---------------------------------------------------------------------------
# Test 3.5: Code Quality - Documentation (5 points)
# ---------------------------------------------------------------------------
def test_code_quality():
    """
    Verify basic code quality standards.

    Expected: Docstrings or comments

    Suggestion: Add documentation to your code.
    """
    script_path = REPO_ROOT / "aht20_sensor.py"

    if not script_path.exists():
        pytest.skip("aht20_sensor.py not found")

    content = script_path.read_text()

    # Check for docstring or comments
    has_docstring = '"""' in content or "'''" in content
    has_comments = content.count("#") >= 3  # At least 3 comment lines

    if not (has_docstring or has_comments):
        pytest.fail(
            f"\n\n"
            f"Expected: Documentation (docstrings or comments)\n"
            f"Actual: Minimal documentation found\n\n"
            f"Suggestion: Add documentation to explain your code:\n"
            f"  \"\"\"Script to read AHT20 I2C temperature and humidity.\"\"\"\n"
            f"\n"
            f"  # Initialize I2C bus\n"
            f"  i2c = board.I2C()\n"
        )
