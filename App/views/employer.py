from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_internship_position,
    view_shortlist_by_internship_id,
    view_all_shortlists,
    accept_student,
    reject_student
)

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

@employer_views.route('/api/<string:employer_id>/create-internship', methods=['POST'])
def create_internship(employer_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    duration_in_months = data.get('durationInMonths')
    salary = data.get('salary')

    create_internship_position(title, description, location, duration_in_months, salary, employer_id)

    return jsonify({"message": "Internship created successfully."}), 201


@employer_views.route('/api/<string:employer_id>/view-shortlist/<int:internship_id>', methods=['GET'])
def view_shortlist(employer_id, internship_id):
    shortlist = view_shortlist_by_internship_id(internship_id)
    return jsonify(shortlist), 200

@employer_views.route('/api/<string:employer_id>/view-all-shortlist', methods=['GET'])
def view_all_shortlist(employer_id):
    shortlists = view_all_shortlists(employer_id, user_type="employer")
    return jsonify(shortlists), 200

@employer_views.route('/api/<string:employer_id>/accept-student/<int:shortlist_id>', methods=['POST'])
def accept_student_route(employer_id, shortlist_id):
    accept_student(shortlist_id)
    return jsonify({"message": "Student accepted."}), 200

@employer_views.route('/api/<string:employer_id>/reject-student/<int:shortlist_id>', methods=['POST'])
def reject_student_route(employer_id, shortlist_id):
    reject_student(shortlist_id)
    return jsonify({"message": "Student rejected."}), 200