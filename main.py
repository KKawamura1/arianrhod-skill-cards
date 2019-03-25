from skill_cards_generator.skill_crawler import main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sleeve', action='store_true',
                        help='Print for sleeves.')
    params = parser.parse_args()

    main(params.sleeve)
