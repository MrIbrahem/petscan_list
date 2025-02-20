# PetScan List Application

A Flask web application that helps manage and process PetScan lists for Wikipedia articles.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Wikipedia account with bot password

## Installation

1. Clone this repository:
```bash
git clone https://github.com/MrIbrahem/petscan_list.git
cd petscan_list
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a bot password for your Wikipedia account:
   - Go to Special:BotPasswords on Wikipedia (https://ar.wikipedia.org/wiki/Special:BotPasswords)
   - Create a new bot password with necessary permissions

2. Set up your credentials:
   - Create a file `confs/user.ini` with the following content:
   ```ini
   botusername = "YOUR_USERNAME"
   botpassword = "YOUR_BOT_PASSWORD"
   ```
   Replace `YOUR_USERNAME` with your Wikipedia username and `YOUR_BOT_PASSWORD` with your bot password.

## Running the Application

You can run this application in two different ways:

### 1. Web Interface (Flask Application)

Start the Flask development server:
```bash
python app.py
```

Then open your web browser and navigate to:
```
http://localhost:5000
```

The web interface allows you to:
- Process individual Wikipedia articles
- View results directly in your browser
- Interactive usage with immediate feedback

### 2. Bot Mode (Automated Processing)

Run the bot script to automatically process multiple pages:
```bash
python bot.py
```

The bot mode:
- Automatically searches for pages with "petscan list" template
- Processes all found pages in batch
- Works specifically with Arabic Wikipedia
- Runs continuously without manual intervention

## Project Structure

- `app.py` - Main Flask web application file
- `bot.py` - Automated bot script for batch processing
- `PetScanList/` - Core functionality modules
- `templates/` - HTML templates
- `static/` - Static files (JavaScript, CSS)
- `confs/` - Configuration files including Wikipedia credentials

## Scripts

- `runall.sh` - Script to run all components
- `update.sh` - Script for updates

## Usage

### Web Interface
1. Navigate to the homepage at `http://localhost:5000`
2. Enter the Wikipedia article title
3. The application will process the PetScan list and display the results

### Bot Mode
1. Make sure your credentials are properly configured
2. Run `python bot.py`
3. The bot will automatically:
   - Find pages with "petscan list" template
   - Process each page
   - Show progress in the terminal

## Development

The application runs in debug mode by default when running locally, which provides detailed error messages and automatic reloading when code changes are made.


## Template Format Params

These parameters are optional:

- **`|_result_=table`**:  to display the result in wikitable.
- **`|_line_format_=`**: Table to modify the value format, example:
  ```wiki
  |_line_format_ = # {{user:Mr. Ibrahem/link|$1}}


## Default Values
- **`|output_limit = 3000`**: Maximum number of results to display.
