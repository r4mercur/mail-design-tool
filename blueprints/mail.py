from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models.mail import Mail, db

mail_blueprint = Blueprint('mail', __name__)


@mail_blueprint.route('/list', methods=['GET'])
@login_required
def list_all_mail_templates():
    all_mail_templates = Mail.query.all()
    return render_template('mail/list.html', mails=all_mail_templates)

@mail_blueprint.route('/edit/<int:mail_id>', methods=['GET'])
@login_required
def edit_mail_template(mail_id: int):
    mail = Mail.query.get(mail_id)
    return render_template('mail/edit.html', mail=mail)


@mail_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_mail_template():
    if request.method == 'POST':
        mail = Mail()
        mail.subject = request.form['subject']
        mail.body = request.form['body']
        mail.user_id = current_user.id
        mail.save()
        flash('Mail template created successfully', 'success')
        return redirect(url_for('mail.list_all_mail_templates'))
    return render_template('mail/create.html')


@mail_blueprint.route('/save', methods=['POST'])
@login_required
def save_mail_template():
    # html from the editor
    html = request.form.get('html')

    # check if mail_id is present in the form else create a new mail template
    if request.form.get('mail_id'):
        mail = Mail.query.get(request.form['mail_id'])
        mail.subject = request.form['subject']
        mail.body = html
        # update mail in the database
        db.session.commit()

        # flash message
        flash_message = 'Mail template updated successfully'
    else:
        mail = Mail()
        mail.subject = request.form['subject']
        mail.body = html
        mail.user_id = current_user.id
        # add mail to the database
        db.session.add(mail)
        db.session.commit()

        # flash message
        flash_message = 'Mail template created successfully'

    flash(flash_message, 'success')
    return redirect(url_for('mail.list_all_mail_templates'))
