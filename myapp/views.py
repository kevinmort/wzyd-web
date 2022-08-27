from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Document
from .forms import DocumentForm
from .post_spike_detection import post_req,detection
import os,time,json
from django.conf import settings
from django.http import JsonResponse
BASE_DIR = os.getcwd()
# print('BASE_DIR:',BASE_DIR)

file_docments = os.path.join(BASE_DIR,'media','documents')
# print('join:',file_docments)

# print('API_URL:', getattr(settings, "API_URL", "取不到就给一个默认值"))
# setattr(settings,"API_URL","https://127.149.212.37:30080/xdjc")
# print('API_URL:', getattr(settings, "API_URL", "取不到就给一个默认值"))


@require_POST
def change_api_url_post(request):
    url = request.POST.get('url_info')   # url新地址参数
    print('1:',url)
    setattr(settings, "API_URL", url)
    print('2 API_URL:', getattr(settings, "API_URL", "取不到就给一个默认值"))
    result = {'Code': 1000, 'Message': 'OK', 'url': url}
    return JsonResponse(result)


# def change_api_url_get(request):
#     url = getattr(settings, "API_URL", "https://117.149.212.37:30080/xdjc")
#     if url is not None:
#         result = {'Code': 0, 'Message': 'Succeeded: api url changed', 'url': url}
#     else:
#         result = {'Code': 503, 'Message': 'Failed: api url not changed', 'url': ''}
#     return JsonResponse(result)


def my_view(request):
    message = '请上传1个待检测的文件'
    message1 = ''
    message2=''
    count = ""
    ding_url = getattr(settings, "API_URL")  # 默认url
    mao_url = getattr(settings, "MAO_URL")  # 默认url
    # Handle file upload
    bg_img_flag = 0
    null_count_flag = 0
    if request.method == 'POST':
        function_info = request.POST.get('function_info')  # 获取功能参数
        form = DocumentForm(request.POST, request.FILES)
        print(function_info, request.FILES)
        if form.is_valid():
            # 删除所有文件
            delete_files(file_docments)
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            # rename all files
            change_name(file_docments)
            if function_info == 'ding':
                respone_raw = detection(file_docments,ding_url,function_info)
                result = json.loads(respone_raw)
                count = len(result['Response'][2])
                positons = str(result['Response'][2])
            elif function_info == 'mao':
                respone_raw = detection(file_docments,mao_url,function_info)
            elif function_info == "face":
                pass

            print('------------------positons:', positons)
            # filelist = detection()
            # Redirect to the document list after POST
            # return redirect('my-view')
            return redirect(f"{reverse('my-view')}?count={count}&positons={positons}")
            # return HttpResponseRedirect(reverse('getting_started_info', kwargs={'count': count}))
            # return redirect(f"{reverse('my-view')}?count='How to redirect with arguments'")

        else:
            message = '表单有错.请修复一下错误:'
    else: # GET
        print(request)
        count = request.GET.get('count', default=None)
        positons = request.GET.get('positons', default=None)
        if count is not None and positons is not None:
            if int(count) >= 1:
                message1 = '不合格，发现钉子 '+count+'个'
                message2 = "坐标："+ positons
                bg_img_flag = 1
                null_count_flag = 0

            elif int(count) == 0:
                message1 = '合格'
                message2 = '没有发现钉子'
                bg_img_flag = 1
                null_count_flag = 1
        else:
            message1 = '还未上传图片'
            message2 = '请上传图片'
            bg_img_flag = 0
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    random = int(round(time.time() * 1000000))
    # Render list page with the documents and the form
    context = {'documents': documents,
               'form': form, 'message': message,
               'api_url': ding_url,
               'count': count,
               'random':random,
               'message1':message1,
               'message2':message2,
               'bg_img_flag':bg_img_flag,
               'null_count_flag':null_count_flag,
               }
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
        biaozhungeshi=['jpeg','jpg']
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

