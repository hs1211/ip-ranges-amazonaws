import requests
import json
import ipaddress


def get_aws_ip_range(region, service_name):
    regional_ips = __invoke_ip_range_api__(region)
    filtered_list = list(filter(lambda ec2: ec2['service'] == service_name, regional_ips)) if service_name else regional_ips
    return list(map(lambda ec2: ec2['ip_prefix'], filtered_list))


def convert_ips_from_cidrs(cidr_list):
    return [str(ip) for cidr in cidr_list for ip in ipaddress.IPv4Network(cidr)]


def __invoke_ip_range_api__(region):
    try:
        r = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json')
        if r.status_code != 200:
            return []
        ip_ranges = json.loads(r.text)
        return list(filter(lambda obj: obj['region']==region, ip_ranges.get('prefixes',[])))
    except Exception as e:
        print(e.__traceback__)
        return []

if __name__ == "__main__":
    ip_ranges = get_aws_ip_range('ap-northeast-2','EC2')
    convert_ips_from_cidrs(ip_ranges)
