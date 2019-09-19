def PET_Interpolation(nii_file, target_file):
    import SimpleITK as sitk
    image = sitk.ReadImage(nii_file)
    image_array = sitk.GetArrayFromImage(image)  
    print(image_array.shape)  # (z, y, x)

    import nibabel as nib
    data = nib.load(nii_file)
    pixdim = data.header['pixdim']  # ex. <class 'numpy.ndarray'> [1.      1.01821 1.01821 2.027   0.      0.      0.      0.     ]
    spacing_x, spacing_y, thickness =  pixdim[1], pixdim[2], pixdim[3]
    # factor_x, factor_y, factor_z = 1.0/spacing_x , 1.0/spacing_y, 1.0/thickness  
    # print(spacing_x, spacing_y, thickness)
    # print(factor_x, factor_y, factor_z)

    import scipy.ndimage
    # new_image_array = scipy.ndimage.zoom(image_array, (factor_z, factor_x, factor_y), order=3)
    new_image_array = scipy.ndimage.zoom(image_array, (thickness, spacing_x, spacing_y), order=3)

    new_image = sitk.GetImageFromArray(new_image_array)
    sitk.WriteImage(new_image, target_file) # default: spacing_x, spacing_y, thickness: 1.0, 1.0, 1.0
    print(new_image_array.shape)  
    print(new_image_array == image_array)

if __name__ == "__main__":
    # # (109, 400, 400) → (221, 407, 407)
    # nii_file = '/Users/Captain/Desktop/ADNI/130_S_4641/ADNI_FDG_Brain_30min_dyn/2014-04-25_10_27_08.0/I421705/ADNI_130_S_4641_PT_ADNI_FDG_Brain_30min_dyn_br_raw_20140425121131055_359_S217053_I421705.nii'  
    # target_file = 'new_image_ADNI_FDG_Brain_30min_dyn.nii'
    
    # # (162, 256, 256) → (161, 341, 341)
    # nii_file = '/Users/Captain/Desktop/ADNI/019_S_4252/PET_Brain__FDG/2013-10-22_09_55_11.0/I396559/ADNI_019_S_4252_PT_PET_Brain__FDG_br_raw_20131030141227989_72_S205246_I396559.nii' 
    # target_file = 'new_image_PET_Brain__FDG.nii'
    
    # (63, 128, 128) → (153, 330, 330)
    nii_file = '/Users/Captain/Desktop/ADNI/006_S_4192/ADNI_FDG_6F_4i_16s/2013-10-09_05_59_08.0/I393810/ADNI_006_S_4192_PET_ADNI_FDG_6F_4i_16s__br_raw_20131009135509696_1_S203396_I393810.nii'
    target_file = 'new_image_ADNI_FDG_6F_4i_16s.nii'

    # # (161, 341, 341) → (161, 341, 341)  (changed: order=3)
    # nii_file = '/Users/Captain/Desktop/ADNI/new_image_PET_Brain__FDG.nii'
    # target_file = 'new_image_PET_Brain__FDG_1.nii'
    
    # 1. Spacing、thickness 缩放
    PET_Interpolation(nii_file, target_file)

    # 2. 颅骨剔除
    # 3. 剔除背景边缘
    # 4. 平面尺寸缩放
    pass