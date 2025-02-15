from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.goal import Goal
from app.models.task import Task
from .routes_helpers import *


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# CREATE
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_body = dict(goal=to_dict(new_goal))

    return make_response(jsonify(response_body), 201)

# READ
@goals_bp.route("", methods=["GET"])
def handle_goals():
    goals = query_sort(Goal)

    response_body = [to_dict(goal) for goal in goals]

    return make_response(jsonify(response_body),200)

@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response_body = dict(goal=to_dict(goal))

    return make_response(jsonify(response_body), 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def handle_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [to_dict(task) for task in goal.tasks]

    response_body = dict(id=goal.id, tasks=tasks_response, title=goal.title)
    
    return make_response(jsonify(response_body), 200)

# UPDATE
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body['title'],
    
    db.session.commit()

    response_body = dict(goal=to_dict(goal))

    return make_response(jsonify(response_body), 200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    tasks = Task.query.filter(Task.id.in_(request_body['task_ids']))
    for task in tasks:
        goal.tasks.append(task)
    
    db.session.commit()

    added_task_ids = [task.id for task in goal.tasks]
    response_body = dict(id=goal.id , task_ids=added_task_ids)

    return make_response(jsonify(response_body), 200)

# DELETE
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    response_body = dict(details=f'Goal {goal.id} "{goal.title}" successfully deleted')
    return make_response(jsonify(response_body), 200)

