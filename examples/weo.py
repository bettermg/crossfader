import csv
import autoencoder
import json

# Using data from http://www.imf.org/external/pubs/ft/weo/2014/02/weodata/download.aspx

with open('examples/data/WEOOct2014all.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    headers = reader.next() # ignore headers

    series_by_country = {}
    for row in reader:
        country = row[3]
        metric = row[4]
        data = row[9:-1]

        if not metric:
            continue

        series_by_country.setdefault(country, {})[metric] = data

    data = []
    headers = set()
    for country, series in series_by_country.iteritems():
        # Go through all years now
        series_keys = list(series.keys())
        headers.update(series_keys)

        for values in zip(*[series[key] for key in series_keys]):
            data_row = {}
            for key, value in zip(series_keys, values):
                if value in ['', 'n/a', '--']:
                    continue

                data_row[key] = float(value.replace(',', ''))

            data.append(data_row)

    headers = list(headers)

    for model in autoencoder.train(headers, data, bins=30,
                                   n_hidden_layers=3, n_hidden_units=32):
        content = 'var data = %s;' % json.dumps(model)
        f = open('models/weo.js', 'w')
        f.write(content)
        f.close()
