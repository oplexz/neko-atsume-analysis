import json

item_to_name = "data_inferred/item_to_name.json"
item_localization_file = "NekoAtsume2Data/localization/en/Goods.json"
playspace_to_name = "data_inferred/playspace_to_name.json"
goods_record_table = "NekoAtsume2Data/tables/GoodsRecordTable.json"
item_to_size = "data_inferred/item_to_size.json"

with open(item_to_name, "r") as f:
    item_to_name_dict = json.load(f)

with open(playspace_to_name, "r") as f:
    playspace_to_name_dict = json.load(f)

with open(item_localization_file, "r") as f:
    item_localization = json.load(f)

with open(goods_record_table, "r") as f:
    goods_record_table = json.load(f)

with open(item_to_size, "r") as f:
    item_to_size_dict = json.load(f)


item_ids = list(item_to_name_dict.keys())

for key in item_localization:
    if key.startswith("GoodsName"):
        item_id = key.split("GoodsName")[1]

        if int(item_id) >= 10000:
            continue

        if item_id not in item_ids:
            item_to_name_dict[item_id] = item_localization[key]
            playspace_to_name_dict[item_id + "0"] = item_localization[key]

            for item in goods_record_table:
                if item["Id"] == int(item_id):
                    item_to_size_dict[item_id] = bool(item["Attribute"])


with open(item_to_name, "w") as f:
    json.dump(
        dict(sorted(item_to_name_dict.items(), key=lambda x: int(x[0]))), f, indent=4
    )

with open(playspace_to_name, "w") as f:
    json.dump(
        dict(sorted(playspace_to_name_dict.items(), key=lambda x: int(x[0]))),
        f,
        indent=4,
    )

with open(item_to_size, "w") as f:
    json.dump(
        dict(sorted(item_to_size_dict.items(), key=lambda x: int(x[0]))),
        f,
        indent=4,
    )