from flask import Flask, render_template,request,Response
import os
import re,requests
import docker
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = docker.DockerClient(base_url='unix://var/run/docker.sock')
class Image():
    def __init__(self,name,tag,size,id):
        self.name=name
        self.tag=tag
        self.size=size
        self.id=id
@app.route("/")
def test():
    response = requests.get('http://10.0.10.141:5004/getlist')
    s = response.text.replace('\n', ' ')
    pattern = re.compile(r'\S+')
    list1= pattern.findall(s)
    images_temp = list1[6:]
    length=len(images_temp)
    images=[]
    i=0
    k=0
    while(i<length):
        image=Image(images_temp[i],images_temp[i+1],images_temp[i+6],k)
        images.append(image)
        i=i+7
        k=k+1
    return render_template("test.html",list=images)

@app.route("/getlist")
def get_list():
    res=os.popen("docker images")
    return res.read()
@app.route("/save/")
def save():
    image=request.args.get('image',None)
    if not image:
        return "未输入镜像名称"
    tag=request.args.get('tag',None)
    filename=image+'-'+tag+'.tgz'
    res=os.popen("docker save -o {} {}:{}".format(filename,image,tag))
    return filename
@app.route("/pull/")
def pull():
    image_name = request.args.get('image', None)
    if not image_name:
        return "未输入镜像名称"
    tag = request.args.get('tag', "latest")
    arch = request.args.get('arch', None)
    if arch is None:
        res = os.popen("docker pull {}:{}".format(image_name, tag))

    else:
        res = os.popen("docker pull --platform {} {}:{}".format(arch, image_name, tag))
    return res.read()

@app.route("/download/")
def download():
    image=request.args.get('image',None)
    if not image:
        return "未输入镜像名称"
    tag=request.args.get('tag',"latest")
    img=client.images.get("{}:{}".format(image,tag))
    filename=image+'-'+tag+'.tgz'

    def send_file():
        for data in img.save():
            yield data
    response=Response(send_file(),content_type='application/octet-stream')
    response.headers['Content-disposition'] = 'attachment; filename=%s'%filename
    return response

if __name__ == "__main__":

    app.run(port=5000,host='0.0.0.0')

