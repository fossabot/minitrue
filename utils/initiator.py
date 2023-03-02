import subprocess
from urllib import request
import logging
from utils.fetcher import Fetcher
import platform
import sys
from utils.generator import Generator
import json


class Initiator:
    @staticmethod
    def start_program(mode, count):
        subprocess.run("python -m pip install -r ./requirements.txt", shell=True)
        nodes_base = './config/sub_list.json'
        try:
            request.urlretrieve('https://cdn.jsdelivr.net/gh/Loyalsoldier/geoip@release/Country.mmdb',
                                './country/Country.mmdb')
            logging.info('Country.mmdb updated')
        except Exception:
            logging.info('Update Country.mmdb failed')
            pass

        with open('./config/nodes_link.json', 'r', encoding='utf-8') as f:
            test_links = json.load(f)
            f.close()
        test_link = test_links['all']
        if mode != 'b':
            test_link = test_links['separate']

        if platform.system() == 'Windows':
            subprocess.run("start /b ./subconverter/subconverter.exe  >./output/subconverter.log 2>&1", shell=True)
            if mode != 'd':
                Fetcher.retrieve_subs(nodes_base)
            if mode != 'i':
                subprocess.run(
                    f"./speedtest/lite.exe --config ./config/speedtest_config.json --test {test_link} ./output/all_proxies.yml >./output/speedtest.log 2>&1",
                    shell=True)
                Generator.generate_subs('./out.json', count)
        elif platform.system() == 'Linux':
            subprocess.run("chmod +x ./subconverter/subconverter && chmod +x ./speedtest/lite", shell=True)
            subprocess.run("nohup ./subconverter/subconverter >./output/subconverter.log 2>&1 &", shell=True)

            if mode != 'd':
                Fetcher.retrieve_subs(nodes_base)
            if mode != 'i':
                subprocess.run(
                    f"./speedtest/lite --config ./config/speedtest_config.json --test {test_link} >./output/speedtest.log 2>&1 &")
                Generator.generate_subs('./out.json', count)
        else:
            logging.exception('Unsupported OS, exit program')
            sys.exit(0)
