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

def solver(problem):
    problem = problem.replace("x", "*").replace("=", "==")
    alphabet = sorted(set(filter(str.isalpha, problem)))
    for numbers in itertools.permutations("0123456789", len(alphabet)):
        exp = problem
        for a, n in zip(alphabet, numbers):
            exp = exp.replace(a, n)
        try:
            if eval(exp):
                return " ".join(f"{c}: {n}" for c, n in zip(alphabet, numbers))
        except:
            pass
    return "答えが見つかりませんでした"
        

if __name__ == '__main__':
    app.run()
