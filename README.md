<h1 align="center">
    <img src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/letto.png" width="300" alt="Letto">
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
  <a href="https://www.mongodb.com">
    <img src="https://img.shields.io/badge/-MongoDB-13aa52?style=flat-square&logo=mongodb&logoColor=white)" alt="mongodb" style="height: 20px;">
  </a>
</h4>

<p align="center">
  <img src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/00.png" width="100%" alt="Letto">
</p>


## Introduction

`Letto` is a Python-based command-line tool designed to streamline email list processing and personalized email delivery. It helps you process multiple email files, remove duplicate and invalid addresses, organize recipients into manageable batches, and automate personalized email sending — all through a simple, menu-driven interface.

Designed to reduce manual work and make email workflows more efficient, letting your team focus on what matters most    ദ്ദി˙∇˙)ว.

<details open>
<summary>
  What Letto offers
</summary> <br/>

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/01.png" alt="automation"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/04.png" alt="data export"/>
</p>

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/03.png" alt="personalization"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/02.png" alt="database"/>
</p> 

</details>

## Features 

- **Bulk Email Import** ~ Import participant email addresses directly from Excel spreadsheets (.xlsx) and process them through a unified workflow.
- **Automated Email Cleaning** ~ Automatically identify invalid email formats and remove duplicate entries to maintain cleaner mailing lists.
- **Cross-Event Data Aggregation** ~ Combine email records from multiple events into a single dataset while identifying and removing duplicates across events.
- **Centralized Database Management** ~ Store raw email records, cleaned datasets, and processed data chunks in MongoDB for organized data management.
- **Automated Data Chunking** ~ Organize processed email addresses into manageable data chunks based on selected events.
- **Flexible Data Export** ~ Generate files (.txt) from selected data chunks with a customizable number of email addresses per line, ready for direct use in email BCC fields.
- **Personalized Certificate Distribution** ~ Automatically match recipients with their corresponding files (eg. certificate) and distribute them through email attachments.
- **Interactive CLI Interface** ~ Navigate Letto's features through an interactive terminal menu with keyboard-based selection.
- **Event & Dataset Management** ~ Create, view, and delete event records and processed data chunks directly through the application.

<details closed>
<summary>
  Version 2 Major updates (•ᴗ•)
</summary>
<ul>
    <li>Integrated MongoDB database ( local | cloud ) support for easier data access and management.</li>
    <li>Introduced data chunking for more flexible email processing.</li>
    <li>Major improvement on terminal UI for a cleaner and more user-friendly experience.</li>
</ul>

</details> <br>

<details open>
<summary>
 See our features processing
</summary> <br />

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/videos/vid1.gif" alt="flawless processing"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/videos/vid2.gif" alt="efficient error handling"/>
</p>

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/videos/vid3.gif" alt="simple personalized files"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/videos/vid4.gif" alt="sending personalized mails"/>
</p>

<p align="center">
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/videos/vid5.gif" alt="personlized mails"/>
&nbsp;
    <img width="49%" src="https://raw.githubusercontent.com/BoKu237723/Repo-Images/main/lettov2/videos/vid6.gif" alt="sending personalized mails"/>
</p>

</details>

## Folder Structure 
```
Letto/
├── .venv/                     # Virtual Enviroment
├── codes/                     # Main Folder
│   └── functions.py           # Processing functions 
│   └── personalized.py        # Personalized email sending functions
│   └── main.py                # Main file to process (main)
│   └── personalized/          # Personalized file folder
│       └── Certificates       # File list
│       └── emails.json        # Corresponding email and file
│              
├──  README.md                 # Summary of Letto
├── .env                       # Enviromental veriables
├── .gitignore                 # Gitignore file
├── .pyproject.toml            # Python Configuration File
├── .python-version            # Python Version
└── uv.lock                    # uv's lock file, contains libraries and such
```

## Database
Letto adopts MongoDB to store raw email records, cleaned datasets and processed email chunks. You can configure eiither a MongoDB Atlas cloud database or a local MonogoDB instance. Make sure the Database collection names are "Past-Cleaned", "Past-Raw" and "Processed-Chunks"


<details closed>
<summary>Document Structure</summary>

### 1. Processed-Chunks

Stores processed email datasets created by combining data from selected events.

| Field | Type | Description |
|---|---|---|
| `_id` | ObjectId | Automatically generated document identifier. |
| `Unique Name` | String | Unique name assigned to the chunk. |
| `Description` | String | Description of the chunk. |
| `Created Date` | String | Chunk creation date and time. |
| `Included Events` | Array | Events included in the chunk. |
| `Cleaned Mails` | Array | Final email dataset after processing. |
| `Duplicate Mails` | Array | Duplicate email addresses identified across selected events. |

### 2. Past-Raw

Stores original email data imported from each event before processing.

| Field | Type | Description |
|---|---|---|
| `_id` | ObjectId | Automatically generated document identifier. |
| Event Name | Object | Contains the original event data. |
| `datetime` | String | Import date and time. |
| `mails` | Array | Original email addresses extracted from the file. |

### 3. Past-Cleaned

Stores processed email data, including validation results and deduplication.

| Field | Type | Description |
|---|---|---|
| `_id` | ObjectId | Automatically generated document identifier. |
| Event Name | Object | Contains the cleaned event data. |
| `datetime` | String | Processing date and time. |
| `valid_mails` | Array | Email addresses that passed validation. |
| `invalid_mails` | Array | Email addresses that failed validation. |
| `unique_mails` | Array | Unique email addresses identified during processing. |
| `duplicate_mails` | Array | Duplicate email addresses detected during processing. |
| `final_mails` | Array | Final email dataset after cleaning and deduplication. |

</details>


## Usage

- `git clone https://github.com/BoKu237723/Letto`
-  Enter credentials in `.env` file
- `cd codes`
- `uv run main.py`

### Personalized Email Configuration

Place your attachment files in the `certificates` directory and configure `emails.json` in 'personalized' folder as follows:

```json
[
  {
    "email": "user1@example.com",
    "file": "cert1.pdf"
  }
]
```

## Optimal
### UV Installation

This project uses [`uv`](https://docs.astral.sh/uv/) for fast and reliable Python environment and dependency management.

1. Install `uv` by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).
2. Clone the repository: `https://github.com/BoKu237723/Letto.git`

3. Install the project dependencies (in terminal): `uv sync`

4. Run the application (in terminal): `uv run main.py`

**Note:** `uv sync` automatically creates a virtual environment and installs the dependencies defined in the project's configuration files.

## Contributors
[//]: contributor-faces
<a href="https://github.com/boku237723"><img src="https://github.com/BoKu237723.png?utm_source=chatgpt.com" title="BoKu" width="50" height="50"></a>

## License
This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Developers are free to use, modify, and distribute this software for personal or commercial purposes, provided that you comply with the license terms. The license also grants an express patent license and requires preservation of applicable copyright and license notices.

### Side Note 
I originally made this project to make my own workflow easier in a previous role, helped reduce ~80% of my manual work time. Later, I decided to keep updating it so that others with similar workflows could benefit from it too. So... some features might be a little specific to my own past experience and workflow.  (◜ᴗ◝)