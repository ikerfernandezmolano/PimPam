from flask import Blueprint, request, redirect, render_template, flash

from app.controller.model.loan_controller import LoanController


def loan_blueprint(db):
    bp = Blueprint('loans', __name__)
    service = LoanController(db)

    @bp.route('/loans', methods=['GET', 'POST'])
    def loans():
        if request.method == 'POST':
            try:
                service.create_loan(
                    request.form['user_id'],
                    request.form['book_id'],
                )
                flash("Préstamos registrado correctamente", 'success')
            except ValueError as e:
                flash(str(e), "error")
            return redirect('/loans')

        return render_template('loans.html', loans=service.get_all())

    return bp