from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions
import os
import random

app = Flask(__name__, static_folder="static")

# BẮT BUỘC để session hoạt động
app.secret_key = "my-secret-key-123"


@app.route("/")
def index():
    # Reset khi bắt đầu lại quiz
    session["correct"] = 0
    session["wrong"] = 0

    # Tạo danh sách thứ tự câu hỏi và xáo trộn
    order = list(range(1, len(questions) + 1))
    random.shuffle(order)

    # Lưu vào session
    session["order"] = order

    return render_template("index.html", total=len(questions))


@app.route("/quiz/<int:q_id>", methods=["GET", "POST"])
def quiz(q_id):

    # Nếu vượt quá câu cuối → finish
    if q_id > len(questions):
        return redirect(url_for("finish"))

    # Nếu chưa có session thì quay về trang chủ
    if "order" not in session:
        return redirect(url_for("index"))

    # Lấy danh sách ID thật đã shuffle
    order = session["order"]

    # Lấy ID thật tương ứng với vị trí q_id
    real_id = order[q_id - 1]

    question = questions[real_id - 1]

    # Nếu user submit đáp án
    if request.method == "POST":
        user_answer = request.form.get("answer")
        correct = (user_answer == question["answer"])

        if correct:
            session["correct"] += 1
        else:
            session["wrong"] += 1

        return render_template(
            "result.html",
            question=question,
            user_answer=user_answer,
            correct=correct,
            next_id=q_id + 1
        )

    # GET → hiện câu hỏi
    return render_template("quiz.html", question=question, q_id=q_id)


@app.route("/finish")
def finish():
    correct = session.get("correct", 0)
    wrong = session.get("wrong", 0)
    total = len(questions)

    return render_template(
        "finish.html",
        correct=correct,
        wrong=wrong,
        total=total
    )


if __name__ == "__main__":
    # Cấu hình chuẩn cho Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
