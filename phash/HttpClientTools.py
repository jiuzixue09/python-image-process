
import urllib3


def do_get(url, headers=None, retries=3):
    # The timeout value will be applied to both the connect and the read timeouts.
    http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=5.0, read=10.0))
    r = http.request('GET', url, headers=headers, retries=retries)
    if r.status == 404:
        return None

    return r.data
