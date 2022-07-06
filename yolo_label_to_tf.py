import glob
import cv2
import re

yolo_files = glob.glob("E:\\master_thesis\\project\\vehicle_dataset\\CUSTOM_DATA_yolo//*.txt")

classes_path = open("E:\\master_thesis\\project\\vehicle_dataset\\CUSTOM_DATA_yolo//classes.txt")
class_strng = classes_path.readlines()
classes = [i.strip() for i in class_strng]

print(classes)

for txt_file in yolo_files:
    if txt_file != "E:\\master_thesis\\project\\vehicle_dataset\\CUSTOM_DATA_yolo\\classes.txt":

        file_name = txt_file[58:]
        file_name = file_name[:-4]+".jpg"

        img_path = txt_file[:-4] + ".jpg"
        img_path = "E:\\master_thesis\\project\\vehicle_dataset\\custom_data_tf\\"+file_name

        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

        width = int(img.shape[1])
        height = int(img.shape[0])

        file = open(txt_file, "r")
        lines = file.readlines()

        with open("E:\\master_thesis\\project\\vehicle_dataset\\custom_data_tf\\"+str(file_name[:-4])+".xml", 'w') as f:
            f.write('<annotation>\n')
            f.write('\t<folder>custom_data_tf</folder>\n')
            f.write('\t<filename>' + str(file_name) + '</filename>\n')
            f.write('\t<path>' + img_path + '</path>\n')
            f.write('\t<source>\n')
            f.write('\t\t<database>Unknown</database>\n')
            f.write('\t</source>\n')
            f.write('\t<size>\n')
            f.write('\t\t<width>' + str(width) + '</width>\n')
            f.write('\t\t<height>' + str(height) + '</height>\n')
            f.write('\t\t<depth>3</depth>\n')  # assuming a 3 channel color image (RGB)
            f.write('\t</size>\n')
            f.write('\t<segmented>0</segmented>\n')

            for each_line in lines:
                yolo_array = re.split("\s", each_line.rstrip())

                class_number = int(yolo_array[0])
                object_name = classes[class_number]
                x_yolo = float(yolo_array[1])
                y_yolo = float(yolo_array[2])
                yolo_width = float(yolo_array[3])
                yolo_height = float(yolo_array[4])

                box_width = yolo_width * width
                box_height = yolo_height * height
                x_min = str(int(x_yolo * width - (box_width / 2)))
                y_min = str(int(y_yolo * height - (box_height / 2)))
                x_max = str(int(x_yolo * width + (box_width / 2)))
                y_max = str(int(y_yolo * height + (box_height / 2)))

                f.write('\t<object>\n')
                f.write('\t\t<name>' + object_name + '</name>\n')
                f.write('\t\t<pose>Unspecified</pose>\n')
                f.write('\t\t<truncated>0</truncated>\n')
                f.write('\t\t<difficult>0</difficult>\n')
                f.write('\t\t<bndbox>\n')
                f.write('\t\t\t<xmin>' + x_min + '</xmin>\n')
                f.write('\t\t\t<ymin>' + y_min + '</ymin>\n')
                f.write('\t\t\t<xmax>' + x_max + '</xmax>\n')
                f.write('\t\t\t<ymax>' + y_max + '</ymax>\n')
                f.write('\t\t</bndbox>\n')
                f.write('\t</object>\n')

            f.write('</annotation>\n')
        f.close()