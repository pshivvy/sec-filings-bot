import requests
from bs4 import BeautifulSoup
from webhook import send_data
from dateutil.parser import parse
from firebase_info import get_tickers_by_url, set_value, get_all_data

# main url
main_webhook_url = 'URL'


def generate_full_url(url):
    return str('https://discordapp.com/api/webhooks/' + url[:url.find('-')] + '/' + url[url.find('-')+1:])


def get_xml_by_cik(tickers, webhook):
    if len(tickers) > 0:
        for cik in tickers:
            get_xml(cik, tickers[cik], webhook)
    else:
        return ""

def get_xml(ticker, past_val, hook_url):
    get_latest_ticker_xml = requests.get('https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK='+ ticker + '&type=&owner=include&count=40&action=getcurrent&output=atom')
    soup = BeautifulSoup(get_latest_ticker_xml.content, 'lxml')

    if soup.find('entry') is None:
        if(past_val == ""):
            print('No recent filings. Status stays the same.')
            return
        else:
            print('No new filings present, updating old status.')
            set_value(ticker, "", hook_url)
            return
    else:
        entries = soup.find_all('entry')
        if(formatted_info(entries) == past_val and past_val != ""):
            print('Messages already sent, status stays the same.')
            return
        else:
            for e in entries:
                if e.find('link').attrs['href'] in past_val:
                    print(e.find('title').text + ' already sent')
                else:
                    try:
                        send_data(
                            hookrl=generate_full_url(hook_url),
                            title=e.find('title').text,
                            type=e.find('category').attrs['term'],
                            datetime=parse_dt(e.find('updated').text),
                            filingUrl=e.find('link').attrs['href']
                        )
                        # sends to central fillings channel
                        # can be excluded
                        send_data(
                            hookrl=generate_full_url(main_webhook_url),
                            title=e.find('title').text,
                            type=e.find('category').attrs['term'],
                            datetime=parse_dt(e.find('updated').text),
                            filingUrl=e.find('link').attrs['href']
                        )
                        set_value(ticker, formatted_info(entries), hook_url)
                        print('Messages Sent! Status has been updated.')
                    except:
                        print('Link invalid')
            
        


def parse_dt(dt):
    date_time = parse(dt)
    return date_time.strftime("%b %d, %Y at %I:%M:%S %p")

def formatted_info(all_entries):
    val = ''
    for e in all_entries:
        val = val + e.find('title').text + ' ' + e.find('link').attrs['href'] + ' ' + parse_dt(e.find('updated').text) + '\n'
    return val


def hello_pubsub(event, content):
    all_data = get_all_data()
    for data in all_data:
        get_xml_by_cik(data.to_dict(), data.id)
