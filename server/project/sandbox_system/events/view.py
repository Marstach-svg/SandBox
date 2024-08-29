from flask import Blueprint,render_template, url_for, redirect, abort, flash, request
from flask_login import login_required, current_user

from sandbox_system import db
from sandbox_system.models import Event
from sandbox_system.events.form import EventForm
from sandbox_system.blogs.image import add_image


events = Blueprint('events', __name__)


#イベントトップページ
@events.route('/event_index', methods=['GET'])
def event_index():
    page = request.args.get('page', 1, type=int)
    if Event.query.filter_by(category='ハッカソン').first():
        hackathon_events = Event.query.filter_by(category='ハッカソン').order_by(Event.id.desc()).paginate(page=page, per_page=3)
    else:
        hackathon_events = ''
    if Event.query.filter_by(category='就活').first():
        job_search_events = Event.query.filter_by(category='就活').order_by(Event.id.desc()).paginate(page=page, per_page=3)
    else:
        job_search_events = ''
    return render_template('event/event_index.html', hackathon_events=hackathon_events, job_search_events=job_search_events)

#ハッカソン情報一覧
@events.route('/hackathon_event', methods=['GET', 'POST'])
def hackathon_event():
    page = request.args.get('page', 1, type=int)
    if Event.query.filter_by(category='ハッカソン').first():
        hackathon_events = Event.query.filter_by(category='ハッカソン').order_by(Event.id.desc()).paginate(page=page, per_page=10)
    else:
        hackathon_events = ''
    if Event.query.filter_by(category='就活').first():
        recent_job_search_events = Event.query.filter_by(category='就活').order_by(Event.id.desc()).limit(3).all()
    else:
        recent_job_search_events = ''
    return render_template('event/hackathon_event.html', hackathon_events=hackathon_events, recent_job_search_events=recent_job_search_events)

#就活情報一覧
@events.route('/job_search_event', methods=['GET', 'POST'])
def job_search_event():
    page = request.args.get('page', 1, type=int)
    if Event.query.filter_by(category='就活').first():
        job_search_events = Event.query.filter_by(category='就活').order_by(Event.id.desc()).paginate(page=page, per_page=10)
    else:
        job_search_events = ''
    if Event.query.filter_by(category='ハッカソン').first():
        recent_hackathon_events = Event.query.filter_by(category='ハッカソン').order_by(Event.id.desc()).limit(3).all()
    else:
        recent_hackathon_events = ''
    return render_template('event/job_search_event.html', job_search_events=job_search_events, recent_hackathon_events=recent_hackathon_events)

#ハッカソン検索
@events.route('/hackathon_event_search', methods=['GET', 'POST'])
def hackathon_event_search():
    if request.form.get('hackathon_event_search'):
        searchtext = request.form.get('hackathon_event_search')
    else:
        searchtext = ''
    page = request.args.get('page', 1, type=int)
    if Event.query.filter_by(category='ハッカソン').filter((Event.text.contains(searchtext)) | (Event.title.contains(searchtext)) | (Event.summary.contains(searchtext))).first():
        hackathon_events = Event.query.filter_by(category='ハッカソン').filter((Event.text.contains(searchtext)) | (Event.title.contains(searchtext)) | (Event.summary.contains(searchtext))).order_by(Event.id.desc()).paginate(page=page, per_page=10)
    else:
        hackathon_events = ''
    if Event.query.filter_by(category='就活').first():
        recent_job_search_events = Event.query.filter_by(category='就活').order_by(Event.id.desc()).limit(3).all()
    else:
        recent_job_search_events = ''
    return render_template('event/hackathon_event.html', hackathon_events=hackathon_events, searchtext=searchtext, recent_job_search_events=recent_job_search_events)

#就活検索
@events.route('/job_search_event_search', methods=['GET', 'POST'])
def job_search_event_search():
    if request.form.get('job_search_event_search'):
        searchtext = request.form.get('job_search_event_search')
    else:
        searchtext = ''
    page = request.args.get('page', 1, type=int)
    if Event.query.filter_by(category='就活').filter((Event.text.contains(searchtext)) | (Event.title.contains(searchtext)) | (Event.summary.contains(searchtext))).first():
        job_search_events = Event.query.filter_by(category='就活').filter((Event.text.contains(searchtext)) | (Event.title.contains(searchtext)) | (Event.summary.contains(searchtext))).order_by(Event.id.desc()).paginate(page=page, per_page=10)
    else:
        job_search_events = ''
    if Event.query.filter_by(category='ハッカソン').first():
        recent_hackathon_events = Event.query.filter_by(category='ハッカソン').order_by(Event.id.desc()).limit(3).all()
    else:
        recent_hackathon_events = ''
    return render_template('event/job_search_event.html', job_search_events=job_search_events, searchtext=searchtext, recent_hackathon_events=recent_hackathon_events)

#ハッカソン情報追加
@events.route('/add_hackathon_event', methods=['GET', 'POST'])
@login_required
def add_hackathon_event():
    if not current_user.is_administrator():
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        if form.category.data == 'ハッカソン':
            if form.picture.data:
                picture = add_image(form.picture.data)
            else:
                picture = ''
            hackathon_event = Event(category=form.category.data, title=form.title.data, summary=form.summary.data, text=form.text.data, url=form.url.data, image=picture)
            db.session.add(hackathon_event)
            db.session.commit()
            flash('ハッカソン情報が追加されました')
            return redirect(url_for('events.hackathon_event'))
        else:
            flash('カテゴリ名が間違っています')
            return redirect(url_for('events.hackathon_event'))
    return render_template('event/add_event.html', form=form)

#ハッカソン情報削除
@events.route('/<int:hackathon_event_id>/delete_hackathon_event', methods=['GET', 'POST'])
@login_required
def delete_hackathon_event(hackathon_event_id):
    if not current_user.is_administrator():
        abort(403)
    hackathon_event = Event.query.filter_by(category='ハッカソン', id=hackathon_event_id).first()
    db.session.delete(hackathon_event)
    db.session.commit()
    flash('ハッカソン情報を削除しました')
    return redirect(url_for('events.hackathon_event'))

#就活情報追加
@events.route('/add_job_search_event', methods=['GET', 'POST'])
@login_required
def add_job_search_event():
    if not current_user.is_administrator():
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        if form.category.data == '就活':
            if form.picture.data:
                picture = add_image(form.picture.data)
            else:
                picture = ''
            job_search_event = Event(category=form.category.data, title=form.title.data, summary=form.summary.data, text=form.text.data, url=form.url.data, image=picture)
            db.session.add(job_search_event)
            db.session.commit()
            flash('就活情報が追加されました')
            return redirect(url_for('events.job_search_event'))
        else:
            flash('カテゴリ名が間違っています')
            return redirect(url_for('events.job_search_event'))
    return render_template('event/add_event.html', form=form)

#就活情報削除
@events.route('/<int:job_search_event_id>/delete_job_search__event', methods=['GET', 'POST'])
@login_required
def delete_job_search_event(job_search_event_id):
    if not current_user.is_administrator():
        abort(403)
    job_search_event = Event.query.filter_by(category='就活', id=job_search_event_id).first()
    db.session.delete(job_search_event)
    db.session.commit()
    flash('就活情報を削除しました')
    return redirect(url_for('events.job_search_event'))