import os
import random

import scipy.io as sio
from psychopy import visual, core, event, data
import matplotlib.pyplot as plt

img_nums = 1854  # Number of images to randomize from
choice_nums = 3  # How many images to choose
img_key_name_in_source = 'im'  # The name of the key in the mat file that has the image


def get_three_new_imgs():
    """
    Chooses 3 randoms between 0 to var img_nums then turns the numbers to names of file
    :return: array of three uniques filenames
    """
    unique_numbers = random.sample(range(img_nums), choice_nums)
    choice_imgs = []
    for i in unique_numbers:
        num = f"{i:04d}"
        filename = f'im{num}.png'
        choice_imgs.append(filename)
    return choice_imgs


class Database:
    def __init__(self, img_source, trial_num=100, load_imgs=False):
        """
        initialize the data
        :param img_source: which mat file to load the images from
        :param trial_num: How many times trials there are
        :param load_imgs: To create the images from the start
        """
        if load_imgs:
            self.img_source = sio.loadmat(img_source)
            self.turn_mat_to_img()
        self.trial_num = trial_num

    def turn_mat_to_img(self):
        """
        Using the mat files create the images
        """
        images = self.img_source[img_key_name_in_source]
        for i in range(len(images)):
            num = f"{i:04d}"
            filename = f'imgs/im{num}.png'
            plt.imsave(filename, images[i][0], cmap='gray')

    def get_all_trial_imgs(self):
        """
        Creates trial_num of 3 image names
        :return: array of size trial_num each cell full of 3 image names
        """
        all_imgs = []
        for i in range(self.trial_num):
            all_imgs.append(get_three_new_imgs())
        return all_imgs


def create_unique_filename(base_name, extension):
    """
    Create a unique filename by adding a number if it already exists
    :param base_name: name of the file
    :param extension: extension of the file
    :return: A unique name that doesn't exist
    """
    counter = 1
    filename = f"{base_name}{extension}"
    while os.path.exists(f"logs/{filename}"):
        filename = f"{base_name}_{counter}{extension}"
        counter += 1
    return filename


class Visuals:
    def __init__(self, question, all_imgs, trails_num=100, wait_timer=0.3, file_name="log"):
        """
        initiate all the data
        :param question: The question to ask
        :param all_imgs: the img names to choose from
        :param trails_num: number of trials
        :param wait_timer: how much time to wait between each trial
        """
        self.window = visual.Window(monitor="TestMonitor", size=(800, 600), units="pix", fullscr=False, color='white',
                                    autoLog=False)
        self.message = visual.TextStim(self.window, text=question, pos=(0, 200), height=30, color='black')
        self.rectangle = visual.Rect(self.window, width=600, height=300, lineColor='black', lineWidth=3, pos=(0, 0))
        self.mouse = event.Mouse(visible=True, win=self.window)
        self.display_timer = core.Clock()
        self.click_timer = core.Clock()
        self.basename = file_name
        self.new_filename = None
        self.trials_num = trails_num
        self.all_imgs = all_imgs
        self.wait_timer = wait_timer
        self.click_time = None
        self.display_time = None
        self.clicked_image = None
        self.imgs = []
        self.log = []

    def start_imgs(self, imgs):
        """
        :param imgs: group of 3 image names to simulate
        """
        self.imgs = [
            visual.ImageStim(self.window, image=f"imgs/{img}", pos=pos)
            for img, pos in zip(imgs, [(-200, 0), (0, 0), (200, 0)])
        ]

    def show_window(self):
        """
        Draw all the visuals in the window and handle the mouse click and timers
        """
        self.message.draw()
        self.rectangle.draw()
        for img_stim in self.imgs:
            img_stim.draw()
        self.window.flip()
        self.display_time = self.display_timer.getTime()
        self.click_timer.reset()
        while self.clicked_image is None:
            self.clicked_image = self.get_img_pressed()
        self.click_time = self.click_timer.getTime() * 1000

    def get_img_pressed(self):
        """
        Check which image was clicked
        :return: number of image clicked or None
        """
        for i, stim in enumerate(self.imgs):
            if self.mouse.isPressedIn(stim):
                return i
        return None

    def trial_run(self, imgs):
        """
        Reassign the images in the window and draw the visuals and add everything to the log
        :param imgs: 3 images to load into the window
        """
        self.start_imgs(imgs)
        self.show_window()
        self.append_to_log(
            f"\n{imgs[0]}, {imgs[1]}, {imgs[2]}, {self.clicked_image}, {self.display_time}, {self.click_time}")

    def clear_window(self):
        """
        Reset the image clicked and the window then wait the wait_time before drawing again
        """
        self.clicked_image = None
        self.window.flip()
        core.wait(self.wait_timer)

    def append_to_log(self, trial_result):
        with open(f"logs/{self.new_filename}", 'a') as file:
            file.write(trial_result)

    def runner(self):
        """
        Run the trial using TrialHandler then save the data each time into a new log file
        """
        self.new_filename = create_unique_filename(self.basename, ".csv")
        with open(f"logs/{self.new_filename}", 'w') as file:
            file.write(f"image1, image2, image3, clicked_image, display_time, click_time")
        trials = data.TrialHandler(trialList=[{'choices': choices} for choices in self.all_imgs], nReps=1,
                                   autoLog=False)
        # logging.console.setLevel(logging.INFO)  # Set to INFO level for console output
        self.display_timer.reset()
        for trial in trials:
            current_choices = trial['choices']
            self.trial_run(current_choices)
            self.clear_window()
        self.close()

    def close(self):
        """
        Close and quit the program when the experment is done
        """
        self.window.close()
        core.quit()
