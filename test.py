from ftplib import FTP

from kafka import KafkaProducer
import json
import logging
from time import sleep

from argparse import ArgumentParser

parser = ArgumentParser(description='Bouchon googlethon')

parser.add_argument("-v", "--verbosity", action="store_true", help="show debug logs")

options = parser.parse_args()


def main():
    try:
        ftp = FTP("192.168.0.9")
        ftp.login("nimir", "@soleil1")
        ftp.cwd("dev/ftp")
        crdir("94A", ftp)

    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin du bouchon ")
        exit(0)


def directory_exists(directory, ftp):
    filelist = []
    ftp.retrlines('LIST', filelist.append)
    for f in filelist:
        if f.split()[-1] == directory and f.upper().startswith('D'):
            return True
    return False


"""
Create a given directory
"""


def crdir(dir, ftp):
    if len(dir.rsplit("/", 1)) == 2:
        ftp.cwd(dir.rsplit("/", 1)[0])
        dir = dir.rsplit("/", 1)[1]
    if directory_exists(dir, ftp) is False:  # (or negate, whatever you prefer for readability)
        ftp.mkd(dir)


if __name__ == '__main__':
    main()