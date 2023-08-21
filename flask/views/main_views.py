from flask import Flask, Blueprint, session, render_template, request, make_response, jsonify, redirect, url_for


dashbord_abtest =  Blueprint('dashbord', __name__)


# @dashbord_abtest.route('/')
# def index():
#     render_template('index.html')
#     # return render_template('loop.html', values=value_list)