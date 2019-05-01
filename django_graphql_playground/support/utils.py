from datetime import date
from datetime import timedelta

from dateutil import relativedelta


def retrieve_ip_address(request):
    """
    Makes the best attempt to get the client's real IP or return the loopback
    https://stackoverflow.com/a/35108884/3899136
    """
    PRIVATE_IPS_PREFIX = ("10.", "172.", "192.", "127.")
    ip_address = ""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if x_forwarded_for and "," not in x_forwarded_for:
        if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(",")]
        for ip in ips:
            if ip.startswith(PRIVATE_IPS_PREFIX):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get("HTTP_X_REAL_IP", "")
        if x_real_ip:
            if not x_real_ip.startswith(PRIVATE_IPS_PREFIX):
                ip_address = x_real_ip.strip()
    if not ip_address:
        remote_addr = request.META.get("REMOTE_ADDR", "")
        if remote_addr:
            if not remote_addr.startswith(PRIVATE_IPS_PREFIX):
                ip_address = remote_addr.strip()
    if not ip_address:
        ip_address = "127.0.0.1"
    return ip_address


def some_day_from_next_month():
    return date.today() + relativedelta.relativedelta(months=1)


def get_first_day(dt, delta_years=0, delta_months=0):
    y, m = dt.year + delta_years, dt.month + delta_months
    a, m = divmod(m - 1, 12)
    return date(y + a, m + 1, 1)


def get_last_day(dt):
    return get_first_day(dt, 0, 1) + timedelta(-1)


def option(function):
    def wrapper(*args, **kwargs):
        if len(args) > 0 and args[0] is not None:
            try:
                return function(*args, **kwargs)
            except:
                return None

    return wrapper
