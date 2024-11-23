
from copy import copy
from random import choice, randint, random
from time import time
from types import SimpleNamespace

import numpy as np

from analyze import DataLoader, NekoAtsumeAnalyzer

cat_id_to_name = DataLoader.load_json_data("data_inferred/cat_id_to_name.json")
cat_name_to_id = {v: int(k) for k, v in cat_id_to_name.items()}


# All rare cats
cats_to_analyze = list(cat_name_to_id.keys())
cats_to_analyze = [name for name, id in cat_name_to_id.items() if int(id) >= 100]
# # Peaches
cats_to_analyze.append("Peaches")

# Example: already got mementos for some cats
for x in [
    "Snowball",
    "Smokey", 
    "Spots", 
    "Shadow", 
    "Sunny", 
    # "Fred", 
    "Pumpkin", 
    "Callie", 
    "Tabitha", 
    # "Bandit", 
    # "Gabriel", 
    # "Marshmallow", 
    # "Socks", 
    "Lexy", 
    # "Bolt", 
    # "Breezy", 
    # "Misty", 
    # "Pickles", 
    # "Pepper", 
    # "Patches", 
    "Gozer", 
    # "Cocoa", 
    # "Princess", 
    # "Ginger", 
    # "Peaches", 
    # "Spud", 
    # "Mack", 
    "Speckles", 
    # "Willie", 
    # "Rascal", 
    # "Dottie", 
    "Spooky", 
    # "Apricot", 
    "Ganache", 
    # "Pasty", 
    # "Chip", 
    # "Macchiato", 
    "Melange", 
    # "Chocola", 
    "Willow", 
    # "Sooty", 
    # "Quicksilver", 
    # "Maple", 
    # "Caramel", 

    # "Joe DiMeowgio", 
    # "Senor Don Gato", 
    # "Xerxes IX", 
    # "Chairman Meow", 
    # "Saint Purrtrick", 
    # "Ms. Fortune", 
    # "Bob the Cat", 
    # "Conductor Whiskers", 
    "Tubbs", 
    # "Mr. Meowgi", 
    # "Lady Meow-Meow", 
    # "Guy Furry", 
    # "Kathmandu", 
    # "Ramses the Great", 
    # "Sassy Fran", 
    # "Billy the Kitten", 
    # "Frosty", 
    # "Sapphire", 
    # "Jeeves", 
    # "Bengal Jack", 
    # "Whiteshadow", 
    # "Hermeowne", 
    # "Informeow", 
    # "Survy", 
    # "Red Purrhood", 
    ]: 
    if cats_to_analyze.count(x) > 0:
        cats_to_analyze.remove(x)

ALLOWED_FOODS = range(1, 8)
# ALLOWED_FOODS = [7]
# Penalty for expensive foods, eg. cost to buy them (assuming with the 15% bulk discount) 
# (cost per bulk (/50 for silver -> gold) / 3 (items per bulk) * 24 hours / hours per food)
FOOD_PENALTY = [-9999, 0, 30/50 /3 * 24/6, 7/3 * 24/3, 17/3 * 24/3, 30/3 * 24/3, 5 * 24/3, 15 * 24] 
# FOOD_PENALTY = [0 for _ in range(0, 8)]
BASE_ARGS = SimpleNamespace(**{
    "food_type": ALLOWED_FOODS[0], 
    "item_damage_state": 0,
    "output_type": 'gold_equiv',
    "cat_id": [cat_name_to_id[cat_name] for cat_name in cats_to_analyze],
    "total_duration_minutes": 1440, 
    "group_def": 'custom',
    "items_of_interest_indoors": [], 
    "items_of_interest_outdoors": [], 
    "weather": 0, 
    "num_iterations_for_cat_on_cat": 10, 
})

analyzer = NekoAtsumeAnalyzer(BASE_ARGS)
ITEMS = [x for x in analyzer.item_existence_set if x > 10 and x != 121]

# When for example optimizing layout after having done a cat_probability optimization
# ITEMS = [100, 108, 129, 211, 258, 278, 296, 298, 300]
# or when only having done indoor with expensive food (NOTE: cat vs cat interactions will be wrong)
# for item in [111, 120, 122, 211]:
#     ITEMS.remove(item)

