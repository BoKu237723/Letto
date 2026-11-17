<!-- <h1 align="center">
    <img src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/letto.png" width="300" alt="Letto">
</h1>

<p align="center">
  <i align="center">Take the busywork out of your organization's email with Letto — So your team can focus on what matters most. 🚀</i>
</p>

<p align="center">
    <i align="center">Developed by BoKu</i>
</p>

<h4 align="center">
  <a href="https://docs.astral.sh/uv/">
    <img src="https://img.shields.io/badge/uv-Astral_DEVELOPMENT-DE5FE9?style=for-the-badge&logo=uv&logoColor=white" alt="uv by Astral" style="height: 20px;">
  </a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0">
    <img src="https://img.shields.io/badge/License-Apache 2.0-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="license" style="height: 20px;">
  </a>
  <br>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="python" style="height: 20px;">
  </a>
  <a href="https://git-scm.com/">
    <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="git" style="height: 20px;">
  </a>
  <a href="https://github.com/BoKu237723/Letto">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)" alt="github link" style="height: 20px;">
  </a>
</h4>

<p align="center">
  <img src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/00.png" width="100%" alt="Letto">
</p>


## Introduction

`Letto` is a Python-based command-line tool designed to streamline email list processing and personalized email delivery. It helps you process multiple email files, remove duplicate and invalid addresses, organize recipients into manageable batches, and automate personalized email sending — all through a simple, menu-driven interface.

Designed to reduce manual work and make email workflows more efficient, letting your team focus on what matters most 💻.

<details open>
<summary>
 What Letto offers
</summary> <br />

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/01.png" alt="01"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/04.png" alt="04"/>
</p>

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/03.png" alt="03"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/02.png" alt="02"/>
</p> 

</details>

## Features

- **Bulk Email Processing** — Import email addresses from multiple text files and consolidate them into a single workflow.
- **Intelligent Email Cleaning** — Automatically identify and remove duplicate and invalid email entries to maintain a cleaner mailing list.
- **Automated Email Chunking** — Split cleaned email lists into manageable batches based on your preferred batch size.
- **Personalized Email Automation** — Streamline personalized email delivery to reduce repetitive manual work.
- **Intelligent Error Handling** — Handle invalid inputs and unexpected interruptions gracefully alongisde with suggestions.
- **Built-in Help Menu** — Provide accessible instructions, usage guidance, and feature explanations on each features to help users navigate the application and understand its available commands.

<details open>
<summary>
 See our features
</summary> <br />

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/06.png" alt="flawless processing"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/05.png" alt="efficient error handling"/>
</p>

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/07.png" alt="simple personalized files"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/08.png" alt="sending personalized mails"/>
</p>

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/09.png" alt="personlized mails"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/letto/10.png" alt="sending personalized mails"/>
</p>

</details>

## Folder Structure 
```
Letto/
├── .venv/                     # Virtual Enviroment
│   └── unique-files/          # Personalized file folder
│       └── sample1.pdf
│       └── sample2.pdf
│       └── sample3.png
│       └── sample4.jpg
│              
├──  main.py                   # Main file to run Letto
├──  emails.json               # Personalized emails paired with unique files
├──  README.md                 # Summary of Letto
├── .env                       # Enviromental veriables
├── .gitignore                 # Gitignore file
├── .pyproject.toml            # Python Configuration File
├── .python-version            # Python Version
└── uv.lock                    # uv's lock file, contains libraries and such
```

## Usage

Run the program and enter the two-digit option number followed by the required input, if any.

### Available Options

| Option | Description | Usage Samples | Requirements |
|--------|-------------|-------|-------------|
| `01` | Process Emails | `01 file1.txt, file2.txt` | Provide one or more `.txt` files containing one email address per line. Separate multiple filenames with a comma and a space. |
| `02` | Remove Duplicate Emails | `02` | Require Option `01` to be executed first. |
| `03` | Remove Invalid Emails which are also not in valid domain names| `03` | Require Option `01` to be executed first. |
| `04` | Remove Duplicates and Invalid Emails | `04` | Require Option `01` to be executed first. |
| `05` | View Total Processed Emails | `05` | Require Option `01` to be executed first. |
| `06` | Split Emails into Chunks | `06 300` | Require Option `01` to be executed first. Specify the desired chunk size (eg. `06 300`). The output is saved to `chunks.txt`. |
| `07` | Send Personalized Emails with Attachments | `07` | Works independently of the email processing options. Place attachments in the `certificates` folder, configure `emails.json`, and set `MYEMAIL` and `MYPASSWORD` in your `.env` file. |
| `08` | Show Main Menu | `08` |  |
| `09` | Display Help Documentation | `09` |  |
| `10` | Exit the Program | `10` | Exits the program. You can also press `Ctrl+C` to interrupt execution. |

### Personalized Email Configuration

Place your attachment files in the `certificates` directory and configure `emails.json` as follows:

```json
[
  {
    "email": "user1@example.com",
    "file": "cert1.pdf"
  }
]
```

## Optimal
### Installation

This project uses [`uv`](https://docs.astral.sh/uv/) for fast and reliable Python environment and dependency management.

1. Install `uv` by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).
2. Clone the repository:

   ```bash
   git clone https://github.com/BoKu237723/Letto.git
   cd Letto
   ```

3. Install the project dependencies:

   ```bash
   uv sync
   ```

4. Run the application:

   ```bash
   uv run main.py
   ```

**Note:** `uv sync` automatically creates a virtual environment and installs the dependencies defined in the project's configuration files.

## Contributors
[//]: contributor-faces
<a href="https://github.com/boku237723@gmail.com"><img src="https://github.com/BoKu237723.png?utm_source=chatgpt.com" title="BoKu" width="50" height="50"></a>

## License
This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Developers are free to use, modify, and distribute this software for personal or commercial purposes, provided that you comply with the license terms. The license also grants an express patent license and requires preservation of applicable copyright and license notices. -->

On Maintainance! Will be fully updated in a few days!