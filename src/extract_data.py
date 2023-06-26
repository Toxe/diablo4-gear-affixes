import json
import os
import sys

from bs4 import BeautifulSoup


def extract_data(input_filename):
    with open(input_filename, encoding="utf-8") as fp:
        data = {}
        soup = BeautifulSoup(fp, "html.parser")

        for slot in soup.find_all("div", class_="stats__slot"):
            slot_name = str(slot.div.string)
            class_name = None
            data[slot_name] = {}

            for tag in slot.ul.find_all(["div", "li"]):
                if tag.name == "div":
                    class_name = str(tag.string)
                    data[slot_name][class_name] = []
                else:
                    if class_name is None:
                        raise RuntimeError("unknown class")
                    data[slot_name][class_name].append(str(tag.string))
    return data


def dump_data(output_filename, data):
    with open(output_filename, "wt", encoding="utf-8") as fp:
        fp.write(json.dumps(data, indent=4))


def eval_args(argv):
    if len(argv) != 3:
        raise RuntimeError("invalid number of arguments")
    input_filename = argv[1]
    output_filename = argv[2]
    if not os.path.isfile(input_filename):
        raise RuntimeError(f"input file {input_filename} not found")
    return input_filename, output_filename


def main():
    input_filename, output_filename = eval_args(sys.argv)
    data = extract_data(input_filename)
    dump_data(output_filename, data)


if __name__ == "__main__":
    main()
