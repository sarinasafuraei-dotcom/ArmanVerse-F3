
from flask import Flask, render_template, request
from questions_data import questions

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/questions")
def show_questions():
    return render_template("question.html", questions=questions)


@app.route("/submit", methods=["POST"])
def submit():
    results = []
    correct_count = 0
    counted_questions = 0

    for question in questions:
        question_id = question["id"]
        selected_value = request.form.get(f"answer_{question_id}")

        try:
            selected_option = int(selected_value)
        except (TypeError, ValueError):
            selected_option = None

        options = question.get("options", [])

        if (
            selected_option is not None
            and not 1 <= selected_option <= len(options)
        ):
            selected_option = None

        is_excluded = question.get("answer_mode") == "reveal_only"

        if is_excluded:
            is_correct = None
        else:
            counted_questions += 1
            correct_index = question.get("correct_index")

            is_correct = (
                selected_option is not None
                and correct_index is not None
                and selected_option == correct_index + 1
            )

            if is_correct:
                correct_count += 1

        results.append({
            "question": question,
            "selected_option": selected_option,
            "is_correct": is_correct,
            "is_excluded": is_excluded
        })

    percentage = round(
        correct_count / counted_questions * 100
    ) if counted_questions else 0

    if percentage >= 90:
        message = "فوق‌العاده بود! تسلطت به فیزیک تحسین‌برانگیز است."
    elif percentage >= 70:
        message = "آفرین! عملکرد خیلی خوبی داشتی."
    elif percentage >= 50:
        message = "خوب پیش رفتی! با کمی تمرین بهتر هم می‌شی."
    else:
        message = "ناامید نشو! هر سؤال فرصتی برای یادگیری بیشتره."

    return render_template(
        "result.html",
        results=results,
        correct_count=correct_count,
        total_questions=counted_questions,
        percentage=percentage,
        message=message
    )


@app.route("/answers")
def answers():
    return render_template("answers.html")


if __name__ == "__main__":
    app.run(debug=True)
