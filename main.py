import requests as req
import time
import argparse
import pandas as pd
import os

URL = 'https://www.trulia.com/json/search/dots/?url=https://www.trulia.com/for_sale/{city},{state}/{beds_n}p_beds/' \
      '{min_price}-{max_price}_price/date;d_sort'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 '
                  'Safari/537.36 '
}

# crate data directory if it is not exist
if not os.path.isdir('data'):
    os.makedirs('data')

parser = argparse.ArgumentParser(prog='trulia')

parser.add_argument('-s', '--state', help='state name. e.g. NY', type=str, default='NY')
parser.add_argument('-c', '--city', help='city or borough name. e.g. Manhattan', type=str, default='Manhattan')
parser.add_argument('-b', '--beds', help='beds number, to increase -bbbb = 4 beds', action='count', default=1)
parser.add_argument('-min', help='minimum price 100', type=int, default=190000)
parser.add_argument('-max', help='max price 100000', type=int, default=1000000)
parser.add_argument('-o', '--out', help='file name', type=str)


def get_homes(state, city, beds, min_price, max_price) -> dict:
    """
    :param state: the state name e.g NY.
    :param city: the city or borough name.
    :param beds: number of beds.
    :param min_price: min unit price.
    :param max_price: max unit price.

    """

    url_at = URL.format(state=state, city=city, beds_n=beds, min_price=min_price, max_price=max_price)
    response = req.get(url=url_at, headers=headers)
    status = response.status_code
    print('search status: %d' % status)

    if status == 200:
        return response.json().get('dots')

    return {}


args = vars(parser.parse_args())

homes = get_homes(
    state=args['state'],
    city=args['city'],
    beds=args['beds'],
    min_price=args['min'],
    max_price=args['max']
)

df = pd.DataFrame(homes)

if not args.get('out'):
    # auto generate file name
    file_name = '%s,%s_%sbeds_min%d_max%d_%s' % (
        args['city'], args['state'], args['beds'], args['min'], args['max'], time.strftime("%Y%m%d_%H%M%S")
    )
else:
    file_name = args['out']

save_path = os.path.join('data', file_name + '.csv')

# save to csv
df.to_csv(save_path)

print('result saved to %s' % save_path)
