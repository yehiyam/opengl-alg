import argparse
from functools import reduce

import bson

def get_from_dict(dataDict, mapList):
    """Iterate nested dictionary"""
    return reduce(dict.get, mapList, dataDict)

def main():
    parser = argparse.ArgumentParser(description='decode property from bson.')
    parser.add_argument('bson_file')
    parser.add_argument('prop_path')
    parser.add_argument('out_file')
    args = parser.parse_args()
    path_array = args.prop_path.split('.')
    with open(args.bson_file,"rb") as file:
        bson_data=file.read()
        raw_data=bson.decode(bson_data)
        data = get_from_dict(raw_data.get('data')[0],path_array)
        with open(args.out_file,"wb") as out_file:
            out_file.write(data)

if __name__ == "__main__":
    main()