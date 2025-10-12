from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    view_response,
    view_all_shortlists
)

from App.controllers import *

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/api/<string:student_id>/view-all-shortlist', methods=['GET'])
def view_all_shortlist(student_id):
    shortlists = view_all_shortlists(student_id, user_type="student")
    return jsonify(shortlists), 200

@student_views.route('/api/<string:student_id>/view-employer-response/<int:shortlist_id>', methods=['GET'])
def view_employer_response(student_id, shortlist_id):
    employer_response = view_response(shortlist_id)
    return jsonify(employer_response), 200