#!/usr/bin/env python
# -*- coding=utf-8 -*-

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return '<h1>The login page</h1>'

@auth_bp.route('/logout')
def logout():
    return 'Logout'
