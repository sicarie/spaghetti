from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import User, Group, UserGroup
from . import db

bp = Blueprint('user_group', __name__)

@bp.route('/user/<int:user_id>/groups', methods=['GET'])
@login_required
def get_user_groups(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.id != user.id:
        return jsonify({"message": "Access denied"}), 403
    groups = [group.name for group in user.groups]
    return jsonify({"groups": groups}), 200

@bp.route('/group', methods=['POST'])
@login_required
def create_group():
    data = request.get_json()
    name = data.get('name')
    if Group.query.filter_by(name=name).first():
        return jsonify({"message": "Group already exists"}), 400
    new_group = Group(name=name)
    db.session.add(new_group)
    db.session.commit()
    return jsonify({"message": "Group created successfully"}), 201

@bp.route('/user/<int:user_id>/group/<int:group_id>', methods=['POST'])
@login_required
def add_user_to_group(user_id, group_id):
    user = User.query.get_or_404(user_id)
    group = Group.query.get_or_404(group_id)
    if current_user.id != user.id:
        return jsonify({"message": "Access denied"}), 403
    if group in user.groups:
        return jsonify({"message": "User already in group"}), 400
    user.groups.append(group)
    db.session.commit()
    return jsonify({"message": "User added to group successfully"}), 200

@bp.route('/user/<int:user_id>/group/<int:group_id>', methods=['DELETE'])
@login_required
def remove_user_from_group(user_id, group_id):
    user = User.query.get_or_404(user_id)
    group = Group.query.get_or_404(group_id)
    if current_user.id != user.id:
        return jsonify({"message": "Access denied"}), 403
    if group not in user.groups:
        return jsonify({"message": "User not in group"}), 400
    user.groups.remove(group)
    db.session.commit()
    return jsonify({"message": "User removed from group successfully"}), 200
