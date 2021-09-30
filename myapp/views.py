from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
from .post_spike_detection import post_req,detection
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_docments = os.path.join(BASE_DIR,'media','documents')

def my_view(request):
    print(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            # 删除所有文件
            delete_files(file_docments)
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            # rename all files
            change_name(file_docments)
            detection(file_docments)
            # filelist = detection()
            # Redirect to the document list after POST
            return redirect('my-view')
        else:
            message = '表单有错.请修复一下错误:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'list.html', context)

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
           os.rename(path, wenjianlujin[0] + '/' +str(key)+'.' + wenjianmingchafen[1])        #判断给定的路径是否是目录
    if os.path.isdir(path):
        # 如果是目录，则遍历目录列表中的所有项
        for key, x in enumerate(os.listdir(path)):
            print(key)
            name = os.path.join(path, x)
            change_name(name,key)


def delete_files(path):
    if not os.path.isdir(path) and not os.path.isfile(path):
        return False
    # 如果是文件
    if os.path.isfile(path):
        #用来区分文件目录和文件名称。2个打印内容实际中可以不写，这里主要是为了看清楚
        wenjianlujin=os.path.split(path)
        os.remove(path)        #判断给定的路径是否是目录
    if os.path.isdir(path):
        # 如果是目录，则遍历目录列表中的所有项
        for key, x in enumerate(os.listdir(path)):
            print(key)
            name = os.path.join(path, x)
            delete_files(name)