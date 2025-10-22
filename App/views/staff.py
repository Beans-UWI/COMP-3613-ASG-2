from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from.index import index_views
from App.utils.user_type_decorator import require_jwt_role

from App.controllers import (
    view_all_internships,
    create_shortlist
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/api/<string:staff_id>/list-internships', methods=['GET'])
@require_jwt_role('staff')
def list_internships(staff_id):
    internships = view_all_internships()
    return jsonify(internships), 200

@staff_views.route('/api/<string:staff_id>/add-student', methods=['POST'])
@require_jwt_role('staff')
def add_student(staff_id):
    data = request.get_json()
    student_id = data.get('student_id')
    internship_id = data.get('internship_id')

    create_shortlist(student_id, internship_id, staff_id)

    return jsonify({"message": "Student added to shortlist."}), 201