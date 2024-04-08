import os
import shutil


train_percent = .8
mother = './outputs/my_dataset/'
daughter = './outputs/amydata/'


mother = os.path.abspath(mother) + '/'
daughter = os.path.abspath(daughter) + '/'


daughters = {
    'train_labels_path': f'{daughter}labels/train/',
    'train_images_path': f'{daughter}images/train/',
    'val_labels_path' : f'{daughter}labels/val/',
    'val_images_path' : f'{daughter}images/val/'
}


for dau in daughters:
    if not os.path.exists(daughters[dau]):
        os.makedirs(daughters[dau])


files = os.listdir(mother)


train_count = int(len(files) * train_percent)
val_count = len(files) - train_count


for i in range(train_count):
    if files[i].endswith('.png'):
        png = mother + files[i]
        txt = ''.join(png.split('.png')) + '.txt'
        if os.path.exists(txt):
            target = ''.join([daughters['train_images_path']] + png.split(mother))
            print(f'from: {png} =====> to:{target}')
            shutil.copy(png, target)
            target = ''.join([daughters['train_labels_path']]  + txt.split(mother))
            print(f'from: {txt} =====> to:{target}')
            shutil.copy(txt, target)
    print(f"({i} of {len(files)} completed!)")


os.system('cls')


for i in range(train_count, len(files)):
    if files[i].endswith('.png'):
        png = mother + files[i]
        txt = ''.join(png.split('.png')) + '.txt'
        if os.path.exists(txt):
            target = ''.join([daughters['val_images_path']] + png.split(mother))
            print(f'from: {png} =====> to:{target}')
            shutil.copy(png, target)
            target = ''.join([daughters['val_labels_path']]  + txt.split(mother))
            print(f'from: {txt} =====> to:{target}')
            shutil.copy(txt, target)
    print(f"({i} of {len(files)} completed!)")