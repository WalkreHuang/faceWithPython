import face_recognition
from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return '''
    <h1>hello,flask!</h1>
    '''

# 人脸检测
@app.route('/detect', methods=['POST'])
def detect():
    # 检测图片是否上传成功
    if 'face' not in request.files:
        return response(400, '缺少图片参数')

    face = request.files['face']
    if face.filename == '':
        return response(400, '图片没有名称')
    if not face or not allowed_file(face.filename):
        return response(400, '只能上传png,jpg,jpeg,gif格式的图片')

    detect_ret = face_detect(face)
    data = {"detect_ret": detect_ret}
    return response(200, '', data)

# 人脸比对
@app.route('/compare', methods=['POST'])
def compare():
    # 检测图片是否上传成功
    if 'face1' not in request.files or 'face2' not in request.files:
        return response(400, '缺少图片参数')

    face1 = request.files['face1']
    face2 = request.files['face2']
    if face1.filename == '' or face2.filename == '':
        return response(400, '图片没有名称')
    if not face1 or not allowed_file(face1.filename):
        return response(400, 'face1只能上传png,jpg,jpeg,gif格式的图片')
    if not face2 or not allowed_file(face2.filename):
        return response(400, 'face2只能上传png,jpg,jpeg,gif格式的图片')

    detect_ret = compare_two_face_images(face1, face2)
    data = {"detect_ret": detect_ret}
    return response(200, '', data)

def face_detect(img_stream):
    img = face_recognition.load_image_file(img_stream)
    img_face_encodings = face_recognition.face_encodings(img)
    return len(img_face_encodings) > 0 

def compare_two_face_images(face_stream1, face_stream2):
    img1 = face_recognition.load_image_file(face_stream1)
    img1_face_encodings = face_recognition.face_encodings(img1)

    img2 = face_recognition.load_image_file(face_stream2)
    img2_face_encodings = face_recognition.face_encodings(img2)

    is_same_person = False
    if len(img1_face_encodings) > 0 and len(img2_face_encodings) > 0:
        match_results = face_recognition.compare_faces(img1_face_encodings, img2_face_encodings[0])
        if match_results[0]:
            is_same_person = True
    return is_same_person

def response(code, error, data = ''):
    result = {"code":code,"error":error,"data":data}
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
