# NextchipDB dataset

import os
import numpy as np
import PIL.Image as pil

from .mono_dataset import MonoDataset


class NextchipDataset(MonoDataset):

    def __init__(self, *args, **kwargs):
        super(NextchipDataset, self).__init__(*args, **kwargs)


        fx = 2000.0
        fy = 2000.0
        cx = 960.0
        cy = 540.0

        self.full_res_shape = (1920, 1080)
        # NOTE: Make sure your intrinsics matrix is *normalized* by the original image size
        self.K = np.array([[1.04, 0, 0.5, 0],
                           [0, 1.85, 0.5, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype=np.float32)

    def get_image_path(self, folder, frame_index, side):
        f_str = "{:010d}{}".format(frame_index, self.img_ext)
        image_path = os.path.join(
            self.data_path, folder, f_str)
        return image_path

    def check_depth(self):
        return False

    def index_to_folder_and_frame_idx(self, index):
        """Convert index in the dataset to a folder name, frame_idx and any other bits
        """
        line = self.filenames[index].split()
        folder = line[0]
        frame_index = int(line[1])
        side = None
        return folder, frame_index, side

    def get_color(self, folder, frame_index, side, do_flip):
        color = self.loader(self.get_image_path(folder, frame_index, side))

        if do_flip:
            color = color.transpose(pil.FLIP_LEFT_RIGHT)
        return color