#!/bin/bash

# script to do local development
# activates the virtualenv
# re-install everything in dev-requirements.txt
# starts redis, DB
# starts the development server
# autopep8 on the code when running


# starts the server
uvicorn app.main:app --reload