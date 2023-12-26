<img width="1404" alt="Skjermbilde 2023-12-26 kl  21 47 21" src="https://github.com/KhalilIbrahimm/Super-Dashboard-Exploratory-Data-Analysis-/assets/118692114/444cf728-688e-4a68-9951-5dde49260e0b">
<img width="1435" alt="Skjermbilde 2023-12-26 kl  21 48 22" src="https://github.com/KhalilIbrahimm/Super-Dashboard-Exploratory-Data-Analysis-/assets/118692114/658eb61e-db66-47ef-9ee9-d0675f2d29a7">

<img width="1434" alt="Skjermbilde 2023-12-26 kl  21 48 41" src="https://github.com/KhalilIbrahimm/Super-Dashboard-Exploratory-Data-Analysis-/assets/118692114/d373dd1e-b8b2-4ae7-8a78-169408c5820e">
<img width="1250" alt="Skjermbilde 2023-12-26 kl  21 49 23" src="https://github.com/KhalilIbrahimm/Super-Dashboard-Exploratory-Data-Analysis-/assets/118692114/9ddff4dc-c305-4f6a-83fc-cfe647df88b7">

## Create a Virtual Environment:
  1. Open your terminal or command prompt.
  2. Navigate to the project directory where you want to set up the virtual environment.
  3. Run the following command to create a new virtual environment:
```bash
python3 -m venv venv
```
  - Here, venv is the name of the directory that will contain the virtual environment. You can replace the second venv with any name you prefer for your virtual environment.

## Activate the Virtual Environment:
- On Windows, run:
```bash
venv\Scripts\activate
```
- On macOS and Linux, run:
```bash
source venv/bin/activate
```

Once the virtual environment is activated, you'll typically see its name in your terminal prompt, indicating that it is currently active.

## Install Dependencies from requirements.txt:
- Ensure you have a requirements.txt file in your current directory.
- Run the following command to install the dependencies:
```bash
pip install -r requirements.txt
```
- This will install all the packages and their respective versions defined in the requirements.txt file into the virtual environment.

## Verify Installed Packages:
- To check that the correct packages have been installed, you can run:
```bash
pip freeze
```
- This will list all the installed packages and their versions.

## Deactivate the Virtual Environment:
- When you're done working in the virtual environment, you can deactivate it by running:
```bash
deactivate
```

# Reminder comment: the script is to be run with 'streamlit run main.py' in the terminal!
