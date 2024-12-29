#!/usr/bin/env python3
import os
import sys
import argparse
import requests

def get_list_id_by_name(key, token, board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {
        'key': key,
        'token': token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    lists = response.json()
    
    for lst in lists:
        if lst['name'].lower() == list_name.lower():
            return lst['id']
    return None


def get_labelId_by_title(key, token, board_id, titles):
    url = f"https://api.trello.com/1/boards/{board_id}/labels"
    params = {
        'key': key,
        'token': token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    labels = response.json()

    label_map = {label['name'].lower(): label['id'] for label in labels if label.get('name')}

    found_label_ids = []
    for title in titles:
        label_id = label_map.get(title.lower())
        if label_id:
            found_label_ids.append(label_id)
        else:
            print(f"Warning: No label found with the title '{title}'")

    return found_label_ids

def create_card(key, token, list_id, name, desc, label_ids):
    url = "https://api.trello.com/1/cards"
    query = {
        'key': key,
        'token': token,
        'idList': list_id,
        'name': name,
        'desc': desc,
    }

    # If labels were provided, add them as idLabels[]
    for i, lid in enumerate(label_ids):
        query[f'idLabels[{i}]'] = lid

    response = requests.post(url, params=query)
    response.raise_for_status()
    return response.json()

def add_comment_to_card(key, token, card_id, comment):
    url = f"https://api.trello.com/1/cards/{card_id}/actions/comments"
    query = {
        'key': key,
        'token': token,
        'text': comment
    }
    response = requests.post(url, params=query)
    response.raise_for_status()
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Add a card to a Trello board list (column) by column name.")
    parser.add_argument("--board-id", required=True, help="The ID of the Trello board")
    parser.add_argument("--list-name", required=True, help="The name of the Trello list (column)")
    parser.add_argument("--name", required=True, help="The name of the card to create")
    parser.add_argument("--desc", default="", help="The description of the card")
    parser.add_argument("--labels", nargs='*', default=[], help="One or more labels to attach to the card")
    parser.add_argument("--comment", default="", help="A comment to add to the newly created card")

    args = parser.parse_args()

    key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")

    if not key or not token:
        sys.stderr.write("Error: Trello API key and token are required. Set them as environment variables TRELLO_KEY and TRELLO_TOKEN.\n")
        sys.exit(1)

    # Find the list ID by name
    list_id = get_list_id_by_name(key, token, args.board_id, args.list_name)
    if not list_id:
        sys.stderr.write(f"Error: No list found with name '{args.list_name}' on board '{args.board_id}'.\n")
        sys.exit(1)

    #get label IDs
    label_ids = []
    if args.labels:
        label_ids = get_labelId_by_title(key, token, args.board_id, args.labels)


    # Create the card on the found list
    card_info = create_card(
        key=key,
        token=token,
        list_id=list_id,
        name=args.name,
        desc=args.desc,
        label_ids=label_ids
    )

    print(f"Card created: {card_info.get('shortUrl')}")

    # If a comment was requested, add it
    if args.comment:
        add_comment_to_card(
            key=key,
            token=token,
            card_id=card_info['id'],
            comment=args.comment
        )
        print("Comment added to the card.")

if __name__ == "__main__":
    main()
