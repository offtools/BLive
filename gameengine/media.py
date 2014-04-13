# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Script copyright (C) 2012 Thomas Achtner (offtools)

# --- import bge modules
import bge
from bge import texture
from bge import logic
import aud
from gameengine import error

# FIX: loop and in/outpoints

TEXTURE_STATES = {'PLAY', 'PAUSE', 'STOP'}

class _BasePlayer(object):
    '''
        _BasePlayer (base class for bge.texture wrapper modules)
    '''
    def __init__(self, obname, imgname):
        if obname is None or imgname is None:
            raise ValueError('no object name or image name given')
        if not obname in logic.getCurrentScene().objects:
            raise IndexError('requested object not found')

        self.__state = 'STOP'
        gameobject = logic.getCurrentScene().objects[obname]

        # -- Get the material that is using our texture
        img = "IM{0}".format(imgname)
        matID = texture.materialID(gameobject, img)

        # -- Create the video texture
        self._texture = texture.Texture(gameobject, matID)

    def refresh(self, play):
        #self._texture.refresh(play)
        pass

class FFmpegPlayer(_BasePlayer):
    '''
        FFmpegPlayer (bge.texture Movie Playback)
        param: obname (name of game object used for playback)
        type: string
        param: imgname (name of the texture image)
        type: string
        param: filename (file used for playback)
        type: string
        param: audio (decode audio)
        type: bool
        param: inp (movie inpoint in seconds)
        type: float
        param: outp (movie outpoint in seconds)
        type: float
        param: loop (loop movie playback)
        type: bool
        param: preseek (preseek seconds)
        type: int
        param: deinterlace (deinterlace movie)
        type: bool
    '''
    def __init__(self, obname=None, imgname=None, filename=None, audio=True, inp=0.0, outp=0.0, loop=False, preseek=0, deinterlace=False):
        super(FFmpegPlayer, self).__init__(obname, imgname)

        self.__file = None
        self.__hassound = False
        self.__audio = audio
        self.__sound = None
        self.__handle = None
        self.__state = 'STOP'

        # --- set source
        self.source = filename
        self.range = (inp, outp)
        self.preseek = preseek
        self.loop = loop

    def __del__(self):
        if self.__hassound:
            self.__handle.stop()
            self.__hassound = False
            self.__sound = None
            self.__handle = None

    def refresh(self, play=True):
        if hasattr(self, "_texture"):
            if self.__hassound == True:
                self._texture.refresh(play, self.range[0]+self.__handle.position)
            else:
                self._texture.refresh(play)

    def get_source(self):
        return self.__file

    def setup_audio(self):
        if self.__audio:
            try:
                if self.__hassound is True:
                    self.__handle.stop()
                self.__sound = aud.Factory(self.__file)
                device = aud.device()
                self.__handle = device.play(self.__sound)
                self.__handle.loop_count = -1
                self.__hassound = True
            except aud.error as err:
                print('Error: MoviePlayer.load - no sound available\n', err)
                self.__hassound = None
                self.__sound = None
                self.__audio = False
        else:
            if self.__handle:
                self.__handle.stop()
            self.__hassound = None
            self.__sound = None


    def set_source(self, _file):
        self.__file = _file
        if self.state != 'STOP':
            self.state = 'STOP'

        self._texture.source = texture.VideoFFmpeg(_file)

        if not self._texture.source:
            self.__file = None
            self.__audio = None
            return

        # --- configure and play audio stream
        self.setup_audio()

        # -- scale the video
        self._texture.source.scale = True

        # -- play the video
        self.state = 'PLAY'

    def get_state(self):
        return self.__state

    def set_state(self, state):
        if state == 'PLAY':
            if self.state == 'PAUSE':
                if self.__hassound:
                    self.__handle.resume()
            if self.state == 'STOP' and self.__hassound:
                self.__handle.resume()
            self._texture.source.play()

        elif state == 'PAUSE':
            self._texture.source.pause()
            if self.__hassound:
                self.__handle.pause()

        elif state == 'STOP':
            self._texture.source.stop()
            if self.__hassound:
                self.__handle.pause()
                self.__handle.position = 0
        else:
            return

        self.__state = state

    def get_loop(self):
        return self._texture.source.repeat

    def set_loop(self, loop):
        if loop is True:
            self._texture.source.repeat = -1
        else:
            self._texture.source.repeat = 0
        if self.__hassound:
            self.__handle.loop_count = self._texture.source.repeat

    def get_preseek(self):
        return self._texture.source.preseek

    def set_preseek(self, preseek):
        self._texture.source.preseek = preseek

    def get_range(self):
        return self._texture.source.range

    def set_range(self, seq):
        inp = seq[0]
        outp = seq[1]

        if inp > 0 and inp < outp:
            if self._texture.source:
                self._texture.source.range = (inp, outp)
            if self.__audio and self.__hassound:
                self.__handle.stop()
                self.__sound = self.__sound.limit(inp, outp)
                device = aud.device()
                self.__handle = device.play(self.__sound)

    def get_audio(self):
        return self.__audio

    def set_audio(self, audio):
        self.__audio = bool(audio)
        self.setup_audio()

    def get_volume(self):
        if self.__hassound:
            return self.__sound.volume
        else:
            return -1.0

    def set_volume(self, volume):
        if self.__hassound:
            self.__handle.volume = volume

    source = property(get_source, set_source)
    range = property(get_range, set_range)
    state = property(get_state, set_state)
    loop = property(get_loop, set_loop)
    audio = property(get_audio, set_audio)
    volume = property(get_volume, set_volume)

