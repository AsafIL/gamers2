from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from  sqlalchemy.sql.expression import func, select


def matching(current_user, matched_user):
    ''' This function gets as parameters 2 users and returns a matching grade to them using their
    profile.'''
    grade = 0
    if abs(int(current_user.age) - int(matched_user.age)) <= 2:
        grade += 15
    if current_user.country == matched_user.country:
        grade += 10
    if current_user.league_player == True and matched_user.league_player == True:
        grade += 10
    if current_user.fortnite_player and matched_user.fortnite_player:
        grade += 10
    if current_user.cs_player == True and matched_user.cs_player == True:
        grade += 10
    if current_user.minecraft_player == True and matched_user.minecraft_player == True:
        grade += 10
    if current_user.r6_player == True and matched_user.r6_player == True:
        grade += 10
    if current_user.cod_player == True and matched_user.cod_player == True:
        grade += 10

    return grade
