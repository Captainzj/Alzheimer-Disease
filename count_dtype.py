import os


def count_type(path):

    ad_count, cn_count, em_count, lm_count = 0, 0, 0, 0
    for filename in os.listdir(path):
        if filename.startswith('ad'):
            ad_count += 1
        elif filename.startswith('cn'):
            cn_count += 1
        elif filename.startswith('em'):
            em_count += 1
        elif filename.startswith('lm'):
            lm_count += 1

    print('{}{}\nad_count:{}, cn_count:{}, em_count:{}, lm_count:{}'
          .format(path, '-'*20, ad_count, cn_count, em_count, lm_count))


if __name__ == '__main__':

    dataset = r'/openbayes/input/input0/SHF'
    for dtype in ['train', 'val', 'test']:
        count_type(os.path.join(dataset, dtype))
    pass
