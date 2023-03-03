import json
import logging
import platform
import subprocess
import sys
from urllib import request
from pathlib import Path
import pkg_resources
from utils.fetcher import Fetcher
from utils.generator import Generator


class Initiator:
    @staticmethod
    def check_pkg():
        try:
            pkg_resources.require(Path('./requirements.txt').open())
            return True
        except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
            return False

    @staticmethod
    def start_program(mode, count):
        if not Initiator.check_pkg():
            output = subprocess.run("python -m pip install -r ./requirements.txt", capture_output=True, shell=True)
            logging.warning(output.stdout.decode('utf-8'))
            if not Initiator.check_pkg():
                logging.exception('Requirements unsatisfied')
                sys.exit(1)

        try:
            request.urlretrieve('https://cdn.jsdelivr.net/gh/Loyalsoldier/geoip@release/Country.mmdb',
                                './country/Country.mmdb')
        except Exception:
            logging.info('Update Country.mmdb failed')
            pass

        with open('./config/test_link.json', 'r', encoding='utf-8') as f:
            test_links = json.load(f)
            f.close()
        test_link = test_links['both']
        if mode != 'b':
            test_link = test_links['separate']

        # Notice: Switch here between test list and production list
        nodes_base = './config/sub_list_test.json'
        # nodes_base = './config/sub_list.json'

        logging.info(f'Program starting with mode: {mode} and count: {count}')
        if platform.system() == 'Windows':

            subconverter_pid = subprocess.run('tasklist | findstr "subconverter"', capture_output=True, shell=True)
            if subconverter_pid.stdout.decode('utf-8') == "":
                try:
                    subprocess.run("start /b ./subconverter/subconverter.exe  >./output/subconverter.log 2>&1", timeout=5,
                       shell=True)
                except subprocess.TimeoutExpired:
                    logging.exception('Failed to run subconverter')
                    sys.exit(1)

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
            sys.exit(1)
