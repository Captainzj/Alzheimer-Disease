import shutil
import os 


def select_group_collection(collections):

    for collection_name in collections:
        if 'AD' in collection_name:
            ad_collection = collection_name
        elif 'CN' in collection_name:
            cn_collection = collection_name
        elif 'EMCI' in collection_name:
            em_collection = collection_name
        elif 'LMCI' in collection_name:
            lm_collection = collection_name

    return ad_collection,  cn_collection, em_collection, lm_collection


def is_exists_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def copy_items(group_path, target_path):
    for root, dirs, files in os.walk(group_path):
        for file in files:
            if file.endswith('nii'):
                shutil.copy(os.path.join(root, file), target_path)
                print(os.path.join(root, file) + ' Copied')


def extract(origin_path, target_path, series_list):
    """
    breif: 将数据从collection_path拷贝到data_path

    :param origin_path:
    :param target_path:
    :param series_list:  ex. [Match_AD_Select, Match_CN_select, Match_EMCI_select, Match_LMCI_select]
    :return:
    """

    # 4. Match_select (329 items)
    select_pet_data = os.path.join(target_path, 'Match_select_ORIGIN')
    select_pet_ad = os.path.join(select_pet_data, 'AD')        
    select_pet_cn = os.path.join(select_pet_data, 'CN')        
    select_pet_em = os.path.join(select_pet_data, 'EMCI')      
    select_pet_lm = os.path.join(select_pet_data, 'LMCI')      
    is_exists_dir(select_pet_ad)
    is_exists_dir(select_pet_cn)
    is_exists_dir(select_pet_em)
    is_exists_dir(select_pet_lm)

    ad_collection,  cn_collection, em_collection, lm_collection = select_group_collection(series_list)
    # ad (84 items, 14 subjects)
    copy_items(os.path.join(origin_path, ad_collection), select_pet_ad)
    # cn (54 items, 9 subjects)
    copy_items(os.path.join(origin_path, cn_collection), select_pet_cn)
    # em (115 items, 20 subjects)
    copy_items(os.path.join(origin_path, em_collection), select_pet_em)  
    # lm (76 items, 13 subjects)
    copy_items(os.path.join(origin_path, lm_collection), select_pet_lm)

    pass


def rename_kernel(path, dst):
    """

    :param path:
    :param dst:
    :return:
    """

    group_tags = os.listdir(path)
    for tag in group_tags:
        group_path = os.path.join(path, tag)
        for file in os.listdir(group_path):
            if file.endswith('nii'):
                os.symlink(os.path.join(group_path, file), os.path.join(dst, "{}_{}".format(tag, file)))
                print('{} create symlink.'.format(file))
    pass


def division_dataset(rename_dir_path, target_path, proportion):
    """
    确保同一受试者的数据处于同一数据子集（手动调整）

    :param rename_dir_path:
    :param target_path:
    :param proportion:
    :return:
    """

    ad_list, cn_list, em_list, lm_list = [], [], [], []
    for filename in os.listdir(rename_dir_path):
        if filename.startswith('AD'):
            ad_list.append(filename)
        elif filename.startswith('CN'):
            cn_list.append(filename)
        elif filename.startswith('EMCI'):
            em_list.append(filename)
        elif filename.startswith('LMCI'):
            lm_list.append(filename)
    
    print('AD items:{}; CN items:{}; \nEM items:{}; LM items:{}.'
          .format(len(ad_list), len(cn_list), len(em_list), len(lm_list)))

    for group_list in [ad_list, cn_list, em_list, lm_list]:
        group_count = len(group_list)
        train_count = int((proportion[0]/(proportion[0] + proportion[1] + proportion[2])) * group_count)
        valid_count = int((proportion[1]/(proportion[0] + proportion[1] + proportion[2])) * group_count)

        # import numpy as np
        # str_arr_train = np.random.choice(group_list, size=train_count, replace=False, p=None)
        # str_arr_valid = np.random.choice(list(set(group_list) - set(str_arr_train)),
        #                                  size=valid_count, replace=False, p=None)
        group_list.sort()
        str_arr_train = group_list[:train_count]
        str_arr_valid = group_list[train_count:train_count+valid_count]
        str_arr_test = list(set(group_list) - set(str_arr_train) - set(str_arr_valid))
        result = (str_arr_train, str_arr_valid, str_arr_test)
        print('{} -----------\ntrain_list: {} items\nvalid_list: {} items\ntest_list: {} items'
              .format(group_list[0][:2], len(result[0]), len(result[1]), len(result[2])))

        for file in str_arr_train:
            shutil.copy(os.path.join(rename_dir_path, file), os.path.join(target_path, 'train'))
            print(file, '→', os.path.join(target_path, 'train'))
        for file in str_arr_valid:
            shutil.copy(os.path.join(rename_dir_path, file), os.path.join(target_path, 'val'))
            print(file, '→', os.path.join(target_path, 'val'))
        for file in str_arr_test:
            shutil.copy(os.path.join(rename_dir_path, file), os.path.join(target_path, 'test'))
            print(file, '→', os.path.join(target_path, 'test'))
    pass


if __name__ == "__main__":

    # # 1. 将数据从collection_path拷贝到data_path
    # collection_path = '/home/captain/Desktop/Snorlax-AD/ADNI_Collections'
    # data_path = './data/ORIGIN'
    # series_list = ["Match_AD_Select", "Match_CN_select", "Match_EMCI_select", "Match_LMCI_select"]
    # extract(origin_path=collection_path, target_path=data_path, series_list=series_list)
    
    # # 2. 重命名
    # origin_path = '/home/captain/Desktop/Snorlax-AD/data/ORIGIN/Match_ORIGIN'
    # rename_path = '/home/captain/Desktop/Snorlax-AD/data/rename/Match_rename'
    # is_exists_dir(dst_path)
    # rename_kernel(origin_path, dst_path)

    # # 3. 划分数据集
    # path = '/home/captain/Desktop/Snorlax-AD/data/rename_symlink/PET_rename'
    # target_path = '/home/captain/Desktop/Snorlax-AD/data/dataset/PET_dataset'
    # proportion = (6, 2, 2)
    # division_dataset(path, target_path, proportion)  # need 额外手动调整
    pass
