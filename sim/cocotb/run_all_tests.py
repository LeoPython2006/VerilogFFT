#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def run_cocotb_test(test_dir, dut_file, test_file, simulator="icarus"):
    env = os.environ.copy()
    env["TOPLEVEL_LANG"] = "verilog"
    env["VERILOG_SOURCES"] = str(Path(test_dir) / dut_file)
    env["MODULE"] = Path(test_file).stem
    env["SIM"] = simulator
    
    cmd = ["cocotb-run", "--sim", simulator]
    
    print(f"Running test in {test_dir}")
    print(f"Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, env=env, cwd=test_dir)
    return result.returncode == 0

def main():
    test_configs = [
        {
            "name": "FFT Basic Test",
            "dir": "sim/cocotb/fft_basic",
            "dut": "dut.sv",
            "test": "test.py"
        },
        {
            "name": "FFT Accuracy Test", 
            "dir": "sim/cocotb/fft_accuracy",
            "dut": "dut.sv",
            "test": "test.py"
        }
    ]
    
    results = {}
    
    for config in test_configs:
        print(f"\n{'='*50}")
        print(f"Running: {config['name']}")
        print(f"{'='*50}")
        
        success = run_cocotb_test(
            config["dir"],
            config["dut"],
            config["test"]
        )
        
        results[config["name"]] = success
        
        if success:
            print(f"✅ {config['name']} PASSED")
        else:
            print(f"❌ {config['name']} FAILED")
    
    print(f"\n{'='*50}")
    print("Test Results Summary:")
    print(f"{'='*50}")
    
    all_passed = True
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main() 