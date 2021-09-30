import os

def change_name(path,key=None):
    if not os.path.isdir(path) and not os.path.isfile(path):
        return False
    # 如果是文件
    if os.path.isfile(path):
        #用来区分文件目录和文件名称。2个打印内容实际中可以不写，这里主要是为了看清楚
        wenjianlujin=os.path.split(path)
        # print(wenjianlujin[0])  # 路径
        # print(wenjianlujin[1])   # 文件名
        # 下面这段代码主要是用来将获取到的文件名称按split方法来切割获取文件前缀和文件后缀
        wenjianmingchen = wenjianlujin[1]
        wenjianmingchafen=wenjianmingchen.split('.')
        # print(wenjianmingchafen[0])
        # print(wenjianmingchafen[1])
        #定义一个列表，用来规定哪些文件满足要改名字的后缀
        biaozhungeshi=['bmp','jpeg','gft','psd','png','jpg']
        # 　　　　根据获取到的文件后缀，在上面的列表中遍历
        if wenjianmingchafen[1] in biaozhungeshi:
           #如果遍历到需要修改的文件，用os.rename(旧名字，新名字)
           os.rename(path, wenjianlujin[0] + '/' + wenjianmingchafen[0] + '_1' + wenjianmingchafen[1])        #判断给定的路径是否是目录
    if os.path.isdir(path):
        # 如果是目录，则遍历目录列表中的所有项
        for key, x in enumerate(os.listdir(path)):
            print(key)
            name = os.path.join(path, x)
            change_name(name,key)
#定义一个需要修改的文件的目录路径
img_dir="D:\Projects\django_upload\wzyd-web\media\documents"
#将'\'转变成'/' 注意'\'需要使用\来转义
img_dir=img_dir.replace('\\','/')
#将路径当成参数传递给函数
change_name(img_dir,)