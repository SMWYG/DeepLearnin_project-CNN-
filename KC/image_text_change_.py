from PIL import Image #이미지 resize를 위한 라이브러리
import os
import numpy as np
from skimage.color import rgb2gray #이미지 grayscale을 위한 라이브러리
import matplotlib.pyplot as plt


class ImagePreprocess:
    # __IMAGE_PATH = "/Users/kyungchankim/Documents/Spyder/Python_Study/RL_KERAS/data/mushroom_images/"
    # __DATA_PATH = "/Users/kyungchankim/Documents/Spyder/Python_Study/RL_KERAS/preprocessed_data/"
    __DATA_PATH = "C:\\Users\\dahan\\Downloads\\"

    def __init__(self):

        # 로드할 이미지들을 어떻게 pre processing할 것인지 셋팅하는 초기화 함수

        self.image_count = 0
        self.isThumbnail = True # raw 이미지를 Thumbnail 가공 여부
        self.imgsize = (32, 32) # 최종적으로 저장할 이미지의 size 설정


        # Image load 하는 함수 실행
        # self.preprocessing(isThumbnail=self.isThumbnail)


        self.text2Image() # 최종 가공된 이미지를 Text로 바꾼 것을 이미지로 출력하는 함수 실행

    def plot_image(self, image):
        """image array를 plot으로 보여주는 함수
        Args:
            image (2-D or 3-D array): (H, W) or (H, W, C)
        """
        image = np.squeeze(image)
        shape = image.shape

        if len(shape) == 2:
            plt.imshow(image, cmap="gray")
        else:
            plt.imshow(image)
        plt.show()

    def preprocessing(self, isThumbnail=False):
        """
        directory에서 images load 하여 preprocessing 하는 함수
        :return:
        """
        print("Image Preprocessing Start")
        for name in [filename for filename in os.listdir(ImagePreprocess.__IMAGE_PATH)]:

            try:
                img = Image.open(self.__IMAGE_PATH + str(name))

                # Thumbnail 진행 여부에 따라 나누어짐
                # Raw Image 들의 크기를 조정하면서 grayscale 할 때
                if isThumbnail:
                    img = self.rgb2grayThumbnailFlat(img)
                    self.image2Text(img)

                # 이미 Resized 된 이미지를 처리 할 때
                else:
                    img = self.rgb2grayFlat(img)
                    self.image2Text(img)

            except OSError as e:
                print("OSError 발생, continue 합니다. ")
                continue

    def rgb2grayFlat(self, img):
        """
        rgb image를 grayscale 후 flattend numpy array로 변환하는 함수
        :param img: rgb image
        :return: flattend numpy array (1차원)
        """

        # 이미지를 numpy array로 바꾸고 효율을 위해 255를 곱해 int로 저장한 후 flat 한다.
        img = np.asarray(img, dtype=np.uint8)
        img = np.uint8(rgb2gray(img) * 255)
        img = img.flatten()

        return img

    def rgb2grayThumbnailFlat(self, img):
        """
        기존 image를 Thumbnail과 grayscale 하는 함수
        :param img: 로드 한 image
        :return: Thunbnail 된 image array
        """
        self.image_count += 1
        print("Thumbnail Process {}".format(self.image_count))

        # Thumbnail로 크기를 조정한 것을 조정하려는 사이즈위에 다시그리기 위해 조정하려는 사이즈 만큼의 백색 도화지를 만듦
        new_img = Image.new("RGB", self.imgsize, "white")

        # 기존 raw 이미지를 thumbnail 사진 크기에 맞추기 위한 작업
        # 보통 가로, 세로 중 한쪽을 resize한다. (256, 130)   ---->   (128, xx)와 같이 된다.
        img.thumbnail(self.imgsize, Image.ANTIALIAS)

        # Thumbnail된 img를 numpy array로 변환하는 과정
        # grayscale 후 효율을 위해 255를 곱하여 int값으로 바꾼다.
        load_img = np.asarray(img, dtype=np.uint8)
        load_img = np.uint8(rgb2gray(load_img) * 255)
        load_newimg = np.asarray(new_img, dtype=np.uint8)  # new_img.load()
        load_newimg = np.uint8(rgb2gray(load_newimg) * 255)

        # (128,xx) 됐을 때 빈 공간을 보충하기(메우기) 위한 과정 offset
        i_offset = (self.imgsize[0] - load_img.shape[0]) / 2
        j_offset = (self.imgsize[0] - load_img.shape[1]) / 2
        i_offset = round(i_offset)
        j_offset = round(j_offset)

        # offset 과정
        for i in range(0, load_img.shape[0]):
            for j in range(0, load_img.shape[1]):
                load_newimg[i + i_offset, j + j_offset] = load_img[i, j]

        # numpy array flat
        result_image = load_newimg.flatten()

        return result_image

    def image2Text(self, img):
        """
        array로 된 image를 text로 바꾸는 함수
        :param img: numpy flattend array
        :return:
        """
        # numpy array를 text파일로 저장하는 과정, 끝에 이미지 라벨ㅇ을 붙인다.
        # 고양이 0 , 개 1, 꽃 2, 버섯 3, 코끼리 4, 코뿔소 5, 녹지 6, 빌딩 7, 심슨가족 8, 뱀 9
        label = '3'
        with open(ImagePreprocess.__DATA_PATH + "128_cat_dog_flower_mushroom_data", "a", encoding="utf-8") as file:
            for idx in range(len(img)):
                file.write(str(img[idx]) + ',')

            # 라벨 추가 부분
            file.write(label + ',')
            file.write('\n')
            file.close()

    def text2Image(self):
        """
        Text로 된 Images를 1줄씩 읽어오는 함수
        :return:
        """
        with open(ImagePreprocess.__DATA_PATH + "cifar10_data", "r", encoding="utf-8") as file:
            # lines : 모든 lines(데이터행)을 불러온다.
            lines = file.readlines()
            for i in range(50000):
                line = lines[i].split(',')
                line.pop()
                print(line.pop())
                line = np.array(line, dtype=np.uint8)
                line = np.reshape([line], self.imgsize)
                line = line / 255.
                # self.plot_image(line)

            # for line in lines:
            #     # ','를 기준으로 나누어서 리스트로 만들고 numpy array로 바꾸는 과정
            #     # line.pop은 리스트 마지막에 '\n'이 추가되기때문에 제거하기 위한 과정
            #     line = line.split(',')
            #     line.pop()
            #     line.pop()
            #     line = np.array(line, dtype=np.uint8)
            #     line = np.reshape([line], self.imgsize)
            #     line = line/255.
            #     self.plot_image(line)

        file.close()


img2txt = ImagePreprocess()