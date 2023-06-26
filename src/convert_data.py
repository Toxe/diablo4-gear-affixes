import csv
import json
import os
import sys


def collect_d4_classes(import_data):
    return list(import_data)


def collect_affix_slots_data(import_data):
    data = {}
    for slot, slot_data in import_data.items():
        for slot_class, affixes in slot_data.items():
            if slot_class not in data:
                data[slot_class] = {}
            for affix in affixes:
                if affix not in data[slot_class]:
                    data[slot_class][affix] = []
                data[slot_class][affix].append(slot)
    return data


def prepare_affix_slots_output_row(d4_classes, slot_class, affix):
    row = {}
    for c in d4_classes:
        row[c] = ""
    row["Class"] = slot_class
    row["Affix"] = affix
    return row


def write_affix_slots(d4_classes, affix_slots_data, output_affix_slots_filename):
    fieldnames = ["Class", "Affix"] + d4_classes

    with open(output_affix_slots_filename, "wt", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()

        for slot_class, slot_class_affixes in affix_slots_data.items():
            for affix, affix_slots in slot_class_affixes.items():
                row = prepare_affix_slots_output_row(d4_classes, slot_class, affix)
                for slot in affix_slots:
                    row[slot] = "x"
                writer.writerow(row)


def read_import_data(input_filename):
    with open(input_filename, encoding="utf-8") as fp:
        return json.load(fp)


def eval_args(argv):
    if len(argv) != 3:
        raise RuntimeError("invalid number of arguments")
    input_filename = argv[1]
    output_affix_slots_filename = argv[2]
    if not os.path.isfile(input_filename):
        raise RuntimeError(f"input file {input_filename} not found")
    return input_filename, output_affix_slots_filename


def main():
    input_filename, output_affix_slots_filename = eval_args(sys.argv)
    import_data = read_import_data(input_filename)

    d4_classes = collect_d4_classes(import_data)
    affix_slots_data = collect_affix_slots_data(import_data)

    write_affix_slots(d4_classes, affix_slots_data, output_affix_slots_filename)


if __name__ == "__main__":
    main()
