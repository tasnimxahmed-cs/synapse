from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return redirect('/dashboard')
