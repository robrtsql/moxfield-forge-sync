import requests
import os

HOST = "api.moxfield.com"
USERNAME = "robrtsql"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0"
FORGE_DECKS_FOLDER = "/Users/rob/commonsync/Forge/decks"
TEMPLATE = """[metadata]
Name={}
[Avatar]

[Commander]
{}

[Main]
{}

[Sideboard]

[Planes]

[Schemes]

[Conspiracy]

[Attractions]


"""


def main():
    print("moxfield-forge-sync")
    decks_resp = requests.get(
        f'https://api.moxfield.com/v2/users/{USERNAME}/decks?pageSize=100',
        headers={
            "User-Agent": USER_AGENT
        },
    )
    decks_resp.raise_for_status()
    decks = decks_resp.json().get("data", [])
    commander_decks = [deck for deck in decks if deck.get("format") == "commander"]
    for deck in commander_decks:
        deck_resp = requests.get(
            f'https://api2.moxfield.com/v3/decks/all/{deck["publicId"]}',
            headers={
                "User-Agent": USER_AGENT
            },
        )
        deck_resp.raise_for_status()
        deck_json = deck_resp.json()
        build_dck_file(deck_json)


def build_dck_file(deck_json):
    mainboard = '\n'.join([get_card_string(card["card"], card["quantity"])
                      for card in list(deck_json["boards"]["mainboard"]["cards"].values())])
    commanders = '\n'.join([get_card_string(card["card"], card["quantity"])
                            for card in list(deck_json["boards"]["commanders"]["cards"].values())])
    dck_txt = TEMPLATE.format(
        deck_json["name"],
        commanders,
        mainboard
    )
    dck_filename = f'{deck_json["name"]}.dck'
    dck_full_path = os.path.join(FORGE_DECKS_FOLDER, 'commander', dck_filename)
    print(f'Writing {dck_full_path}.')
    with open(dck_full_path, 'w') as dck_file:
        dck_file.write(dck_txt)


def get_card_string(card, quantity):
    return f'{quantity} {card["name"]}|{card["set"].upper()}|1'


if __name__ == "__main__":
    main()