LARGE_ITEMS = [x for x in ITEMS if analyzer.item_to_size.get(str(x)) == True]
SMALL_ITEMS = [x for x in ITEMS if analyzer.item_to_size.get(str(x)) == False]
PLACES_INDOOR = 5
PLACES_OUTDOOR = 5

# Genetic algorithm Parameters
POOL_SIZE = 200
TOURNAMENT_K = 5
TOURNAMENT_SELECTION_SIZE = round(POOL_SIZE * 0.5)
MUTATION_RATE = 0.05
MUTATION_OFFSPRING_RATE = 0.5
REPOPULATION_SIZE = round(POOL_SIZE * 0.25)

class Yard:
    def __init__(self, food_type: int, indoor_large: set[int], indoor_small: set[int], outdoor_large: set[int], outdoor_small: set[int], value: float):
        self.food_type = food_type
        self.indoor_large = indoor_large
        self.indoor_small = indoor_small
        self.outdoor_large = outdoor_large
        self.outdoor_small = outdoor_small
        self.value = value

        self.hash = hash((self.food_type, tuple(self.indoor_large), tuple(self.indoor_small), tuple(self.outdoor_large), tuple(self.outdoor_small)))

        if len(self.indoor_large) > 1 or len(self.indoor_small) + len(self.indoor_large) * 2 != PLACES_INDOOR:
            raise ValueError(f"indoor_large={self.indoor_large}, indoor_small={self.indoor_small}")
        
        if len(self.outdoor_large) > 1 or len(self.outdoor_small) + len(self.outdoor_large) * 2 != PLACES_OUTDOOR:
            raise ValueError(f"outdoor_large={self.outdoor_large}, outdoor_small={self.outdoor_small}")
        
        self.used = set(self.indoor_large)
        self.used.update(self.indoor_small)
        self.used.update(self.outdoor_large)
        self.used.update(self.outdoor_small)
        if len(self.used) != len(self.indoor_large) + len(self.indoor_small) + len(self.outdoor_large) + len(self.outdoor_small):
            raise ValueError(f"used={self.used}, indoor_large={self.indoor_large}, indoor_small={self.indoor_small}, outdoor_large={self.outdoor_large}, outdoor_small={self.outdoor_small}")

    def __str__(self) -> str:
        return f"Yard(indoor_large={self.indoor_large}, indoor_small={self.indoor_small}, outdoor_large={self.outdoor_large}, outdoor_small={self.outdoor_small}, value={self.value})"    

    def __hash__(self) -> int:
        return self.hash

    def __eq__(self, other) -> bool:
        return self.indoor_large == other.indoor_large and self.indoor_small == other.indoor_small and self.outdoor_large == other.outdoor_large and self.outdoor_small == other.outdoor_small and self.food_type == other.food_type

def main():
    total_start_time = time()
    pool = set()
    print("Creating initial pool")

    # Initialization
    pool.update(generate_random_pool())

    print("Starting loop")
    iteration = 0
    while True:
        iteration += 1
        start_time = time()

        # Repopulate
        if iteration > 1:
            pool.update(generate_random_pool(REPOPULATION_SIZE))

        # Selection
        winners = list(k_tournament(pool))

        # Mutation
        pool.update(create_offspring_and_mutate(pool, winners))

        top_results = sorted(pool, key=lambda p: -p.value)[0:POOL_SIZE]
        pool = set(top_results)
        best = top_results[0]

        end_time = time()

        print(f"Iteration #{iteration} iteration took {round(end_time - start_time, 2)}s total time so far {round(end_time - total_start_time, 2)}s")
        print("Best yard", best.indoor_large, best.indoor_small, best.outdoor_large, best.outdoor_small)
        print("  Food:", analyzer.item_to_name[str(best.food_type)])
        print("  Items", sorted(list(best.indoor_large) + list(best.indoor_small) + list(best.outdoor_large) + list(best.outdoor_small)))
        print("  Value: ", best.value)
        print("  Indoor:", list(analyzer.item_to_name[str(i)] for i in list(best.indoor_large) + list(best.indoor_small)))
        print("  Outdoor:", list(analyzer.item_to_name[str(i)] for i in list(best.outdoor_large) + list(best.outdoor_small)))

        if iteration % 10 == 0:
            for type in ["gold_equiv", "silver_equiv", "gold", "silver"]:
                value = get_value(best.food_type, best.indoor_large, best.indoor_small, best.outdoor_large, best.outdoor_small, type)
                print(f"  Value for {type}: {value}")

        analyze_command = "python analyze.py "
        analyze_command += f"--output_type {BASE_ARGS.output_type} "
        analyze_command += f"--food_type {best.food_type} "
        analyze_command += f"--group_def {BASE_ARGS.group_def} "
        if BASE_ARGS.total_duration_minutes != 1440:
            analyze_command += f"--total_duration_minutes {BASE_ARGS.total_duration_minutes} "
        if BASE_ARGS.item_damage_state != 0:
            analyze_command += f"--item_damage_state {BASE_ARGS.item_damage_state} "
        if BASE_ARGS.output_type == 'cat_probability':
            analyze_command += f"--cat_id {' '.join(str(i) for i in BASE_ARGS.cat_id)} "
        analyze_command += f"--items_of_interest_indoors {' '.join(str(i) for i in list(best.indoor_large) + list(best.indoor_small))} "
        analyze_command += f"--items_of_interest_outdoors {' '.join(str(i) for i in list(best.outdoor_large) + list(best.outdoor_small))} "
        print(analyze_command.strip())


        
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count

