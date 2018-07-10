import sys
import os
import pyaudio
import struct
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), './python'))

import porcupine

audio_stream = None
handle = None
pa = None

try:
    library_path = './lib/mac/x86_64/libpv_porcupine.dylib'
    model_file_path = './lib/common/porcupine_params.pv'
    keyword_file_paths = ['./resources/blackberry_mac.ppn']
    num_keywords = len(keyword_file_paths)
    sensitivities = [0.2]
    handle = porcupine.Porcupine(library_path,
                                 model_file_path,
                                 keyword_file_paths=keyword_file_paths,
                                 sensitivities=sensitivities)

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
            rate=handle.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=handle.frame_length)
    print('Listening for keyword blackberry...')

    while True:
        pcm = audio_stream.read(handle.frame_length)
        pcm = struct.unpack_from("h" * handle.frame_length, pcm)

        result = handle.process(pcm)
        if num_keywords == 1 and result:
            print('[%s] detected keyword' % str(datetime.now()))
        elif num_keywords > 1 and result >= 0:
            print('[%s] detected keyword #%d' % (str(datetime.now()), result))

except KeyboardInterrupt:
    print('stopping ...')
finally:
    if handle is not None:
        handle.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
        pa.terminate()


_AUDIO_DEVICE_INFO_KEYS = ['index',
                           'name',
                           'defaultSampleRate',
                           'maxInputChannels']
