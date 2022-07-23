# 필요한 PyTorch 라이브러리 불러오기
import torch, wget, os, cv2, json, random
import torch.nn as nn

from torchvision import transforms
from torchvision.utils import save_image

from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm

def calc_mean_std(feat, eps=1e-5):
    size = feat.size()
    assert (len(size) == 4)
    N, C = size[:2]
    feat_var = feat.view(N, C, -1).var(dim=2) + eps
    feat_std = feat_var.sqrt().view(N, C, 1, 1)
    feat_mean = feat.view(N, C, -1).mean(dim=2).view(N, C, 1, 1)
    return feat_mean, feat_std

def adaptive_instance_normalization(content_feat, style_feat):
    assert (content_feat.size()[:2] == style_feat.size()[:2])
    size = content_feat.size()
    style_mean, style_std = calc_mean_std(style_feat)
    content_mean, content_std = calc_mean_std(content_feat)

    # 평균(mean)과 표준편차(std)를 이용하여 정규화 수행
    normalized_feat = (content_feat - content_mean.expand(size)) / content_std.expand(size)
    # 정규화 이후에 style feature의 statistics를 가지도록 설정
    return normalized_feat * style_std.expand(size) + style_mean.expand(size)
# 인코더(Encoder) 정의
vgg = nn.Sequential(
    nn.Conv2d(3, 3, (1, 1)),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(3, 64, (3, 3)),
    nn.ReLU(), # relu1-1
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(64, 64, (3, 3)),
    nn.ReLU(), # relu1-2
    nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(64, 128, (3, 3)),
    nn.ReLU(), # relu2-1
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(128, 128, (3, 3)),
    nn.ReLU(), # relu2-2
    nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(128, 256, (3, 3)),
    nn.ReLU(), # relu3-1
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(), # relu3-2
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(), # relu3-3
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(), # relu3-4
    nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 512, (3, 3)),
    nn.ReLU(), # relu4-1, this is the last layer used
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(), # relu4-2
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(), # relu4-3
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(), # relu4-4
    nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(), # relu5-1
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(), # relu5-2
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU(), # relu5-3
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 512, (3, 3)),
    nn.ReLU() # relu5-4
)

# 디코더(Decoder) 정의
decoder = nn.Sequential(
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(512, 256, (3, 3)),
    nn.ReLU(),
    nn.Upsample(scale_factor=2, mode='nearest'),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 256, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(256, 128, (3, 3)),
    nn.ReLU(),
    nn.Upsample(scale_factor=2, mode='nearest'),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(128, 128, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(128, 64, (3, 3)),
    nn.ReLU(),
    nn.Upsample(scale_factor=2, mode='nearest'),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(64, 64, (3, 3)),
    nn.ReLU(),
    nn.ReflectionPad2d((1, 1, 1, 1)),
    nn.Conv2d(64, 3, (3, 3)),
)

decoder.eval()
vgg.eval()

vgg_path = './vgg_normalised.pth'
decoder_path = './decoder.pth'

decoder.load_state_dict(torch.load(decoder_path))
vgg.load_state_dict(torch.load(vgg_path))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vgg.to(device)
decoder.to(device)

vgg = nn.Sequential(*list(vgg.children())[:31]) # ReLU4_1까지만 사용

class Net(nn.Module):
    def __init__(self, encoder, decoder):
        super(Net, self).__init__()
        enc_layers = list(encoder.children())
        self.enc_1 = nn.Sequential(*enc_layers[:4]) # input -> relu1_1
        self.enc_2 = nn.Sequential(*enc_layers[4:11]) # relu1_1 -> relu2_1
        self.enc_3 = nn.Sequential(*enc_layers[11:18]) # relu2_1 -> relu3_1
        self.enc_4 = nn.Sequential(*enc_layers[18:31]) # relu3_1 -> relu4_1
        self.decoder = decoder
        self.mse_loss = nn.MSELoss()

        # fix the encoder
        for name in ['enc_1', 'enc_2', 'enc_3', 'enc_4']:
            for param in getattr(self, name).parameters():
                param.requires_grad = False

    # extract relu1_1, relu2_1, relu3_1, relu4_1 from input image (중간 결과를 기록)
    def encode_with_intermediate(self, input):
        results = [input]
        for i in range(4):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]

    # extract relu4_1 from input image (최종 결과만 기록)
    def encode(self, input):
        for i in range(4):
            input = getattr(self, 'enc_{:d}'.format(i + 1))(input)
        return input

    # 콘텐츠 손실(feature 값 자체가 유사해지도록)
    def calc_content_loss(self, input, target):
        assert (input.size() == target.size())
        assert (target.requires_grad is False)
        return self.mse_loss(input, target)

    # 스타일 손실(feature의 statistics가 유사해지도록)
    def calc_style_loss(self, input, target):
        assert (input.size() == target.size())
        assert (target.requires_grad is False)
        input_mean, input_std = calc_mean_std(input)
        target_mean, target_std = calc_mean_std(target)
        return self.mse_loss(input_mean, target_mean) + self.mse_loss(input_std, target_std)

    def forward(self, content, style, alpha=1.0):
        # 콘텐츠와 스타일 중 어떤 것에 더 많은 가중치를 둘지 설정 가능
        assert 0 <= alpha <= 1 # 0에 가까울수록 콘텐츠를 많이 살림
        style_feats = self.encode_with_intermediate(style)
        content_feat = self.encode(content)
        t = adain(content_feat, style_feats[-1])
        t = alpha * t + (1 - alpha) * content_feat

        g_t = self.decoder(t) # 결과 이미지
        g_t_feats = self.encode_with_intermediate(g_t)

        # 콘텐츠 손실과 스타일 손실을 줄이기 위해 두 개의 손실 값 반환
        loss_c = self.calc_content_loss(g_t_feats[-1], t)
        loss_s = self.calc_style_loss(g_t_feats[0], style_feats[0])
        for i in range(1, 4):
            loss_s += self.calc_style_loss(g_t_feats[i], style_feats[i])
        return loss_c, loss_s

