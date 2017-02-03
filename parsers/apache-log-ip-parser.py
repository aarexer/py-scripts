import sys
import os
import re
import csv
import logging
from collections import Counter
from operator import itemgetter


def get_ips_from_file(filename):
    regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    with open(filename) as file:
        log = file.read()
        ip_list = re.findall(regexp, log)

    return ip_list


def counter(ip_list):
    return Counter(ip_list)


def write_to_csv(pairs_of_ip_freq):
    with open('result.csv', 'w') as file:
        writer = csv.writer(file)
        header = ['Ip', 'Frequency']
        writer.writerow(header)

        for pair in pairs_of_ip_freq:
            writer.writerow((pair[0], pair[1]))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = 'log.txt'
        logging.warning('Empty command line arguments, filename by default {}'.format(filename))

    if not os.path.exists(filename):
        logging.error('File {} doesnt exist'.format(filename))
    else:
        logging.info('Parse file: {0}'.format(filename))
        ips = get_ips_from_file(filename)
        if len(ips) == 0:
            logging.info('No ip addresses in file')
        else:
            ip_pairs = counter(ips).items()
            ip_freq = sorted(ip_pairs, key=itemgetter(1), reverse=True)
            write_to_csv(pairs_of_ip_freq=ip_freq)
