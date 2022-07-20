import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Item, User
from shop.forms import RegistrationForm, LoginForm, CheckoutForm, UpdateEmailForm, UpdatePasswordForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods= ['GET', 'POST'])

@app.route("/home")
def home():

	return render_template('home.html', items = Item.query.all(), title='Home')

@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/Asc")
def Asc():
	return render_template('home.html', items = Item.query.order_by(Item.price).all(), title='Home')

@app.route("/Desc")
def Desc():
	return render_template('home.html', items = Item.query.order_by(Item.price.desc()).all(), title='Home')

@app.route("/AZ")
def AZ():
	return render_template('home.html', items = Item.query.order_by(Item.title).all())

@app.route("/ZA")
def ZA():
	return render_template('home.html', items = Item.query.order_by(Item.title.desc()).all())

@app.route("/item/<int:item_id>")
def item(item_id):
	item = Item.query.get_or_404(item_id)
	return render_template('item.html', item=item)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created.  You can now log in.')
		return redirect(url_for('tyfr'))
	return render_template('register.html', title='Register', form=form)


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
	form = CheckoutForm()
	if form.validate_on_submit():
		session["basket"] = []

		return redirect(url_for('thankyou'))
	return render_template('checkout.html', title='Checkout', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			flash('You are now logged in.')
			return redirect(url_for('home'))
		flash('Invalid email or password.')

		return render_template('login.html', form=form)

	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
		db.session.commit()
		session.clear()
		logout_user()
		return redirect(url_for('home'))

@app.route("/add_to_basket/<int:item_id>")
def add_to_basket(item_id):
	if current_user.is_anonymous:
		flash('Please login to add to basket')
		return redirect("/login")
	else:
		if "basket" not in session:
			session["basket"] = []
		session["basket"].append(item_id)
		flash("The item is added to your shopping basket!")
		return redirect("/basket")

@app.route("/basket", methods=['GET', 'POST'])
def basket_display():
	if current_user.is_anonymous:
		flash('Please login to view basket')
		return redirect("/login")
	else:
		if "basket" not in session:
			flash('There is nothing in your basket.')
			return render_template("basket.html", display_basket = {}, total = 0)
		else:
			items = session["basket"]
			basket = {}
			total_price = 0
			total_quantity = 0
			for item in items:
				item = Item.query.get_or_404(item)
				total_price += item.price
				if item.id in basket:
					basket[item.id]["quantity"] += 1
				else:
					basket[item.id] = {"quantity":1, "title": item.title, "price":item.price}
				total_quantity = sum(item['quantity'] for item in basket.values())
			return render_template("basket.html", title='Your Shopping Basket', display_basket = basket, total = total_price, total_quantity = total_quantity)
		return render_template('basket.html')
@app.route("/delete_item/<int:item_id>", methods=['GET', 'POST'])
def delete_item(item_id):
	if "basket" not in session:
		session["basket"] = []
	session["basket"].remove(item_id)
	flash("The item has been removed from your shopping basket!")
	session.modified = True
	return redirect("/basket")

@app.route("/add_to_wishlist/<int:item_id>")
def add_to_wishlist(item_id):
	if current_user.is_anonymous:
		flash('Please login to add to wishlist')
		return redirect("/login")
	else:
		if "wishlist" not in session:
			session["wishlist"] = []
		session["wishlist"].append(item_id)
		flash("The item has been added to your wishlist")
		return redirect("/wishlist")

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist_display():
	if current_user.is_anonymous:
		flash('Please login to view wishlist')
		return redirect("/login")
	else:
		if "wishlist" not in session:
			flash('There is nothing in your wishlist.')
			return render_template("wishlist.html", display_wishlist = {}, total = 0)
		else:
			items = session["wishlist"]
			wishlist = {}
			total_price = 0
			total_quantity = 0
			for item in items:
				item = Item.query.get_or_404(item)
				total_price += item.price
				if item.id in wishlist:
					wishlist[item.id]["quantity"] += 1
				else:
					wishlist[item.id] = {"quantity":1, "title": item.title, "price":item.price}
				total_quantity = sum(item['quantity'] for item in wishlist.values())
			return render_template("wishlist.html", title='Your Shopping Basket', display_wishlist = wishlist, total = total_price, total_quantity = total_quantity)
		return render_template('wishlist.html')

@app.route("/delete_item_wishlist/<int:item_id>", methods=['GET', 'POST'])
def delete_item_wishlist(item_id):
	if "wishlist" not in session:
		session["wishlist"] = []
	session["wishlist"].remove(item_id)
	flash("The item has been removed from your wishlist")
	session.modified = True
	return redirect("/wishlist")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html", title='Thank You')

@app.route("/tyfr")
def tyfr():
	return render_template("tyfr.html", title='Thank You')

@app.route("/adminpage")
def adminpage():
	return render_template("admin.html", title='Admin')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	email_form = UpdateEmailForm(prefix="updemail")
	password_form = UpdatePasswordForm(prefix="updpass")

	if request.method == "POST":
		update_user = User.query.filter_by(id=current_user.id).first()

		if email_form.validate_on_submit():
			entered_email = email_form.email.data
			entered_pass = email_form.password.data

			results = User.query.filter_by(email=entered_email).all()
			if len(results) > 0:
				flash("This email is already in use by somebody else")
				return redirect(url_for('account'))

			if not current_user.verify_password(entered_pass):
				flash("Account password was incorrect.")
				return redirect(url_for('account'))

			update_user.email = entered_email
			db.session.commit()

			flash("Email was updated!")

		if password_form.validate_on_submit():
			entered_pass = password_form.password.data
			entered_newpass = password_form.new_password.data

			# Check password is correct
			if not current_user.verify_password(entered_pass):
				flash("Current password was incorrect.")
				return redirect(url_for('account'))

			update_user.password = entered_newpass
			db.session.commit()

			flash("Password was updated!")
	return render_template('account.html', title='Account', update_email=email_form, update_password=password_form)
