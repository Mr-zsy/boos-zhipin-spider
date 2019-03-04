from flask import Flask, jsonify, request, render_template
# from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__,static_url_path='')
# CORS(app, supports_credentials=True)

app.config.update(
    MONGO_URI='mongodb://localhost:27017/bs',
)
mongo = PyMongo(app)
table = mongo.db.info


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/baseMsg', methods=['POST'])
def baseMsg():

    base = request.form['base']
    kind = request.form['position']

    positionNum = table.find({'base':base, "kind":kind}).count()
    try:
        eduBgNum1 = table.find({'base':base, 'eduBg':'硕士', "kind":kind}).count()
    except ZeroDivisionError:
        eduBgNum1 = 0
    try:
        eduBgNum2 = table.find({'base':base, 'eduBg':'本科', "kind":kind}).count()
    except ZeroDivisionError:
        eduBgNum2 = 0
    try:
        eduBgNum3 = table.find({'base': base, 'eduBg': '大专', "kind":kind}).count()
    except ZeroDivisionError:
        eduBgNum3 = 0
    try:
        eduBgNum4 = table.find({'base': base, 'eduBg': '学历不限', "kind":kind}).count()
    except ZeroDivisionError:
        eduBgNum4 = 0

    eduBgNum = {
        "硕士" : eduBgNum1,
        "本科": eduBgNum2,
        "大专": eduBgNum3,
        "学历不限": eduBgNum4

    }

    month = {
        1:'',
        2:'',
        3:'',
        4:'',
        5:'',
        6:'',
        7:'',
        8:'',
        9:'',
        10:'',
        11:'',
        12:''
    }


    for i in range(1,13):

        num = table.find({'base':base, "kind":kind, 'updateMonth':i}).count()
        minPaymentAvg = table.aggregate([
            {
                '$match': {'base':base, 'updateMonth':i}
            },
            {
                '$group': {'_id': 'null', 'minPayment_avg': {'$avg': '$minPayment'}}
            }
        ])
        maxPaymentAvg = table.aggregate([
            {
                '$match': {'base': base, 'updateMonth': i}
            },
            {
                '$group': {'_id': 'null', 'maxPayment_avg': {'$avg': '$maxPayment'}}
            }
        ])

        min = 0
        max = 0
        for j in minPaymentAvg:
            min = '%.2f'%j['minPayment_avg']
        for j in maxPaymentAvg:
            max = '%.2f'%j['maxPayment_avg']
        month[i] = {
            'min':min,
            'max':max,
            'positionNum':num
        }

    result = {
        "month" : month,
        "positionNum" : positionNum,
        "eduBgNum" : eduBgNum
    }

    return  jsonify(result)



@app.route('/payment1', methods=['POST'])
def payment1():
    kind = request.form['position']
    baseList = ['北京', '上海', '广州', '深圳', '杭州', '天津', '西安', '成都', '武汉']
    list = []
    for base in baseList:
        minPaymentAvg = table.aggregate([
            {
                '$match': {'base': base, 'kind': kind}
            },
            {
                '$group': {'_id': 'null', 'minPayment_avg': {'$avg': '$minPayment'}}
            }
        ])
        maxPaymentAvg = table.aggregate([
            {
                '$match': {'base': base, 'kind': kind}
            },
            {
                '$group': {'_id': 'null', 'maxPayment_avg': {'$avg': '$maxPayment'}}
            }
        ])

        min = 0
        max = 0
        for j in minPaymentAvg:
            min = '%.2f' % j['minPayment_avg']
        for j in maxPaymentAvg:
            max = '%.2f' % j['maxPayment_avg']
        list.append({
            'base':base,
            'min':min,
            'max':max
        })
    return jsonify({
        'list':list
    })

@app.route('/payment2', methods=['POST'])
def payment2():
    base = request.form['base']
    kindList = ['Python', "Java", "Web前端", 'C++']
    list = []
    for kind in kindList:
        minPaymentAvg = table.aggregate([
            {
                '$match': {'base': base, 'kind': kind}
            },
            {
                '$group': {'_id': 'null', 'minPayment_avg': {'$avg': '$minPayment'}}
            }
        ])
        maxPaymentAvg = table.aggregate([
            {
                '$match': {'base': base, 'kind': kind}
            },
            {
                '$group': {'_id': 'null', 'maxPayment_avg': {'$avg': '$maxPayment'}}
            }
        ])

        min = 0
        max = 0
        for j in minPaymentAvg:
            min = '%.2f' % j['minPayment_avg']
        for j in maxPaymentAvg:
            max = '%.2f' % j['maxPayment_avg']
        list.append({
            'position': kind,
            'min': min,
            'max': max
        })
    return jsonify({
        'list':list
    })



#TEST

@app.route('/post_create_data', methods=["POST"])
def test():
    return {
        'hhh':'hahh'
    }

if __name__ == '__main__':
    app.run()