def style_transfer(vgg, decoder, content, style, alpha=1.0):
    assert (0.0 <= alpha <= 1.0)
    content_f = vgg(content)
    style_f = vgg(style)
    feat = adaptive_instance_normalization(content_f, style_f)
    feat = feat * alpha + content_f * (1 - alpha)
    return decoder(feat)

def test_transform(size=512):
    transform_list = []
    if size != 0:
        transform_list.append(transforms.Resize(size))
    transform_list.append(transforms.ToTensor())
    transform = transforms.Compose(transform_list)
    return transform

content_tf = test_transform()
style_tf = test_transform()

design_json = json.load(open("./design_gen.json", encoding='utf-8'))
def set_design(user_pt, user_st1, user_st2, design_json):
    if user_pt == '자개':
        design0 = design_json['패턴']['풀컬러'][0]
        design1 = design_json['패턴']['마블'][random.randint(0,len(design_json['패턴']['마블'])-1)]
        design2 = design0
        design3 = design_json['패턴'][user_pt][random.randint(0,len(design_json['패턴'][user_pt])-1)]
        design4 = design1

    elif user_pt == '마블':
        design0 = design_json['패턴'][user_pt][random.randint(0,len(design_json['패턴'][user_pt])-1)]
        design1 = design_json['패턴']['풀컬러'][0]
        design2 = design_json['패턴']['풀컬러'][0]
        design3 = design_json['패턴']['패턴'][random.randint(0,len(design_json['패턴']['패턴'])-1)]
        design4 = design0

    elif user_pt == '꽃잎':
        design0 = design_json['패턴'][user_pt][random.randint(0,len(design_json['패턴'][user_pt])-1)]
        design1 = design_json['패턴']['풀컬러'][0]
        design2 = design_json['패턴']['마블'][random.randint(0,len(design_json['패턴']['마블'])-1)]
        design3 = design0
        design4 = design_json['패턴']['풀컬러'][0]

    elif user_pt == '체크':
        design0 = design_json['패턴'][user_pt][random.randint(0,len(design_json['패턴'][user_pt])-1)]
        design1 = design_json['패턴']['풀컬러'][0]
        design2 = design_json['패턴']['마블'][random.randint(0,len(design_json['패턴']['마블']))-1]
        design3 = design0
        design4 = design_json['패턴']['풀컬러'][0]

    elif user_pt == '패턴':
        design0 = design_json['패턴']['풀컬러'][0]
        design1 = design_json['패턴'][user_pt][random.randint(0,len(design_json['패턴'][user_pt]))-1]
        design2 = design_json['패턴']['풀컬러'][0]
        design3 = design_json['패턴']['풀컬러'][0]
        design4 = design_json['패턴'][user_pt][random.randint(0,len(design_json['패턴'][user_pt]))-1]

    sty = design_json['그림'][user_st1][user_st2]
    
    return design0, design1, design2, design3, design4, sty

user_pt = "자개"; user_st1 = "만화"; user_st2 = 3
design0, design1, design2, design3, design4, sty = set_design(user_pt, user_st1, user_st2, design_json)

design0 = Image.open('./패턴/'+design0)
design1 = Image.open('./패턴/'+design1)
design2 = Image.open('./패턴/'+design2)
design3 = Image.open('./패턴/'+design3)
design4 = Image.open('./패턴/'+design4)
style_path = './그림/'+sty

# 이미지 생성  : 30초 정도 소요됨
fname = 'manhwa_3'
for num in tqdm(range(5)):
    content = content_tf(globals()['design{}'.format(num)])
    style = style_tf(Image.open(str(style_path)))

    style = style.to(device).unsqueeze(0)
    content = content.to(device).unsqueeze(0)
    with torch.no_grad():
        output = style_transfer(vgg, decoder, content, style, alpha=1.0)
    output = output.cpu()

    save_image(output, f'./ADAIN/{fname}_design{num}.png')

# 네일쉐입 불러오기
user_shape = 'amond.jpg'
shape_path = './shape/'+user_shape

# 생성된 디자인 불러오기
gen_path = './ADAIN/'
gen_lst = [nm for nm in os.listdir(gen_path) if nm.startswith(fname)]
print(gen_lst)

nail_shape = cv2.imread(shape_path)
gen_img = cv2.imread(gen_path+gen_lst[0])
gen_img = cv2.cvtColor(gen_img, cv2.COLOR_BGR2RGB)
gen_img = cv2.resize(gen_img, (nail_shape.shape[1], nail_shape.shape[0]))
gen_shape1 = cv2.bitwise_and(gen_img, nail_shape)

# 다섯 개 디자인 합치기
for num in range(1,5):
    gen_img = cv2.imread(gen_path+gen_lst[num])
    gen_img = cv2.cvtColor(gen_img, cv2.COLOR_BGR2RGB)
    gen_img = cv2.resize(gen_img, (nail_shape.shape[1], nail_shape.shape[0]))
    gen_shape2 = cv2.bitwise_and(gen_img, nail_shape)
    gen_shape1 = cv2.hconcat([gen_shape1, gen_shape2])
    
plt.imsave(f'./ADAIN/{fname}.jpg', gen_shape1);

