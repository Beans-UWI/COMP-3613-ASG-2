from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    view_response,
    view_all_shortlists
)

from App.controllers import *

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/api/student/view-all-shortlist', methods=['GET'])
def view_all_shortlist():
    shortlists = view_all_shortlists()
    return jsonify(shortlists), 200

@student_views.route('/api/student/view-employer-response/<int:shortlist_id>', methods=['GET'])
def view_employer_response(shortlist_id):
    employer_response = view_response(shortlist_id)
    return jsonify(employer_response), 200