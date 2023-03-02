import argparse
import logging
import platform
import subprocess
import sys
from urllib import request

from utils.fetcher import Fetcher
from utils.generator import Generator

parser = argparse.ArgumentParser(prog='minitrue.py', description='Welcome to the brand new world!',
                                 epilog='H²=(ȧ/a)²=8πGρ/3-κc²/a²+Δc²/3')
parser.add_argument('-p', type=str, default='a',
                    help='current place, d for domestic, i for international, default for both')
parser.add_argument('-n', type=int, default=200, help='extract nodes count, default 200')

# TODO: International and domestic should have different speedtest link
# TODO: Clash Profiles
# TODO: Readme.md

if __name__ == '__main__':
    args = parser.parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M"))
    file_handler = logging.FileHandler('./output/log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s", "%Y-%m-%d %H:%M"))
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # lite-windows-amd64-v3 & lite-linux-amd64 v0.14.1 https://github.com/xxf098/LiteSpeedTest
    # subconverter-win64 & subconverter-linux64 v0.7.2 https://github.com/tindy2013/subconverter
    subprocess.run("python -m pip install -r ./requirements.txt", shell=True)
    nodes_base = './config/sub_list.json'
    try:
        request.urlretrieve('https://cdn.jsdelivr.net/gh/Loyalsoldier/geoip@release/Country.mmdb',
                            './country/Country.mmdb')
        logging.info('Country.mmdb updated')
    except Exception:
        logging.info('Update Country.mmdb failed')
        pass

    if platform.system() == 'Windows':
        subprocess.run("start /b ./subconverter/subconverter.exe  >./output/subconverter.log 2>&1", shell=True)
        if args.p != 'd':
            Fetcher.retrieve_subs(nodes_base)
        if args.p != 'i':
            subprocess.run(
                "./speedtest/lite.exe --config ./config/speedtest_config.json --test ./output/all_proxies.yml >./output/speedtest.log 2>&1",
                shell=True)
            Generator.generate_subs('./out.json', args.n)
    elif platform.system() == 'Linux':
        subprocess.run("chmod +x ./subconverter/subconverter && chmod +x ./speedtest/lite", shell=True)
        subprocess.run("nohup ./subconverter/subconverter >./output/subconverter.log 2>&1 &", shell=True)

        if args.p != 'd':
            Fetcher.retrieve_subs(nodes_base)
        if args.p != 'i':
            subprocess.run(
                "./speedtest/lite --config ./config/speedtest_config.json --test ./output/all_proxies.yml >./output/speedtest.log 2>&1 &")
            Generator.generate_subs('./out.json', args.n)
    else:
        logging.exception('Unsupported OS, exit program')
        sys.exit(0)
