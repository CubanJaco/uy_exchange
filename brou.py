import http.client
from lxml import html
import os
from datetime import datetime


def to_double(value):
    try:
        return float(value.strip().replace(',', '.'))
    except ValueError:
        return 0.0


def line_builder(buy, sell):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y,%H:%M:%S")
    return '%s,%s,%s' % (date_time, buy, sell)


def get_file_path(language):
    return '%s/currencies/brou/%s.csv' % (os.getcwd(), language)


def line_writer(language, line):
    with open(get_file_path(language), 'a') as f:
        f.write("%s\n" % line)
        f.close()


def get_currencies():

    conn = http.client.HTTPSConnection("www.brou.com.uy")

    headers = {'Accept': "text/html, */*"}

    conn.request(
        "POST",
        "/c/portal/render_portlet?p_l_id=20593&p_p_id=cotizacionfull_WAR_broutmfportlet_INSTANCE_otHfewh1klyS&p_p_lifecycle=0&p_t_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=0&p_p_col_count=2&p_p_isolated=1&currentURL=%2Fcotizaciones",
        headers=headers)

    res = conn.getresponse()
    data = res.read()

    tree = html.fromstring(data.decode("utf-8"))
    rows = tree.xpath('//tr')
    rows.pop(0)  # Eliminar el header
    for row in rows:
        # p class="moneda"
        content = html.fromstring(html.tostring(row).decode("utf-8"))
        currency = content.xpath('//p[@class="moneda"]/text()')[0]
        prices = content.xpath('//td/div/p[@class="valor"]/text()')
        buy = to_double(prices[0])
        sell = to_double(prices[1])
        file_name = ''
        if currency == 'Dólar eBROU':
            file_name = 'usd_brou'
        elif currency == 'Dólar':
            file_name = 'usd'
        # elif currency == 'Euro':
        #     file_name = 'eur'

        if file_name != '':
            line_writer(file_name, line_builder(buy, sell))

