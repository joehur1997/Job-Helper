from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from JobHelper.auth import login_required
from JobHelper.db import get_db

bp = Blueprint('jobpost', __name__)

@bp.route('/') #code for creating index(blog) view
def index():
    db = get_db()
    jobPosts = db.execute(
        'SELECT p.id, jobtitle, jobURL, applydate, poster_id, username'
        ' FROM jobPost p JOIN user u ON p.poster_id = u.id'
        ' ORDER BY applydate DESC'
    ).fetchall()
    return render_template('jobpost/index.html', jobPosts=jobPosts)

@bp.route('/create', methods=('GET', 'POST')) #view for creating a post for blog
@login_required
def create():
    if request.method == 'POST' :
        jobtitle = request.form['jobtitle']
        jobURL = request.form['jobURL']
        error = None

        if not jobtitle:
            error = 'Job Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO jobPost (jobtitle, jobURL, poster_id)'
                ' VALUES (?, ?, ?)',
                (jobtitle, jobURL, g.user['id'])
            )
            db.commit()
            return redirect(url_for('jobpost.index'))

    return render_template('jobpost/create.html')

def get_jobPost(id, check_poster=True):
    jobPost = get_db().execute(
        'SELECT p.id, jobtitle, jobURL, applydate, poster_id, username'
        ' FROM jobPost p JOIN user u ON p.poster_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if jobPost is None:
        abort(404, f"Post id {id} doesn't exist.")
    
    if check_poster and jobPost['poster_id'] != g.user['id']:
        abort(403)
    
    return jobPost

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id): #repurpose this so user can update job status
    jobPost = get_jobPost(id)

    if request.method == 'POST':
        jobtitle = request.form['jobtitle']
        jobURL = request.form['jobURL']
        error = None

        if not jobtitle:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE jobPost SET jobtitle = ?, jobURL = ?'
                ' WHERE id = ?',
                (jobtitle, jobURL, id)
            )
            db.commit()
            return redirect(url_for('jobpost.index'))

    return render_template('jobpost/update.html', jobPost=jobPost)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_jobPost(id)
    db = get_db()
    db.execute('DELETE FROM jobPost WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('jobpost.index'))