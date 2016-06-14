
from spider.wordAna.contentTool import *
from newsPredict import *
from predictTool import *
import os
ct = ContentOperator()
# urlstr = "http://toutiao.com/a6292379445978808577/"
# urlstr ="http://toutiao.com/a6292665412145365250/"
# urlstr = "http://toutiao.com/group/6292605706580803842/" #汽车
# urlstr = "http://toutiao.com/a6291989690913620225/" #美文
# urlstr = "http://toutiao.com/a6292346062074691841/" #游戏
# urlstr = "http://toutiao.com/a6280854429832233218/"  #科技
# urlstr = "http://toutiao.com/group/6291592935427604737/" #故事
# urlstr = "http://toutiao.com/a6292516516223680770/" #养生
# urlstr = "http://toutiao.com/a6292528444404973826/" #历史
# urlstr = "http://toutiao.com/a6292557068092080386/" #美食
# urlstr = "http://toutiao.com/a6292374615201153537/" #发现
# urlstr = "http://toutiao.com/a6292035179544412417/" #时尚
# urlstr = "http://toutiao.com/a6292511961298059521/" #旅游
urlstr = "http://toutiao.com/a6292830759922729218/"  #育儿
textContent, htmlContent, img_url_list = ct.getToutiaoContent(urlstr)
data_list = []
new = {}
new["id"] = "1"
new["textContent"] = textContent
data_list.append(new)
np = NewPredict(data_list)
np.getNewInfo()
test_data_file = os.path.abspath('.') + "/NavieBayesInfo/predict_new_word.txt"
model_file = os.path.abspath('.') + "/NavieBayesInfo/model.txt"
result_file = os.path.abspath('.') + "/NavieBayesInfo/predict_result.txt"
print(test_data_file)
nb = NavieBayesPredict(test_data_file,model_file,result_file)
nb.predict()