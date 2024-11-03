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

To analyze probability of a specific cat appearing:
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
|   GoodId | Name                      |     Value |
|----------|---------------------------|-----------|
|      260 | -                         | 660.696   |
|      227 | -                         | 630.944   |
|      230 | -                         | 629.607   |
|      259 | -                         | 627.436   |
|      261 | -                         | 597.065   |
|      226 | -                         | 588.515   |
|      123 | -                         | 586.344   |
|      231 | -                         | 578.133   |
|      229 | -                         | 560.773   |
|      221 | -                         | 488.095   |
|      121 | HouseDeluxe               | 480.949   |
|      169 | -                         | 476.61    |
|      235 | -                         | 471.988   |
|      267 | -                         | 470.208   |
|      228 | -                         | 468.036   |
|      223 | -                         | 454.463   |
|      222 | BeachParasol              | 438.127   |
|      264 | -                         | 428.857   |
|      122 | CafeDeluxe                | 422.901   |
|      207 | -                         | 372.934   |
|      234 | TunnelT                   | 372.663   |
|      265 | -                         | 369.601   |
|      159 | -                         | 362.954   |
|      225 | Tower3                    | 360.209   |
|      158 | -                         | 354.883   |
|      197 | -                         | 345.284   |
|      224 | Tower2                    | 332.501   |
|      180 | -                         | 332.438   |
|      233 | TunnelU                   | 325.18    |
|      160 | -                         | 318.357   |
|      156 | -                         | 317.474   |
|      155 | -                         | 312.77    |
|      157 | -                         | 311.709   |
|      239 | -                         | 302.138   |
|      124 | -                         | 294.818   |
|      232 | TunnelI                   | 294.459   |
|      306 | -                         | 287.972   |
|      128 | -                         | 285.692   |
|      200 | BigCushionWhite           | 282.005   |
|      199 | BigCushion                | 282.003   |
|      286 | -                         | 279.703   |
|      237 | -                         | 279.442   |
|      161 | -                         | 277.456   |
|      238 | -                         | 276.195   |
|      196 | -                         | 274.991   |
|      266 | -                         | 274.784   |
|      293 | -                         | 273.904   |
|      236 | -                         | 273.449   |
|      285 | -                         | 261.556   |
|      287 | -                         | 258.234   |
|      181 | -                         | 256.49    |
|      213 | -                         | 255.393   |
|      194 | -                         | 250.522   |
|      182 | -                         | 238.868   |
|      214 | -                         | 235.834   |
|      212 | -                         | 235.52    |
|      195 | -                         | 232.899   |
|      281 | -                         | 231.761   |
|      179 | -                         | 230.44    |
|      270 | -                         | 226.849   |
|      131 | -                         | 225.823   |
|      187 | -                         | 225.612   |
|      193 | -                         | 223.873   |
|      190 | -                         | 223.035   |
|      130 | -                         | 219.037   |
|      111 | TemariBall                | 218.439   |
|      107 | -                         | 218.438   |
|      175 | -                         | 217.875   |
|      188 | PlumCocoon                | 217.748   |
|      129 | -                         | 214.839   |
|      100 | Baseball                  | 208.228   |
|      276 | -                         | 207.62    |
|      210 | -                         | 207.209   |
|      142 | -                         | 202.489   |
|      162 | -                         | 201.532   |
|      178 | BurgerCushion             | 199.97    |
|      254 | -                         | 198.689   |
|      298 | WesternHats               | 198.511   |
|      192 | -                         | 197.652   |
|      186 | -                         | 196.758   |
|      191 | -                         | 195.932   |
|      252 | -                         | 193.252   |
|      198 | BeadedCushion             | 192.994   |
|      168 | -                         | 192.489   |
|      263 | -                         | 189.205   |
|      176 | -                         | 189.02    |
|      216 | -                         | 188.568   |
|      183 | -                         | 188.115   |
|      217 | -                         | 187.727   |
|      104 | -                         | 184.114   |
|      108 | StressReliever            | 184.095   |
|      189 | -                         | 183.945   |
|      145 | -                         | 182.568   |
|      184 | -                         | 181.828   |
|      139 | -                         | 181.743   |
|      280 | -                         | 181.716   |
|      167 | -                         | 181.419   |
|      278 | EarthenwarePot            | 180.357   |
|      177 | -                         | 179.516   |
|      172 | -                         | 179.514   |
|      294 | GoldfishBowl              | 178.732   |
|      271 | -                         | 178.499   |
|      185 | -                         | 178.19    |
|      154 | -                         | 177.799   |
|      140 | -                         | 177.429   |
|      146 | -                         | 177.186   |
|      255 | -                         | 175.481   |
|      126 | -                         | 175.411   |
|      115 | ShoppingBoxSmall          | 175.032   |
|      174 | -                         | 174.327   |
|      269 | -                         | 174.169   |
|      305 | -                         | 174.169   |
|      171 | UmeCushionRed             | 173.268   |
|      152 | FluffyBedWhite            | 172.82    |
|      109 | BallOfYarn                | 172.624   |
|      125 | -                         | 172.592   |
|      110 | -                         | 172.011   |
|      132 | -                         | 171.41    |
|      165 | -                         | 171.405   |
|      106 | PingPongBall              | 170.8     |
|      163 | -                         | 170.195   |
|      138 | -                         | 169.641   |
|      268 | -                         | 169.435   |
|      114 | -                         | 168.589   |
|      103 | -                         | 168.544   |
|      295 | -                         | 168.53    |
|      101 | RubberBallRed             | 168.12    |
|      253 | -                         | 166.79    |
|      127 | -                         | 166.376   |
|      113 | -                         | 166.138   |
|      262 | -                         | 165.847   |
|      117 | -                         | 164.517   |
|      245 | -                         | 164.479   |
|      275 | VerticalRopeNailClogger   | 164.252   |
|      247 | -                         | 164.168   |
|      251 | GripesMmouse              | 164.132   |
|      244 | Catnip                    | 163.928   |
|      218 | -                         | 163.208   |
|      170 | FluffyCushion             | 163.084   |
|      147 | -                         | 162.211   |
|      277 | FruitBasket               | 161.179   |
|      105 | -                         | 160.589   |
|      303 | -                         | 160.36    |
|      220 | -                         | 159.658   |
|      102 | -                         | 159.463   |
|      258 | RailHereAndThere          | 159.34    |
|      137 | -                         | 159.015   |
|      134 | -                         | 158.418   |
|      211 | -                         | 158.138   |
|      279 | -                         | 157.474   |
|      173 | -                         | 157.294   |
|      292 | -                         | 157.095   |
|      153 | -                         | 156.405   |
|      135 | -                         | 156.022   |
|      149 | -                         | 155.273   |
|      302 | -                         | 154.473   |
|      219 | -                         | 154.405   |
|      301 | -                         | 153.466   |
|      118 | CardboardTruck            | 153.427   |
|      249 | -                         | 152.782   |
|      215 | -                         | 152.677   |
|      304 | Tissue                    | 152.583   |
|      133 | -                         | 152.497   |
|      300 | CatMacaroonPink           | 152.272   |
|      274 | HorizontalRopeNailClogger | 151.916   |
|      201 | -                         | 151.749   |
|      148 | -                         | 151.748   |
|      250 | -                         | 150.08    |
|      296 | GlassVase                 | 149.501   |
|      116 | ShoppingBoxMiddle         | 148.636   |
|      288 | -                         | 147.758   |
|      144 | -                         | 147.623   |
|      164 | -                         | 146.155   |
|      202 | -                         | 146.153   |
|      240 | -                         | 145.723   |
|      205 | -                         | 145.468   |
|      141 | -                         | 145.447   |
|      206 | -                         | 144.816   |
|      150 | -                         | 144.77    |
|      256 | AutomaticBunbunmaru       | 142.469   |
|      284 | -                         | 142.115   |
|      297 | OversizedPatternedGlass   | 141.788   |
|      209 | -                         | 140.793   |
|      204 | -                         | 140.49    |
|      246 | -                         | 140.074   |
|      283 | -                         | 138.939   |
|      299 | -                         | 138.934   |
|      282 | Tsubo                     | 138.332   |
|      151 | -                         | 138.22    |
|      120 | -                         | 137.582   |
|      136 | -                         | 137.472   |
|      166 | -                         | 137.444   |
|      208 | -                         | 134.877   |
|      119 | -                         | 134.151   |
|      243 | -                         | 133.412   |
|      241 | -                         | 132.652   |
|      203 | -                         | 129.622   |
|      242 | -                         | 128.873   |
|      257 | -                         | 128.683   |
|      248 | -                         | 127.592   |
|      289 | BucketBlue                | 123.24    |
|      273 | VinylBag                  | 121.544   |
|      291 | -                         | 118.686   |
|      290 | -                         | 116.927   |
|      112 | CakeBox                   | 116.672   |
|      272 | PaperBag                  | 116.241   |
|      143 | -                         | 109.288   |
|        6 | Sashimi                   | 102.768   |
|        2 | GoodKarikari              | 101.018   |
|        3 | NekoCan                   |  96.443   |
|        5 | MaguroCan                 |   4.15461 |
|        4 | KatsuoCan                 |   3.40977 |

### Outdoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Intact
#### Args
Namespace(food_type=2, item_damage_state=0, weather=0, is_indoor=False, output_type='gold_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   GoodId | Name                      |     Value |
|----------|---------------------------|-----------|
|      227 | -                         | 21.2458   |
|      260 | -                         | 20.0598   |
|      230 | -                         | 19.9582   |
|      226 | -                         | 19.4255   |
|      259 | -                         | 19.1952   |
|      231 | -                         | 19.0685   |
|      123 | -                         | 18.1548   |
|      261 | -                         | 17.8122   |
|      229 | -                         | 17.3395   |
|      235 | -                         | 15.6417   |
|      228 | -                         | 15.3766   |
|      221 | -                         | 14.7199   |
|      169 | -                         | 14.5777   |
|      267 | -                         | 14.4383   |
|      121 | HouseDeluxe               | 14.2422   |
|      223 | -                         | 13.75     |
|      264 | -                         | 13.6147   |
|      222 | BeachParasol              | 13.508    |
|      122 | CafeDeluxe                | 12.8399   |
|      234 | TunnelT                   | 12.2929   |
|      225 | Tower3                    | 11.755    |
|      265 | -                         | 11.687    |
|      207 | -                         | 10.7174   |
|      159 | -                         | 10.5234   |
|      158 | -                         | 10.5175   |
|      224 | Tower2                    |  9.94268  |
|      233 | TunnelU                   |  9.71598  |
|      156 | -                         |  9.68495  |
|      160 | -                         |  9.62901  |
|      157 | -                         |  9.529    |
|      239 | -                         |  9.20334  |
|      232 | TunnelI                   |  9.07597  |
|      124 | -                         |  8.98072  |
|      238 | -                         |  8.86414  |
|      161 | -                         |  8.84849  |
|      200 | BigCushionWhite           |  8.83962  |
|      236 | -                         |  8.81153  |
|      237 | -                         |  8.78147  |
|      199 | BigCushion                |  8.76837  |
|      266 | -                         |  8.75578  |
|      180 | -                         |  8.74853  |
|      293 | -                         |  8.7219   |
|      197 | -                         |  8.50875  |
|      213 | -                         |  8.49321  |
|      212 | -                         |  7.80265  |
|      155 | -                         |  7.75387  |
|      306 | -                         |  7.47606  |
|      128 | -                         |  7.29102  |
|      181 | -                         |  7.21221  |
|      196 | -                         |  7.20278  |
|      286 | -                         |  7.20005  |
|      285 | -                         |  6.96463  |
|      287 | -                         |  6.9158   |
|      194 | -                         |  6.82286  |
|      182 | -                         |  6.80172  |
|      179 | -                         |  6.64774  |
|      195 | -                         |  6.43383  |
|      281 | -                         |  6.38661  |
|      214 | -                         |  6.33065  |
|      270 | -                         |  6.23846  |
|      187 | -                         |  6.19562  |
|      130 | -                         |  6.19054  |
|      107 | -                         |  6.15308  |
|      131 | -                         |  6.15018  |
|      193 | -                         |  6.1109   |
|      129 | -                         |  6.07789  |
|      175 | -                         |  6.02161  |
|      178 | BurgerCushion             |  6.02053  |
|      298 | WesternHats               |  5.94566  |
|      188 | PlumCocoon                |  5.90585  |
|      100 | Baseball                  |  5.89757  |
|      111 | TemariBall                |  5.8734   |
|      190 | -                         |  5.82791  |
|      162 | -                         |  5.7576   |
|      276 | -                         |  5.74482  |
|      186 | -                         |  5.71471  |
|      192 | -                         |  5.643    |
|      254 | -                         |  5.61821  |
|      191 | -                         |  5.584    |
|      210 | -                         |  5.58313  |
|      168 | -                         |  5.53915  |
|      142 | -                         |  5.53303  |
|      252 | -                         |  5.52367  |
|      176 | -                         |  5.44201  |
|      216 | -                         |  5.43966  |
|      198 | BeadedCushion             |  5.42997  |
|      108 | StressReliever            |  5.42318  |
|      104 | -                         |  5.41787  |
|      263 | -                         |  5.40866  |
|      217 | -                         |  5.3985   |
|      189 | -                         |  5.32494  |
|      271 | -                         |  5.30516  |
|      269 | -                         |  5.28675  |
|      305 | -                         |  5.28675  |
|      172 | -                         |  5.23921  |
|      294 | GoldfishBowl              |  5.2391   |
|      278 | EarthenwarePot            |  5.23011  |
|      154 | -                         |  5.22518  |
|      177 | -                         |  5.22292  |
|      171 | UmeCushionRed             |  5.22289  |
|      139 | -                         |  5.21894  |
|      183 | -                         |  5.20087  |
|      255 | -                         |  5.19812  |
|      115 | ShoppingBoxSmall          |  5.19707  |
|      145 | -                         |  5.19663  |
|      184 | -                         |  5.18882  |
|      126 | -                         |  5.18776  |
|      280 | -                         |  5.18592  |
|      101 | RubberBallRed             |  5.18113  |
|      140 | -                         |  5.15966  |
|      125 | -                         |  5.14626  |
|      138 | -                         |  5.13908  |
|      268 | -                         |  5.12375  |
|      109 | BallOfYarn                |  5.1222   |
|      174 | -                         |  5.11801  |
|      146 | -                         |  5.11287  |
|      132 | -                         |  5.08131  |
|      167 | -                         |  5.07922  |
|      103 | -                         |  5.07316  |
|      185 | -                         |  5.06174  |
|      251 | GripesMmouse              |  5.06157  |
|      152 | FluffyBedWhite            |  5.04647  |
|      244 | Catnip                    |  5.04606  |
|      114 | -                         |  5.02308  |
|      247 | -                         |  5.01669  |
|      110 | -                         |  5.01486  |
|      295 | -                         |  5.01164  |
|      253 | -                         |  5.00328  |
|      127 | -                         |  4.99517  |
|      105 | -                         |  4.98718  |
|      218 | -                         |  4.98076  |
|      163 | -                         |  4.97941  |
|      137 | -                         |  4.97813  |
|      245 | -                         |  4.97556  |
|      113 | -                         |  4.94881  |
|      262 | -                         |  4.94732  |
|      170 | FluffyCushion             |  4.91837  |
|      106 | PingPongBall              |  4.9161   |
|      147 | -                         |  4.91002  |
|      102 | -                         |  4.89932  |
|      117 | -                         |  4.85604  |
|      135 | -                         |  4.83423  |
|      134 | -                         |  4.83049  |
|      303 | -                         |  4.81836  |
|      220 | -                         |  4.81643  |
|      292 | -                         |  4.80698  |
|      304 | Tissue                    |  4.79421  |
|      173 | -                         |  4.77902  |
|      277 | FruitBasket               |  4.76406  |
|      153 | -                         |  4.7477   |
|      301 | -                         |  4.73201  |
|      300 | CatMacaroonPink           |  4.7219   |
|      118 | CardboardTruck            |  4.71761  |
|      165 | -                         |  4.70504  |
|      250 | -                         |  4.70038  |
|      275 | VerticalRopeNailClogger   |  4.68864  |
|      215 | -                         |  4.6828   |
|      279 | -                         |  4.68225  |
|      302 | -                         |  4.68047  |
|      201 | -                         |  4.66812  |
|      133 | -                         |  4.66133  |
|      148 | -                         |  4.6241   |
|      116 | ShoppingBoxMiddle         |  4.62231  |
|      274 | HorizontalRopeNailClogger |  4.60764  |
|      219 | -                         |  4.60576  |
|      240 | -                         |  4.6055   |
|      249 | -                         |  4.60183  |
|      296 | GlassVase                 |  4.57885  |
|      202 | -                         |  4.57829  |
|      297 | OversizedPatternedGlass   |  4.55998  |
|      258 | RailHereAndThere          |  4.54839  |
|      288 | -                         |  4.52325  |
|      205 | -                         |  4.52088  |
|      206 | -                         |  4.4754   |
|      136 | -                         |  4.45691  |
|      256 | AutomaticBunbunmaru       |  4.43905  |
|      211 | -                         |  4.41959  |
|      299 | -                         |  4.41801  |
|      149 | -                         |  4.40047  |
|      209 | -                         |  4.39816  |
|      243 | -                         |  4.37862  |
|      241 | -                         |  4.34967  |
|      164 | -                         |  4.2968   |
|      144 | -                         |  4.2847   |
|      141 | -                         |  4.2665   |
|      119 | -                         |  4.23734  |
|      208 | -                         |  4.23497  |
|      246 | -                         |  4.21514  |
|      242 | -                         |  4.21478  |
|      120 | -                         |  4.2137   |
|      204 | -                         |  4.20268  |
|      166 | -                         |  4.18313  |
|      284 | -                         |  4.17603  |
|      282 | Tsubo                     |  4.16737  |
|      283 | -                         |  4.15846  |
|      289 | BucketBlue                |  4.09512  |
|      150 | -                         |  4.03416  |
|      291 | -                         |  4.03315  |
|      203 | -                         |  4.02946  |
|      273 | VinylBag                  |  3.94168  |
|      112 | CakeBox                   |  3.94141  |
|      290 | -                         |  3.92542  |
|      151 | -                         |  3.87257  |
|      248 | -                         |  3.83605  |
|      257 | -                         |  3.81354  |
|      272 | PaperBag                  |  3.65898  |
|      143 | -                         |  3.29843  |
|        6 | Sashimi                   |  2.26062  |
|        2 | GoodKarikari              |  2.25299  |
|        3 | NekoCan                   |  2.18471  |
|        5 | MaguroCan                 |  0.134993 |
|        4 | KatsuoCan                 |  0.110792 |

### Indoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Intact
#### Args
Namespace(food_type=2, item_damage_state=0, weather=0, is_indoor=True, output_type='gold_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   GoodId | Name                      |     Value |
|----------|---------------------------|-----------|
|      227 | -                         | 38.3334   |
|      226 | -                         | 34.5644   |
|      230 | -                         | 34.4727   |
|      231 | -                         | 33.9112   |
|      260 | -                         | 33.4861   |
|      259 | -                         | 32.2422   |
|      123 | -                         | 30.7899   |
|      229 | -                         | 29.3753   |
|      261 | -                         | 29.301    |
|      235 | -                         | 27.9106   |
|      228 | -                         | 27.269    |
|      169 | -                         | 24.4817   |
|      221 | -                         | 24.4356   |
|      267 | -                         | 24.3245   |
|      264 | -                         | 23.5423   |
|      121 | HouseDeluxe               | 23.2805   |
|      223 | -                         | 22.8871   |
|      222 | BeachParasol              | 22.8316   |
|      234 | TunnelT                   | 21.8633   |
|      122 | CafeDeluxe                | 21.4339   |
|      225 | Tower3                    | 20.746    |
|      265 | -                         | 20.1479   |
|      158 | -                         | 17.2041   |
|      207 | -                         | 17.0599   |
|      159 | -                         | 16.8855   |
|      224 | Tower2                    | 16.3881   |
|      156 | -                         | 16.2303   |
|      160 | -                         | 16.0234   |
|      233 | TunnelU                   | 16.0036   |
|      157 | -                         | 15.9962   |
|      238 | -                         | 15.4536   |
|      236 | -                         | 15.408    |
|      239 | -                         | 15.4044   |
|      161 | -                         | 15.3535   |
|      232 | TunnelI                   | 15.337    |
|      213 | -                         | 15.1921   |
|      266 | -                         | 15.1828   |
|      200 | BigCushionWhite           | 15.137    |
|      293 | -                         | 15.1165   |
|      237 | -                         | 15.0669   |
|      124 | -                         | 15.0322   |
|      199 | BigCushion                | 14.9203   |
|      212 | -                         | 13.9197   |
|      180 | -                         | 12.7585   |
|      197 | -                         | 11.4939   |
|      181 | -                         | 11.2501   |
|      306 | -                         | 10.7409   |
|      182 | -                         | 10.7357   |
|      179 | -                         | 10.6185   |
|      155 | -                         | 10.5526   |
|      196 | -                         | 10.4505   |
|      194 | -                         | 10.3145   |
|      285 | -                         | 10.2859   |
|      287 | -                         | 10.2758   |
|      128 | -                         | 10.273    |
|      286 | -                         | 10.2459   |
|      178 | BurgerCushion             |  9.98036  |
|      195 | -                         |  9.86544  |
|      298 | WesternHats               |  9.81343  |
|      281 | -                         |  9.76921  |
|      130 | -                         |  9.70301  |
|      107 | -                         |  9.61405  |
|      129 | -                         |  9.53532  |
|      270 | -                         |  9.52329  |
|      187 | -                         |  9.44452  |
|      214 | -                         |  9.42932  |
|      131 | -                         |  9.29752  |
|      100 | Baseball                  |  9.26226  |
|      193 | -                         |  9.25926  |
|      175 | -                         |  9.23762  |
|      186 | -                         |  9.184    |
|      162 | -                         |  9.11552  |
|      192 | -                         |  8.92864  |
|      188 | PlumCocoon                |  8.89078  |
|      168 | -                         |  8.82787  |
|      108 | StressReliever            |  8.8249   |
|      269 | -                         |  8.82351  |
|      305 | -                         |  8.82351  |
|      276 | -                         |  8.82301  |
|      191 | -                         |  8.82083  |
|      254 | -                         |  8.80999  |
|      104 | -                         |  8.80791  |
|      111 | TemariBall                |  8.76333  |
|      101 | RubberBallRed             |  8.75426  |
|      252 | -                         |  8.74899  |
|      271 | -                         |  8.69906  |
|      216 | -                         |  8.68863  |
|      176 | -                         |  8.67696  |
|      171 | UmeCushionRed             |  8.66679  |
|      217 | -                         |  8.59851  |
|      263 | -                         |  8.56781  |
|      138 | -                         |  8.56301  |
|      251 | GripesMmouse              |  8.55675  |
|      189 | -                         |  8.53231  |
|      268 | -                         |  8.52497  |
|      244 | Catnip                    |  8.51809  |
|      137 | -                         |  8.51618  |
|      115 | ShoppingBoxSmall          |  8.51477  |
|      255 | -                         |  8.49927  |
|      294 | GoldfishBowl              |  8.48843  |
|      154 | -                         |  8.48494  |
|      105 | -                         |  8.47811  |
|      198 | BeadedCushion             |  8.47475  |
|      126 | -                         |  8.47066  |
|      125 | -                         |  8.46186  |
|      172 | -                         |  8.45617  |
|      190 | -                         |  8.43345  |
|      247 | -                         |  8.41879  |
|      103 | -                         |  8.40817  |
|      177 | -                         |  8.40654  |
|      278 | EarthenwarePot            |  8.39338  |
|      142 | -                         |  8.39259  |
|      109 | BallOfYarn                |  8.38737  |
|      218 | -                         |  8.34949  |
|      210 | -                         |  8.34832  |
|      132 | -                         |  8.31358  |
|      174 | -                         |  8.30363  |
|      139 | -                         |  8.30163  |
|      140 | -                         |  8.30106  |
|      245 | -                         |  8.28068  |
|      253 | -                         |  8.26871  |
|      127 | -                         |  8.26131  |
|      102 | -                         |  8.2578   |
|      114 | -                         |  8.25401  |
|      304 | Tissue                    |  8.22476  |
|      295 | -                         |  8.22166  |
|      184 | -                         |  8.20648  |
|      135 | -                         |  8.20319  |
|      280 | -                         |  8.20233  |
|      145 | -                         |  8.19941  |
|      147 | -                         |  8.17587  |
|      146 | -                         |  8.16891  |
|      170 | FluffyCushion             |  8.16484  |
|      152 | FluffyBedWhite            |  8.14884  |
|      262 | -                         |  8.13781  |
|      113 | -                         |  8.13022  |
|      134 | -                         |  8.09198  |
|      110 | -                         |  8.08642  |
|      292 | -                         |  8.0756   |
|      163 | -                         |  8.05425  |
|      250 | -                         |  8.04364  |
|      300 | CatMacaroonPink           |  8.01777  |
|      301 | -                         |  7.99879  |
|      220 | -                         |  7.99757  |
|      173 | -                         |  7.98228  |
|      183 | -                         |  7.9812   |
|      303 | -                         |  7.97418  |
|      185 | -                         |  7.97153  |
|      297 | OversizedPatternedGlass   |  7.96212  |
|      118 | CardboardTruck            |  7.95661  |
|      240 | -                         |  7.93661  |
|      153 | -                         |  7.92405  |
|      117 | -                         |  7.9156   |
|      167 | -                         |  7.89019  |
|      215 | -                         |  7.88195  |
|      201 | -                         |  7.876    |
|      116 | ShoppingBoxMiddle         |  7.86637  |
|      106 | PingPongBall              |  7.83646  |
|      202 | -                         |  7.83593  |
|      136 | -                         |  7.82846  |
|      133 | -                         |  7.82418  |
|      302 | -                         |  7.80006  |
|      277 | FruitBasket               |  7.77488  |
|      243 | -                         |  7.75945  |
|      148 | -                         |  7.74215  |
|      241 | -                         |  7.70306  |
|      296 | GlassVase                 |  7.69811  |
|      205 | -                         |  7.68981  |
|      274 | HorizontalRopeNailClogger |  7.68507  |
|      279 | -                         |  7.68045  |
|      299 | -                         |  7.64919  |
|      249 | -                         |  7.63132  |
|      288 | -                         |  7.60164  |
|      206 | -                         |  7.57868  |
|      219 | -                         |  7.57564  |
|      256 | AutomaticBunbunmaru       |  7.56591  |
|      209 | -                         |  7.51137  |
|      242 | -                         |  7.45026  |
|      275 | VerticalRopeNailClogger   |  7.41747  |
|      291 | -                         |  7.32224  |
|      289 | BucketBlue                |  7.321    |
|      119 | -                         |  7.29892  |
|      208 | -                         |  7.26148  |
|      258 | RailHereAndThere          |  7.19553  |
|      165 | -                         |  7.16929  |
|      112 | CakeBox                   |  7.12711  |
|      120 | -                         |  7.08409  |
|      290 | -                         |  7.06787  |
|      166 | -                         |  6.99685  |
|      246 | -                         |  6.98463  |
|      164 | -                         |  6.97964  |
|      204 | -                         |  6.9294   |
|      273 | VinylBag                  |  6.92497  |
|      141 | -                         |  6.91698  |
|      149 | -                         |  6.91508  |
|      282 | Tsubo                     |  6.9119   |
|      144 | -                         |  6.88169  |
|      283 | -                         |  6.85953  |
|      203 | -                         |  6.85532  |
|      211 | -                         |  6.8538   |
|      284 | -                         |  6.78066  |
|      248 | -                         |  6.35164  |
|      272 | PaperBag                  |  6.28604  |
|      150 | -                         |  6.23849  |
|      257 | -                         |  6.23771  |
|      151 | -                         |  6.0199   |
|      143 | -                         |  5.47903  |
|        2 | GoodKarikari              |  2.64375  |
|        3 | NekoCan                   |  2.62669  |
|        6 | Sashimi                   |  2.59405  |
|        5 | MaguroCan                 |  0.237497 |
|        4 | KatsuoCan                 |  0.194919 |

### Outdoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Fixed
#### Args
Namespace(food_type=2, item_damage_state=2, weather=0, is_indoor=False, output_type='gold_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   GoodId | Name                      |     Value |
|----------|---------------------------|-----------|
|      227 | -                         | 21.2462   |
|      260 | -                         | 20.0598   |
|      230 | -                         | 19.9582   |
|      226 | -                         | 19.4255   |
|      259 | -                         | 19.1952   |
|      231 | -                         | 19.0685   |
|      123 | -                         | 18.138    |
|      261 | -                         | 17.8122   |
|      229 | -                         | 17.3395   |
|      235 | -                         | 15.6417   |
|      228 | -                         | 15.3766   |
|      221 | -                         | 14.7199   |
|      169 | -                         | 14.5777   |
|      267 | -                         | 14.4383   |
|      121 | HouseDeluxe               | 14.2422   |
|      122 | CafeDeluxe                | 14.1659   |
|      223 | -                         | 13.75     |
|      264 | -                         | 13.6147   |
|      222 | BeachParasol              | 13.508    |
|      234 | TunnelT                   | 12.2929   |
|      225 | Tower3                    | 11.755    |
|      265 | -                         | 11.687    |
|      207 | -                         | 10.7174   |
|      159 | -                         | 10.5234   |
|      158 | -                         | 10.5175   |
|      224 | Tower2                    |  9.94268  |
|      233 | TunnelU                   |  9.71598  |
|      156 | -                         |  9.68495  |
|      160 | -                         |  9.62901  |
|      157 | -                         |  9.529    |
|      239 | -                         |  9.20334  |
|      232 | TunnelI                   |  9.07597  |
|      124 | -                         |  8.98072  |
|      238 | -                         |  8.86414  |
|      161 | -                         |  8.84849  |
|      200 | BigCushionWhite           |  8.84579  |
|      236 | -                         |  8.81153  |
|      237 | -                         |  8.78147  |
|      199 | BigCushion                |  8.77366  |
|      266 | -                         |  8.75578  |
|      180 | -                         |  8.74853  |
|      293 | -                         |  8.7219   |
|      197 | -                         |  8.50875  |
|      213 | -                         |  8.49321  |
|      212 | -                         |  7.80265  |
|      155 | -                         |  7.75387  |
|      306 | -                         |  7.47606  |
|      128 | -                         |  7.2783   |
|      181 | -                         |  7.21221  |
|      196 | -                         |  7.20278  |
|      286 | -                         |  7.20005  |
|      285 | -                         |  6.96463  |
|      287 | -                         |  6.9158   |
|      194 | -                         |  6.82286  |
|      182 | -                         |  6.80172  |
|      179 | -                         |  6.64774  |
|      195 | -                         |  6.43383  |
|      281 | -                         |  6.38661  |
|      214 | -                         |  6.33065  |
|      270 | -                         |  6.23846  |
|      187 | -                         |  6.19562  |
|      130 | -                         |  6.19054  |
|      107 | -                         |  6.15308  |
|      131 | -                         |  6.15018  |
|      193 | -                         |  6.1109   |
|      129 | -                         |  6.07789  |
|      175 | -                         |  6.02161  |
|      178 | BurgerCushion             |  6.02053  |
|      298 | WesternHats               |  5.94691  |
|      188 | PlumCocoon                |  5.90585  |
|      100 | Baseball                  |  5.89757  |
|      111 | TemariBall                |  5.8734   |
|      190 | -                         |  5.82791  |
|      162 | -                         |  5.7576   |
|      276 | -                         |  5.74869  |
|      186 | -                         |  5.71471  |
|      192 | -                         |  5.643    |
|      254 | -                         |  5.61821  |
|      191 | -                         |  5.584    |
|      210 | -                         |  5.58313  |
|      168 | -                         |  5.53915  |
|      142 | -                         |  5.53303  |
|      252 | -                         |  5.52367  |
|      176 | -                         |  5.44201  |
|      216 | -                         |  5.43966  |
|      198 | BeadedCushion             |  5.42997  |
|      108 | StressReliever            |  5.42318  |
|      104 | -                         |  5.41787  |
|      263 | -                         |  5.40866  |
|      217 | -                         |  5.3985   |
|      189 | -                         |  5.32494  |
|      271 | -                         |  5.30516  |
|      269 | -                         |  5.28675  |
|      305 | -                         |  5.28675  |
|      172 | -                         |  5.23921  |
|      294 | GoldfishBowl              |  5.2391   |
|      278 | EarthenwarePot            |  5.23011  |
|      154 | -                         |  5.22518  |
|      177 | -                         |  5.22292  |
|      171 | UmeCushionRed             |  5.22289  |
|      139 | -                         |  5.21894  |
|      183 | -                         |  5.20087  |
|      255 | -                         |  5.19812  |
|      115 | ShoppingBoxSmall          |  5.19707  |
|      145 | -                         |  5.19663  |
|      184 | -                         |  5.18882  |
|      126 | -                         |  5.18776  |
|      280 | -                         |  5.18592  |
|      101 | RubberBallRed             |  5.18113  |
|      140 | -                         |  5.15966  |
|      125 | -                         |  5.14626  |
|      138 | -                         |  5.13908  |
|      268 | -                         |  5.12375  |
|      109 | BallOfYarn                |  5.1222   |
|      174 | -                         |  5.11801  |
|      146 | -                         |  5.11287  |
|      132 | -                         |  5.08131  |
|      167 | -                         |  5.07922  |
|      103 | -                         |  5.07316  |
|      185 | -                         |  5.06174  |
|      251 | GripesMmouse              |  5.06157  |
|      152 | FluffyBedWhite            |  5.04647  |
|      244 | Catnip                    |  5.04606  |
|      114 | -                         |  5.02308  |
|      247 | -                         |  5.01669  |
|      110 | -                         |  5.01486  |
|      295 | -                         |  5.01164  |
|      253 | -                         |  5.00328  |
|      127 | -                         |  4.99517  |
|      105 | -                         |  4.98718  |
|      218 | -                         |  4.98076  |
|      163 | -                         |  4.97941  |
|      137 | -                         |  4.97813  |
|      245 | -                         |  4.97556  |
|      113 | -                         |  4.94881  |
|      262 | -                         |  4.94732  |
|      170 | FluffyCushion             |  4.91837  |
|      106 | PingPongBall              |  4.9161   |
|      147 | -                         |  4.91002  |
|      102 | -                         |  4.89932  |
|      117 | -                         |  4.85604  |
|      135 | -                         |  4.83423  |
|      134 | -                         |  4.83049  |
|      303 | -                         |  4.81836  |
|      220 | -                         |  4.81643  |
|      292 | -                         |  4.80698  |
|      304 | Tissue                    |  4.79421  |
|      173 | -                         |  4.77902  |
|      277 | FruitBasket               |  4.76406  |
|      204 | -                         |  4.75995  |
|      153 | -                         |  4.7477   |
|      301 | -                         |  4.73201  |
|      300 | CatMacaroonPink           |  4.7219   |
|      118 | CardboardTruck            |  4.71761  |
|      165 | -                         |  4.70504  |
|      250 | -                         |  4.70038  |
|      275 | VerticalRopeNailClogger   |  4.68864  |
|      215 | -                         |  4.6828   |
|      279 | -                         |  4.68225  |
|      302 | -                         |  4.68047  |
|      201 | -                         |  4.66812  |
|      133 | -                         |  4.66133  |
|      148 | -                         |  4.6241   |
|      116 | ShoppingBoxMiddle         |  4.62231  |
|      274 | HorizontalRopeNailClogger |  4.60764  |
|      219 | -                         |  4.60576  |
|      240 | -                         |  4.6055   |
|      249 | -                         |  4.60183  |
|      296 | GlassVase                 |  4.57885  |
|      202 | -                         |  4.57829  |
|      297 | OversizedPatternedGlass   |  4.55998  |
|      258 | RailHereAndThere          |  4.54839  |
|      288 | -                         |  4.52325  |
|      205 | -                         |  4.52088  |
|      206 | -                         |  4.4754   |
|      136 | -                         |  4.45691  |
|      256 | AutomaticBunbunmaru       |  4.43905  |
|      299 | -                         |  4.41801  |
|      149 | -                         |  4.40047  |
|      209 | -                         |  4.39816  |
|      243 | -                         |  4.37862  |
|      241 | -                         |  4.34967  |
|      164 | -                         |  4.2968   |
|      144 | -                         |  4.2847   |
|      141 | -                         |  4.2665   |
|      119 | -                         |  4.23734  |
|      208 | -                         |  4.23497  |
|      246 | -                         |  4.21514  |
|      242 | -                         |  4.21478  |
|      120 | -                         |  4.2137   |
|      166 | -                         |  4.18313  |
|      284 | -                         |  4.17603  |
|      282 | Tsubo                     |  4.16737  |
|      283 | -                         |  4.15846  |
|      289 | BucketBlue                |  4.09512  |
|      211 | -                         |  4.05983  |
|      150 | -                         |  4.03416  |
|      291 | -                         |  4.03315  |
|      203 | -                         |  4.02946  |
|      273 | VinylBag                  |  3.94168  |
|      112 | CakeBox                   |  3.94141  |
|      290 | -                         |  3.92542  |
|      151 | -                         |  3.87257  |
|      248 | -                         |  3.83605  |
|      257 | -                         |  3.81354  |
|      272 | PaperBag                  |  3.65898  |
|      143 | -                         |  3.29843  |
|        6 | Sashimi                   |  2.26062  |
|        2 | GoodKarikari              |  2.25299  |
|        3 | NekoCan                   |  2.18471  |
|        5 | MaguroCan                 |  0.134993 |
|        4 | KatsuoCan                 |  0.110792 |

### Indoors, Gold Fish Equivalent per Item, Frisky Bitz, All Items Fixed
#### Args
#### Args
Namespace(food_type=2, item_damage_state=2, weather=0, is_indoor=True, output_type='gold_equiv', total_duration_minutes=1440, cat_id=None, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   GoodId | Name                      |     Value |
|----------|---------------------------|-----------|
|      227 | -                         | 38.3343   |
|      226 | -                         | 34.5644   |
|      230 | -                         | 34.4727   |
|      231 | -                         | 33.9112   |
|      260 | -                         | 33.4861   |
|      259 | -                         | 32.2422   |
|      123 | -                         | 30.8195   |
|      229 | -                         | 29.3753   |
|      261 | -                         | 29.301    |
|      235 | -                         | 27.9106   |
|      228 | -                         | 27.269    |
|      169 | -                         | 24.4817   |
|      221 | -                         | 24.4356   |
|      267 | -                         | 24.3245   |
|      264 | -                         | 23.5423   |
|      122 | CafeDeluxe                | 23.4659   |
|      121 | HouseDeluxe               | 23.2805   |
|      223 | -                         | 22.8871   |
|      222 | BeachParasol              | 22.8316   |
|      234 | TunnelT                   | 21.8633   |
|      225 | Tower3                    | 20.746    |
|      265 | -                         | 20.1479   |
|      158 | -                         | 17.2041   |
|      207 | -                         | 17.0599   |
|      159 | -                         | 16.8855   |
|      224 | Tower2                    | 16.3881   |
|      156 | -                         | 16.2303   |
|      160 | -                         | 16.0234   |
|      233 | TunnelU                   | 16.0036   |
|      157 | -                         | 15.9962   |
|      238 | -                         | 15.4536   |
|      236 | -                         | 15.408    |
|      239 | -                         | 15.4044   |
|      161 | -                         | 15.3535   |
|      232 | TunnelI                   | 15.337    |
|      213 | -                         | 15.1921   |
|      266 | -                         | 15.1828   |
|      200 | BigCushionWhite           | 15.1504   |
|      293 | -                         | 15.1165   |
|      237 | -                         | 15.0669   |
|      124 | -                         | 15.0322   |
|      199 | BigCushion                | 14.9323   |
|      212 | -                         | 13.9197   |
|      180 | -                         | 12.7585   |
|      197 | -                         | 11.4939   |
|      181 | -                         | 11.2501   |
|      306 | -                         | 10.7409   |
|      182 | -                         | 10.7357   |
|      179 | -                         | 10.6185   |
|      155 | -                         | 10.5526   |
|      196 | -                         | 10.4505   |
|      194 | -                         | 10.3145   |
|      285 | -                         | 10.2859   |
|      128 | -                         | 10.2809   |
|      287 | -                         | 10.2758   |
|      286 | -                         | 10.2459   |
|      178 | BurgerCushion             |  9.98036  |
|      195 | -                         |  9.86544  |
|      298 | WesternHats               |  9.81533  |
|      281 | -                         |  9.76921  |
|      130 | -                         |  9.70301  |
|      107 | -                         |  9.61405  |
|      129 | -                         |  9.53532  |
|      270 | -                         |  9.52329  |
|      187 | -                         |  9.44452  |
|      214 | -                         |  9.42932  |
|      131 | -                         |  9.29752  |
|      100 | Baseball                  |  9.26226  |
|      193 | -                         |  9.25926  |
|      175 | -                         |  9.23762  |
|      186 | -                         |  9.184    |
|      162 | -                         |  9.11552  |
|      192 | -                         |  8.92864  |
|      188 | PlumCocoon                |  8.89078  |
|      276 | -                         |  8.82839  |
|      168 | -                         |  8.82787  |
|      108 | StressReliever            |  8.8249   |
|      269 | -                         |  8.82351  |
|      305 | -                         |  8.82351  |
|      191 | -                         |  8.82083  |
|      254 | -                         |  8.80999  |
|      104 | -                         |  8.80791  |
|      111 | TemariBall                |  8.76333  |
|      101 | RubberBallRed             |  8.75426  |
|      252 | -                         |  8.74899  |
|      271 | -                         |  8.69906  |
|      216 | -                         |  8.68863  |
|      176 | -                         |  8.67696  |
|      171 | UmeCushionRed             |  8.66679  |
|      217 | -                         |  8.59851  |
|      263 | -                         |  8.56781  |
|      138 | -                         |  8.56301  |
|      251 | GripesMmouse              |  8.55675  |
|      189 | -                         |  8.53231  |
|      268 | -                         |  8.52497  |
|      244 | Catnip                    |  8.51809  |
|      137 | -                         |  8.51618  |
|      115 | ShoppingBoxSmall          |  8.51477  |
|      255 | -                         |  8.49927  |
|      294 | GoldfishBowl              |  8.48843  |
|      154 | -                         |  8.48494  |
|      105 | -                         |  8.47811  |
|      198 | BeadedCushion             |  8.47475  |
|      126 | -                         |  8.47066  |
|      125 | -                         |  8.46186  |
|      172 | -                         |  8.45617  |
|      190 | -                         |  8.43345  |
|      247 | -                         |  8.41879  |
|      103 | -                         |  8.40817  |
|      177 | -                         |  8.40654  |
|      278 | EarthenwarePot            |  8.39338  |
|      142 | -                         |  8.39259  |
|      109 | BallOfYarn                |  8.38737  |
|      218 | -                         |  8.34949  |
|      210 | -                         |  8.34832  |
|      132 | -                         |  8.31358  |
|      174 | -                         |  8.30363  |
|      139 | -                         |  8.30163  |
|      140 | -                         |  8.30106  |
|      245 | -                         |  8.28068  |
|      253 | -                         |  8.26871  |
|      127 | -                         |  8.26131  |
|      102 | -                         |  8.2578   |
|      114 | -                         |  8.25401  |
|      304 | Tissue                    |  8.22476  |
|      295 | -                         |  8.22166  |
|      184 | -                         |  8.20648  |
|      135 | -                         |  8.20319  |
|      280 | -                         |  8.20233  |
|      145 | -                         |  8.19941  |
|      147 | -                         |  8.17587  |
|      146 | -                         |  8.16891  |
|      170 | FluffyCushion             |  8.16484  |
|      152 | FluffyBedWhite            |  8.14884  |
|      262 | -                         |  8.13781  |
|      113 | -                         |  8.13022  |
|      134 | -                         |  8.09198  |
|      110 | -                         |  8.08642  |
|      292 | -                         |  8.0756   |
|      163 | -                         |  8.05425  |
|      250 | -                         |  8.04364  |
|      300 | CatMacaroonPink           |  8.01777  |
|      301 | -                         |  7.99879  |
|      220 | -                         |  7.99757  |
|      173 | -                         |  7.98228  |
|      183 | -                         |  7.9812   |
|      303 | -                         |  7.97418  |
|      185 | -                         |  7.97153  |
|      297 | OversizedPatternedGlass   |  7.96212  |
|      118 | CardboardTruck            |  7.95661  |
|      240 | -                         |  7.93661  |
|      153 | -                         |  7.92405  |
|      117 | -                         |  7.9156   |
|      167 | -                         |  7.89019  |
|      215 | -                         |  7.88195  |
|      201 | -                         |  7.876    |
|      116 | ShoppingBoxMiddle         |  7.86637  |
|      204 | -                         |  7.84823  |
|      106 | PingPongBall              |  7.83646  |
|      202 | -                         |  7.83593  |
|      136 | -                         |  7.82846  |
|      133 | -                         |  7.82418  |
|      302 | -                         |  7.80006  |
|      277 | FruitBasket               |  7.77488  |
|      243 | -                         |  7.75945  |
|      148 | -                         |  7.74215  |
|      241 | -                         |  7.70306  |
|      296 | GlassVase                 |  7.69811  |
|      205 | -                         |  7.68981  |
|      274 | HorizontalRopeNailClogger |  7.68507  |
|      279 | -                         |  7.68045  |
|      299 | -                         |  7.64919  |
|      249 | -                         |  7.63132  |
|      288 | -                         |  7.60164  |
|      206 | -                         |  7.57868  |
|      219 | -                         |  7.57564  |
|      256 | AutomaticBunbunmaru       |  7.56591  |
|      209 | -                         |  7.51137  |
|      242 | -                         |  7.45026  |
|      275 | VerticalRopeNailClogger   |  7.41747  |
|      291 | -                         |  7.32224  |
|      289 | BucketBlue                |  7.321    |
|      119 | -                         |  7.29892  |
|      208 | -                         |  7.26148  |
|      258 | RailHereAndThere          |  7.19553  |
|      165 | -                         |  7.16929  |
|      112 | CakeBox                   |  7.12711  |
|      120 | -                         |  7.08409  |
|      290 | -                         |  7.06787  |
|      166 | -                         |  6.99685  |
|      246 | -                         |  6.98463  |
|      164 | -                         |  6.97964  |
|      273 | VinylBag                  |  6.92497  |
|      141 | -                         |  6.91698  |
|      149 | -                         |  6.91508  |
|      282 | Tsubo                     |  6.9119   |
|      144 | -                         |  6.88169  |
|      283 | -                         |  6.85953  |
|      203 | -                         |  6.85532  |
|      284 | -                         |  6.78066  |
|      211 | -                         |  6.77233  |
|      248 | -                         |  6.35164  |
|      272 | PaperBag                  |  6.28604  |
|      150 | -                         |  6.23849  |
|      257 | -                         |  6.23771  |
|      151 | -                         |  6.0199   |
|      143 | -                         |  5.47903  |
|        2 | GoodKarikari              |  2.64375  |
|        3 | NekoCan                   |  2.62669  |
|        6 | Sashimi                   |  2.59405  |
|        5 | MaguroCan                 |  0.237497 |
|        4 | KatsuoCan                 |  0.194919 |

### Doesn't Matter Indoor / Outdoor, Peach Occur Chance, Frisky Bitz, All Items Intact (Also Doesn't Really Matter)
#### Args
Namespace(food_type=2, item_damage_state=0, weather=0, is_indoor=True, output_type='cat_probability', total_duration_minutes=1440, cat_id=24, group_def='item', items_of_interest_indoors=None, items_of_interest_outdoors=None, num_iterations_for_cat_on_cat=10)

#### Results
|   GoodId | Name                      |       Value |
|----------|---------------------------|-------------|
|      158 | -                         | 0.00316131  |
|      221 | -                         | 0.00307804  |
|      182 | -                         | 0.00284305  |
|      222 | BeachParasol              | 0.00277958  |
|      223 | -                         | 0.00244007  |
|      301 | -                         | 0.00218188  |
|      181 | -                         | 0.0021742   |
|      179 | -                         | 0.00211988  |
|      122 | CafeDeluxe                | 0.0020896   |
|      300 | CatMacaroonPink           | 0.00205637  |
|      231 | -                         | 0.00194748  |
|      228 | -                         | 0.00168874  |
|      265 | -                         | 0.00164949  |
|      229 | -                         | 0.00163103  |
|      267 | -                         | 0.00152319  |
|      239 | -                         | 0.00149281  |
|      180 | -                         | 0.00145366  |
|      258 | RailHereAndThere          | 0.00139984  |
|      303 | -                         | 0.00133751  |
|      157 | -                         | 0.00128612  |
|      203 | -                         | 0.00126211  |
|      227 | -                         | 0.00125812  |
|      156 | -                         | 0.00124071  |
|      192 | -                         | 0.00117643  |
|      169 | -                         | 0.00114941  |
|      237 | -                         | 0.00113444  |
|      159 | -                         | 0.00108832  |
|      296 | GlassVase                 | 0.00108339  |
|      213 | -                         | 0.001042    |
|      212 | -                         | 0.00101762  |
|      226 | -                         | 0.00100536  |
|      230 | -                         | 0.000966415 |
|      264 | -                         | 0.000918961 |
|      176 | -                         | 0.00089144  |
|      160 | -                         | 0.000873231 |
|      238 | -                         | 0.000868725 |
|      123 | -                         | 0.000812552 |
|      254 | -                         | 0.000761226 |
|      252 | -                         | 0.000753527 |
|      286 | -                         | 0.000734165 |
|      260 | -                         | 0.00073276  |
|      144 | -                         | 0.000718065 |
|      261 | -                         | 0.00071737  |
|      151 | -                         | 0.000715698 |
|      121 | HouseDeluxe               | 0.000714268 |
|      293 | -                         | 0.000714267 |
|      283 | -                         | 0.000707727 |
|      150 | -                         | 0.000704421 |
|      266 | -                         | 0.00069524  |
|      235 | -                         | 0.000694091 |
|      145 | -                         | 0.000674237 |
|      165 | -                         | 0.000673401 |
|      124 | -                         | 0.00065314  |
|      207 | -                         | 0.000647164 |
|      287 | -                         | 0.000647144 |
|      285 | -                         | 0.000618797 |
|      143 | -                         | 0.000606399 |
|      137 | -                         | 0.000604518 |
|      234 | TunnelT                   | 0.000595218 |
|      166 | -                         | 0.000562213 |
|      191 | -                         | 0.000559976 |
|      225 | Tower3                    | 0.000552804 |
|      280 | -                         | 0.000545757 |
|      190 | -                         | 0.000540272 |
|      284 | -                         | 0.000537178 |
|      146 | -                         | 0.00053006  |
|      259 | -                         | 0.000527085 |
|      185 | -                         | 0.00052537  |
|      149 | -                         | 0.00052302  |
|      161 | -                         | 0.000518125 |
|      108 | StressReliever            | 0.000512613 |
|      136 | -                         | 0.000509828 |
|      170 | FluffyCushion             | 0.00049872  |
|      277 | FruitBasket               | 0.000497447 |
|      199 | BigCushion                | 0.000486745 |
|      282 | Tsubo                     | 0.000484552 |
|      224 | Tower2                    | 0.000481083 |
|      248 | -                         | 0.000480283 |
|      242 | -                         | 0.000478168 |
|      200 | BigCushionWhite           | 0.000468683 |
|      193 | -                         | 0.000466802 |
|      167 | -                         | 0.00046543  |
|      297 | OversizedPatternedGlass   | 0.000461277 |
|      162 | -                         | 0.000460327 |
|      209 | -                         | 0.000459353 |
|      243 | -                         | 0.000453434 |
|      279 | -                         | 0.000452139 |
|      217 | -                         | 0.000444512 |
|      208 | -                         | 0.000440222 |
|      106 | PingPongBall              | 0.000438789 |
|      164 | -                         | 0.000436857 |
|      168 | -                         | 0.000436807 |
|      291 | -                         | 0.000435206 |
|      134 | -                         | 0.00043436  |
|      189 | -                         | 0.000428628 |
|      246 | -                         | 0.000426439 |
|      178 | BurgerCushion             | 0.000426346 |
|      104 | -                         | 0.000421964 |
|      290 | -                         | 0.000419936 |
|      236 | -                         | 0.000417666 |
|      172 | -                         | 0.000417514 |
|      171 | UmeCushionRed             | 0.000414915 |
|      241 | -                         | 0.000413178 |
|      251 | GripesMmouse              | 0.000411224 |
|      141 | -                         | 0.000407005 |
|      289 | BucketBlue                | 0.00040374  |
|      135 | -                         | 0.000398177 |
|      210 | -                         | 0.000395051 |
|      188 | PlumCocoon                | 0.000390665 |
|      253 | -                         | 0.000386987 |
|      255 | -                         | 0.000386304 |
|      110 | -                         | 0.000376592 |
|      103 | -                         | 0.000374716 |
|      298 | WesternHats               | 0.000374114 |
|      153 | -                         | 0.00037275  |
|      177 | -                         | 0.000369362 |
|      306 | -                         | 0.00036263  |
|      232 | TunnelI                   | 0.000360441 |
|      187 | -                         | 0.000356122 |
|      211 | -                         | 0.000355705 |
|      194 | -                         | 0.000351933 |
|      152 | FluffyBedWhite            | 0.000351072 |
|      102 | -                         | 0.000349168 |
|      148 | -                         | 0.00034464  |
|      275 | VerticalRopeNailClogger   | 0.00034296  |
|      142 | -                         | 0.000337658 |
|      196 | -                         | 0.000336924 |
|      271 | -                         | 0.0003356   |
|      155 | -                         | 0.000334375 |
|      292 | -                         | 0.000333027 |
|      154 | -                         | 0.000332037 |
|      120 | -                         | 0.00033078  |
|      131 | -                         | 0.000321925 |
|      270 | -                         | 0.000321783 |
|      302 | -                         | 0.00031996  |
|      109 | BallOfYarn                | 0.000319569 |
|      173 | -                         | 0.000316284 |
|      201 | -                         | 0.000316284 |
|      233 | TunnelU                   | 0.000315076 |
|      117 | -                         | 0.000314439 |
|      220 | -                         | 0.000307468 |
|      281 | -                         | 0.000300657 |
|      269 | -                         | 0.000299755 |
|      305 | -                         | 0.000299755 |
|      257 | -                         | 0.000299064 |
|      175 | -                         | 0.000293584 |
|      139 | -                         | 0.000292632 |
|      111 | TemariBall                | 0.000292555 |
|      174 | -                         | 0.00029062  |
|      215 | -                         | 0.00028361  |
|      184 | -                         | 0.000275173 |
|      197 | -                         | 0.000273913 |
|      112 | CakeBox                   | 0.000270339 |
|      105 | -                         | 0.000270001 |
|      195 | -                         | 0.000265391 |
|      273 | VinylBag                  | 0.000263368 |
|      133 | -                         | 0.000260461 |
|      202 | -                         | 0.000256246 |
|      299 | -                         | 0.000255402 |
|      114 | -                         | 0.000253232 |
|      147 | -                         | 0.000252811 |
|      272 | PaperBag                  | 0.000252056 |
|      262 | -                         | 0.000249762 |
|      240 | -                         | 0.000249663 |
|      113 | -                         | 0.000247034 |
|      198 | BeadedCushion             | 0.000246449 |
|      214 | -                         | 0.000245708 |
|      274 | HorizontalRopeNailClogger | 0.000240157 |
|      132 | -                         | 0.000239009 |
|      119 | -                         | 0.000233473 |
|      205 | -                         | 0.000230313 |
|      263 | -                         | 0.000225325 |
|      288 | -                         | 0.000224021 |
|      204 | -                         | 0.000222443 |
|      100 | Baseball                  | 0.000222281 |
|      183 | -                         | 0.000221072 |
|      206 | -                         | 0.000218645 |
|      107 | -                         | 0.000216549 |
|      138 | -                         | 0.000214235 |
|      163 | -                         | 0.000214066 |
|      247 | -                         | 0.000213543 |
|      118 | CardboardTruck            | 0.000208236 |
|      245 | -                         | 0.000207707 |
|      216 | -                         | 0.000206362 |
|      244 | Catnip                    | 0.000205328 |
|      250 | -                         | 0.000200846 |
|      219 | -                         | 0.000195172 |
|      140 | -                         | 0.00019398  |
|      129 | -                         | 0.000190878 |
|      128 | -                         | 0.000189526 |
|      130 | -                         | 0.000188843 |
|      256 | AutomaticBunbunmaru       | 0.000185996 |
|      304 | Tissue                    | 0.000183393 |
|      126 | -                         | 0.000181988 |
|      218 | -                         | 0.000180922 |
|      186 | -                         | 0.000174276 |
|      268 | -                         | 0.000160891 |
|      276 | -                         | 0.000156788 |
|      295 | -                         | 0.000154221 |
|      249 | -                         | 0.000152543 |
|      101 | RubberBallRed             | 0.000144408 |
|      125 | -                         | 0.000128112 |
|      127 | -                         | 0.000123167 |
|      116 | ShoppingBoxMiddle         | 0.000111962 |
|      294 | GoldfishBowl              | 0.000110067 |
|      115 | ShoppingBoxSmall          | 0.000108077 |
|      278 | EarthenwarePot            | 8.19902e-05 |
