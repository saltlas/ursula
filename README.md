# Voice Input Module
This branch contains the voice input module as part of the multi-modal input project.

1. [Setup](#setup)
	1. [Requirements](#requirements)
	2. [Google Cloud API](#google-cloud-api)
	3. [config.json](#configjson)
2. [Common Issues on Lab Machines](#common-issues-on-lab-machines)
	1. [RabbitMQ](#rabbitmq)
	2. [Unity Hub won't open the project](#unity-hub-wont-open-the-project)


## Setup

### Requirements

The `requirements.txt` file should have all python libraries needed to run the project. Run `pip install -r requirements.txt` from command line.

### Google Cloud API

You will need to create an account on [Google Cloud](https://cloud.google.com/) and recieve your free trial credits. If you have already used up all of your free trial credits, you will need to set up payment with Google Cloud for this module to work.

Once done, you will need to create a project using [Cloud Speech-to-Text API](https://console.cloud.google.com/apis/api/speech.googleapis.com/), and then [use those credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc) to set up Google Cloud CLI on your machine. Once done, `pip install google-cloud-speech` and run `gcloud auth application-default login` from the project directory. If the project gives you errors about permissions and credentials when it tries to access Google Cloud API, you've done this step wrong.


### config.json

Add a file named `config.json` to the root directory containing the following fields:

- phrases 

A list of phrases to bias the transcription model towards. This would usually be a list of the commands you expect to need recognised.

Example: \["select select_word", "deselect select_word", "rotate select_word", "scale select_word"\]\*

\* Note that "select_word" is representative of a wildcard, in this case "that" or "this", so both "select that" and "select this" will be added. To see existing wildcards or implement your own, see `utils/wildcards.py`.

- project_number

The 12-digit ID number corresponding to the Google Cloud project you set up in the previous step. This should be available on the project page for your project.

Example: 123456789876

- project_id

The name that represents your project on the project page. This should be available in the same place the project number is.

Example: "lava-street-101010"

- language-code

A BCP-47 language tag telling the speech to text model which language and accent will be spoken in. [Here](https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages) is a list of supported languages. Note that the "en-NZ" model has fewer features than most, so I've been using "en-AU" for my own accent and it has still been working well.

Example: "en-AU"

- transcription_mode

Either "interim" or "stable". Interim mode means interim results from the transcription API will be processed, not just final results, which improves speed but may worsen accuracy. Stable mode means only final results will be considered, improving accuracy and worsening speed of sending words to the input manager.

Example: "stable"

- websocket_port

The port the input manager will be listening on for websocket messages from this module.

Example: "ws://localhost:8001"

- wrong_words_allowed

The number of wrong word you want to allow between keywords of a command (e.g. given a command "put that there", "put that over there" would not work with wrong_words_allowed = 0 but will work with wrong_words_allowed = 1)

example: 1

**Example `config.json`:**

```
{
"phrases": ["select select_word", "deselect select_word", "rotate select_word", "scale select_word"],
"project_number": "123456789876",
"project_id": "lava-street-101010",
"language_code": "en-AU",
"transcription_mode": "stable",
"websocket_port": "ws://localhost:8001",
"wrong_words_allowed": 1
}
```


## Common issues on lab machines

### RabbitMQ

Installing RabbitMQ as per the instructions on their website, with their installer, will give an error on lab machines (Exited with exit code 1, or something similar). Install it anyway, get that error, and then solve it using the following steps:

- Create a new folder in an accessible area of the file system - I created a folder at `C:\Users\[MY_USER]\rabbitmq`, with MY_USER being my UID. Let the path of this folder be YOUR_FOLDER_PATH for step 3.

- Go to `C:\Program Files\RabbitMQ Server\rabbitmq_server-3.12.11\sbin` and create a new file named `start-rabbit.bat`. You may have issues creating a file within the directory directly, so you can also create it elsewhere and then move it into the directory.

- In `start-rabbit.bat`, put the following two lines:

`set HOMEDRIVE=YOUR_FOLDER_PATH` (replace YOUR_FOLDER_PATH with the path of the folder you created)

`rabbitmq-plugins.bat enable rabbitmq_management`

- Open command prompt as administrator and navigate to `C:\Program Files\RabbitMQ Server\rabbitmq_server-3.12.11\sbin`

- Run `start-rabbit` from CLI

- Run `rabbitmq-service start` from CLI

- The server should be accessible on `http://localhost:15672`

If this doesn't work, try running `rabbitmq-service install` and then `rabbitmq-service start`

### Unity Hub won't open the project
If Unity Hub is just restarting itself whenever you try to open a project, make sure the project is not on your `P:`. If it is, move it to `C:`.
