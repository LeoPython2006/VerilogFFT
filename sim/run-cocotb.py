#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_cocotb_test(verilog_file, test_file, simulator="icarus", extra_args=None):
    env = os.environ.copy()
    env["TOPLEVEL_LANG"] = "verilog"
    env["VERILOG_SOURCES"] = str(Path(verilog_file).absolute())
    env["MODULE"] = Path(test_file).stem
    env["SIM"] = simulator
    
    cmd = ["cocotb-run", "--sim", simulator]
    if extra_args:
        cmd.extend(extra_args)
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, env=env, cwd=Path(test_file).parent)
    return result.returncode == 0

def run_multiple_tests(test_configs):
    results = {}
    for config in test_configs:
        print(f"\n{'='*50}")
        print(f"Running test: {config['name']}")
        print(f"{'='*50}")
        
        success = run_cocotb_test(
            config["verilog_file"],
            config["test_file"],
            config.get("simulator", "icarus"),
            config.get("extra_args", [])
        )
        results[config["name"]] = success
        
        if not success:
            print(f"❌ Test {config['name']} failed!")
        else:
            print(f"✅ Test {config['name']} passed!")
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Run Cocotb tests")
    parser.add_argument("--test", help="Run specific test file")
    parser.add_argument("--verilog", help="Verilog file to test")
    parser.add_argument("--simulator", default="icarus", help="Simulator to use")
    parser.add_argument("--all", action="store_true", help="Run all configured tests")
    
    args = parser.parse_args()
    
    if args.test and args.verilog:
        success = run_cocotb_test(args.verilog, args.test, args.simulator)
        sys.exit(0 if success else 1)
    
    elif args.all:
        test_configs = [
            {
                "name": "Simple Adder Test",
                "verilog_file": "simple_adder.v",
                "test_file": "test_simple_adder.py",
                "simulator": "icarus"
            }
        ]
        
        results = run_multiple_tests(test_configs)
        
        print(f"\n{'='*50}")
        print("Test Results Summary:")
        print(f"{'='*50}")
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        all_passed = all(results.values())
        sys.exit(0 if all_passed else 1)
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