executor = ProcessPoolExecutor(max_workers=cpu_count())
MULTI_THREAD = True

def generate_random_pool(size = POOL_SIZE) -> set[Yard]:
    pool = set()

    if MULTI_THREAD:
        futures = [
            executor.submit(generate_yard)
            for _ in range(size)
        ]

        for future in as_completed(futures):
            yard = future.result()
            pool.add(yard)
    else:
        for _ in range(size):
            yard = generate_yard()
            pool.add(yard)
    return pool

def create_offspring_and_mutate(pool: set[Yard], winners: list[Yard]) -> list[Yard]:
    offspring = []
    leftHalf = winners[:len(winners)//2+1]
    rightHalf = winners[len(winners)//2+1:]

    if MULTI_THREAD:
        futures = [
            executor.submit(crossover_mutation, left, right)
            for left, right in zip(leftHalf, rightHalf)
        ]
        futures.extend([
            executor.submit(inside_outside_crossover, left, right)
            for left, right in zip(leftHalf, rightHalf)
        ])

        next_futures = [
            executor.submit(mutate_yard, yard)
            for yard in list(pool) if random() < MUTATION_RATE
        ]

        for future in as_completed(futures):
            results = future.result()
            offspring.extend(results)
            for result in results:
                if random() < MUTATION_OFFSPRING_RATE:
                    next_futures.append(executor.submit(mutate_yard, result))

        for future in as_completed(next_futures):
            offspring.append(future.result())
    else:
        for left, right in zip(leftHalf, rightHalf):
            offspring.extend(crossover_mutation(left, right))
            offspring.extend(inside_outside_crossover(left, right))

        for result in offspring:
            if random() < MUTATION_OFFSPRING_RATE:
                offspring.append(mutate_yard(result))
            
        for yard in list(pool):
            if random() < MUTATION_RATE:
                offspring.append(mutate_yard(yard))
    return offspring


def generate_yard() -> Yard:
    used = set()
    # These checks are likely not fully correct when there's some weird combination of items available
    select_large_indoor = random() < 0.5 and len(LARGE_ITEMS) > 0 and PLACES_INDOOR >= 2 or len(SMALL_ITEMS) < (PLACES_OUTDOOR + PLACES_OUTDOOR - 2)
    select_large_outdoor = random() < 0.5 and len(LARGE_ITEMS) > (1 if select_large_indoor else 0) and PLACES_OUTDOOR >= 2 or len(SMALL_ITEMS) < (PLACES_OUTDOOR + (max(0, PLACES_INDOOR - 2) if select_large_indoor else PLACES_INDOOR))

    indoor_large = generate_large(used, select_large_indoor)
    indoor_small = generate_small(used, select_large_indoor, PLACES_INDOOR)

    outdoor_large = generate_large(used, select_large_outdoor)
    outdoor_small = generate_small(used, select_large_outdoor, PLACES_OUTDOOR)

    food_type = choice(ALLOWED_FOODS)

    return create_yard(food_type, indoor_large, indoor_small, outdoor_large, outdoor_small)

def create_yard(food: int, indoor_large: set[int], indoor_small: set[int], outdoor_large: set[int], outdoor_small: set[int]) -> Yard:
    value = get_value(food, indoor_large, indoor_small, outdoor_large, outdoor_small)
    return Yard(food, indoor_large, indoor_small, outdoor_large, outdoor_small, value)

def generate_large(used: set[int], select_large: bool) -> set[int]:
    if select_large:
        item = choice(list(set(LARGE_ITEMS) - used))
        used.add(item)
        return {item}
    return {}

def generate_small(used: set[int], select_large: bool, max_amount_in_area: int) -> set[int]:
    items = set()
    for _ in range(max_amount_in_area - 2 if select_large else max_amount_in_area):
        item = choice(list(set(SMALL_ITEMS) - used))
        used.add(item)
        items.add(item)
    return items

def get_value(food_type: int, a: set[int], b: set[int], c: set[int], d: set[int], type: str | None = None):
    args = BASE_ARGS
    if type:
        args = copy(args)
        args.output_type = type

    args.food_type = food_type
    args.items_of_interest_indoors = list(a) + list(b)
    args.items_of_interest_outdoors = list(c) + list(d)

    analyzer = NekoAtsumeAnalyzer(args)
    results = analyzer.analyze()
    if type is None:
        max_food = 0 
        # When maximizing for some expensive food while trying to minimize what could've been done cheaper
        # for x in range(1, 8):
        #     if x == args.food_type:
        #         continue
        #     args.food_type = x
        #     baseanalyzer = NekoAtsumeAnalyzer(args)
        #     resultsbase = baseanalyzer.analyze()
        #     max_food = max(max_food, resultsbase['Your Yard Total'])

        # Penalty is only applied when getting value for set type
        return results['Your Yard Total'] - max_food - FOOD_PENALTY[food_type]
    return results['Your Yard Total']

def k_tournament(yards: set[Yard]) -> set[Yard]:
    winners = set()
    yards = list(yards)
    for _ in range(TOURNAMENT_SELECTION_SIZE):
        k = min(TOURNAMENT_K, len(yards))
        if k == 0:
            break
        participants = np.random.choice(yards, k, replace=False)
        best = max(participants, key=lambda p: p.value)
        winners.add(best)
        yards.remove(best)
    return winners

def crossover_mutation(left: Yard, right: Yard) -> list[Yard]:
    crossed = False
    if len(left.indoor_large) == len(right.indoor_large): 
        [a_indoor_large, b_indoor_large] = crossover(left.indoor_large, right.indoor_large, left.used, right.used)
        [a_indoor_small, b_indoor_small] = crossover(left.indoor_small, right.indoor_small, left.used, right.used)
        crossed = True
    else: # No crossover if different
        [a_indoor_large, b_indoor_large] = [left.indoor_large, right.indoor_large]
        [a_indoor_small, b_indoor_small] = [left.indoor_small, right.indoor_small]
    
    if len(left.outdoor_large) == len(right.outdoor_large): 
        [a_outdoor_large, b_outdoor_large] = crossover(left.outdoor_large, right.outdoor_large, left.used, right.used)
        [a_outdoor_small, b_outdoor_small] = crossover(left.outdoor_small, right.outdoor_small, left.used, right.used)
        crossed = True
    else: # No crossover if different
        [a_outdoor_large, b_outdoor_large] = [left.outdoor_large, right.outdoor_large]
        [a_outdoor_small, b_outdoor_small] = [left.outdoor_small, right.outdoor_small]

    if not crossed:
        return []
    
    if random() < 0.5:
        [a_food, b_food] = [right.food_type, left.food_type]
    else:
        [a_food, b_food] = [left.food_type, right.food_type]

    return [
        create_yard(a_food, a_indoor_large, a_indoor_small, a_outdoor_large, a_outdoor_small),
        create_yard(b_food, b_indoor_large, b_indoor_small, b_outdoor_large, b_outdoor_small),
    ]

def inside_outside_crossover(left: Yard, right: Yard) -> list[Yard]:
    # Only perform crossover if the yard sizes are the same
    if len(left.indoor_large) == len(right.indoor_large) and len(left.indoor_large) == len(left.outdoor_large) and len(left.outdoor_large) == len(right.outdoor_large) and len(left.indoor_small) == len(right.indoor_small) and len(left.indoor_small) == len(left.outdoor_small) and len(left.outdoor_small) == len(right.outdoor_small):
        [a_indoor_large, b_indoor_large] = crossover(left.indoor_large, right.outdoor_large, left.used, right.used)
        [a_indoor_small, b_indoor_small] = crossover(left.indoor_small, right.outdoor_small, left.used, right.used)
        [a_outdoor_large, b_outdoor_large] = crossover(left.outdoor_large, right.indoor_large, left.used, right.used)
        [a_outdoor_small, b_outdoor_small] = crossover(left.outdoor_small, right.indoor_small, left.used, right.used)
    
        if random() < 0.5:
            [a_food, b_food] = [right.food_type, left.food_type]
        else:
            [a_food, b_food] = [left.food_type, right.food_type]
        return [
            create_yard(a_food, a_indoor_large, a_indoor_small, a_outdoor_large, a_outdoor_small),
            create_yard(b_food, b_indoor_large, b_indoor_small, b_outdoor_large, b_outdoor_small),
        ]

    return []


def crossover(left: set[int], right: set[int], left_used: set[int], right_used: set[int]) -> list[set[int]]:
    if len(left) == 0:
        return set(left), set(right)
    if len(left) != len(right):
        raise ValueError(f"left={left}, right={right} don't have the same length")

    l = list(left)
    r = list(right)
    
    for _ in range(randint(0, len(l) - 1)):
        swap_index = randint(0, len(l) - 1)
        tmp = l[swap_index]
        if tmp in right_used or r[swap_index] in left_used:
            continue
        l[swap_index] = r[swap_index]
        r[swap_index] = tmp

    return set(l), set(r)

def mutate_yard(yard: Yard) -> Yard:
    indoor_large = list(yard.indoor_large)
    indoor_small = list(yard.indoor_small)
    outdoor_large = list(yard.outdoor_large)
    outdoor_small = list(yard.outdoor_small)

    [indoor_large, removed_indoor_large] = pick(indoor_large)
    [indoor_small, removed_indoor_small] = pick(indoor_small)
    [outdoor_large, removed_outdoor_large] = pick(outdoor_large)
    [outdoor_small, removed_outdoor_small] = pick(outdoor_small)

    indoor_large = set(indoor_large)
    indoor_small = set(indoor_small)
    outdoor_large = set(outdoor_large)    
    outdoor_small = set(outdoor_small)

    used_items = set(yard.used)
    for x in [removed_indoor_large, removed_indoor_small, removed_outdoor_large, removed_outdoor_small]:
        if x is not None:
            used_items.remove(x)

    if removed_indoor_large is not None:
        while True:
            new_item = choice(LARGE_ITEMS)
            if random() < 0.5:
                new_item = removed_indoor_large
            if new_item not in used_items:
                break
        indoor_large.add(new_item)
        used_items.add(new_item)

    if removed_indoor_small is not None:
        while True:
            new_item = choice(SMALL_ITEMS)
            if random() < 0.5:
                new_item = removed_indoor_small
            if new_item not in used_items:
                break
        indoor_small.add(new_item)
        used_items.add(new_item)

    if removed_outdoor_large is not None:
        while True:
            new_item = choice(LARGE_ITEMS)
            if random() < 0.5:
                new_item = removed_outdoor_large
            if new_item not in used_items:
                break
        outdoor_large.add(new_item)
        used_items.add(new_item)

    if removed_outdoor_small is not None:
        while True:
            new_item = choice(SMALL_ITEMS)
            if random() < 0.5:
                new_item = removed_outdoor_small
            if new_item not in used_items:
                break
        outdoor_small.add(new_item)
        used_items.add(new_item)
    
    if random() < 0.3:
        food_type = yard.food_type
    else:
        food_type = choice(ALLOWED_FOODS)

    return create_yard(food_type, indoor_large, indoor_small, outdoor_large, outdoor_small)


def pick(items):
    if len(items) == 0:
        return [items, None]
    picked = choice(items)
    items.remove(picked)
    return [items, picked]

if __name__ == "__main__":
    main()