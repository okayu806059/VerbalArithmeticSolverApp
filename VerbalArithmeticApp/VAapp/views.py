from flask import Flask, render_template, request
import itertools

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    if request.method == 'POST':
        question = request.form.get('question')
        answer = solver(question)
    return render_template("solver.html", answer=answer)

def solver(s):
    s = s.replace(" ", "")
    left_terms = []
    now = 0
    alphabet = []
    equal = 0
    right_term = ""
    operation = ['+', '-', 'x', '/']
    ope_num = [0]
    ZeroNine = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    # 式に含まれる項と登場する文字をリスト化
    for i in range(len(s)):
        if s[i] not in alphabet and s[i] not in operation and s[i] != '=' and s[i] not in ZeroNine:
            alphabet.append(s[i])
        if s[i] in operation:
            tmp = s[now:i]
            left_terms.append(tmp)
            now = i + 1
            if s[i] == '+':
                ope_num.append(0)
            elif s[i] == '-':
                ope_num.append(1)
            elif s[i] == 'x':
                ope_num.append(2)
            else:
                ope_num.append(3)
        if s[i] == '=':
            equal = i
            left_terms.append(s[now:equal])
            right_term = s[equal+1:]

    # 登場した文字をソート
    alphabet = sorted(alphabet) 

    number = len(alphabet)
    # ０〜９の中から答えの候補を全探索
    for i in itertools.permutations(ZeroNine, number):
        cur = list(i)
        answer = {}

        # 各文字についての対応表を作る
        for j in range(number):
            answer[alphabet[j]] = cur[j]
        # 対応表に基づき、数式を作る
        ok = 1

        # 左辺の計算
        Leftside, Rightside = 0, 0
        for j in range(len(left_terms)):
            # 数式の復元
            tmp = ""
            for k in left_terms[j]:
                if k in ZeroNine:
                    tmp += k
                else:
                    tmp += answer[k]
            if tmp[0] == '0':
                ok = 0
            else:
                if ope_num[j] == 0:
                    Leftside += int(tmp)
                elif ope_num[j] == 1:
                    Leftside -= int(tmp)
                elif ope_num[j] == 2:
                    Leftside *= int(tmp)
                else:
                    Leftside /= int(tmp)

        # 右辺の計算
        tmp = ""
        for k in right_term:
            if k in ZeroNine:
                tmp += k
            else:
                tmp += answer[k]
        if tmp[0] == '0':
            ok = 0
        Rightside += int(tmp)

        # ok では、最高位が0出ないという条件を満たしているかを確認している
        if ok == 1:
            if Leftside == Rightside:
                res = ""
                for key in answer:
                    res += str(key)
                    res += ": "
                    res += str(answer[key])
                    res += " "
                return res
    return "答えが見つかりませんでした"
        

if __name__ == '__main__':
    app.run()