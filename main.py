from difflib import SequenceMatcher
import time
import csv


def similarity_score(string_a: str, string_b: str) -> float:
    """
    Calculate the similarity score between two strings using SequenceMatcher.

    Args:
        string_a (str): The first string to compare.
        string_b (str): The second string to compare.

    Returns:
        float: A similarity score between 0.0 and 1.0, where 1.0 indicates an exact match.
                Returns 0.0 if both strings are empty or in case of an error.
    """
    try:
        if not string_a and not string_b:
            return 0.0

        # Use SequenceMatcher to get similarity ratio
        return SequenceMatcher(None, string_a, string_b).ratio()

    except Exception as error:
        print(f"Error comparing strings {string_a} and {string_b}: {error}")

        # In case of error, return 0 similarity
        return 0.0


def score_match(contact_a: dict, contact_b: dict) -> str:
    """
    Calculate a match score between two contact dictionaries and classify it as High, Medium, or Low.

    Args:
        contact_a (dict): The first contact dictionary.
        contact_b (dict): The second contact dictionary.

    Returns:
        str: A string indicating the match accuracy: "High", "Medium", or "Low".
    """
    try:
        score: float = 0.0
        # Compare email in contact_a with the corresponding field in contact_b
        if contact_a["email"] == contact_b["email"] and contact_a["email"]:
            score += 50
        else:
            score += similarity_score(contact_a["email"], contact_b["email"]) * 20

        # first name similarity
        score += similarity_score(contact_a["name"], contact_b["name"]) * 10

        # last name similarity
        score += similarity_score(contact_a["name1"], contact_b["name1"]) * 10

        # address similarity
        score += similarity_score(contact_a["address"], contact_b["address"]) * 30

        # zip code match
        score += (
            10
            if contact_a["postalZip"] == contact_b["postalZip"]
            and contact_a["postalZip"]
            else 0
        )

        # translate score into high-low scale terms
        if score >= 80:
            return "High"
        elif score >= 50:
            return "Medium"
        return "Low"

    except Exception as error:
        print(
            f"Error scoring match between contacts {contact_a['contactID']} and {contact_b['contactID']}: {error}"
        )
        return "Low"


def find_duplicates(contacts: list[dict]) -> list[dict]:
    """
    Find potential duplicate contacts in a list of contact dictionaries.

    Args:
        contacts (list[dict]): A list of contact dictionaries, each containing contact information.

    Returns:
        list[dict]: A list of dictionaries, each containing the source contact ID, the match contact ID,
                    and the accuracy of the match ("High", "Medium", or "Low").
    """
    results = []
    try:
        for i in range(len(contacts)):
            for j in range(i + 1, len(contacts)):
                accuracy = score_match(contacts[i], contacts[j])
                results.append(
                    {
                        "ContactID Source": contacts[i]["contactID"],
                        "ContactID Match": contacts[j]["contactID"],
                        "Accuracy": accuracy,
                    }
                )
    except Exception as error:
        print(f"Error finding duplicates: {error}")

    return results


if __name__ == "__main__":
    # Read contacts from CSV file
    with open("contacts.csv") as csv_file:
        data = csv.DictReader(
            csv_file,
            delimiter=",",
        )
        contacts = list(data)

        # Calculate compute time for finding potential duplicates sequentially. Given more time, this could be parallelized.
        start_time = time.time()
        duplicate_matches = find_duplicates(contacts)
        end_time = time.time()
        print(f"Sequential execution time: {end_time - start_time} seconds")

        with open("results.csv", mode="w", newline="") as results_file:
            fieldnames = ["ContactID Source", "ContactID Match", "Accuracy"]
            writer = csv.DictWriter(results_file, fieldnames=fieldnames)

            writer.writeheader()
            for match in duplicate_matches:
                writer.writerow(match)
