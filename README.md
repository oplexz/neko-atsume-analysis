# Neko Atsume Analysis

A tool for optimizing your Neko Atsume yard setup to maximize fish earnings and cat visits. Data and algorithms based on Neko Atsume 2 V1.0.0.

## Description

This tool analyzes different yard configurations in Neko Atsume to help you:
- Calculate expected fish earnings (both silver and gold)
- Determine probabilities of specific cats visiting
- Account for indoor/outdoor placement considerations, which is crucial for computing gold fish earning rate
- Handle item damage states
- Consider cat-on-cat interactions and preferences
- Deal with loss of precision (rounding down)
- Custom grouping options for analyzing specific item combinations for your yard

## A Note for New Players
If you are here, you are definitely trying to min-max the game :). I hear ya. One suggestion for you is to use silver fish to get the expansion asap. 
1. The conversion rate is more favorable (1:27.8) than other types. Other ones which is almost 25.
2. It's just faster. Suppose you only have Beach Umbrella, (5000 + 340 + 12.28 / 24 * 8 * 10) / 438.127 = 12.28 days (assuming you have food ALL THE TIME) vs 180 / 9.490 = 18.96 days. A full yard can save you 40% of the time to get to that juicy expansion.
3. You double the gold fish income when indoors, which is only available after getting the expansion. 

