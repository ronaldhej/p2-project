## About
This is just a small experiment to get to know the arcade game engine better, rough physics and collision are implemented.

### Features
- Drawing walls with a preview via left click
- Clearing walls with C
- Spawning people via right click
- Map boundaries
- The "people" will follow the cursor as best they can, there are some bugs though.

## Getting started
### Linux / OSX
Before trying to start the program or add packages, generate a virtual environment with `python -m venv venv` in the root folder.

Enter the virtual environment with the following command: `source venv/bin/activate` from within the root folder.

After this, run `pip install -r requirements.txt` to fetch the required packages.

To exit the virtual environment, type `deactivate`

### Windows
Same as for Linux / OSX with a few exceptions.

Generate a virtual environment with `python -m venv venv` in the root folder.

Enter the virtual environment by executing the batch file in the Scripts folder, or use the following command: `venv\Scripts\activate.bat`, you do not need to change directory.

The command line should now say `(venv)`, indicating that you are in a virtual environment.

After this, run `pip install -r requirements.txt` to fetch the required packages.

To exit the virtual environment, type `deactivate`

NOTE: You may need to reinstall the cffi package:
`pip install --upgrade --force-reinstall cffi`

## Running the Program
`python -R main.py` while in the virtual environment
