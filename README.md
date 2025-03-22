# Dolphin
An HTTP remote access tool (RAT)

## Features

- Obfuscated and polymorphic initial payload
- Easy payload generation for different platforms
- Modular payloads

## Planned features

- Staging
- Persistence
- Interactive shell
- File manager
- Multiple included modules
- Client updates

## Installation and usage

Install docker: <https://docs.docker.com/engine/install/>

Install python requirements:
`pip3 install -r requirements.txt`

Apply migrations:
`python manage.py migrate`

Run the server:
`python manage.py runserver`