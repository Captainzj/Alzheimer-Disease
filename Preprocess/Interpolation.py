import os
import nibabel as nib
import numpy as np


def interpolation(data, target_file):
    data_shape = data.shape
    print(data_shape)

    import scipy.ndimage
    new_data = scipy.ndimage.zoom(data, (resize_shape[0]/data.shape[0],
                                         resize_shape[1]/data.shape[1],
                                         resize_shape[2]/data.shape[2]), order=3)
    print(new_data.shape)
    np.save(target_file, new_data)


def convert_npy():
    for i, path in enumerate(origin_list):
        for nii_filename in os.listdir(path):
            filepath = os.path.join(path, nii_filename)
            data = nib.load(filepath).get_data()
            data_arr = np.asarray(data)
            data_arr = np.squeeze(data_arr)

            savepath = os.path.join(dst_list[i], nii_filename[:-4] + ".npy")
            interpolation(data_arr, savepath)

            print('{}\n→{}'.format(filepath, savepath))
            print('-'*20)


if __name__ == '__main__':

    resize_shape = (128, 128, 88)
    dataset_path = '/home/captain/Desktop/Snorlax-AD/data/dataset/Four_Classification/PET_dataset/'
    output = '/home/captain/Desktop/Snorlax-AD/data/dataset/Four_Classification/PET_resize/'

    origin_list, dst_list = [], []
    for tag in ['train', 'val', 'test']:
        origin_list.append(os.path.join(dataset_path, tag))
        dst_list.append(os.path.join(output, tag))
    print("origin_list", origin_list)
    print("dst_list", dst_list)

    # convert_npy()

    pass
