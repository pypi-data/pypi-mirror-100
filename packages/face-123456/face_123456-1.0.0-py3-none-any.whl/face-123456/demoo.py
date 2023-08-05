# coding:utf-8
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import sys

sys.path.append("..")
sys.path.append("./process")
sys.path.append("./model")
from process.data_fusion import *
from process.augmentation import *
from metric import *
from collections import OrderedDict

pwd = os.path.abspath('./')
def load_test_list():
    list = []
    # f = open(DATA_ROOT + '/test_public_list.txt')
    # f = open(DATA_ROOT + '/val_private_list.txt')
    f = open(DATA_ROOT + '/train_list.txt')
    lines = f.readlines()

    for line in lines:
        line = line.strip().split(' ')
        list.append(line)
    return list

# 非活体
index = 2000
# 活体
# index =22000
test_list = load_test_list()
print(test_list[index])


class FaceAnti:
    def __init__(self):
        # from FaceBagNet_model_A import Net
        # from model.FaceBagNet_model_C import Net
        from model_fusion.FaceBagNet_model_A_SEFusion import FusionNet
        Net = FusionNet
        self.net = Net(num_class=2)  # ,is_first_bn=True)
        # model_path = os.path.join(pwd, 'models', 'model_A_color_64', 'checkpoint', 'global_min_acer_model.pth')
        model_path = "./global_min_acer_model.pth"
        # if torch.cuda.is_available():
        #     state_dict = torch.load(model_path, map_location='cuda')
        # else:
        state_dict = torch.load(model_path, map_location='cpu')
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k[7:]  # remove `module.`
            new_state_dict[name] = v
        self.net.load_state_dict(new_state_dict)
        # self.net.load_state_dict(state_dict)
        # if torch.cuda.is_available():
        #     self.net = self.net.cuda()
        print('loaded model from: ', model_path)

        self.net.eval()
        color, depth, ir = test_list[index][:3]
        test_id = color + ' ' + depth + ' ' + ir
        os.system("open %s" % (os.path.join(DATA_ROOT, color)))
        os.system("open %s" % (os.path.join(DATA_ROOT, depth)))
        os.system("open %s" % (os.path.join(DATA_ROOT, ir)))

        color = cv2.imread(os.path.join(DATA_ROOT, color), 1)
        # depth = cv2.imread(os.path.join(DATA_ROOT, depth), 1)
        # ir = cv2.imread(os.path.join(DATA_ROOT, ir), 1)
        # whole_image = np.concatenate([color, depth, ir], axis=0)
        # cv2.imshow('color', color)
        # cv2.imshow('depth', depth)
        # cv2.imshow('ir', ir)
        # cv2.waitKey(0)
        # cv2.destroyWindow('whole_image')

        color = cv2.resize(color, (RESIZE_SIZE, RESIZE_SIZE))
        # depth = cv2.resize(depth, (RESIZE_SIZE, RESIZE_SIZE))
        # ir = cv2.resize(ir, (RESIZE_SIZE, RESIZE_SIZE))

        image = color_augumentor(color, target_shape=(48, 48, 3))

        image = cv2.resize(image, (48, 48))
        image = np.transpose(image, (2, 0, 1))
        image = image.astype(np.float32)
        image = image / 255.0
        input_image = torch.FloatTensor(image).unsqueeze(0)

        label = test_id

        with torch.no_grad():
            logit, _, _ = self.net(input_image)
            prob = F.softmax(logit, 1)

        print('probabilistic：', prob)
        try:
            print('label: ', test_list[index][-1], '，predict: ', np.argmax(prob.detach().cpu().numpy()))
        except:
            print('predict: ', np.argmax(prob.detach().cpu().numpy()))






if __name__ == "__main__":
    FA = FaceAnti()

    img = cv2.imread('1.jpg', 1)
    FA.detect(img)