import sys, os, re, csv, logging
from collections import Counter


def get_ips_from_file(filename):
    regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    with open(filename) as file:
        log = file.read()
        ip_list = re.findall(regexp, log)

    return ip_list


def counter(ip_list):
    return Counter(ip_list)


def write_to_csv(count_of_ips):
    with open('result.csv', 'w') as file:
        writer = csv.writer(file)
        header = ['Ip', 'Frequency']
        writer.writerow(header)

        for item in count_of_ips:
            writer.writerow((item, count_of_ips[item]))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        logging.warning("Empty command line arguments, filename by default")
        filename = 'log.txt'

    if not os.path.exists(filename):
        logging.error('File {} doesnt exist'.format(filename))
    else:
        logging.info('Parse file: {0}'.format(filename))
        ips = get_ips_from_file(filename)
        if len(ips) == 0:
            logging.info('No ip addresses in file')
        else:
            write_to_csv(count_of_ips=counter(ips))
