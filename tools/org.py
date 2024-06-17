from pathlib import Path
import random

current_dir = Path(__file__).resolve().parent


def org_name_generator(num_words=3):
    astronomer_terms_path = current_dir / "static" / "astronomy-terms.txt"
    with open(astronomer_terms_path, "r") as f:
        astronomer_terms = f.readlines()
    astronomer_terms = [term.strip().lower() for term in astronomer_terms]
    org_name = "-".join(random.sample(astronomer_terms, num_words))
    return org_name


if __name__ == "__main__":
    print(org_name_generator())
