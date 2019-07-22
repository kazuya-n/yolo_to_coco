import argparse
import datetime
import json
import os

from PIL import Image

w = 1080
h = 1920

def main(args):
    created = datetime.datetime.today().strftime("%Y/%m/%d")
    out_dic = {
                "info":{
                    "description" : "MyDataset",
                    "date_created" : created
                },
                "images" : [],
                "annotations" : []
              }
    
    all_list = os.listdir(args.in_dir)
    l_list = [f for f in all_list if ".txt" in f]
    
    an_idx = 0

    for im_idx, label in enumerate(l_list):
        file_name = os.path.splitext(label)[0] + ".jpg"

        im = Image.open(os.path.join(args.im_dir, file_name))
        width = im.width
        height = im.height
        
        image = dict(
            id = im_idx,
            width = width,
            height = height,
            file_name = file_name
        )
        out_dic["images"].append(image)

        with open(os.path.join(args.in_dir,label), mode = 'r')as f:
            anno_list = f.readlines()
            for anno in anno_list:
                anno = anno.strip().split()
                
                for i in range(1, 5):
                    anno[i] = float(anno[i])
                # "class x y w h"
                x = (anno[1] - anno[3] / 2) * width
                y = (anno[2] - anno[4] / 2) * height
                w = anno[3] * width
                h = anno[4] * height
                
                cls = anno[0]

                annotation = dict(
                    id = an_idx,
                    category_id = int(cls),
                    image_id = im_idx,
                    bbox = [x, y, w, h],
                    iscrowd = int(len(anno_list) > 1)
                )
                out_dic["annotations"].append(annotation)
                an_idx += 1

    with open(args.out, mode="w")as f:
        # dump = json.dumps(out_dic)
        # print(type(dump))
        json.dump(out_dic, f, indent=2)
    

    print(f"{an_idx+1} annotations created for {im_idx} images.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--in_dir')
    parser.add_argument('-o', '--out')
    parser.add_argument('-i', '--im_dir')
    main(parser.parse_args())
