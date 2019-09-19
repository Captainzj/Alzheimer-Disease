import os


def rm_group_data():
    for group in dataset_group:
        dirpath = os.path.join(path, group)
        for filename in os.listdir(dirpath):
            for tag in rm_tag:
                if filename.startswith(tag):
                    rm_filepath = os.path.join(dirpath, filename)
                    print("rm_filepath", rm_filepath)
                    os.remove(rm_filepath)
                    break


if __name__ == '__main__':
    path = '/home/captain/Desktop/Snorlax-AD/data/dataset/Two_Classification/PET_MPS_EMvsLM'
    dataset_group = os.listdir(path)  # ['val', 'test', 'train']
    rm_tag = ['AD', 'CN']
    rm_group_data()

    pass
