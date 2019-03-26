from skill_cards_generator.skill_crawler import main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sleeve', action='store_true',
                        help='Print for sleeves.')
    parser.add_argument('--large', action='store_true',
                        help='Enlarge skill names.')
    params = parser.parse_args()

    main(params.sleeve, params.large)
