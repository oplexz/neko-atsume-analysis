# Note: this is arguably the most clear way to list the commands
python fetch_new_items.py

output_folder=ran_tables
rm -r $output_folder
mkdir $output_folder

name="Outdoors, Silver Fish Equivalent per Item, Frisky Bitz, All Items Intact"
python analyze.py --output_type silver_equiv
mv output.md "$output_folder/$name.md"

name="Outdoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Intact"
python analyze.py
mv output.md "$output_folder/$name.md"

name="Indoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Intact"
python analyze.py --is_indoor
mv output.md "$output_folder/$name.md"

name="Outdoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Broken"
python analyze.py --item_damage_state=1
mv output.md "$output_folder/$name.md"

name="Indoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Broken"
python analyze.py --item_damage_state=1 --is_indoor
mv output.md "$output_folder/$name.md"

name="Outdoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Fixed"
python analyze.py --item_damage_state=2
mv output.md "$output_folder/$name.md"

name="Indoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Fixed"
python analyze.py --item_damage_state=2 --is_indoor
mv output.md "$output_folder/$name.md"

name="Doesn't Matter Indoor or Outdoor, Peach Occur Chance, Frisky Bitz, All Items Intact (Also Doesn't Really Matter)"
python analyze.py --output_type='cat_probability' --cat_id=24
mv output.md "$output_folder/$name.md"