class CameraPlayer(_BasePlayer):
    def __init__(self, obname=None, imgname=None, device="/dev/video0", width=720, height=576, rate=0.0, deinterlace=True):
        super().__init__(obname, imgname)

        print("CameraPlayer: ", device, width, height, rate, deinterlace)

        self.__rate = rate
        self.__width = width
        self.__height = height
        self.__device = device
        self.__state = 'STOP'

        self.source = self.__device
        self.deinterlace = deinterlace
        self.state = 'PLAY'

    def get_state(self):
        return self.__state

    def set_state(self, state):
        if state == 'PLAY':
            self._texture.source.play()
        elif state == 'PAUSE':
            self._texture.source.pause()
        elif state == 'STOP':
            self._texture.source.stop()
        else:
            return
        self.__state = state

    def get_device(self):
        return self.__device

    def set_device(self, device):
        self.__device = device
        if self.state != 'STOP':
            self.state = 'STOP'

        self._texture.source = texture.VideoFFmpeg(self.__device, 1, self.__rate, self.__width, self.__height)

        if not self._texture.source:
            print("Error! inopening Camera")
            return

        # -- scale the video
        self._texture.source.scale = True

    def get_deinterlace(self):
        if hasattr(self._texture, "source"):
            return self._texture.source.deinterlace
        else:
            return False

    def set_deinterlace(self, deinterlace):
        if hasattr(self._texture, "source"):
            self._texture.source.deinterlace = deinterlace

    def refresh(self, play=True):
        if hasattr(self._texture, "source"):
            self._texture.refresh(play)

    source = property(get_device, set_device)
    state = property(get_state, set_state)
    deinterlace = property(get_deinterlace, set_deinterlace)


def openMovie(path, args, types, source, user_data):
    obname = args[0]
    imgname = args[1]
    filename = args[2]
    audio = bool(args[3])
    inp = args[4]
    outp = args[5]
    loop= args[6]
    preseek = args[7]
    deinterlace = bool(args[8])

    if imgname in bge.logic.media:
        del bge.logic.media[imgname]
    try:
        bge.logic.media[imgname] = FFmpegPlayer(obname=obname,
                                                imgname=imgname,
                                                filename=filename,
                                                audio=audio,
                                                inp=inp,
                                                outp=outp,
                                                loop=loop,
                                                preseek=preseek,
                                                deinterlace=deinterlace)
    except (TypeError, RuntimeError) as err:
        print("err in videotexture.open: ", err)

def enableAudio(path, args, types, source, user_data):
    imgname = args[0]
    audio = bool(args[1])

    if imgname in bge.logic.media:
        pl =  bge.logic.media[imgname]
        if isinstance(pl, FFmpegPlayer):
            pl.audio = audio

def enableLoop(path, args, types, source, user_data):
    imgname = args[0]
    loop = args[1]

    if imgname in bge.logic.media:
        pl =  bge.logic.media[imgname]
        if isinstance(pl, FFmpegPlayer):
            pl.loop = loop

def setRange(path, args, types, source, user_data):
    imgname = args[0]
    inp = args[1]
    outp = args[2]

    if imgname in bge.logic.media:
        pl =  bge.logic.media[imgname]
        if isinstance(pl, FFmpegPlayer):
            pl.range = (inp, outp)


