<h2 align="center">PyMQ!</h2>

### Simple Messaging Queue in Python

PyMQ! is a simple messaging queue developed in Python.

[![Python Version](https://img.shields.io/badge/python-3.9+-FF8400)](https://www.python.org) 
[![License](https://img.shields.io/badge/license-GPLv3-FF8400.svg)](https://github.com/blacklanternsecurity/bbot/blob/dev/LICENSE)

## Features

- FIFO messaging queue
- Adressed messages with sender and recipient
- TCP connection to push/retrieve messages
- Token authentication
- In memory cache (with size limit)
- Storage in PostgreSQL database 

## TODO

- Change to a nonblocking socket (currently you cant ctrl+c to exit lol)
- Make it async
- Create API routes to push/retrieve messages
- Create cleaning routines for DB

## Installation and usage

### Installation
 
Installing PyQ! is as simple as cloning and running a Python project on any OS. It requires just a terminal and Python 3.9+. 

```bash
git clone https://github.com/dbx0/pymq
cd pymq/
pip install -r requirements.txt
```

### Setup

Use the [schema.sql](database/schema.sql) file to create your schema in a PostgreSQL database.

Create your own `.env` file based on `.env.example` and add your settings.

To get started right away, just run it with Python.

```bash
python3 run.py
```

### Usage

The TCP listener is waiting for your message through socket in the selected port. 

You can check some Python code examples inside the [examples](examples/) folder.
The conversation should go as below:

#### Authentication

To start a conversation, your first message will be your authentication token. You can get two responses in this case.

Failed authentication:
```
client: <authentication token>
server: "Invalid token"
```
Success authentication:
```
client: <authentication token>
server: "Authentication successful"
```

#### Retrieving data

The `get_message` command will retrieve messages to the recipient based on the token provided in the authentication.

Empty queue:
```
client: get_message
server: "No messages available"
```

Getting multiple messages from queue.
```
client: get_message
server: <message body>
client: get_message
server: <message body>
...
client: get_message
server: "No messages available"
```

#### Pushing data

The `push_message` command will start a conversation to get your message. It requires the recipient name as a parameter.

```
client: push_message <recipient_name>
server: "Waiting message"
client: <message body>
server: "Message added to queue
```

## Feedback

If you have any feedback, please reach out to me at X [@malwarebx0](https://x.com/malwarebx0)

## License

[GPL3.0](LICENSE)

