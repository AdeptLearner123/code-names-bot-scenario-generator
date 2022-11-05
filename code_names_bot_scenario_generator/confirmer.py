from config import SCENARIOS_DIR, GUESSES_DIR

import os
import yaml
from argparse import ArgumentParser
import random

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-t", type=str, required=True)
    args = parser.parse_args()
    return args.t


def get_guess(scenario):
    words = scenario["pos"] + scenario["neg"]
    random.shuffle(words)
    clue = scenario["clue"]
    num = len(scenario["pos"])

    print("Words:")
    for i, word in enumerate(words):
        print(f"[{i}]  {word}")
    print("Clue:", clue, num)

    guesses = []
    while True:
        guess = input("Guess: ")
        if guess.isdigit():
            idx = int(guess)
            word = words[idx]
            guesses.append(word)
        else:
            print("Invalid guess")
            break

    return guesses


def main():
    scenarios = dict()

    for filename in os.listdir(SCENARIOS_DIR):
        path = os.path.join(SCENARIOS_DIR, filename)
        with open(path, "r") as file:
            scenarios.update(yaml.safe_load(file))

    print("Total scenarios:", len(scenarios))

    target_file = parse_args()

    guesses_path = os.path.join(GUESSES_DIR, target_file)
    if not os.path.exists(guesses_path):
        scenario_guesses = dict()
    else:
        with open(guesses_path, "r") as file:
            scenario_guesses = yaml.safe_load(file)
    
    unguessed_scenarios = set(scenarios.keys()).difference(set(scenario_guesses.keys()))
    unguessed_scenarios = sorted(list(unguessed_scenarios))

    print("Unguessed:", len(unguessed_scenarios))

    for i, scenario_id in enumerate(unguessed_scenarios):
        print(f"{i} / {len(unguessed_scenarios)}")
        guesses = get_guess(scenarios[scenario_id])
        scenario_guesses[scenario_id] = guesses

        with open(guesses_path, "w+") as file:
            yaml.safe_dump(scenario_guesses, file)
    
    correct = 0
    for scenario_id in scenarios.keys():
        scenario = scenarios[scenario_id]
        guesses = scenario_guesses[scenario_id]

        if set(scenario["pos"]) != set(guesses):
            print("Incorrect:", scenario_id)
            print("\tClue:", scenario["clue"])
            print("\tExpected:", scenario["pos"])
            print("\tGuessed:", guesses)
        else:
            correct += 1
    print("Accuracy:", correct, "/", len(scenarios), "=", correct / len(scenarios))