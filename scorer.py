def score_answers(student_answers, answer_key):
    score = 0
    per_question = {}
    for q, correct_ans_list in answer_key.items():
        marked = student_answers.get(q, [])
        per_question[f"Q{q}"] = ",".join(marked)
        if set(marked) == set(correct_ans_list):
            score += 1
    return score, per_question