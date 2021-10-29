import requests
from bs4 import BeautifulSoup
import re
import os

url = 'https://multirbl.valli.org/list/'

r = requests.get(url).text

soup = BeautifulSoup(r, 'lxml')

table = soup.find('table')

tds = []
for tr in table.find_all('tr'):
    for td in tr.find_all('td'):
        tds.append(td)

def pull_providers():
    """
    Massively over-engineered way of handling file processing to clean up bs4 data (because the site is written gross)
    Step1: from the tds extracted, write these as str to tmp1
    Step2: run a regex over file1 to get data we actually care about and write it to tmp2
    Step3: using tmp2, replace empty [] with blank lines then strip these blank lines from the file, write this to tmp3
    Step4: using tmp3, strip out the [] and () surrounding the current data and write this to tmp4
    Step5: using tmp4, split the remaining lines on , and only take idx0 (because that's where our actual site is)
    Final: write the above to all_providers and cry because of how gross this solution is
    """
    with open('tmp1.txt', 'w') as f:
        for td in tds:
            f.write(str(td) + '\n')

    res = [re.findall(r"^<td>([a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+)</td>$", line) for line in open('tmp1.txt')]

    with open('tmp2.txt', 'w') as f:
        for r in res:
            f.write(str(r) + '\n')


    with open('tmp2.txt', 'r') as f:
        data = f.read()

        data = data.replace('[]', '')
        lines = data.split('\n')
        clean_data = [line for line in lines if line.strip() != '']

        new_data = ''

        for line in clean_data:
            new_data += line + '\n'


    with open('tmp3.txt', 'w') as f:
        f.write(new_data)


    sites = []
    with open('tmp3.txt', 'r') as f:
        for line in f.readlines():
            sites.append(line)


    clean_sites = []
    for i in sites:
        i = i.replace('[', '')
        i = i.replace(']', '')
        i = i.replace('(', '')
        i = i.replace(')', '')

        clean_sites.append(i)

    with open('tmp4.txt', 'w') as f:
        for site in clean_sites:
            f.write(site)

    new_lines = []
    with open('tmp4.txt', 'r') as f:
        for line in f.readlines():
            split_line = line.split(',', 1)
            new_line = split_line[0]
            new_lines.append(new_line)

    with open('all_providers.txt', 'w') as f:
        for line in new_lines:
            f.write(line + '\n')


    with open('all_providers.txt', 'r+') as f:
        data = f.read()

        lines = data.split('\n')
        clean_data = [line for line in lines if line.strip() != '']

        new_data = ''

        for line in clean_data:
            new_data += line + '\n'

        f.truncate(0)
        f.seek(0)

        f.write(new_data[:-1])


    clean_tmp()


def clean_tmp():
    # cleanup the mess we've made doing this thing
    files = ['tmp1.txt', 'tmp2.txt', 'tmp3.txt', 'tmp4.txt']
    for file in files:
        os.remove(file)

if __name__ == '__main__':
    pull_providers()
