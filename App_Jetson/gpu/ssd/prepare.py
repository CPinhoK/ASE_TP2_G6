import glob, os

# Current directory
cur_dir = os.path.dirname(os.path.abspath(__file__))

print(cur_dir)

current_dir = cur_dir+'/data/MaskDetector/JPEGImages'

print(current_dir)

# Percentage of images to be used for the test set
percentage_test = 10;

# Create and/or truncate trainval.txt and test.txt
file_train = open(cur_dir+'/data/MaskDetector/ImageSets/Main/trainval.txt', 'w+')
file_test = open(cur_dir+'/data/MaskDetector/ImageSets/Main/test.txt', 'w+')

# Populate trainval.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)
for pathAndFilename in glob.iglob(os.path.join(current_dir, "*.jpg")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    if counter == index_test:
        counter = 1
        file_test.write(title  + "\n")
    else:
        file_train.write(title + "\n")
        counter = counter + 1