from flask import Flask, flash, redirect, render_template, request

from model.contacts import Contacts

app = Flask(__name__)
app.secret_key = b"much secret"

Contacts.load_db()


@app.route("/")
def index():
    return redirect("/contacts")


@app.route("/contacts")
def get_contacts():
    q = request.args.get("q")
    if q is not None:
        contacts = Contacts.search(q)
    else:
        contacts = Contacts.all()

    return render_template("index.html", contacts=contacts)


@app.route("/contacts/new", methods=["GET"])
def get_new_contact():
    return render_template("new_contact.html", contact=Contacts())


@app.route("/contacts/new", methods=["POST"])
def post_new_contact():
    c = Contacts(
        None,
        request.form["first_name"],
        request.form["last_name"],
        request.form["phone"],
        request.form["email"],
    )
    if c.save():
        flash("Created new contact!")
        return redirect("/contacts")
    else:
        return render_template("new_contact.html", contact=c)


@app.route("/contacts/<id>")
def get_contact(id):
    c = Contacts.find(id)
    return render_template("contact.html", contact=c)


@app.route("/contacts/<id>/edit", methods=["GET"])
def get_edit_contact(id):
    c = Contacts.find(id)
    return render_template("edit_contact.html", contact=c)


@app.route("/contacts/<id>/edit", methods=["POST"])
def post_edit_contact(id):
    c = Contacts.find(id)
    c.update(
        request.form["first_name"],
        request.form["last_name"],
        request.form["phone"],
        request.form["email"],
    )
    if c.save():
        flash("Edited contact!")
        return redirect("/contacts")
    else:
        return render_template("edit_contact.html", contact=c)


@app.route("/contacts/<id>/delete", methods=["POST"])
def delete_contact(id):
    c = Contacts.find(id)
    c.delete()
    flash("Deleted contact!")
    return redirect("/contacts")
