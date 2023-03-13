## About
This is just a small experiment to get to know the arcade game engine better, rough physics and collision is implemented.

### Features
- Drawing walls with a preview via left click
- Clearing walls with C
- Spawning people via right click
- Map boundaries
- The "people" will follow the cursor as best they can, there are some bugs though

## Getting started
### Linux / OSX
Before trying to start the program or add packages, generate a virtual environment with `python -m venv venv` in the root folder.

Enter the virtual environment with the following command: `source venv/bin/activate` from within the root folder.

After this, run `pip install -r requirements.txt` to fetch the required packages.

To exit the virtual environment, type `deactivate`

### Windows
No idea, I recommend doing the above steps with WSL

## Running the Program
`python -R main.py`