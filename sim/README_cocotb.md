# Cocotb Testing with run-cocotb.py

## Usage

### Run single test:
```bash
python run-cocotb.py --verilog simple_adder.v --test test_simple_adder.py
```

### Run all configured tests:
```bash
python run-cocotb.py --all
```

### Run with specific simulator:
```bash
python run-cocotb.py --verilog simple_adder.v --test test_simple_adder.py --simulator icarus
```

## Adding New Tests

To add a new test to the automated test suite, modify the `test_configs` list in `run-cocotb.py`:

```python
test_configs = [
    {
        "name": "Simple Adder Test",
        "verilog_file": "simple_adder.v",
        "test_file": "test_simple_adder.py",
        "simulator": "icarus"
    },
    {
        "name": "Your New Test",
        "verilog_file": "your_module.v",
        "test_file": "test_your_module.py",
        "simulator": "icarus"
    }
]
```

## Advantages over Makefile

- Easier to modify and extend
- Better error handling and reporting
- Support for multiple test scenarios
- Python-native configuration
- More flexible argument parsing 