Finally, this is a chill, cute cat collection game, so please just have fun and close this page if you want!! (I'm definitely not doing it right.)

## Installation

```bash
git clone https://github.com/catlover627/neko-atsume-analysis.git
cd neko-atsume-analysis
pip install numpy pandas
```

## Usage

Basic usage example:
```bash
python analyze.py --food_type 2 --output_type gold_equiv
```

To analyze probability of a specific cat appearing (You can find the cat id to name mapping [here](data/cat_id_to_name.json)):
```bash
python analyze.py --output_type cat_probability --cat_id 24
```

To analyze custom item groups:
```bash
python analyze.py --group_def custom --items_of_interest_indoors 1 2 3 --items_of_interest_outdoors 4 5 6
```

## Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--food_type` | int | 2 | Type of food to place:<br>1=Thrifty Bitz<br>2=Frisky Bitz<br>3=Ritzy Bitz<br>4=Bonito Bitz<br>5=Deluxe Tuna Bitz<br>6=Sashimi<br>7=Sashimi Boat<br>99=idk |
| `--item_damage_state` | int | 0 | State of item damage:<br>0=Good<br>1=Broken<br>2=Fixed |
| `--weather` | int | 0 | Weather condition:<br>0=None<br>1=Spring<br>2=Summer<br>4=Autumn<br>8=Winter<br>16=Snow<br>32=Burning |
| `--is_indoor` | bool | False | If set, considers the yard as an indoor space. Ignored when group_def is 'custom' |
| `--output_type` | str | "gold_equiv" | Type of output to generate. Options:<br>- `silver`: Silver fish<br>- `gold`: Gold fish<br>- `silver_equiv`: Silver fish equivalent<br>- `gold_equiv`: Gold fish equivalent<br>- `cat_probability`: Probability (0-1) of a specific cat appearing |
| `--total_duration_minutes` | int | 1440 | Duration in minutes over which to aggregate the selected output_type. Ignored when output_type is 'cat_probability' |
| `--cat_id` | int | None | ID of the specific cat to analyze when output_type is 'cat_probability' |
| `--group_def` | str | "item" | Defines how to group items where a single cat cannot appear simultaneously:<br>- `playspace`: Individual seats within goodies (Turns off the consideration of whether the same can appear at different places at the same time)<br>- `item`: Entire goodie<br>- `custom`: User-defined groups via items_of_interest arguments |
| `--items_of_interest_indoors` | List[int] | None | List of goodie IDs to analyze as indoor items. Only used when group_def is 'custom' |
| `--items_of_interest_outdoors` | List[int] | None | List of goodie IDs to analyze as outdoor items. Only used when group_def is 'custom' |
| `--num_iterations_for_cat_on_cat` | int | 10 | Number of iterations to simulate cat-on-cat interactions |

## Output Types Explained

- **Silver/Gold Fish**: Direct count of expected fish earnings
- **Silver/Gold Equivalent**: Converts all earnings to a single currency using exchange rate. Neko Atsume 2 removed the option to go from silver to gold, but you can still "convert" it by purchasing "Selectable" items.
- **Cat Probability**: Shows likelihood (0-1) of specified cat appearing

## Examples

### Maximizing Gold Fish Earnings
```bash
# Use premium food in indoor yard
python analyze.py --food_type 5 --is_indoor --output_type gold

# Check earnings over 12 hours
python analyze.py --food_type 2 --total_duration_minutes 720
```

### Analyzing Specific Cat Visits
```bash
# Check probability of rare cat (Peaches!!) appearing
# You can find the cat id to name mapping in `data/cat_id_to_name.json`
python analyze.py --output_type cat_probability --cat_id 24 --food_type 5

# Analyze with specific weather condition
python analyze.py --output_type cat_probability --cat_id 12 --weather 1
```

### Understanding Your Yard's Gold Fish Equivalent Per Day
```bash
# Analyze specific indoor/outdoor item combinations
python analyze.py --group_def custom \
                   --items_of_interest_indoors 122 100 178 109 \
                   --items_of_interest_outdoors 258 222 106 304
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Based on game data from Neko Atsume 2, V1.0.0 by Hit-Point Co.,Ltd. Thanks a lot for this cute cats game!!!
- All the previous efforts! [1](https://www.reddit.com/r/nekoatsume/comments/blmtwo/neko_atsume_data_mining_spreadsheet_update_1130/), [2](https://www.reddit.com/r/nekoatsume/comments/fhwtb3/neko_atsume_datamining_webapp/), [3](https://www.reddit.com/r/nekoatsume/comments/1gb7qap/neko_atsume_2_datamining_thread/), [4](https://www.reddit.com/r/nekoatsume/comments/42cuc2/reverse_engineering_and_data_mining_neko_atsume/), [5](https://www.reddit.com/r/nekoatsume/comments/5q69v1/which_is_the_best_goodie_per_feed_goodie_analysis/) and more.

## High Level Overview
![](figs/flowchart.svg)

## Notes/Caveats
- After computing the same cat interaction, I should still update the cat-on-cat charm value, but I didn't do that. 
- The same cat interaction implementation is wrong. It should give some approximation. It'd be nice if someone can pick it up! 
- I did not do Sapphire & Jeeves calculation as 
    1. They are not added yet
    2. It will result in hardcoding a ton of stuff
    3. My current framework also does not support the exclusion indices they require (they take up 2 spots from other spaces, but my excluded indices supports only one spot calculation. It'd also be nice if someone can fix it)
- Most of the goodies are not in NA 2 yet!

## Todos

- Automatic optimizing the yard setup
- Include Tubbs calculation (Tubb's included in the output, but I didn't consider when they eat off the entire bowl)
- Keep it up-to-date
- Address the caveats

## Outputs 
### Outdoors, Silver Fish Equivalent per Item, Frisky Bitz, All Items Intact
Putting it here for the new players :)
#### Args
Namespace(food_type=2, item_damage_state=0, weather=0, is_indoor=False, output_type='silver_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   Goodie Id | Name                                  | Is Large   |     Value |
|-------------|---------------------------------------|------------|-----------|
|         260 | Round Kotatsu                         | True       | 660.696   |
|         227 | Cat Metropolis                        | True       | 630.944   |
|         230 | Tower of Treats                       | True       | 629.607   |
|         259 | Kotatsu                               | True       | 627.436   |
|         261 | Sunken Fireplace                      | True       | 597.065   |
|         226 | Cat Condo Complex                     | True       | 588.515   |
|         123 | Cardboard Choo-choo                   | True       | 586.344   |
|         231 | Bureau with Pot                       | True       | 578.133   |
|         229 | Art Deco Cat Tree                     | True       | 560.773   |
|         221 | Paper Umbrella                        | True       | 488.095   |
|         121 | Cardboard House                       | True       | 480.949   |
|         169 | Large Cooling Mat                     | True       | 476.61    |
|         235 | Tunnel (3D Piece)                     | True       | 471.988   |
|         267 | Space Heater                          | True       | 470.208   |
|         228 | Athletic Cat-Gym                      | True       | 468.036   |
|         223 | Fairy-tale Parasol                    | True       | 454.463   |
|         222 | Beach Umbrella                        | True       | 438.127   |
|         264 | Hot Mat (Large)                       | True       | 428.857   |
|         122 | Cardboard Cafe                        | True       | 422.901   |
|         207 | Antique Chair                         | True       | 372.934   |
|         234 | Tunnel (T Piece)                      | True       | 372.663   |
|         265 | Heating Stove                         | True       | 369.601   |
|         159 | Dice Cube                             | False      | 362.954   |
|         225 | Three-tier Cat Tree                   | True       | 360.209   |
|         158 | Tiramisu Cube                         | False      | 354.883   |
|         197 | Zanzibar Cushion                      | False      | 345.284   |
|         224 | Two-tier Cat Tree                     | True       | 332.501   |
|         180 | -                                     | -          | 332.438   |
|         233 | Tunnel (U Piece)                      | True       | 325.18    |
|         160 | Stump House                           | False      | 318.357   |
|         156 | Orange Cube                           | False      | 317.474   |
|         155 | Royal Bed                             | False      | 312.77    |
|         157 | Navy-blue Cube                        | False      | 311.709   |
|         239 | Doughnut Tunnel                       | True       | 302.138   |
|         124 | Dino Deluxe                           | True       | 294.818   |
|         232 | Tunnel (I Piece)                      | True       | 294.459   |
|         306 | -                                     | -          | 287.972   |
|         128 | Silk Crepe Pillow                     | False      | 285.692   |
|         200 | Giant Cushion (White)                 | True       | 282.005   |
|         199 | Giant Cushion                         | False      | 282.003   |
|         286 | Kokeshi Pot (Flow)                    | False      | 279.703   |
|         237 | Fish-stick Tunnel                     | False      | 279.442   |
|         161 | Bamboo House                          | False      | 277.456   |
|         238 | Cow Tunnel                            | True       | 276.195   |
|         196 | Egg Bed (Nightview)                   | False      | 274.991   |
|         266 | Panel Heater                          | True       | 274.784   |
|         293 | Snow Sled                             | False      | 273.904   |
|         236 | Carp Tunnel                           | True       | 273.449   |
|         285 | Kokeshi Pot (Blossom)                 | False      | 261.556   |
|         287 | Kokeshi Pot (Spring)                  | False      | 258.234   |
|         181 | -                                     | -          | 256.49    |
|         213 | Shiitake House                        | False      | 255.393   |
|         194 | Egg Bed (Black)                       | False      | 250.522   |
|         182 | -                                     | -          | 238.868   |
|         214 | Bamboo Rocket                         | False      | 235.834   |
|         212 | Mushroom House                        | False      | 235.52    |
|         195 | Egg Bed (Pink)                        | False      | 232.899   |
|         281 | Lacquered Bowl                        | False      | 231.761   |
|         179 | Pancake Cushion                       | False      | 230.44    |
|         270 | Kiddy Rucksack (Blue)                 | False      | 226.849   |
|         131 | Snowy Pillow                          | False      | 225.823   |
|         187 | Chestnut Cushion                      | False      | 225.612   |
|         193 | Egg Bed (White)                       | False      | 223.873   |
|         190 | Melon Coccoon                         | False      | 223.035   |
|         130 | Maple Pillow                          | False      | 219.037   |
|         111 | Temari Ball                           | False      | 218.439   |
|         107 | Soccer Ball                           | False      | 218.438   |
|         175 | Mister Penguin                        | False      | 217.875   |
|         188 | Plum Coccoon                          | False      | 217.748   |
|         129 | Sakura Pillow                         | False      | 214.839   |
|         100 | Baseball                              | False      | 208.228   |
|         276 | Scratching Log                        | False      | 207.62    |
|         210 | Tent (Blizzard)                       | False      | 207.209   |
|         142 | Cushion (Green)                       | False      | 202.489   |
|         162 | Biscuit Mat                           | False      | 201.532   |
|         178 | Burger Cushion                        | False      | 199.97    |
|         254 | Kick Toy (Saury)                      | False      | 198.689   |
|         298 | Cowboy Hat                            | False      | 198.511   |
|         192 | Strawberry Cocoon                     | False      | 197.652   |
|         186 | Basket Case                           | False      | 196.758   |
|         191 | Berry Coccoon                         | False      | 195.932   |
|         252 | Kick Toy (Fish)                       | False      | 193.252   |
|         198 | Bean Bag                              | False      | 192.994   |
|         168 | Manta Gel Mat                         | False      | 192.489   |
|         263 | Hot Mat (Small)                       | False      | 189.205   |
|         176 | Sakuramochi Cushion                   | False      | 189.02    |
|         216 | Pom-pom Sock                          | False      | 188.568   |
|         183 | Head Space                            | False      | 188.115   |
|         217 | Colorful Sock                         | False      | 187.727   |
|         104 | Watermelon Ball                       | False      | 184.114   |
|         108 | Stress Reliever                       | False      | 184.095   |
|         189 | Orange Coccoon                        | False      | 183.945   |
|         145 | Cushion (Lemon)                       | False      | 182.568   |
|         184 | Black Head Space                      | False      | 181.828   |
|         139 | Cushion (Pink)                        | False      | 181.743   |
|         280 | Iron Teapod                           | False      | 181.716   |
|         167 | Marble Pad                            | False      | 181.419   |
|         278 | Earthenware Pot                       | False      | 180.357   |
|         177 | Kashiwamochi Cushion                  | False      | 179.516   |
|         172 | Plum Cushion (Pink)                   | False      | 179.514   |
|         294 | Goldfish Bowl                         | False      | 178.732   |
|         271 | Kiddy Rucksack (Lime)                 | False      | 178.499   |
|         185 | White Head Space                      | False      | 178.19    |
|         154 | Fluffy Bed (Brown)                    | False      | 177.799   |
|         140 | Cushion (Brown)                       | False      | 177.429   |
|         146 | Cushion (Orange)                      | False      | 177.186   |
|         255 | -                                     | -          | 175.481   |
|         126 | Pillow (Yellow)                       | False      | 175.411   |
|         115 | Shopping Box (Small)                  | False      | 175.032   |
|         174 | Sheep Cushion                         | False      | 174.327   |
|         269 | Kiddy Rucksack (Pink)                 | False      | 174.169   |
|         305 | Kiddy Rucksack (Pink)                 | False      | 174.169   |
|         171 | Plum Cushion (Red)                    | False      | 173.268   |
|         152 | Fluffy Bed (White)                    | False      | 172.82    |
|         109 | Ball of Yarn                          | False      | 172.624   |
|         125 | Pillow (Purple)                       | False      | 172.592   |
|         110 | Toy Capsule                           | False      | 172.011   |
|         132 | Grass Cushion (Red)                   | False      | 171.41    |
|         165 | Aluminium Bowl                        | False      | 171.405   |
|         106 | Ping-Pong Ball                        | False      | 170.8     |
|         163 | Thick Cooling Pad                     | False      | 170.195   |
|         138 | Cushion (Beige)                       | False      | 169.641   |
|         268 | Pile of Leaves                        | False      | 169.435   |
|         114 | Gift Box (Green)                      | False      | 168.589   |
|         103 | Rubber Ball (Blue)                    | False      | 168.544   |
|         295 | Snow Dome                             | False      | 168.53    |
|         101 | Rubber Ball (Red)                     | False      | 168.12    |
|         253 | Kick Toy (Bunny)                      | False      | 166.79    |
|         127 | Pillow (Green)                        | False      | 166.376   |
|         113 | Gift Box (Red)                        | False      | 166.138   |
|         262 | Hot-Water Bottle                      | False      | 165.847   |
|         117 | Cardboard (Flat)                      | False      | 164.517   |
|         245 | Wing-thing Teaser                     | False      | 164.479   |
|         275 | Scratching Post                       | False      | 164.252   |
|         247 | Zebra Grass Gadget                    | False      | 164.168   |
|         251 | Kick Toy (Mouse)                      | False      | 164.132   |
|         244 | Tail-thing Teaser                     | False      | 163.928   |
|         218 | Arabesque Blanket                     | False      | 163.208   |
|         170 | Fluffy Cushion                        | False      | 163.084   |
|         147 | -                                     | -          | 162.211   |
|         277 | Fruit Basket                          | False      | 161.179   |
|         105 | Beach Ball                            | False      | 160.589   |
|         303 | Cream-puff House                      | False      | 160.36    |
|         220 | Cozy Blanket (Yellow)                 | False      | 159.658   |
|         102 | Rubber Ball (Yellow)                  | False      | 159.463   |
|         258 | Twisty Rail                           | True       | 159.34    |
|         137 | Cypress Mat                           | False      | 159.015   |
|         134 | Grass Cushion (Green)                 | False      | 158.418   |
|         211 | Tent (Pyramid)                        | False      | 158.138   |
|         279 | Rice Kettle                           | False      | 157.474   |
|         173 | Plum Cushion (White)                  | False      | 157.294   |
|         292 | Wooden Pail                           | False      | 157.095   |
|         153 | Fluffy Bed (Pink)                     | False      | 156.405   |
|         135 | Grass Cushion (Purple)                | False      | 156.022   |
|         149 | Shroom House (Red)                    | False      | 155.273   |
|         302 | Cat Pancake                           | False      | 154.473   |
|         219 | Cozy Blanket (Red)                    | False      | 154.405   |
|         301 | Cat Macaron (Green)                   | False      | 153.466   |
|         118 | Cardboard Truck                       | False      | 153.427   |
|         249 | Mister Mouse                          | False      | 152.782   |
|         215 | Warm Sock                             | False      | 152.677   |
|         304 | Box Tissue                            | False      | 152.583   |
|         133 | Grass Cushion (Navy)                  | False      | 152.497   |
|         300 | Cat Macaron (Pink)                    | False      | 152.272   |
|         274 | Scratching Board                      | False      | 151.916   |
|         201 | Hammock (Yellow)                      | False      | 151.749   |
|         148 | Lucky Cushion                         | False      | 151.748   |
|         250 | Mister Dragonfly                      | False      | 150.08    |
|         296 | Glass Vase                            | False      | 149.501   |
|         116 | Shopping Box (Large)                  | False      | 148.636   |
|         288 | Planter                               | False      | 147.758   |
|         144 | Cushion (B&W)                         | False      | 147.623   |
|         164 | Cool Aluminum Pad                     | False      | 146.155   |
|         202 | Hammock (Pink)                        | False      | 146.153   |
|         240 | Choco Cornet Tunnel                   | False      | 145.723   |
|         205 | -                                     | -          | 145.468   |
|         141 | Cushion (Yellow)                      | False      | 145.447   |
|         206 | -                                     | -          | 144.816   |
|         150 | Shroom House (Blue)                   | False      | 144.77    |
|         256 | Busy Bee                              | False      | 142.469   |
|         284 | Honey Pot                             | False      | 142.115   |
|         297 | Jumbo Glass Mug                       | False      | 141.788   |
|         209 | Tent (Modern Red)                     | False      | 140.793   |
|         204 | Luxurious Hammock                     | False      | 140.49    |
|         246 | Wild-thing Teaser                     | False      | 140.074   |
|         283 | Pickling Pot                          | False      | 138.939   |
|         299 | Wood Pail                             | False      | 138.934   |
|         282 | Clay Pot                              | False      | 138.332   |
|         151 | Shroom House (Green)                  | False      | 138.22    |
|         120 | Luxury Treasure-box                   | False      | 137.582   |
|         136 | Pinewood Mat                          | False      | 137.472   |
|         166 | Aluminium Pot                         | False      | 137.444   |
|         208 | Tent (Nature)                         | False      | 134.877   |
|         119 | Treasure-box                          | False      | 134.151   |
|         243 | Shell Tunnel (White)                  | False      | 133.412   |
|         241 | Shell Tunnel (Pink)                   | False      | 132.652   |
|         203 | Hammock (Woven)                       | False      | 129.622   |
|         242 | Shell Tunnel (Blue)                   | False      | 128.873   |
|         257 | Butterfly Swarm                       | False      | 128.683   |
|         248 | Fluff-thing Teaser                    | False      | 127.592   |
|         289 | Bucket (Blue)                         | False      | 123.24    |
|         273 | Plastic Bag                           | False      | 121.544   |
|         291 | Bucket (Yellow)                       | False      | 118.686   |
|         290 | Bucket (Red)                          | False      | 116.927   |
|         112 | Cake Box                              | False      | 116.672   |
|         272 | Paper Bag                             | False      | 116.241   |
|         143 | Cushion (Choco mint)                  | False      | 109.288   |
|           6 | Sashimi  (Tubbs/Whiteshadow)          | False      | 102.768   |
|           2 | Frisky Bitz (Tubbs/Whiteshadow)       | False      | 101.018   |
|           3 | Ritzy Bitz  (Tubbs/Whiteshadow)       | False      |  96.443   |
|           5 | Bonito Bitz  (Tubbs/Whiteshadow)      | False      |   4.15461 |
|           4 | Deluxe Tuna Bitz  (Tubbs/Whiteshadow) | False      |   3.40977 |

### Outdoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Intact
#### Args
Namespace(food_type=2, item_damage_state=0, weather=0, is_indoor=False, output_type='gold_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   Goodie Id | Name                                  | Is Large   |     Value |
|-------------|---------------------------------------|------------|-----------|
|         227 | Cat Metropolis                        | True       | 21.2458   |
|         260 | Round Kotatsu                         | True       | 20.0598   |
|         230 | Tower of Treats                       | True       | 19.9582   |
|         226 | Cat Condo Complex                     | True       | 19.4255   |
|         259 | Kotatsu                               | True       | 19.1952   |
|         231 | Bureau with Pot                       | True       | 19.0685   |
|         123 | Cardboard Choo-choo                   | True       | 18.1548   |
|         261 | Sunken Fireplace                      | True       | 17.8122   |
|         229 | Art Deco Cat Tree                     | True       | 17.3395   |
|         235 | Tunnel (3D Piece)                     | True       | 15.6417   |
|         228 | Athletic Cat-Gym                      | True       | 15.3766   |
|         221 | Paper Umbrella                        | True       | 14.7199   |
|         169 | Large Cooling Mat                     | True       | 14.5777   |
|         267 | Space Heater                          | True       | 14.4383   |
|         121 | Cardboard House                       | True       | 14.2422   |
|         223 | Fairy-tale Parasol                    | True       | 13.75     |
|         264 | Hot Mat (Large)                       | True       | 13.6147   |
|         222 | Beach Umbrella                        | True       | 13.508    |
|         122 | Cardboard Cafe                        | True       | 12.8399   |
|         234 | Tunnel (T Piece)                      | True       | 12.2929   |
|         225 | Three-tier Cat Tree                   | True       | 11.755    |
|         265 | Heating Stove                         | True       | 11.687    |
|         207 | Antique Chair                         | True       | 10.7174   |
|         159 | Dice Cube                             | False      | 10.5234   |
|         158 | Tiramisu Cube                         | False      | 10.5175   |
|         224 | Two-tier Cat Tree                     | True       |  9.94268  |
|         233 | Tunnel (U Piece)                      | True       |  9.71598  |
|         156 | Orange Cube                           | False      |  9.68495  |
|         160 | Stump House                           | False      |  9.62901  |
|         157 | Navy-blue Cube                        | False      |  9.529    |
|         239 | Doughnut Tunnel                       | True       |  9.20334  |
|         232 | Tunnel (I Piece)                      | True       |  9.07597  |
|         124 | Dino Deluxe                           | True       |  8.98072  |
|         238 | Cow Tunnel                            | True       |  8.86414  |
|         161 | Bamboo House                          | False      |  8.84849  |
|         200 | Giant Cushion (White)                 | True       |  8.83962  |
|         236 | Carp Tunnel                           | True       |  8.81153  |
|         237 | Fish-stick Tunnel                     | False      |  8.78147  |
|         199 | Giant Cushion                         | False      |  8.76837  |
|         266 | Panel Heater                          | True       |  8.75578  |
|         180 | -                                     | -          |  8.74853  |
|         293 | Snow Sled                             | False      |  8.7219   |
|         197 | Zanzibar Cushion                      | False      |  8.50875  |
|         213 | Shiitake House                        | False      |  8.49321  |
|         212 | Mushroom House                        | False      |  7.80265  |
|         155 | Royal Bed                             | False      |  7.75387  |
|         306 | -                                     | -          |  7.47606  |
|         128 | Silk Crepe Pillow                     | False      |  7.29102  |
|         181 | -                                     | -          |  7.21221  |
|         196 | Egg Bed (Nightview)                   | False      |  7.20278  |
|         286 | Kokeshi Pot (Flow)                    | False      |  7.20005  |
|         285 | Kokeshi Pot (Blossom)                 | False      |  6.96463  |
|         287 | Kokeshi Pot (Spring)                  | False      |  6.9158   |
|         194 | Egg Bed (Black)                       | False      |  6.82286  |
|         182 | -                                     | -          |  6.80172  |
|         179 | Pancake Cushion                       | False      |  6.64774  |
|         195 | Egg Bed (Pink)                        | False      |  6.43383  |
|         281 | Lacquered Bowl                        | False      |  6.38661  |
|         214 | Bamboo Rocket                         | False      |  6.33065  |
|         270 | Kiddy Rucksack (Blue)                 | False      |  6.23846  |
|         187 | Chestnut Cushion                      | False      |  6.19562  |
|         130 | Maple Pillow                          | False      |  6.19054  |
|         107 | Soccer Ball                           | False      |  6.15308  |
|         131 | Snowy Pillow                          | False      |  6.15018  |
|         193 | Egg Bed (White)                       | False      |  6.1109   |
|         129 | Sakura Pillow                         | False      |  6.07789  |
|         175 | Mister Penguin                        | False      |  6.02161  |
|         178 | Burger Cushion                        | False      |  6.02053  |
|         298 | Cowboy Hat                            | False      |  5.94566  |
|         188 | Plum Coccoon                          | False      |  5.90585  |
|         100 | Baseball                              | False      |  5.89757  |
|         111 | Temari Ball                           | False      |  5.8734   |
|         190 | Melon Coccoon                         | False      |  5.82791  |
|         162 | Biscuit Mat                           | False      |  5.7576   |
|         276 | Scratching Log                        | False      |  5.74482  |
|         186 | Basket Case                           | False      |  5.71471  |
|         192 | Strawberry Cocoon                     | False      |  5.643    |
|         254 | Kick Toy (Saury)                      | False      |  5.61821  |
|         191 | Berry Coccoon                         | False      |  5.584    |
|         210 | Tent (Blizzard)                       | False      |  5.58313  |
|         168 | Manta Gel Mat                         | False      |  5.53915  |
|         142 | Cushion (Green)                       | False      |  5.53303  |
|         252 | Kick Toy (Fish)                       | False      |  5.52367  |
|         176 | Sakuramochi Cushion                   | False      |  5.44201  |
|         216 | Pom-pom Sock                          | False      |  5.43966  |
|         198 | Bean Bag                              | False      |  5.42997  |
|         108 | Stress Reliever                       | False      |  5.42318  |
|         104 | Watermelon Ball                       | False      |  5.41787  |
|         263 | Hot Mat (Small)                       | False      |  5.40866  |
|         217 | Colorful Sock                         | False      |  5.3985   |
|         189 | Orange Coccoon                        | False      |  5.32494  |
|         271 | Kiddy Rucksack (Lime)                 | False      |  5.30516  |
|         269 | Kiddy Rucksack (Pink)                 | False      |  5.28675  |
|         305 | Kiddy Rucksack (Pink)                 | False      |  5.28675  |
|         172 | Plum Cushion (Pink)                   | False      |  5.23921  |
|         294 | Goldfish Bowl                         | False      |  5.2391   |
|         278 | Earthenware Pot                       | False      |  5.23011  |
|         154 | Fluffy Bed (Brown)                    | False      |  5.22518  |
|         177 | Kashiwamochi Cushion                  | False      |  5.22292  |
|         171 | Plum Cushion (Red)                    | False      |  5.22289  |
|         139 | Cushion (Pink)                        | False      |  5.21894  |
|         183 | Head Space                            | False      |  5.20087  |
|         255 | -                                     | -          |  5.19812  |
|         115 | Shopping Box (Small)                  | False      |  5.19707  |
|         145 | Cushion (Lemon)                       | False      |  5.19663  |
|         184 | Black Head Space                      | False      |  5.18882  |
|         126 | Pillow (Yellow)                       | False      |  5.18776  |
|         280 | Iron Teapod                           | False      |  5.18592  |
|         101 | Rubber Ball (Red)                     | False      |  5.18113  |
|         140 | Cushion (Brown)                       | False      |  5.15966  |
|         125 | Pillow (Purple)                       | False      |  5.14626  |
|         138 | Cushion (Beige)                       | False      |  5.13908  |
|         268 | Pile of Leaves                        | False      |  5.12375  |
|         109 | Ball of Yarn                          | False      |  5.1222   |
|         174 | Sheep Cushion                         | False      |  5.11801  |
|         146 | Cushion (Orange)                      | False      |  5.11287  |
|         132 | Grass Cushion (Red)                   | False      |  5.08131  |
|         167 | Marble Pad                            | False      |  5.07922  |
|         103 | Rubber Ball (Blue)                    | False      |  5.07316  |
|         185 | White Head Space                      | False      |  5.06174  |
|         251 | Kick Toy (Mouse)                      | False      |  5.06157  |
|         152 | Fluffy Bed (White)                    | False      |  5.04647  |
|         244 | Tail-thing Teaser                     | False      |  5.04606  |
|         114 | Gift Box (Green)                      | False      |  5.02308  |
|         247 | Zebra Grass Gadget                    | False      |  5.01669  |
|         110 | Toy Capsule                           | False      |  5.01486  |
|         295 | Snow Dome                             | False      |  5.01164  |
|         253 | Kick Toy (Bunny)                      | False      |  5.00328  |
|         127 | Pillow (Green)                        | False      |  4.99517  |
|         105 | Beach Ball                            | False      |  4.98718  |
|         218 | Arabesque Blanket                     | False      |  4.98076  |
|         163 | Thick Cooling Pad                     | False      |  4.97941  |
|         137 | Cypress Mat                           | False      |  4.97813  |
|         245 | Wing-thing Teaser                     | False      |  4.97556  |
|         113 | Gift Box (Red)                        | False      |  4.94881  |
|         262 | Hot-Water Bottle                      | False      |  4.94732  |
|         170 | Fluffy Cushion                        | False      |  4.91837  |
|         106 | Ping-Pong Ball                        | False      |  4.9161   |
|         147 | -                                     | -          |  4.91002  |
|         102 | Rubber Ball (Yellow)                  | False      |  4.89932  |
|         117 | Cardboard (Flat)                      | False      |  4.85604  |
|         135 | Grass Cushion (Purple)                | False      |  4.83423  |
|         134 | Grass Cushion (Green)                 | False      |  4.83049  |
|         303 | Cream-puff House                      | False      |  4.81836  |
|         220 | Cozy Blanket (Yellow)                 | False      |  4.81643  |
|         292 | Wooden Pail                           | False      |  4.80698  |
|         304 | Box Tissue                            | False      |  4.79421  |
|         173 | Plum Cushion (White)                  | False      |  4.77902  |
|         277 | Fruit Basket                          | False      |  4.76406  |
|         153 | Fluffy Bed (Pink)                     | False      |  4.7477   |
|         301 | Cat Macaron (Green)                   | False      |  4.73201  |
|         300 | Cat Macaron (Pink)                    | False      |  4.7219   |
|         118 | Cardboard Truck                       | False      |  4.71761  |
|         165 | Aluminium Bowl                        | False      |  4.70504  |
|         250 | Mister Dragonfly                      | False      |  4.70038  |
|         275 | Scratching Post                       | False      |  4.68864  |
|         215 | Warm Sock                             | False      |  4.6828   |
|         279 | Rice Kettle                           | False      |  4.68225  |
|         302 | Cat Pancake                           | False      |  4.68047  |
|         201 | Hammock (Yellow)                      | False      |  4.66812  |
|         133 | Grass Cushion (Navy)                  | False      |  4.66133  |
|         148 | Lucky Cushion                         | False      |  4.6241   |
|         116 | Shopping Box (Large)                  | False      |  4.62231  |
|         274 | Scratching Board                      | False      |  4.60764  |
|         219 | Cozy Blanket (Red)                    | False      |  4.60576  |
|         240 | Choco Cornet Tunnel                   | False      |  4.6055   |
|         249 | Mister Mouse                          | False      |  4.60183  |
|         296 | Glass Vase                            | False      |  4.57885  |
|         202 | Hammock (Pink)                        | False      |  4.57829  |
|         297 | Jumbo Glass Mug                       | False      |  4.55998  |
|         258 | Twisty Rail                           | True       |  4.54839  |
|         288 | Planter                               | False      |  4.52325  |
|         205 | -                                     | -          |  4.52088  |
|         206 | -                                     | -          |  4.4754   |
|         136 | Pinewood Mat                          | False      |  4.45691  |
|         256 | Busy Bee                              | False      |  4.43905  |
|         211 | Tent (Pyramid)                        | False      |  4.41959  |
|         299 | Wood Pail                             | False      |  4.41801  |
|         149 | Shroom House (Red)                    | False      |  4.40047  |
|         209 | Tent (Modern Red)                     | False      |  4.39816  |
|         243 | Shell Tunnel (White)                  | False      |  4.37862  |
|         241 | Shell Tunnel (Pink)                   | False      |  4.34967  |
|         164 | Cool Aluminum Pad                     | False      |  4.2968   |
|         144 | Cushion (B&W)                         | False      |  4.2847   |
|         141 | Cushion (Yellow)                      | False      |  4.2665   |
|         119 | Treasure-box                          | False      |  4.23734  |
|         208 | Tent (Nature)                         | False      |  4.23497  |
|         246 | Wild-thing Teaser                     | False      |  4.21514  |
|         242 | Shell Tunnel (Blue)                   | False      |  4.21478  |
|         120 | Luxury Treasure-box                   | False      |  4.2137   |
|         204 | Luxurious Hammock                     | False      |  4.20268  |
|         166 | Aluminium Pot                         | False      |  4.18313  |
|         284 | Honey Pot                             | False      |  4.17603  |
|         282 | Clay Pot                              | False      |  4.16737  |
|         283 | Pickling Pot                          | False      |  4.15846  |
|         289 | Bucket (Blue)                         | False      |  4.09512  |
|         150 | Shroom House (Blue)                   | False      |  4.03416  |
|         291 | Bucket (Yellow)                       | False      |  4.03315  |
|         203 | Hammock (Woven)                       | False      |  4.02946  |
|         273 | Plastic Bag                           | False      |  3.94168  |
|         112 | Cake Box                              | False      |  3.94141  |
|         290 | Bucket (Red)                          | False      |  3.92542  |
|         151 | Shroom House (Green)                  | False      |  3.87257  |
|         248 | Fluff-thing Teaser                    | False      |  3.83605  |
|         257 | Butterfly Swarm                       | False      |  3.81354  |
|         272 | Paper Bag                             | False      |  3.65898  |
|         143 | Cushion (Choco mint)                  | False      |  3.29843  |
|           6 | Sashimi  (Tubbs/Whiteshadow)          | False      |  2.26062  |
|           2 | Frisky Bitz (Tubbs/Whiteshadow)       | False      |  2.25299  |
|           3 | Ritzy Bitz  (Tubbs/Whiteshadow)       | False      |  2.18471  |
|           5 | Bonito Bitz  (Tubbs/Whiteshadow)      | False      |  0.134993 |
|           4 | Deluxe Tuna Bitz  (Tubbs/Whiteshadow) | False      |  0.110792 |

### Indoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Intact
#### Args
Namespace(food_type=2, item_damage_state=0, weather=0, is_indoor=True, output_type='gold_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   Goodie Id | Name                                  | Is Large   |     Value |
|-------------|---------------------------------------|------------|-----------|
|         227 | Cat Metropolis                        | True       | 38.3334   |
|         226 | Cat Condo Complex                     | True       | 34.5644   |
|         230 | Tower of Treats                       | True       | 34.4727   |
|         231 | Bureau with Pot                       | True       | 33.9112   |
|         260 | Round Kotatsu                         | True       | 33.4861   |
|         259 | Kotatsu                               | True       | 32.2422   |
|         123 | Cardboard Choo-choo                   | True       | 30.7899   |
|         229 | Art Deco Cat Tree                     | True       | 29.3753   |
|         261 | Sunken Fireplace                      | True       | 29.301    |
|         235 | Tunnel (3D Piece)                     | True       | 27.9106   |
|         228 | Athletic Cat-Gym                      | True       | 27.269    |
|         169 | Large Cooling Mat                     | True       | 24.4817   |
|         221 | Paper Umbrella                        | True       | 24.4356   |
|         267 | Space Heater                          | True       | 24.3245   |
|         264 | Hot Mat (Large)                       | True       | 23.5423   |
|         121 | Cardboard House                       | True       | 23.2805   |
|         223 | Fairy-tale Parasol                    | True       | 22.8871   |
|         222 | Beach Umbrella                        | True       | 22.8316   |
|         234 | Tunnel (T Piece)                      | True       | 21.8633   |
|         122 | Cardboard Cafe                        | True       | 21.4339   |
|         225 | Three-tier Cat Tree                   | True       | 20.746    |
|         265 | Heating Stove                         | True       | 20.1479   |
|         158 | Tiramisu Cube                         | False      | 17.2041   |
|         207 | Antique Chair                         | True       | 17.0599   |
|         159 | Dice Cube                             | False      | 16.8855   |
|         224 | Two-tier Cat Tree                     | True       | 16.3881   |
|         156 | Orange Cube                           | False      | 16.2303   |
|         160 | Stump House                           | False      | 16.0234   |
|         233 | Tunnel (U Piece)                      | True       | 16.0036   |
|         157 | Navy-blue Cube                        | False      | 15.9962   |
|         238 | Cow Tunnel                            | True       | 15.4536   |
|         236 | Carp Tunnel                           | True       | 15.408    |
|         239 | Doughnut Tunnel                       | True       | 15.4044   |
|         161 | Bamboo House                          | False      | 15.3535   |
|         232 | Tunnel (I Piece)                      | True       | 15.337    |
|         213 | Shiitake House                        | False      | 15.1921   |
|         266 | Panel Heater                          | True       | 15.1828   |
|         200 | Giant Cushion (White)                 | True       | 15.137    |
|         293 | Snow Sled                             | False      | 15.1165   |
|         237 | Fish-stick Tunnel                     | False      | 15.0669   |
|         124 | Dino Deluxe                           | True       | 15.0322   |
|         199 | Giant Cushion                         | False      | 14.9203   |
|         212 | Mushroom House                        | False      | 13.9197   |
|         180 | -                                     | -          | 12.7585   |
|         197 | Zanzibar Cushion                      | False      | 11.4939   |
|         181 | -                                     | -          | 11.2501   |
|         306 | -                                     | -          | 10.7409   |
|         182 | -                                     | -          | 10.7357   |
|         179 | Pancake Cushion                       | False      | 10.6185   |
|         155 | Royal Bed                             | False      | 10.5526   |
|         196 | Egg Bed (Nightview)                   | False      | 10.4505   |
|         194 | Egg Bed (Black)                       | False      | 10.3145   |
|         285 | Kokeshi Pot (Blossom)                 | False      | 10.2859   |
|         287 | Kokeshi Pot (Spring)                  | False      | 10.2758   |
|         128 | Silk Crepe Pillow                     | False      | 10.273    |
|         286 | Kokeshi Pot (Flow)                    | False      | 10.2459   |
|         178 | Burger Cushion                        | False      |  9.98036  |
|         195 | Egg Bed (Pink)                        | False      |  9.86544  |
|         298 | Cowboy Hat                            | False      |  9.81343  |
|         281 | Lacquered Bowl                        | False      |  9.76921  |
|         130 | Maple Pillow                          | False      |  9.70301  |
|         107 | Soccer Ball                           | False      |  9.61405  |
|         129 | Sakura Pillow                         | False      |  9.53532  |
|         270 | Kiddy Rucksack (Blue)                 | False      |  9.52329  |
|         187 | Chestnut Cushion                      | False      |  9.44452  |
|         214 | Bamboo Rocket                         | False      |  9.42932  |
|         131 | Snowy Pillow                          | False      |  9.29752  |
|         100 | Baseball                              | False      |  9.26226  |
|         193 | Egg Bed (White)                       | False      |  9.25926  |
|         175 | Mister Penguin                        | False      |  9.23762  |
|         186 | Basket Case                           | False      |  9.184    |
|         162 | Biscuit Mat                           | False      |  9.11552  |
|         192 | Strawberry Cocoon                     | False      |  8.92864  |
|         188 | Plum Coccoon                          | False      |  8.89078  |
|         168 | Manta Gel Mat                         | False      |  8.82787  |
|         108 | Stress Reliever                       | False      |  8.8249   |
|         269 | Kiddy Rucksack (Pink)                 | False      |  8.82351  |
|         305 | Kiddy Rucksack (Pink)                 | False      |  8.82351  |
|         276 | Scratching Log                        | False      |  8.82301  |
|         191 | Berry Coccoon                         | False      |  8.82083  |
|         254 | Kick Toy (Saury)                      | False      |  8.80999  |
|         104 | Watermelon Ball                       | False      |  8.80791  |
|         111 | Temari Ball                           | False      |  8.76333  |
|         101 | Rubber Ball (Red)                     | False      |  8.75426  |
|         252 | Kick Toy (Fish)                       | False      |  8.74899  |
|         271 | Kiddy Rucksack (Lime)                 | False      |  8.69906  |
|         216 | Pom-pom Sock                          | False      |  8.68863  |
|         176 | Sakuramochi Cushion                   | False      |  8.67696  |
|         171 | Plum Cushion (Red)                    | False      |  8.66679  |
|         217 | Colorful Sock                         | False      |  8.59851  |
|         263 | Hot Mat (Small)                       | False      |  8.56781  |
|         138 | Cushion (Beige)                       | False      |  8.56301  |
|         251 | Kick Toy (Mouse)                      | False      |  8.55675  |
|         189 | Orange Coccoon                        | False      |  8.53231  |
|         268 | Pile of Leaves                        | False      |  8.52497  |
|         244 | Tail-thing Teaser                     | False      |  8.51809  |
|         137 | Cypress Mat                           | False      |  8.51618  |
|         115 | Shopping Box (Small)                  | False      |  8.51477  |
|         255 | -                                     | -          |  8.49927  |
|         294 | Goldfish Bowl                         | False      |  8.48843  |
|         154 | Fluffy Bed (Brown)                    | False      |  8.48494  |
|         105 | Beach Ball                            | False      |  8.47811  |
|         198 | Bean Bag                              | False      |  8.47475  |
|         126 | Pillow (Yellow)                       | False      |  8.47066  |
|         125 | Pillow (Purple)                       | False      |  8.46186  |
|         172 | Plum Cushion (Pink)                   | False      |  8.45617  |
|         190 | Melon Coccoon                         | False      |  8.43345  |
|         247 | Zebra Grass Gadget                    | False      |  8.41879  |
|         103 | Rubber Ball (Blue)                    | False      |  8.40817  |
|         177 | Kashiwamochi Cushion                  | False      |  8.40654  |
|         278 | Earthenware Pot                       | False      |  8.39338  |
|         142 | Cushion (Green)                       | False      |  8.39259  |
|         109 | Ball of Yarn                          | False      |  8.38737  |
|         218 | Arabesque Blanket                     | False      |  8.34949  |
|         210 | Tent (Blizzard)                       | False      |  8.34832  |
|         132 | Grass Cushion (Red)                   | False      |  8.31358  |
|         174 | Sheep Cushion                         | False      |  8.30363  |
|         139 | Cushion (Pink)                        | False      |  8.30163  |
|         140 | Cushion (Brown)                       | False      |  8.30106  |
|         245 | Wing-thing Teaser                     | False      |  8.28068  |
|         253 | Kick Toy (Bunny)                      | False      |  8.26871  |
|         127 | Pillow (Green)                        | False      |  8.26131  |
|         102 | Rubber Ball (Yellow)                  | False      |  8.2578   |
|         114 | Gift Box (Green)                      | False      |  8.25401  |
|         304 | Box Tissue                            | False      |  8.22476  |
|         295 | Snow Dome                             | False      |  8.22166  |
|         184 | Black Head Space                      | False      |  8.20648  |
|         135 | Grass Cushion (Purple)                | False      |  8.20319  |
|         280 | Iron Teapod                           | False      |  8.20233  |
|         145 | Cushion (Lemon)                       | False      |  8.19941  |
|         147 | -                                     | -          |  8.17587  |
|         146 | Cushion (Orange)                      | False      |  8.16891  |
|         170 | Fluffy Cushion                        | False      |  8.16484  |
|         152 | Fluffy Bed (White)                    | False      |  8.14884  |
|         262 | Hot-Water Bottle                      | False      |  8.13781  |
|         113 | Gift Box (Red)                        | False      |  8.13022  |
|         134 | Grass Cushion (Green)                 | False      |  8.09198  |
|         110 | Toy Capsule                           | False      |  8.08642  |
|         292 | Wooden Pail                           | False      |  8.0756   |
|         163 | Thick Cooling Pad                     | False      |  8.05425  |
|         250 | Mister Dragonfly                      | False      |  8.04364  |
|         300 | Cat Macaron (Pink)                    | False      |  8.01777  |
|         301 | Cat Macaron (Green)                   | False      |  7.99879  |
|         220 | Cozy Blanket (Yellow)                 | False      |  7.99757  |
|         173 | Plum Cushion (White)                  | False      |  7.98228  |
|         183 | Head Space                            | False      |  7.9812   |
|         303 | Cream-puff House                      | False      |  7.97418  |
|         185 | White Head Space                      | False      |  7.97153  |
|         297 | Jumbo Glass Mug                       | False      |  7.96212  |
|         118 | Cardboard Truck                       | False      |  7.95661  |
|         240 | Choco Cornet Tunnel                   | False      |  7.93661  |
|         153 | Fluffy Bed (Pink)                     | False      |  7.92405  |
|         117 | Cardboard (Flat)                      | False      |  7.9156   |
|         167 | Marble Pad                            | False      |  7.89019  |
|         215 | Warm Sock                             | False      |  7.88195  |
|         201 | Hammock (Yellow)                      | False      |  7.876    |
|         116 | Shopping Box (Large)                  | False      |  7.86637  |
|         106 | Ping-Pong Ball                        | False      |  7.83646  |
|         202 | Hammock (Pink)                        | False      |  7.83593  |
|         136 | Pinewood Mat                          | False      |  7.82846  |
|         133 | Grass Cushion (Navy)                  | False      |  7.82418  |
|         302 | Cat Pancake                           | False      |  7.80006  |
|         277 | Fruit Basket                          | False      |  7.77488  |
|         243 | Shell Tunnel (White)                  | False      |  7.75945  |
|         148 | Lucky Cushion                         | False      |  7.74215  |
|         241 | Shell Tunnel (Pink)                   | False      |  7.70306  |
|         296 | Glass Vase                            | False      |  7.69811  |
|         205 | -                                     | -          |  7.68981  |
|         274 | Scratching Board                      | False      |  7.68507  |
|         279 | Rice Kettle                           | False      |  7.68045  |
|         299 | Wood Pail                             | False      |  7.64919  |
|         249 | Mister Mouse                          | False      |  7.63132  |
|         288 | Planter                               | False      |  7.60164  |
|         206 | -                                     | -          |  7.57868  |
|         219 | Cozy Blanket (Red)                    | False      |  7.57564  |
|         256 | Busy Bee                              | False      |  7.56591  |
|         209 | Tent (Modern Red)                     | False      |  7.51137  |
|         242 | Shell Tunnel (Blue)                   | False      |  7.45026  |
|         275 | Scratching Post                       | False      |  7.41747  |
|         291 | Bucket (Yellow)                       | False      |  7.32224  |
|         289 | Bucket (Blue)                         | False      |  7.321    |
|         119 | Treasure-box                          | False      |  7.29892  |
|         208 | Tent (Nature)                         | False      |  7.26148  |
|         258 | Twisty Rail                           | True       |  7.19553  |
|         165 | Aluminium Bowl                        | False      |  7.16929  |
|         112 | Cake Box                              | False      |  7.12711  |
|         120 | Luxury Treasure-box                   | False      |  7.08409  |
|         290 | Bucket (Red)                          | False      |  7.06787  |
|         166 | Aluminium Pot                         | False      |  6.99685  |
|         246 | Wild-thing Teaser                     | False      |  6.98463  |
|         164 | Cool Aluminum Pad                     | False      |  6.97964  |
|         204 | Luxurious Hammock                     | False      |  6.9294   |
|         273 | Plastic Bag                           | False      |  6.92497  |
|         141 | Cushion (Yellow)                      | False      |  6.91698  |
|         149 | Shroom House (Red)                    | False      |  6.91508  |
|         282 | Clay Pot                              | False      |  6.9119   |
|         144 | Cushion (B&W)                         | False      |  6.88169  |
|         283 | Pickling Pot                          | False      |  6.85953  |
|         203 | Hammock (Woven)                       | False      |  6.85532  |
|         211 | Tent (Pyramid)                        | False      |  6.8538   |
|         284 | Honey Pot                             | False      |  6.78066  |
|         248 | Fluff-thing Teaser                    | False      |  6.35164  |
|         272 | Paper Bag                             | False      |  6.28604  |
|         150 | Shroom House (Blue)                   | False      |  6.23849  |
|         257 | Butterfly Swarm                       | False      |  6.23771  |
|         151 | Shroom House (Green)                  | False      |  6.0199   |
|         143 | Cushion (Choco mint)                  | False      |  5.47903  |
|           2 | Frisky Bitz (Tubbs/Whiteshadow)       | False      |  2.64375  |
|           3 | Ritzy Bitz  (Tubbs/Whiteshadow)       | False      |  2.62669  |
|           6 | Sashimi  (Tubbs/Whiteshadow)          | False      |  2.59405  |
|           5 | Bonito Bitz  (Tubbs/Whiteshadow)      | False      |  0.237497 |
|           4 | Deluxe Tuna Bitz  (Tubbs/Whiteshadow) | False      |  0.194919 |

### Outdoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Fixed
#### Args
Namespace(food_type=2, item_damage_state=2, weather=0, is_indoor=False, output_type='gold_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   Goodie Id | Name                                  | Is Large   |     Value |
|-------------|---------------------------------------|------------|-----------|
|         227 | Cat Metropolis                        | True       | 21.2462   |
|         260 | Round Kotatsu                         | True       | 20.0598   |
|         230 | Tower of Treats                       | True       | 19.9582   |
|         226 | Cat Condo Complex                     | True       | 19.4255   |
|         259 | Kotatsu                               | True       | 19.1952   |
|         231 | Bureau with Pot                       | True       | 19.0685   |
|         123 | Cardboard Choo-choo                   | True       | 18.138    |
|         261 | Sunken Fireplace                      | True       | 17.8122   |
|         229 | Art Deco Cat Tree                     | True       | 17.3395   |
|         235 | Tunnel (3D Piece)                     | True       | 15.6417   |
|         228 | Athletic Cat-Gym                      | True       | 15.3766   |
|         221 | Paper Umbrella                        | True       | 14.7199   |
|         169 | Large Cooling Mat                     | True       | 14.5777   |
|         267 | Space Heater                          | True       | 14.4383   |
|         121 | Cardboard House                       | True       | 14.2422   |
|         122 | Cardboard Cafe                        | True       | 14.1659   |
|         223 | Fairy-tale Parasol                    | True       | 13.75     |
|         264 | Hot Mat (Large)                       | True       | 13.6147   |
|         222 | Beach Umbrella                        | True       | 13.508    |
|         234 | Tunnel (T Piece)                      | True       | 12.2929   |
|         225 | Three-tier Cat Tree                   | True       | 11.755    |
|         265 | Heating Stove                         | True       | 11.687    |
|         207 | Antique Chair                         | True       | 10.7174   |
|         159 | Dice Cube                             | False      | 10.5234   |
|         158 | Tiramisu Cube                         | False      | 10.5175   |
|         224 | Two-tier Cat Tree                     | True       |  9.94268  |
|         233 | Tunnel (U Piece)                      | True       |  9.71598  |
|         156 | Orange Cube                           | False      |  9.68495  |
|         160 | Stump House                           | False      |  9.62901  |
|         157 | Navy-blue Cube                        | False      |  9.529    |
|         239 | Doughnut Tunnel                       | True       |  9.20334  |
|         232 | Tunnel (I Piece)                      | True       |  9.07597  |
|         124 | Dino Deluxe                           | True       |  8.98072  |
|         238 | Cow Tunnel                            | True       |  8.86414  |
|         161 | Bamboo House                          | False      |  8.84849  |
|         200 | Giant Cushion (White)                 | True       |  8.84579  |
|         236 | Carp Tunnel                           | True       |  8.81153  |
|         237 | Fish-stick Tunnel                     | False      |  8.78147  |
|         199 | Giant Cushion                         | False      |  8.77366  |
|         266 | Panel Heater                          | True       |  8.75578  |
|         180 | -                                     | -          |  8.74853  |
|         293 | Snow Sled                             | False      |  8.7219   |
|         197 | Zanzibar Cushion                      | False      |  8.50875  |
|         213 | Shiitake House                        | False      |  8.49321  |
|         212 | Mushroom House                        | False      |  7.80265  |
|         155 | Royal Bed                             | False      |  7.75387  |
|         306 | -                                     | -          |  7.47606  |
|         128 | Silk Crepe Pillow                     | False      |  7.2783   |
|         181 | -                                     | -          |  7.21221  |
|         196 | Egg Bed (Nightview)                   | False      |  7.20278  |
|         286 | Kokeshi Pot (Flow)                    | False      |  7.20005  |
|         285 | Kokeshi Pot (Blossom)                 | False      |  6.96463  |
|         287 | Kokeshi Pot (Spring)                  | False      |  6.9158   |
|         194 | Egg Bed (Black)                       | False      |  6.82286  |
|         182 | -                                     | -          |  6.80172  |
|         179 | Pancake Cushion                       | False      |  6.64774  |
|         195 | Egg Bed (Pink)                        | False      |  6.43383  |
|         281 | Lacquered Bowl                        | False      |  6.38661  |
|         214 | Bamboo Rocket                         | False      |  6.33065  |
|         270 | Kiddy Rucksack (Blue)                 | False      |  6.23846  |
|         187 | Chestnut Cushion                      | False      |  6.19562  |
|         130 | Maple Pillow                          | False      |  6.19054  |
|         107 | Soccer Ball                           | False      |  6.15308  |
|         131 | Snowy Pillow                          | False      |  6.15018  |
|         193 | Egg Bed (White)                       | False      |  6.1109   |
|         129 | Sakura Pillow                         | False      |  6.07789  |
|         175 | Mister Penguin                        | False      |  6.02161  |
|         178 | Burger Cushion                        | False      |  6.02053  |
|         298 | Cowboy Hat                            | False      |  5.94691  |
|         188 | Plum Coccoon                          | False      |  5.90585  |
|         100 | Baseball                              | False      |  5.89757  |
|         111 | Temari Ball                           | False      |  5.8734   |
|         190 | Melon Coccoon                         | False      |  5.82791  |
|         162 | Biscuit Mat                           | False      |  5.7576   |
|         276 | Scratching Log                        | False      |  5.74869  |
|         186 | Basket Case                           | False      |  5.71471  |
|         192 | Strawberry Cocoon                     | False      |  5.643    |
|         254 | Kick Toy (Saury)                      | False      |  5.61821  |
|         191 | Berry Coccoon                         | False      |  5.584    |
|         210 | Tent (Blizzard)                       | False      |  5.58313  |
|         168 | Manta Gel Mat                         | False      |  5.53915  |
|         142 | Cushion (Green)                       | False      |  5.53303  |
|         252 | Kick Toy (Fish)                       | False      |  5.52367  |
|         176 | Sakuramochi Cushion                   | False      |  5.44201  |
|         216 | Pom-pom Sock                          | False      |  5.43966  |
|         198 | Bean Bag                              | False      |  5.42997  |
|         108 | Stress Reliever                       | False      |  5.42318  |
|         104 | Watermelon Ball                       | False      |  5.41787  |
|         263 | Hot Mat (Small)                       | False      |  5.40866  |
|         217 | Colorful Sock                         | False      |  5.3985   |
|         189 | Orange Coccoon                        | False      |  5.32494  |
|         271 | Kiddy Rucksack (Lime)                 | False      |  5.30516  |
|         269 | Kiddy Rucksack (Pink)                 | False      |  5.28675  |
|         305 | Kiddy Rucksack (Pink)                 | False      |  5.28675  |
|         172 | Plum Cushion (Pink)                   | False      |  5.23921  |
|         294 | Goldfish Bowl                         | False      |  5.2391   |
|         278 | Earthenware Pot                       | False      |  5.23011  |
|         154 | Fluffy Bed (Brown)                    | False      |  5.22518  |
|         177 | Kashiwamochi Cushion                  | False      |  5.22292  |
|         171 | Plum Cushion (Red)                    | False      |  5.22289  |
|         139 | Cushion (Pink)                        | False      |  5.21894  |
|         183 | Head Space                            | False      |  5.20087  |
|         255 | -                                     | -          |  5.19812  |
|         115 | Shopping Box (Small)                  | False      |  5.19707  |
|         145 | Cushion (Lemon)                       | False      |  5.19663  |
|         184 | Black Head Space                      | False      |  5.18882  |
|         126 | Pillow (Yellow)                       | False      |  5.18776  |
|         280 | Iron Teapod                           | False      |  5.18592  |
|         101 | Rubber Ball (Red)                     | False      |  5.18113  |
|         140 | Cushion (Brown)                       | False      |  5.15966  |
|         125 | Pillow (Purple)                       | False      |  5.14626  |
|         138 | Cushion (Beige)                       | False      |  5.13908  |
|         268 | Pile of Leaves                        | False      |  5.12375  |
|         109 | Ball of Yarn                          | False      |  5.1222   |
|         174 | Sheep Cushion                         | False      |  5.11801  |
|         146 | Cushion (Orange)                      | False      |  5.11287  |
|         132 | Grass Cushion (Red)                   | False      |  5.08131  |
|         167 | Marble Pad                            | False      |  5.07922  |
|         103 | Rubber Ball (Blue)                    | False      |  5.07316  |
|         185 | White Head Space                      | False      |  5.06174  |
|         251 | Kick Toy (Mouse)                      | False      |  5.06157  |
|         152 | Fluffy Bed (White)                    | False      |  5.04647  |
|         244 | Tail-thing Teaser                     | False      |  5.04606  |
|         114 | Gift Box (Green)                      | False      |  5.02308  |
|         247 | Zebra Grass Gadget                    | False      |  5.01669  |
|         110 | Toy Capsule                           | False      |  5.01486  |
|         295 | Snow Dome                             | False      |  5.01164  |
|         253 | Kick Toy (Bunny)                      | False      |  5.00328  |
|         127 | Pillow (Green)                        | False      |  4.99517  |
|         105 | Beach Ball                            | False      |  4.98718  |
|         218 | Arabesque Blanket                     | False      |  4.98076  |
|         163 | Thick Cooling Pad                     | False      |  4.97941  |
|         137 | Cypress Mat                           | False      |  4.97813  |
|         245 | Wing-thing Teaser                     | False      |  4.97556  |
|         113 | Gift Box (Red)                        | False      |  4.94881  |
|         262 | Hot-Water Bottle                      | False      |  4.94732  |
|         170 | Fluffy Cushion                        | False      |  4.91837  |
|         106 | Ping-Pong Ball                        | False      |  4.9161   |
|         147 | -                                     | -          |  4.91002  |
|         102 | Rubber Ball (Yellow)                  | False      |  4.89932  |
|         117 | Cardboard (Flat)                      | False      |  4.85604  |
|         135 | Grass Cushion (Purple)                | False      |  4.83423  |
|         134 | Grass Cushion (Green)                 | False      |  4.83049  |
|         303 | Cream-puff House                      | False      |  4.81836  |
|         220 | Cozy Blanket (Yellow)                 | False      |  4.81643  |
|         292 | Wooden Pail                           | False      |  4.80698  |
|         304 | Box Tissue                            | False      |  4.79421  |
|         173 | Plum Cushion (White)                  | False      |  4.77902  |
|         277 | Fruit Basket                          | False      |  4.76406  |
|         204 | Luxurious Hammock                     | False      |  4.75995  |
|         153 | Fluffy Bed (Pink)                     | False      |  4.7477   |
|         301 | Cat Macaron (Green)                   | False      |  4.73201  |
|         300 | Cat Macaron (Pink)                    | False      |  4.7219   |
|         118 | Cardboard Truck                       | False      |  4.71761  |
|         165 | Aluminium Bowl                        | False      |  4.70504  |
|         250 | Mister Dragonfly                      | False      |  4.70038  |
|         275 | Scratching Post                       | False      |  4.68864  |
|         215 | Warm Sock                             | False      |  4.6828   |
|         279 | Rice Kettle                           | False      |  4.68225  |
|         302 | Cat Pancake                           | False      |  4.68047  |
|         201 | Hammock (Yellow)                      | False      |  4.66812  |
|         133 | Grass Cushion (Navy)                  | False      |  4.66133  |
|         148 | Lucky Cushion                         | False      |  4.6241   |
|         116 | Shopping Box (Large)                  | False      |  4.62231  |
|         274 | Scratching Board                      | False      |  4.60764  |
|         219 | Cozy Blanket (Red)                    | False      |  4.60576  |
|         240 | Choco Cornet Tunnel                   | False      |  4.6055   |
|         249 | Mister Mouse                          | False      |  4.60183  |
|         296 | Glass Vase                            | False      |  4.57885  |
|         202 | Hammock (Pink)                        | False      |  4.57829  |
|         297 | Jumbo Glass Mug                       | False      |  4.55998  |
|         258 | Twisty Rail                           | True       |  4.54839  |
|         288 | Planter                               | False      |  4.52325  |
|         205 | -                                     | -          |  4.52088  |
|         206 | -                                     | -          |  4.4754   |
|         136 | Pinewood Mat                          | False      |  4.45691  |
|         256 | Busy Bee                              | False      |  4.43905  |
|         299 | Wood Pail                             | False      |  4.41801  |
|         149 | Shroom House (Red)                    | False      |  4.40047  |
|         209 | Tent (Modern Red)                     | False      |  4.39816  |
|         243 | Shell Tunnel (White)                  | False      |  4.37862  |
|         241 | Shell Tunnel (Pink)                   | False      |  4.34967  |
|         164 | Cool Aluminum Pad                     | False      |  4.2968   |
|         144 | Cushion (B&W)                         | False      |  4.2847   |
|         141 | Cushion (Yellow)                      | False      |  4.2665   |
|         119 | Treasure-box                          | False      |  4.23734  |
|         208 | Tent (Nature)                         | False      |  4.23497  |
|         246 | Wild-thing Teaser                     | False      |  4.21514  |
|         242 | Shell Tunnel (Blue)                   | False      |  4.21478  |
|         120 | Luxury Treasure-box                   | False      |  4.2137   |
|         166 | Aluminium Pot                         | False      |  4.18313  |
|         284 | Honey Pot                             | False      |  4.17603  |
|         282 | Clay Pot                              | False      |  4.16737  |
|         283 | Pickling Pot                          | False      |  4.15846  |
|         289 | Bucket (Blue)                         | False      |  4.09512  |
|         211 | Tent (Pyramid)                        | False      |  4.05983  |
|         150 | Shroom House (Blue)                   | False      |  4.03416  |
|         291 | Bucket (Yellow)                       | False      |  4.03315  |
|         203 | Hammock (Woven)                       | False      |  4.02946  |
|         273 | Plastic Bag                           | False      |  3.94168  |
|         112 | Cake Box                              | False      |  3.94141  |
|         290 | Bucket (Red)                          | False      |  3.92542  |
|         151 | Shroom House (Green)                  | False      |  3.87257  |
|         248 | Fluff-thing Teaser                    | False      |  3.83605  |
|         257 | Butterfly Swarm                       | False      |  3.81354  |
|         272 | Paper Bag                             | False      |  3.65898  |
|         143 | Cushion (Choco mint)                  | False      |  3.29843  |
|           6 | Sashimi  (Tubbs/Whiteshadow)          | False      |  2.26062  |
|           2 | Frisky Bitz (Tubbs/Whiteshadow)       | False      |  2.25299  |
|           3 | Ritzy Bitz  (Tubbs/Whiteshadow)       | False      |  2.18471  |
|           5 | Bonito Bitz  (Tubbs/Whiteshadow)      | False      |  0.134993 |
|           4 | Deluxe Tuna Bitz  (Tubbs/Whiteshadow) | False      |  0.110792 |

### Indoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Fixed
#### Args
Namespace(food_type=2, item_damage_state=2, weather=0, is_indoor=True, output_type='gold_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   Goodie Id | Name                                  | Is Large   |     Value |
|-------------|---------------------------------------|------------|-----------|
|         227 | Cat Metropolis                        | True       | 38.3343   |
|         226 | Cat Condo Complex                     | True       | 34.5644   |
|         230 | Tower of Treats                       | True       | 34.4727   |
|         231 | Bureau with Pot                       | True       | 33.9112   |
|         260 | Round Kotatsu                         | True       | 33.4861   |
|         259 | Kotatsu                               | True       | 32.2422   |
|         123 | Cardboard Choo-choo                   | True       | 30.8195   |
|         229 | Art Deco Cat Tree                     | True       | 29.3753   |
|         261 | Sunken Fireplace                      | True       | 29.301    |
|         235 | Tunnel (3D Piece)                     | True       | 27.9106   |
|         228 | Athletic Cat-Gym                      | True       | 27.269    |
|         169 | Large Cooling Mat                     | True       | 24.4817   |
|         221 | Paper Umbrella                        | True       | 24.4356   |
|         267 | Space Heater                          | True       | 24.3245   |
|         264 | Hot Mat (Large)                       | True       | 23.5423   |
|         122 | Cardboard Cafe                        | True       | 23.4659   |
|         121 | Cardboard House                       | True       | 23.2805   |
|         223 | Fairy-tale Parasol                    | True       | 22.8871   |
|         222 | Beach Umbrella                        | True       | 22.8316   |
|         234 | Tunnel (T Piece)                      | True       | 21.8633   |
|         225 | Three-tier Cat Tree                   | True       | 20.746    |
|         265 | Heating Stove                         | True       | 20.1479   |
|         158 | Tiramisu Cube                         | False      | 17.2041   |
|         207 | Antique Chair                         | True       | 17.0599   |
|         159 | Dice Cube                             | False      | 16.8855   |
|         224 | Two-tier Cat Tree                     | True       | 16.3881   |
|         156 | Orange Cube                           | False      | 16.2303   |
|         160 | Stump House                           | False      | 16.0234   |
|         233 | Tunnel (U Piece)                      | True       | 16.0036   |
|         157 | Navy-blue Cube                        | False      | 15.9962   |
|         238 | Cow Tunnel                            | True       | 15.4536   |
|         236 | Carp Tunnel                           | True       | 15.408    |
|         239 | Doughnut Tunnel                       | True       | 15.4044   |
|         161 | Bamboo House                          | False      | 15.3535   |
|         232 | Tunnel (I Piece)                      | True       | 15.337    |
|         213 | Shiitake House                        | False      | 15.1921   |
|         266 | Panel Heater                          | True       | 15.1828   |
|         200 | Giant Cushion (White)                 | True       | 15.1504   |
|         293 | Snow Sled                             | False      | 15.1165   |
|         237 | Fish-stick Tunnel                     | False      | 15.0669   |
|         124 | Dino Deluxe                           | True       | 15.0322   |
|         199 | Giant Cushion                         | False      | 14.9323   |
|         212 | Mushroom House                        | False      | 13.9197   |
|         180 | -                                     | -          | 12.7585   |
|         197 | Zanzibar Cushion                      | False      | 11.4939   |
|         181 | -                                     | -          | 11.2501   |
|         306 | -                                     | -          | 10.7409   |
|         182 | -                                     | -          | 10.7357   |
|         179 | Pancake Cushion                       | False      | 10.6185   |
|         155 | Royal Bed                             | False      | 10.5526   |
|         196 | Egg Bed (Nightview)                   | False      | 10.4505   |
|         194 | Egg Bed (Black)                       | False      | 10.3145   |
|         285 | Kokeshi Pot (Blossom)                 | False      | 10.2859   |
|         128 | Silk Crepe Pillow                     | False      | 10.2809   |
|         287 | Kokeshi Pot (Spring)                  | False      | 10.2758   |
|         286 | Kokeshi Pot (Flow)                    | False      | 10.2459   |
|         178 | Burger Cushion                        | False      |  9.98036  |
|         195 | Egg Bed (Pink)                        | False      |  9.86544  |
|         298 | Cowboy Hat                            | False      |  9.81533  |
|         281 | Lacquered Bowl                        | False      |  9.76921  |
|         130 | Maple Pillow                          | False      |  9.70301  |
|         107 | Soccer Ball                           | False      |  9.61405  |
|         129 | Sakura Pillow                         | False      |  9.53532  |
|         270 | Kiddy Rucksack (Blue)                 | False      |  9.52329  |
|         187 | Chestnut Cushion                      | False      |  9.44452  |
|         214 | Bamboo Rocket                         | False      |  9.42932  |
|         131 | Snowy Pillow                          | False      |  9.29752  |
|         100 | Baseball                              | False      |  9.26226  |
|         193 | Egg Bed (White)                       | False      |  9.25926  |
|         175 | Mister Penguin                        | False      |  9.23762  |
|         186 | Basket Case                           | False      |  9.184    |
|         162 | Biscuit Mat                           | False      |  9.11552  |
|         192 | Strawberry Cocoon                     | False      |  8.92864  |
|         188 | Plum Coccoon                          | False      |  8.89078  |
|         276 | Scratching Log                        | False      |  8.82839  |
|         168 | Manta Gel Mat                         | False      |  8.82787  |
|         108 | Stress Reliever                       | False      |  8.8249   |
|         269 | Kiddy Rucksack (Pink)                 | False      |  8.82351  |
|         305 | Kiddy Rucksack (Pink)                 | False      |  8.82351  |
|         191 | Berry Coccoon                         | False      |  8.82083  |
|         254 | Kick Toy (Saury)                      | False      |  8.80999  |
|         104 | Watermelon Ball                       | False      |  8.80791  |
|         111 | Temari Ball                           | False      |  8.76333  |
|         101 | Rubber Ball (Red)                     | False      |  8.75426  |
|         252 | Kick Toy (Fish)                       | False      |  8.74899  |
|         271 | Kiddy Rucksack (Lime)                 | False      |  8.69906  |
|         216 | Pom-pom Sock                          | False      |  8.68863  |
|         176 | Sakuramochi Cushion                   | False      |  8.67696  |
|         171 | Plum Cushion (Red)                    | False      |  8.66679  |
|         217 | Colorful Sock                         | False      |  8.59851  |
|         263 | Hot Mat (Small)                       | False      |  8.56781  |
|         138 | Cushion (Beige)                       | False      |  8.56301  |
|         251 | Kick Toy (Mouse)                      | False      |  8.55675  |
|         189 | Orange Coccoon                        | False      |  8.53231  |
|         268 | Pile of Leaves                        | False      |  8.52497  |
|         244 | Tail-thing Teaser                     | False      |  8.51809  |
|         137 | Cypress Mat                           | False      |  8.51618  |
|         115 | Shopping Box (Small)                  | False      |  8.51477  |
|         255 | -                                     | -          |  8.49927  |
|         294 | Goldfish Bowl                         | False      |  8.48843  |
|         154 | Fluffy Bed (Brown)                    | False      |  8.48494  |
|         105 | Beach Ball                            | False      |  8.47811  |
|         198 | Bean Bag                              | False      |  8.47475  |
|         126 | Pillow (Yellow)                       | False      |  8.47066  |
|         125 | Pillow (Purple)                       | False      |  8.46186  |
|         172 | Plum Cushion (Pink)                   | False      |  8.45617  |
|         190 | Melon Coccoon                         | False      |  8.43345  |
|         247 | Zebra Grass Gadget                    | False      |  8.41879  |
|         103 | Rubber Ball (Blue)                    | False      |  8.40817  |
|         177 | Kashiwamochi Cushion                  | False      |  8.40654  |
|         278 | Earthenware Pot                       | False      |  8.39338  |
|         142 | Cushion (Green)                       | False      |  8.39259  |
|         109 | Ball of Yarn                          | False      |  8.38737  |
|         218 | Arabesque Blanket                     | False      |  8.34949  |
|         210 | Tent (Blizzard)                       | False      |  8.34832  |
|         132 | Grass Cushion (Red)                   | False      |  8.31358  |
|         174 | Sheep Cushion                         | False      |  8.30363  |
|         139 | Cushion (Pink)                        | False      |  8.30163  |
|         140 | Cushion (Brown)                       | False      |  8.30106  |
|         245 | Wing-thing Teaser                     | False      |  8.28068  |
|         253 | Kick Toy (Bunny)                      | False      |  8.26871  |
|         127 | Pillow (Green)                        | False      |  8.26131  |
|         102 | Rubber Ball (Yellow)                  | False      |  8.2578   |
|         114 | Gift Box (Green)                      | False      |  8.25401  |
|         304 | Box Tissue                            | False      |  8.22476  |
|         295 | Snow Dome                             | False      |  8.22166  |
|         184 | Black Head Space                      | False      |  8.20648  |
|         135 | Grass Cushion (Purple)                | False      |  8.20319  |
|         280 | Iron Teapod                           | False      |  8.20233  |
|         145 | Cushion (Lemon)                       | False      |  8.19941  |
|         147 | -                                     | -          |  8.17587  |
|         146 | Cushion (Orange)                      | False      |  8.16891  |
|         170 | Fluffy Cushion                        | False      |  8.16484  |
|         152 | Fluffy Bed (White)                    | False      |  8.14884  |
|         262 | Hot-Water Bottle                      | False      |  8.13781  |
|         113 | Gift Box (Red)                        | False      |  8.13022  |
|         134 | Grass Cushion (Green)                 | False      |  8.09198  |
|         110 | Toy Capsule                           | False      |  8.08642  |
|         292 | Wooden Pail                           | False      |  8.0756   |
|         163 | Thick Cooling Pad                     | False      |  8.05425  |
|         250 | Mister Dragonfly                      | False      |  8.04364  |
|         300 | Cat Macaron (Pink)                    | False      |  8.01777  |
|         301 | Cat Macaron (Green)                   | False      |  7.99879  |
|         220 | Cozy Blanket (Yellow)                 | False      |  7.99757  |
|         173 | Plum Cushion (White)                  | False      |  7.98228  |
|         183 | Head Space                            | False      |  7.9812   |
|         303 | Cream-puff House                      | False      |  7.97418  |
|         185 | White Head Space                      | False      |  7.97153  |
|         297 | Jumbo Glass Mug                       | False      |  7.96212  |
|         118 | Cardboard Truck                       | False      |  7.95661  |
|         240 | Choco Cornet Tunnel                   | False      |  7.93661  |
|         153 | Fluffy Bed (Pink)                     | False      |  7.92405  |
|         117 | Cardboard (Flat)                      | False      |  7.9156   |
|         167 | Marble Pad                            | False      |  7.89019  |
|         215 | Warm Sock                             | False      |  7.88195  |
|         201 | Hammock (Yellow)                      | False      |  7.876    |
|         116 | Shopping Box (Large)                  | False      |  7.86637  |
|         204 | Luxurious Hammock                     | False      |  7.84823  |
|         106 | Ping-Pong Ball                        | False      |  7.83646  |
|         202 | Hammock (Pink)                        | False      |  7.83593  |
|         136 | Pinewood Mat                          | False      |  7.82846  |
|         133 | Grass Cushion (Navy)                  | False      |  7.82418  |
|         302 | Cat Pancake                           | False      |  7.80006  |
|         277 | Fruit Basket                          | False      |  7.77488  |
|         243 | Shell Tunnel (White)                  | False      |  7.75945  |
|         148 | Lucky Cushion                         | False      |  7.74215  |
|         241 | Shell Tunnel (Pink)                   | False      |  7.70306  |
|         296 | Glass Vase                            | False      |  7.69811  |
|         205 | -                                     | -          |  7.68981  |
|         274 | Scratching Board                      | False      |  7.68507  |
|         279 | Rice Kettle                           | False      |  7.68045  |
|         299 | Wood Pail                             | False      |  7.64919  |
|         249 | Mister Mouse                          | False      |  7.63132  |
|         288 | Planter                               | False      |  7.60164  |
|         206 | -                                     | -          |  7.57868  |
|         219 | Cozy Blanket (Red)                    | False      |  7.57564  |
|         256 | Busy Bee                              | False      |  7.56591  |
|         209 | Tent (Modern Red)                     | False      |  7.51137  |
|         242 | Shell Tunnel (Blue)                   | False      |  7.45026  |
|         275 | Scratching Post                       | False      |  7.41747  |
|         291 | Bucket (Yellow)                       | False      |  7.32224  |
|         289 | Bucket (Blue)                         | False      |  7.321    |
|         119 | Treasure-box                          | False      |  7.29892  |
|         208 | Tent (Nature)                         | False      |  7.26148  |
|         258 | Twisty Rail                           | True       |  7.19553  |
|         165 | Aluminium Bowl                        | False      |  7.16929  |
|         112 | Cake Box                              | False      |  7.12711  |
|         120 | Luxury Treasure-box                   | False      |  7.08409  |
|         290 | Bucket (Red)                          | False      |  7.06787  |
|         166 | Aluminium Pot                         | False      |  6.99685  |
|         246 | Wild-thing Teaser                     | False      |  6.98463  |
|         164 | Cool Aluminum Pad                     | False      |  6.97964  |
|         273 | Plastic Bag                           | False      |  6.92497  |
|         141 | Cushion (Yellow)                      | False      |  6.91698  |
|         149 | Shroom House (Red)                    | False      |  6.91508  |
|         282 | Clay Pot                              | False      |  6.9119   |
|         144 | Cushion (B&W)                         | False      |  6.88169  |
|         283 | Pickling Pot                          | False      |  6.85953  |
|         203 | Hammock (Woven)                       | False      |  6.85532  |
|         284 | Honey Pot                             | False      |  6.78066  |
|         211 | Tent (Pyramid)                        | False      |  6.77233  |
|         248 | Fluff-thing Teaser                    | False      |  6.35164  |
|         272 | Paper Bag                             | False      |  6.28604  |
|         150 | Shroom House (Blue)                   | False      |  6.23849  |
|         257 | Butterfly Swarm                       | False      |  6.23771  |
|         151 | Shroom House (Green)                  | False      |  6.0199   |
|         143 | Cushion (Choco mint)                  | False      |  5.47903  |
|           2 | Frisky Bitz (Tubbs/Whiteshadow)       | False      |  2.64375  |
|           3 | Ritzy Bitz  (Tubbs/Whiteshadow)       | False      |  2.62669  |
|           6 | Sashimi  (Tubbs/Whiteshadow)          | False      |  2.59405  |
|           5 | Bonito Bitz  (Tubbs/Whiteshadow)      | False      |  0.237497 |
|           4 | Deluxe Tuna Bitz  (Tubbs/Whiteshadow) | False      |  0.194919 |

### Doesn't Matter Indoor / Outdoor, Peach Occur Chance, Frisky Bitz, All Items Intact (Also Doesn't Really Matter)
#### Args
Namespace(food_type=2, item_damage_state=0, weather=0, is_indoor=False, output_type='cat_probability', total_duration_minutes=1440, cat_id=24, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   Goodie Id | Name                   | Is Large   |       Value |
|-------------|------------------------|------------|-------------|
|         158 | Tiramisu Cube          | False      | 0.00316131  |
|         221 | Paper Umbrella         | True       | 0.00307804  |
|         182 | -                      | -          | 0.00284305  |
|         222 | Beach Umbrella         | True       | 0.00277958  |
|         223 | Fairy-tale Parasol     | True       | 0.00244007  |
|         301 | Cat Macaron (Green)    | False      | 0.00218188  |
|         181 | -                      | -          | 0.0021742   |
|         179 | Pancake Cushion        | False      | 0.00211988  |
|         122 | Cardboard Cafe         | True       | 0.0020896   |
|         300 | Cat Macaron (Pink)     | False      | 0.00205637  |
|         231 | Bureau with Pot        | True       | 0.00194748  |
|         228 | Athletic Cat-Gym       | True       | 0.00168874  |
|         265 | Heating Stove          | True       | 0.00164949  |
|         229 | Art Deco Cat Tree      | True       | 0.00163103  |
|         267 | Space Heater           | True       | 0.00152319  |
|         239 | Doughnut Tunnel        | True       | 0.00149281  |
|         180 | -                      | -          | 0.00145366  |
|         258 | Twisty Rail            | True       | 0.00139984  |
|         303 | Cream-puff House       | False      | 0.00133751  |
|         157 | Navy-blue Cube         | False      | 0.00128612  |
|         203 | Hammock (Woven)        | False      | 0.00126211  |
|         227 | Cat Metropolis         | True       | 0.00125812  |
|         156 | Orange Cube            | False      | 0.00124071  |
|         192 | Strawberry Cocoon      | False      | 0.00117643  |
|         169 | Large Cooling Mat      | True       | 0.00114941  |
|         237 | Fish-stick Tunnel      | False      | 0.00113444  |
|         159 | Dice Cube              | False      | 0.00108832  |
|         296 | Glass Vase             | False      | 0.00108339  |
|         213 | Shiitake House         | False      | 0.001042    |
|         212 | Mushroom House         | False      | 0.00101762  |
|         226 | Cat Condo Complex      | True       | 0.00100536  |
|         230 | Tower of Treats        | True       | 0.000966415 |
|         264 | Hot Mat (Large)        | True       | 0.000918961 |
|         176 | Sakuramochi Cushion    | False      | 0.00089144  |
|         160 | Stump House            | False      | 0.000873231 |
|         238 | Cow Tunnel             | True       | 0.000868725 |
|         123 | Cardboard Choo-choo    | True       | 0.000812552 |
|         254 | Kick Toy (Saury)       | False      | 0.000761226 |
|         252 | Kick Toy (Fish)        | False      | 0.000753527 |
|         286 | Kokeshi Pot (Flow)     | False      | 0.000734165 |
|         260 | Round Kotatsu          | True       | 0.00073276  |
|         144 | Cushion (B&W)          | False      | 0.000718065 |
|         261 | Sunken Fireplace       | True       | 0.00071737  |
|         151 | Shroom House (Green)   | False      | 0.000715698 |
|         121 | Cardboard House        | True       | 0.000714268 |
|         293 | Snow Sled              | False      | 0.000714267 |
|         283 | Pickling Pot           | False      | 0.000707727 |
|         150 | Shroom House (Blue)    | False      | 0.000704421 |
|         266 | Panel Heater           | True       | 0.00069524  |
|         235 | Tunnel (3D Piece)      | True       | 0.000694091 |
|         145 | Cushion (Lemon)        | False      | 0.000674237 |
|         165 | Aluminium Bowl         | False      | 0.000673401 |
|         124 | Dino Deluxe            | True       | 0.00065314  |
|         207 | Antique Chair          | True       | 0.000647164 |
|         287 | Kokeshi Pot (Spring)   | False      | 0.000647144 |
|         285 | Kokeshi Pot (Blossom)  | False      | 0.000618797 |
|         143 | Cushion (Choco mint)   | False      | 0.000606399 |
|         137 | Cypress Mat            | False      | 0.000604518 |
|         234 | Tunnel (T Piece)       | True       | 0.000595218 |
|         166 | Aluminium Pot          | False      | 0.000562213 |
|         191 | Berry Coccoon          | False      | 0.000559976 |
|         225 | Three-tier Cat Tree    | True       | 0.000552804 |
|         280 | Iron Teapod            | False      | 0.000545757 |
|         190 | Melon Coccoon          | False      | 0.000540272 |
|         284 | Honey Pot              | False      | 0.000537178 |
|         146 | Cushion (Orange)       | False      | 0.00053006  |
|         259 | Kotatsu                | True       | 0.000527085 |
|         185 | White Head Space       | False      | 0.00052537  |
|         149 | Shroom House (Red)     | False      | 0.00052302  |
|         161 | Bamboo House           | False      | 0.000518125 |
|         108 | Stress Reliever        | False      | 0.000512613 |
|         136 | Pinewood Mat           | False      | 0.000509828 |
|         170 | Fluffy Cushion         | False      | 0.00049872  |
|         277 | Fruit Basket           | False      | 0.000497447 |
|         199 | Giant Cushion          | False      | 0.000486745 |
|         282 | Clay Pot               | False      | 0.000484552 |
|         224 | Two-tier Cat Tree      | True       | 0.000481083 |
|         248 | Fluff-thing Teaser     | False      | 0.000480283 |
|         242 | Shell Tunnel (Blue)    | False      | 0.000478168 |
|         200 | Giant Cushion (White)  | True       | 0.000468683 |
|         193 | Egg Bed (White)        | False      | 0.000466802 |
|         167 | Marble Pad             | False      | 0.00046543  |
|         297 | Jumbo Glass Mug        | False      | 0.000461277 |
|         162 | Biscuit Mat            | False      | 0.000460327 |
|         209 | Tent (Modern Red)      | False      | 0.000459353 |
|         243 | Shell Tunnel (White)   | False      | 0.000453434 |
|         279 | Rice Kettle            | False      | 0.000452139 |
|         217 | Colorful Sock          | False      | 0.000444512 |
|         208 | Tent (Nature)          | False      | 0.000440222 |
|         106 | Ping-Pong Ball         | False      | 0.000438789 |
|         164 | Cool Aluminum Pad      | False      | 0.000436857 |
|         168 | Manta Gel Mat          | False      | 0.000436807 |
|         291 | Bucket (Yellow)        | False      | 0.000435206 |
|         134 | Grass Cushion (Green)  | False      | 0.00043436  |
|         189 | Orange Coccoon         | False      | 0.000428628 |
|         246 | Wild-thing Teaser      | False      | 0.000426439 |
|         178 | Burger Cushion         | False      | 0.000426346 |
|         104 | Watermelon Ball        | False      | 0.000421964 |
|         290 | Bucket (Red)           | False      | 0.000419936 |
|         236 | Carp Tunnel            | True       | 0.000417666 |
|         172 | Plum Cushion (Pink)    | False      | 0.000417514 |
|         171 | Plum Cushion (Red)     | False      | 0.000414915 |
|         241 | Shell Tunnel (Pink)    | False      | 0.000413178 |
|         251 | Kick Toy (Mouse)       | False      | 0.000411224 |
|         141 | Cushion (Yellow)       | False      | 0.000407005 |
|         289 | Bucket (Blue)          | False      | 0.00040374  |
|         135 | Grass Cushion (Purple) | False      | 0.000398177 |
|         210 | Tent (Blizzard)        | False      | 0.000395051 |
|         188 | Plum Coccoon           | False      | 0.000390665 |
|         253 | Kick Toy (Bunny)       | False      | 0.000386987 |
|         255 | -                      | -          | 0.000386304 |
|         110 | Toy Capsule            | False      | 0.000376592 |
|         103 | Rubber Ball (Blue)     | False      | 0.000374716 |
|         298 | Cowboy Hat             | False      | 0.000374114 |
|         153 | Fluffy Bed (Pink)      | False      | 0.00037275  |
|         177 | Kashiwamochi Cushion   | False      | 0.000369362 |
|         306 | -                      | -          | 0.00036263  |
|         232 | Tunnel (I Piece)       | True       | 0.000360441 |
|         187 | Chestnut Cushion       | False      | 0.000356122 |
|         211 | Tent (Pyramid)         | False      | 0.000355705 |
|         194 | Egg Bed (Black)        | False      | 0.000351933 |
|         152 | Fluffy Bed (White)     | False      | 0.000351072 |
|         102 | Rubber Ball (Yellow)   | False      | 0.000349168 |
|         148 | Lucky Cushion          | False      | 0.00034464  |
|         275 | Scratching Post        | False      | 0.00034296  |
|         142 | Cushion (Green)        | False      | 0.000337658 |
|         196 | Egg Bed (Nightview)    | False      | 0.000336924 |
|         271 | Kiddy Rucksack (Lime)  | False      | 0.0003356   |
|         155 | Royal Bed              | False      | 0.000334375 |
|         292 | Wooden Pail            | False      | 0.000333027 |
|         154 | Fluffy Bed (Brown)     | False      | 0.000332037 |
|         120 | Luxury Treasure-box    | False      | 0.00033078  |
|         131 | Snowy Pillow           | False      | 0.000321925 |
|         270 | Kiddy Rucksack (Blue)  | False      | 0.000321783 |
|         302 | Cat Pancake            | False      | 0.00031996  |
|         109 | Ball of Yarn           | False      | 0.000319569 |
|         173 | Plum Cushion (White)   | False      | 0.000316284 |
|         201 | Hammock (Yellow)       | False      | 0.000316284 |
|         233 | Tunnel (U Piece)       | True       | 0.000315076 |
|         117 | Cardboard (Flat)       | False      | 0.000314439 |
|         220 | Cozy Blanket (Yellow)  | False      | 0.000307468 |
|         281 | Lacquered Bowl         | False      | 0.000300657 |
|         269 | Kiddy Rucksack (Pink)  | False      | 0.000299755 |
|         305 | Kiddy Rucksack (Pink)  | False      | 0.000299755 |
|         257 | Butterfly Swarm        | False      | 0.000299064 |
|         175 | Mister Penguin         | False      | 0.000293584 |
|         139 | Cushion (Pink)         | False      | 0.000292632 |
|         111 | Temari Ball            | False      | 0.000292555 |
|         174 | Sheep Cushion          | False      | 0.00029062  |
|         215 | Warm Sock              | False      | 0.00028361  |
|         184 | Black Head Space       | False      | 0.000275173 |
|         197 | Zanzibar Cushion       | False      | 0.000273913 |
|         112 | Cake Box               | False      | 0.000270339 |
|         105 | Beach Ball             | False      | 0.000270001 |
|         195 | Egg Bed (Pink)         | False      | 0.000265391 |
|         273 | Plastic Bag            | False      | 0.000263368 |
|         133 | Grass Cushion (Navy)   | False      | 0.000260461 |
|         202 | Hammock (Pink)         | False      | 0.000256246 |
|         299 | Wood Pail              | False      | 0.000255402 |
|         114 | Gift Box (Green)       | False      | 0.000253232 |
|         147 | -                      | -          | 0.000252811 |
|         272 | Paper Bag              | False      | 0.000252056 |
|         262 | Hot-Water Bottle       | False      | 0.000249762 |
|         240 | Choco Cornet Tunnel    | False      | 0.000249663 |
|         113 | Gift Box (Red)         | False      | 0.000247034 |
|         198 | Bean Bag               | False      | 0.000246449 |
|         214 | Bamboo Rocket          | False      | 0.000245708 |
|         274 | Scratching Board       | False      | 0.000240157 |
|         132 | Grass Cushion (Red)    | False      | 0.000239009 |
|         119 | Treasure-box           | False      | 0.000233473 |
|         205 | -                      | -          | 0.000230313 |
|         263 | Hot Mat (Small)        | False      | 0.000225325 |
|         288 | Planter                | False      | 0.000224021 |
|         204 | Luxurious Hammock      | False      | 0.000222443 |
|         100 | Baseball               | False      | 0.000222281 |
|         183 | Head Space             | False      | 0.000221072 |
|         206 | -                      | -          | 0.000218645 |
|         107 | Soccer Ball            | False      | 0.000216549 |
|         138 | Cushion (Beige)        | False      | 0.000214235 |
|         163 | Thick Cooling Pad      | False      | 0.000214066 |
|         247 | Zebra Grass Gadget     | False      | 0.000213543 |
|         118 | Cardboard Truck        | False      | 0.000208236 |
|         245 | Wing-thing Teaser      | False      | 0.000207707 |
|         216 | Pom-pom Sock           | False      | 0.000206362 |
|         244 | Tail-thing Teaser      | False      | 0.000205328 |
|         250 | Mister Dragonfly       | False      | 0.000200846 |
|         219 | Cozy Blanket (Red)     | False      | 0.000195172 |
|         140 | Cushion (Brown)        | False      | 0.00019398  |
|         129 | Sakura Pillow          | False      | 0.000190878 |
|         128 | Silk Crepe Pillow      | False      | 0.000189526 |
|         130 | Maple Pillow           | False      | 0.000188843 |
|         256 | Busy Bee               | False      | 0.000185996 |
|         304 | Box Tissue             | False      | 0.000183393 |
|         126 | Pillow (Yellow)        | False      | 0.000181988 |
|         218 | Arabesque Blanket      | False      | 0.000180922 |
|         186 | Basket Case            | False      | 0.000174276 |
|         268 | Pile of Leaves         | False      | 0.000160891 |
|         276 | Scratching Log         | False      | 0.000156788 |
|         295 | Snow Dome              | False      | 0.000154221 |
|         249 | Mister Mouse           | False      | 0.000152543 |
|         101 | Rubber Ball (Red)      | False      | 0.000144408 |
|         125 | Pillow (Purple)        | False      | 0.000128112 |
|         127 | Pillow (Green)         | False      | 0.000123167 |
|         116 | Shopping Box (Large)   | False      | 0.000111962 |
|         294 | Goldfish Bowl          | False      | 0.000110067 |
|         115 | Shopping Box (Small)   | False      | 0.000108077 |
|         278 | Earthenware Pot        | False      | 8.19902e-05 |
