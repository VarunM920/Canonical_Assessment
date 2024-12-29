To run the api to the trello board, first ensure that you have a Trello board created and it's ID. Make sure you also have at least one list created on the board.
The command to run the script will look something like this:
python trello_add_card.py --board-id "Your Board ID" --list-name "Example List" --name "Example Name" --desc "Example Desc" --labels Test1 Test2

This should create a card in the board in the appropriate list with the appropriate name, description, and labels. Please note that the script will throw an error if it cannot find the specified board id, list name, or labels
For future improvements, possibly I could add a label system that was using just color instead of a name, since the default value for a label name is empty, but it will always have a color that you can label it.
This task took roughly 3 hours.

I used ChatGPT initially to help me plan out what I would do to solve this, including what Trello was (I had never used it before) the setup with getting a Trello key and token, and how I might design the script to enable the functionality.
