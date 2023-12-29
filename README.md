# MySQL to SQLite Data Transfer

This repository contains a Python script for transferring data from a MySQL database to a SQLite database.

## Prerequisites

- Python 3.6+
- MySQL Connector Python
- SQLite3
- python-dotenv
- simple-term-menu
- rich

## Installation

1. Clone this repository
2. Create Python virtual environment
3. Install the required packages
4. Set up environment variables

```bash
git clone https://github.com/Anzo52/mysql2sqlite3.git
cd mysql2sqlite3
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
python3 main.py
```

## License

This project is Licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
