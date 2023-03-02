import logging
import platform
import subprocess
import sys

from utils.fetcher import Fetcher
from utils.generator import Generator

# TODO: clash_to_surge & clash_to_base
# TODO: Clash Profiles
# TODO: Merge personal subscription
# TODO: Divide international and domestic

if __name__ == '__main__':
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

    if platform.system() == 'Windows':
        subprocess.run("start /b ./subconverter/subconverter.exe", shell=True)
        Fetcher.retrieve_subs(nodes_base)
        subprocess.run(
            "./speedtest/lite.exe --config ./config/speedtest_config.json --test ./output/all_proxies.yml 2>&1",
            shell=True)
        Generator.generate_subs('./out.json', 200)
    elif platform.system() == 'Linux':
        subprocess.run("chmod +x ./subconverter/subconverter && chmod +x ./speedtest/lite", shell=True)
        subprocess.run("nohup ./subconverter/subconverter &", shell=True)
        Fetcher.retrieve_subs(nodes_base)
        subprocess.run(
            "./speedtest/lite --config ./config/speedtest_config.json --test ./output/all_proxies.yml 2>&1")
    else:
        logging.exception('Unsupported OS, exit program')
        sys.exit(0)
