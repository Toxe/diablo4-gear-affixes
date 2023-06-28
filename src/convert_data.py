import csv
import json
import os
import sys


def collect_d4_classes(import_data):
    d4_classes = []
    for slot_data in import_data.values():
        for cl in slot_data.keys():
            if cl not in ["All Classes", "Implicit"]:
                if cl not in d4_classes:
                    d4_classes.append(cl)
    return sorted(d4_classes)


def collect_d4_slots(import_data):
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


def collect_slot_affixes_data(import_data, d4_classes, d4_slots):
    data = {}
    for class_name in d4_classes:
        data[class_name] = {}
        for slot in d4_slots:
            data[class_name][slot] = []

    for slot, slot_data in import_data.items():
        for slot_class, affixes in slot_data.items():
            if slot_class in d4_classes:
                for affix in affixes:
                    data[slot_class][slot].append(affix)
            elif slot_class == "All Classes":
                for class_name in d4_classes:
                    for affix in affixes:
                        data[class_name][slot].append(affix)

    for class_name, slots in data.items():
        for slot, affixes in slots.items():
            affixes.sort()

    return data


def prepare_affix_slots_output_row(d4_slots, slot_class, affix):
    row = {}
    for s in d4_slots:
        row[s] = ""
    row["Class"] = slot_class
    row["Affix"] = affix
    return row


def write_affix_slots(output_filename, affix_slots_data, d4_slots):
    fieldnames = ["Class", "Affix"] + d4_slots

    with open(output_filename, "wt", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()

        for slot_class, slot_class_affixes in affix_slots_data.items():
            for affix in sorted(slot_class_affixes.keys()):
                row = prepare_affix_slots_output_row(d4_slots, slot_class, affix)
                for slot in slot_class_affixes[affix]:
                    row[slot] = "✓"
                writer.writerow(row)


def build_slot_affixes_output_filename(filename, class_name):
    parts = os.path.splitext(filename)
    return parts[0] + f"_{class_name}" + parts[1]


def get_slots_max_row(slots, class_data):
    max_row = 0
    for slot in slots:
        max_row = max(max_row, len(class_data[slot]))
    return max_row


def prepare_slot_affixes_output_row(slots):
    row = {}
    for slot in slots:
        row[slot] = ""
    return row


def write_slot_affixes(output_filename, slot_affixes_data, d4_slots):
    for class_name, class_data in slot_affixes_data.items():
        filename = build_slot_affixes_output_filename(output_filename, class_name)
        with open(filename, "wt", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=d4_slots)
            writer.writeheader()

            slots = list(class_data)
            max_row = get_slots_max_row(slots, class_data)

            for row_id in range(max_row):
                row = prepare_slot_affixes_output_row(slots)
                for slot in slots:
                    row[slot] = class_data[slot][row_id] if row_id < len(class_data[slot]) else ""
                writer.writerow(row)


def read_import_data(input_filename):
    with open(input_filename, encoding="utf-8") as fp:
        return json.load(fp)


def eval_args(argv):
    if len(argv) != 4:
        raise RuntimeError("invalid number of arguments")
    input_filename = argv[1]
    output_affix_slots_filename = argv[2]
    output_slot_affixes_filename = argv[3]
    if not os.path.isfile(input_filename):
        raise RuntimeError(f"input file {input_filename} not found")
    return input_filename, output_affix_slots_filename, output_slot_affixes_filename


def main():
    input_filename, output_affix_slots_filename, output_slot_affixes_filename = eval_args(sys.argv)
    import_data = read_import_data(input_filename)

    d4_classes = collect_d4_classes(import_data)
    d4_slots = collect_d4_slots(import_data)

    affix_slots_data = collect_affix_slots_data(import_data)
    slot_affixes_data = collect_slot_affixes_data(import_data, d4_classes, d4_slots)

    write_affix_slots(output_affix_slots_filename, affix_slots_data, d4_slots)
    write_slot_affixes(output_slot_affixes_filename, slot_affixes_data, d4_slots)


if __name__ == "__main__":
    main()
