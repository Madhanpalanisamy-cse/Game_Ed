from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import GameData

app = Flask(__name__)
game_data = GameData()

@app.route('/')
def index():
    return render_template('index.html', student=game_data.student, tasks=game_data.tasks, questions=game_data.questions)

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    success, level_up = game_data.complete_task(task_id)
    return jsonify({"success": success, "level_up": level_up, "student": game_data.student.to_dict()})

@app.route('/solve/<int:question_id>', methods=['POST'])
def solve(question_id):
    answer = request.json.get('answer')
    success, level_up, message = game_data.solve_question(question_id, answer)
    return jsonify({
        "success": success, 
        "level_up": level_up, 
        "message": message, 
        "student": game_data.student.to_dict()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
