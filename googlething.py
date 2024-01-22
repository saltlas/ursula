# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START speech_transcribe_streaming_mic]

import queue
import re
import sys

from google.cloud import speech

import pyaudio
import json

import processcommands
from utils import phrase_utils, time_utils



# Audio recording parameters
STREAMING_LIMIT = 300000  # 5 minutes
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class ResumableMicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(
        self: object,
        rate: int,
        chunk_size: int,
    ) -> None:
        """Creates a resumable microphone stream.

        Args:
        self: The class instance.
        rate: The audio file's sampling rate.
        chunk_size: The audio file's chunk size.

        returns: None
        """
        self._rate = rate
        self.chunk_size = chunk_size
        self._num_channels = 1
        self._buff = queue.Queue()
        self.closed = True
        self.start_time = time_utils.get_time_milliseconds()
        self.restart_counter = 0
        self.audio_input = []
        self.last_audio_input = []
        self.result_end_time = 0
        self.is_final_end_time = 0
        self.final_request_end_time = 0
        self.bridging_offset = 0
        self.last_transcript_was_final = False
        self.new_stream = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=self._num_channels,
            rate=self._rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

    def __enter__(self: object) -> object:
        """Opens the stream.

        Args:
        self: The class instance.

        returns: None
        """
        self.closed = False
        return self

    def __exit__(
        self: object,
        type: object,
        value: object,
        traceback: object,
    ) -> object:
        """Closes the stream and releases resources.

        Args:
        self: The class instance.
        type: The exception type.
        value: The exception value.
        traceback: The exception traceback.

        returns: None
        """
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(
        self: object,
        in_data: object,
        *args: object,
        **kwargs: object,
    ) -> object:
        """Continuously collect data from the audio stream, into the buffer.

        Args:
        self: The class instance.
        in_data: The audio data as a bytes object.
        args: Additional arguments.
        kwargs: Additional arguments.

        returns: None
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self: object) -> object:
        """Stream Audio from microphone to API and to local buffer

        Args:
            self: The class instance.

        returns:
            The data from the audio stream.
        """
        while not self.closed:
            data = []

            if self.new_stream and self.last_audio_input:
                chunk_time = STREAMING_LIMIT / len(self.last_audio_input)

                if chunk_time != 0:
                    if self.bridging_offset < 0:
                        self.bridging_offset = 0

                    if self.bridging_offset > self.final_request_end_time:
                        self.bridging_offset = self.final_request_end_time

                    chunks_from_ms = round(
                        (self.final_request_end_time - self.bridging_offset)
                        / chunk_time
                    )

                    self.bridging_offset = round(
                        (len(self.last_audio_input) - chunks_from_ms) * chunk_time
                    )

                    for i in range(chunks_from_ms, len(self.last_audio_input)):
                        data.append(self.last_audio_input[i])

                self.new_stream = False

            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            self.audio_input.append(chunk)

            if chunk is None:
                return
            data.append(chunk)
            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)

                    if chunk is None:
                        return
                    data.append(chunk)
                    self.audio_input.append(chunk)

                except queue.Empty:
                    break

            yield b"".join(data)



def listen_print_loop(processor: object, mode: object, responses: object, stream: object) -> str:
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.

    Args:
        responses: List of server responses

    Returns:
        The transcribed text.
    """
    num_chars_printed = 0


    for response in responses:
        if time_utils.get_time_milliseconds() - stream.start_time > STREAMING_LIMIT:
            stream.start_time = time_utils.get_time_milliseconds()
            num_chars_printed = 0
            print("RESTARTING")
            break

        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript


        if mode == "interim":
            if (result.stability == 0.0 or result.stability > 0.7) and num_chars_printed < len(transcript):

                for word in transcript[num_chars_printed:].split():
                  # print("!", word, datetime.datetime.now() - datetime.timedelta(seconds=1)) # roughly a second delay in timestamp accuracy - may vary machine to machine
                    print(word)
                    processor.process_commands(word, time_utils.add_offset(-1, time_utils.get_time(), "seconds"))
                num_chars_printed = len(transcript)

                    
        result_seconds = 0
        result_micros = 0

        if result.result_end_time.seconds:
            result_seconds = result.result_end_time.seconds

        if result.result_end_time.microseconds:
            result_micros = result.result_end_time.microseconds

        stream.result_end_time = int((result_seconds * 1000) + (result_micros / 1000))

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        #overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            #sys.stdout.write(transcript + overwrite_chars + "\r")
            #sys.stdout.flush()

            #num_chars_printed = len(transcript)
            if mode == "interim" and result.stability > 0.7:
                stream.is_final_end_time = stream.result_end_time
                stream.last_transcript_was_final = True
            else:
                stream.last_transcript_was_final = False

        else:
            #print(transcript + overwrite_chars)
            if mode == "stable":

                for word_info in result.alternatives[0].words:
                    end_time = time_utils.convert_timedelta_to_milliseconds(word_info.end_time) 
                    timestamp = time_utils.add_offset(end_time, processor.init_time)
                    print(word_info.word)
                    processor.process_commands(word_info.word, timestamp)


            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.

            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                processor.close()
                break

            num_chars_printed = 0


    return transcript


def main() -> None:
    """Transcribe speech from audio file."""
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    config_file_path = "config.json"

    with open(config_file_path, "r") as config_file:
        project_config = json.load(config_file)
    project_id = project_config["project_id"]
    project_number = project_config["project_number"]
    phrases = project_config["phrases"]
    transcription_mode = project_config["transcription_mode"]
    language_code = project_config["language_code"]  # a BCP-47 language tag
    wildcards = project_config["wildcards"]


    # Create the adaptation client
    adaptation_client = speech.AdaptationClient()
    phrase_set_response = phrase_utils.init_PhraseSet(adaptation_client, phrases, project_number, project_id, wildcards)
    phrase_set_name = phrase_set_response.name
    speech_adaptation = speech.SpeechAdaptation(phrase_set_references=[phrase_set_name])


    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        adaptation=speech_adaptation,
        enable_word_time_offsets=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True,
    )

    mic_manager = ResumableMicrophoneStream(RATE, CHUNK)


    command_processor = None

    with mic_manager as stream:

        while not stream.closed:


            stream.audio_input = []
            audio_generator = stream.generator()

            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            init_time = time_utils.get_time()
            print("!!", init_time)
            if not command_processor:
                command_processor = processcommands.CommandProcessor(init_time)
            else:
                command_processor.init_time = init_time

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            listen_print_loop(command_processor, transcription_mode, responses, stream)

            if stream.result_end_time > 0:
                stream.final_request_end_time = stream.is_final_end_time
            stream.result_end_time = 0
            stream.last_audio_input = []
            stream.last_audio_input = stream.audio_input
            stream.audio_input = []
            stream.restart_counter = stream.restart_counter + 1

            stream.new_stream = True







if __name__ == "__main__":
    main()
# [END speech_transcribe_streaming_mic]