def audioVolume(path, args, types, source, user_data):
    imgname = args[0]
    volume = args[1]

    if imgname in bge.logic.media:
        pl =  bge.logic.media[imgname]
        if isinstance(pl, FFmpegPlayer):
            pl.volume = volume

def openCamera(path, args, types, source, user_data):
    obname = args[0]
    imgname = args[1]
    device = args[2]
    width = args[3]
    height = args[4]
    rate = args[5]
    deinterlace = bool(args[6])

    if imgname in bge.logic.media:
        del bge.logic.media[imgname]
    try:
        bge.logic.media[imgname] = CameraPlayer(obname, imgname, device, width, height, rate, deinterlace)
    except TypeError as err:
        print("Error in VideoTexture.cb_camera_open: ", err)

def play(path, args, types, source, user_data):
    imgname = args[0]
    if imgname in bge.logic.media:
        bge.logic.media[imgname].state = 'PLAY'

def pause(path, args, types, source, user_data):
    imgname = args[0]
    if imgname in bge.logic.media:
        bge.logic.media[imgname].state = 'PAUSE'

def stop(path, args, types, source, user_data):
    imgname = args[0]
    if imgname in bge.logic.media:
        bge.logic.media[imgname].state = 'STOP'

def close(path, args, types, source, user_data):
    imgname = args[0]
    if imgname in bge.logic.media:
        del bge.logic.media[imgname]

def deinterlace(path, args, types, source, user_data):
    imgname = args[0]
    deinterlace = args[1]
    if imgname in bge.logic.media:
        bge.logic.media[imgname].deinterlace = True

def update():
    for key in bge.logic.media.keys():
        bge.logic.media[key].refresh()

def register():
    # adding dict for dynamic textures, keys are Image Names
    bge.logic.media = dict()

    try:
        #
        # --- Videotexture Message handlers
        #

        # --- VideoTexture Movie:
        # --- path "/texture/movie/open"
        #
        # --- Videotexture - open a Movie:
        # --- object name (string)
        # --- image name (string)
        # --- filepath (string)
        # --- sound (bool)
        # --- inpoint (float)
        # --- outpoint ()
        # --- loop (bool)
        # --- preseek (int)
        # --- deinterlace (bool)
        bge.logic.server.add_method("/bge/logic/media/openMovie", "sssiffiii", openMovie)

        # --- Videotexture - set playback range:
        # --- image name (string)
        # --- inpoint (float)
        # --- outpoint (float)
        bge.logic.server.add_method("/bge/logic/media/setRange", "sff", setRange)

        # --- Videotexture - enable audio:
        # --- image name (string)
        # --- audio (bool)
        bge.logic.server.add_method("/bge/logic/media/enableAudio", "si", enableAudio)

        # --- Videotexture - loop playback:
        # --- image name (string)
        # --- loop (bool)
        bge.logic.server.add_method("/bge/logic/media/enableLoop", "si", enableLoop)

        # --- Videotexture - audio volume:
        # --- image name (string)
        # --- volume (float)
        bge.logic.server.add_method("/bge/logic/media/audioVolume", "sf", audioVolume)

        # --- VideoTexture Camera:
        # --- path "/texture/camera/open"
        #
        # --- Videotexture - open a camera device:
        # --- object name (string)
        # --- image name (string)
        # --- device (string)
        # --- width (int)
        # --- height (int)
        # --- rate (float)
        # --- deinterlace (bool)
        bge.logic.server.add_method("/bge/logic/media/openCamera", "sssiifi", openCamera)

        #
        # --- Videotexture - Status ---
        #
        # --- Videotexture - close and reset texture:
        # --- image name (string)
        bge.logic.server.add_method("/bge/logic/media/close", "s", close)

        # --- Videotexture - state is play:
        # --- image name (string)
        bge.logic.server.add_method("/bge/logic/media/play", "s", play)

        # --- Videotexture - state is pause:
        # --- image name (string)
        bge.logic.server.add_method("/bge/logic/media/pause", "s", pause)

        # --- Videotexture - state is stop:
        # --- image name (string)
        bge.logic.server.add_method("/bge/logic/media/stop", "s", stop)

        #
        # --- Filter ---
        #
        # --- Videotexture - deinterlace texture:
        # --- image name (string)
        bge.logic.server.add_method("/bge/logic/media/deinterlace", "s", deinterlace)

        # add update method to server loop
        bge.logic.server.handler.append(update)

    except (AttributeError, ValueError) as err:
        print("SERVER: could not register /bge/logic/media callbacks - ", err)
