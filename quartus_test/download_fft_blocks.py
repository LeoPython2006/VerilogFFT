#!/usr/bin/env python3

import os
import sys
import subprocess
import requests
from pathlib import Path
import zipfile
import tarfile

class FFTBlockDownloader:
    def __init__(self):
        self.download_dir = Path("downloaded_fft_blocks")
        self.download_dir.mkdir(exist_ok=True)
        
    def download_from_github(self, repo_url, target_dir):
        """Загрузка с GitHub"""
        try:
            print(f"Downloading from GitHub: {repo_url}")
            
            # Используем git clone
            repo_name = repo_url.split("/")[-1]
            target_path = self.download_dir / target_dir
            
            if target_path.exists():
                print(f"Directory {target_path} already exists, skipping...")
                return target_path
            
            cmd = ["git", "clone", repo_url, str(target_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Successfully downloaded to {target_path}")
                return target_path
            else:
                print(f"❌ Failed to download: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error downloading from GitHub: {e}")
            return None
    
    def download_from_opencores(self, project_url, target_dir):
        """Загрузка с OpenCores"""
        try:
            print(f"Downloading from OpenCores: {project_url}")
            
            target_path = self.download_dir / target_dir
            target_path.mkdir(exist_ok=True)
            
            # Для OpenCores нужно вручную скачать файлы
            print(f"⚠️  Manual download required for OpenCores project")
            print(f"   Please download files from: {project_url}")
            print(f"   and place them in: {target_path}")
            
            return target_path
            
        except Exception as e:
            print(f"❌ Error with OpenCores download: {e}")
            return None
    
    def find_verilog_files(self, directory):
        """Поиск Verilog файлов в директории"""
        verilog_files = []
        
        for ext in ["*.v", "*.sv", "*.vh"]:
            verilog_files.extend(Path(directory).rglob(ext))
        
        return verilog_files
    
    def create_test_config(self, block_name, verilog_files, top_module):
        """Создание конфигурации для тестирования"""
        config = {
            "name": block_name,
            "files": [str(f) for f in verilog_files],
            "top": top_module,
            "source": "downloaded"
        }
        
        return config
    
    def download_all_blocks(self):
        """Загрузка всех FFT блоков"""
        blocks = [
            {
                "name": "pipelined_fft_128",
                "type": "github",
                "url": "https://github.com/freecores/pipelined_fft_128",
                "top_module": "pipelined_fft_128"
            },
            {
                "name": "pipelined_fft_64",
                "type": "github", 
                "url": "https://github.com/freecores/pipelined_fft_64",
                "top_module": "pipelined_fft_64"
            },
            {
                "name": "fftgen",
                "type": "github",
                "url": "https://github.com/steveri/fftgen",
                "top_module": "fft_gen"
            },
            {
                "name": "versatile_fft",
                "type": "opencores",
                "url": "https://opencores.org/projects/versatile_fft",
                "top_module": "versatile_fft"
            }
        ]
        
        configs = []
        
        for block in blocks:
            print(f"\n{'='*50}")
            print(f"Processing: {block['name']}")
            print(f"{'='*50}")
            
            if block["type"] == "github":
                target_dir = self.download_from_github(block["url"], block["name"])
            elif block["type"] == "opencores":
                target_dir = self.download_from_opencores(block["url"], block["name"])
            
            if target_dir:
                verilog_files = self.find_verilog_files(target_dir)
                if verilog_files:
                    print(f"Found {len(verilog_files)} Verilog files:")
                    for f in verilog_files:
                        print(f"  - {f}")
                    
                    config = self.create_test_config(
                        block["name"], 
                        verilog_files, 
                        block["top_module"]
                    )
                    configs.append(config)
                else:
                    print("⚠️  No Verilog files found")
            else:
                print("❌ Failed to download block")
        
        return configs
    
    def save_configs(self, configs):
        """Сохранение конфигураций в JSON файл"""
        import json
        
        config_file = self.download_dir / "test_configs.json"
        with open(config_file, "w") as f:
            json.dump(configs, f, indent=2)
        
        print(f"\n✅ Test configurations saved to: {config_file}")
        return config_file

def main():
    downloader = FFTBlockDownloader()
    
    print("FFT Blocks Downloader")
    print("=" * 50)
    
    configs = downloader.download_all_blocks()
    
    if configs:
        config_file = downloader.save_configs(configs)
        
        print(f"\n{'='*50}")
        print("Download Summary:")
        print(f"{'='*50}")
        
        for config in configs:
            print(f"✅ {config['name']}: {len(config['files'])} files")
        
        print(f"\nNext steps:")
        print(f"1. Review downloaded files in: {downloader.download_dir}")
        print(f"2. Update test configurations in: {config_file}")
        print(f"3. Run Quartus tests with: python quartus_test_script.py")
        
    else:
        print("❌ No blocks were successfully downloaded")

if __name__ == "__main__":
    main() 