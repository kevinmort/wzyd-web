from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Document
from .forms import DocumentForm
from .post_spike_detection import post_req,detection
import os,time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_docments = os.path.join(BASE_DIR,'media','documents')
count = ''
def my_view(request):
    message = '请上传1个待检测的文件'
    count = ""
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
            count = str(detection(file_docments))
            # filelist = detection()
            # Redirect to the document list after POST
            request.Count = count
            # return redirect('my-view', username=request.Count)
            return redirect(f"{reverse('my-view')}?count={count}")
            # return HttpResponseRedirect(reverse('getting_started_info', kwargs={'count': count}))
            # return redirect(f"{reverse('my-view')}?count='How to redirect with arguments'")

        else:
            message = '表单有错.请修复一下错误:'
    else:
        # print(request)
        count = request.GET.get('count', default='')
        if count != '':
            message1 = '发现钉子'
            message2 = '发现'+count+"个钉子"
        else:
            message1 = '没有发现钉子'
            message2 = ''
        # print("count: ", count)
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    random = int(round(time.time() * 1000000))
    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message, 'count': count,'random':random,'message1':message1,'message2':message2}
    return render(request, 'list.html', context)

def change_name(path,key=None):
    if not os.path.isdir(path) and not os.path.isfile(path):
        return False
    # 如果是文件
    if os.path.isfile(path):
        #用来区分文件目录和文件名称。2个打印内容实际中可以不写，这里主要是为了看清楚
        wenjianlujin=os.path.split(path)
        # print(wenjianlujin[0])  # 路径
        print(wenjianlujin[1])   # 文件名
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
        file_list = []
        for key, x in enumerate(os.listdir(path)):
            # print(key)
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
            # print(key)
            name = os.path.join(path, x)
            delete_files(name)

