from concurrent import futures
import traceback
import cv2
import time
from multiprocessing import Process, Array
from ctypes import c_bool, c_uint8
import numpy as np

from utils.utils import parse_options
from utils.constants import SIMU, TEST, PROD
from ai_simulator.ai_simulator import UnitySimulation
from ai_robot.ai_robots_handler import AIRobotsHandler
from reallife_video_source.ffmpeg_source import VideoSource
from computer_vision.remote_image_processor_client import (
    RemoteImageProcessorClient)


IMAGE_CHANNELS = 3


class Game:
    def __init__(self, mode, shared_array, shared_state, shared_data):
        print(f'Starting game in {mode}-mode')
        self._game_process = Process(
            target=self._start_game_loop,
            args=(mode, shared_array, shared_state, shared_data))
        # self._game_process.daemon = True
        self._game_process.start()

    def _start_game_loop(self, mode, shared_array, shared_state, shared_data):
        try:
            self._mode = mode
            self._shared_data = shared_data
            self._shared_array = shared_array
            if mode == PROD or mode == TEST:
                params = parse_options("params-prod.yaml")
            else:
                params = parse_options("params-simu.yaml")

            self._robot_arucos = []
            for robot in params["ai_robots"]["robots"]:
                self._robot_arucos.append(robot['aruco_code'])

            if 'simulation' in params:
                width = params['simulation']['capture_width']
                height = params['simulation']['capture_height']
            elif 'ai_video_streamer' in params:
                width = params['ai_video_streamer']['capture_width']
                height = params['ai_video_streamer']['capture_height']
            image_size = (width, height, 3)
            arr_size = width * height * 3

            self._step_time = 1 / params['decision_rate']
            self._image_source, self._frontend = \
                self._get_image_source_and_frontend(mode, params)

            self._remote_image_processor = RemoteImageProcessorClient(
                params)

            shared_image = np.frombuffer(
                shared_array.get_obj(),
                dtype=np.uint8)
            self._shared_image = np.reshape(shared_image, image_size)

            while True:
                self._log_time(log_start=True)
                with shared_state.get_lock():
                    if shared_state.value is False:
                        break

                # 1) Get image
                if self._image_source.frame_available() is None:
                    print("==== IMAGE IS NONE")
                if not self._image_source.frame_available():
                    self._shared_data['status'] = 'No image'
                    print("\n\n=========== No image\n\n")
                    time.sleep(0.1)
                    continue
                image = self._image_source.frame()
                self._log_time(log_name='imageCaptureDuration')

                # 2) Get observations from image: Done in remote
                # 3) Get action from brain for the observations: Done in remote
                actions, image_of_game = \
                    self._remote_image_processor.image_to_actions(image=image)
                self._log_time(log_name='actionCreationDuration')
                if mode == PROD or mode == SIMU:
                    # 4) Send the action to frontend
                    _ = self._frontend.make_actions(actions)
                    self._log_time(log_name='frontendDuration')
                    self._shared_data['status'] = 'Playing game'
                else:
                    self._shared_data['status'] = 'Running in test mode'

                self._end_routine(image_of_game)

        except KeyboardInterrupt:
            print("\nGame: Keyboard Interrupt")

        except Exception as error:
            traceback.print_exc()
            shared_state.value = False
            self._image_source.stop()
            print('\n=====\nGot unexpected exception in "_start_game" in '
                  f'Game-class. Message: {error}\n=====\n')

        finally:
            self._stop_robots()
            self._image_source.stop()
            print("Game: Game stopped")

    def _end_routine(self, image):
        with self._shared_array.get_lock():
            self._shared_image[:] = image
        self._log_time(log_name='actualDuration', log_end=True)
        wait_time = self._step_time - self._shared_data['actualDuration']
        if wait_time > 0:
            time.sleep(wait_time)
        self._log_time(log_name='totalDuration', log_end=True)

    def _get_image_source_and_frontend(self, mode, params):
        if mode == PROD or mode == TEST:
            image_source = VideoSource(params)
            if mode == PROD:
                frontend = AIRobotsHandler(params)
            else:
                frontend = None
        elif mode == SIMU:
            simulation = UnitySimulation(params)
            frontend, image_source = simulation, simulation
        return image_source, frontend

    def _stop_robots(self):
        """
        Stop robot by sending frontend the stop command
        if frontend is used

        return : Doesn't return anything
        """
        if self._mode == PROD or self._mode == SIMU:
            # Stop the robot from moving
            if self._frontend.available is True:
                robot_actions = {}
                for aruco in self._robot_arucos:
                    robot_actions[aruco] = 0
                status = self._frontend.make_actions(robot_actions)

    def _log_time(self, log_name=None, log_start=False, log_end=False):
        """
        Log time a step has taken to _game_data-object with given field name

        log_name : str
        log_start : boolean
        log_end : boolean
        return : Doesn't return anything
        """
        if log_name is not None:
            self._shared_data[log_name] = time.time() - self._last_log_time
            self._last_log_time = time.time()
        if log_start:
            self._step_start_time = time.time()
            self._last_log_time = self._step_start_time
        elif log_end:
            total_time = time.time() - self._step_start_time
            self._shared_data[log_name] = total_time
            self._shared_data[f"{log_name}FPS"] = 1 / total_time