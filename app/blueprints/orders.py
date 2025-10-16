from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import date
from ..extensions import db
from ..models import Order, Consignor, Consignee, Goods, Station, BookingAgent, TransactionLog, Builty
from ..forms import OrderForm
from ..auth import login_required

bp = Blueprint("orders", __name__, url_prefix="/orders")


def _choices():
    return {
        "stations": [(s.id, s.name) for s in Station.query.order_by(Station.name).all()],
        "consignors": [(c.id, c.name) for c in Consignor.query.order_by(Consignor.name).all()],
        "consignees": [(c.id, c.name) for c in Consignee.query.order_by(Consignee.name).all()],
        "goods": [(g.id, g.description) for g in Goods.query.order_by(Goods.description).all()],
        "agents": [(a.id, a.name) for a in BookingAgent.query.order_by(BookingAgent.name).all()],
    }


def _populate_form_choices(form):
    """Populate select field choices"""
    choices = _choices()
    form.from_station_id.choices = [(0, 'Select From Station')] + choices['stations']
    form.to_station_id.choices = [(0, 'Select To Station')] + choices['stations']
    form.consignor_id.choices = [(0, 'Select Consignor')] + choices['consignors']
    form.consignee_id.choices = [(0, 'Select Consignee')] + choices['consignees']
    form.goods_id.choices = [(0, 'Select Goods')] + choices['goods']
    form.booking_agent_id.choices = [(0, 'Select Agent')] + choices['agents']


@bp.route("/")
@login_required
def list_orders():
    # Filter by status if provided, default to active orders only
    status_filter = request.args.get('status', 'active')
    search_query = request.args.get('q', '')
    
    query = Order.query
    
    # Apply status filter
    if status_filter == 'active':
        query = query.filter(Order.status.in_(['NEW', 'CONFIRMED']))
    elif status_filter == 'dispatched':
        query = query.filter(Order.status == 'DISPATCHED')
    elif status_filter == 'all':
        pass  # Show all
    else:
        query = query.filter(Order.status == status_filter)
    
    if search_query:
        search_term = f"%{search_query}%"
        # Use explicit joins to avoid ambiguous foreign key errors
        query = query.outerjoin(Consignor, Order.consignor_id == Consignor.id)\
                     .outerjoin(Consignee, Order.consignee_id == Consignee.id)\
                     .outerjoin(Goods, Order.goods_id == Goods.id)\
                     .outerjoin(BookingAgent, Order.booking_agent_id == BookingAgent.id)\
                     .outerjoin(Station, db.or_(
                         Order.from_station_id == Station.id,
                         Order.to_station_id == Station.id
                     )).filter(
            db.or_(
                Order.id.like(search_term),
                Order.date.like(search_term),
                Order.firm.ilike(search_term),
                Consignor.name.ilike(search_term),
                Consignee.name.ilike(search_term),
                Station.name.ilike(search_term),
                Goods.description.ilike(search_term),
                BookingAgent.name.ilike(search_term)
            )
        )
    
    # Eagerly load relationships to avoid N+1 queries
    orders = query.options(
        db.joinedload(Order.consignor),
        db.joinedload(Order.consignee),
        db.joinedload(Order.from_station),
        db.joinedload(Order.to_station),
        db.joinedload(Order.goods),
        db.joinedload(Order.booking_agent)
    ).order_by(Order.id.desc()).limit(200).all()
    return render_template("orders/list.html", orders=orders, search_query=search_query, status_filter=status_filter)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create_order():
    # Check if order type is pre-selected via URL parameter
    order_type = request.args.get('type')
    
    # If no type specified, redirect to type selector
    if not order_type:
        return render_template("orders/type_selector.html")
    
    # Validate order type
    if order_type not in ['PARTY', 'AGENT']:
        flash("Invalid order type", "error")
        return redirect(url_for("orders.create_order"))
    
    form = OrderForm()
    _populate_form_choices(form)
    
    # Pre-select the order type
    form.order_type.data = order_type
    
    if not form.date.data:
        form.date.data = date.today()

    if form.validate_on_submit():
        try:
            # Check for duplicate submission by looking for recent identical orders
            recent_orders = Order.query.filter_by(
                date=form.date.data,
                firm=form.firm.data,
                order_type=form.order_type.data,
                consignor_id=form.consignor_id.data if form.consignor_id.data != 0 else None,
                consignee_id=form.consignee_id.data if form.consignee_id.data != 0 else None,
                goods_id=form.goods_id.data,
                weight=form.weight.data,
                rate=form.rate.data
            ).filter(Order.created_at > db.func.now() - db.text("INTERVAL 1 MINUTE")).first()
            
            if recent_orders:
                flash("Order already exists. Duplicate submission prevented.", "warning")
                return redirect(url_for("orders.list_orders"))
            
            order = Order(
                date=form.date.data,
                firm=form.firm.data,
                order_type=form.order_type.data,
                from_station_id=form.from_station_id.data if form.from_station_id.data != 0 else None,
                to_station_id=form.to_station_id.data if form.to_station_id.data != 0 else None,
                consignor_id=form.consignor_id.data if form.consignor_id.data != 0 else None,
                consignee_id=form.consignee_id.data if form.consignee_id.data != 0 else None,
                goods_id=form.goods_id.data,
                weight=form.weight.data,
                rate=form.rate.data,
                description=form.description.data,
                consignor_phone=form.consignor_phone.data,
                consignee_phone=form.consignee_phone.data,
                booking_agent_id=form.booking_agent_id.data if form.booking_agent_id.data != 0 else None,
                status=form.status.data or "NEW",
                # New phone book fields
                consignor_concerned_person_id=request.form.get('consignor_concerned_person_id') if request.form.get('consignor_concerned_person_id') != '' else None,
                consignor_phone_number_id=request.form.get('consignor_phone_number_id') if request.form.get('consignor_phone_number_id') != '' else None,
                consignee_concerned_person_id=request.form.get('consignee_concerned_person_id') if request.form.get('consignee_concerned_person_id') != '' else None,
                consignee_phone_number_id=request.form.get('consignee_phone_number_id') if request.form.get('consignee_phone_number_id') != '' else None,
                agent_concerned_person_id=request.form.get('agent_concerned_person_id') if request.form.get('agent_concerned_person_id') != '' else None,
                agent_phone_number_id=request.form.get('agent_phone_number_id') if request.form.get('agent_phone_number_id') != '' else None,
            )
            db.session.add(order)
            db.session.flush()
            db.session.add(TransactionLog(entity="Order", entity_id=order.id, action="CREATE"))
            db.session.commit()
            flash("Order created successfully", "success")
            
            # Handle AJAX requests differently
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Order created successfully',
                    'redirect_url': url_for("orders.list_orders")
                })
            else:
                return redirect(url_for("orders.list_orders"))

        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            if "Deadlock found" in error_msg:
                flash("Order creation failed due to system load. Please try again.", "error")
            else:
                flash(f"Error creating order: {error_msg}", "error")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render_template("orders/form.html", form=form, mode="create")
            else:
                return render_template("orders/form.html", form=form, mode="create")
    return render_template("orders/form.html", form=form, mode="create")


@bp.route("/<int:order_id>/view")
@login_required
def view_order(order_id):
    order = Order.query.options(
        db.joinedload(Order.consignor),
        db.joinedload(Order.consignee),
        db.joinedload(Order.from_station),
        db.joinedload(Order.to_station),
        db.joinedload(Order.goods),
        db.joinedload(Order.booking_agent),
        db.joinedload(Order.consignor_concerned_person),
        db.joinedload(Order.consignor_phone_number),
        db.joinedload(Order.consignee_concerned_person),
        db.joinedload(Order.consignee_phone_number),
        db.joinedload(Order.agent_concerned_person),
        db.joinedload(Order.agent_phone_number)
    ).get_or_404(order_id)
    return render_template("orders/detail.html", order=order)


@bp.route("/<int:order_id>", methods=["DELETE"])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"success": True, "message": "Order deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error deleting order: {str(e)}"}), 500


@bp.route("/<int:order_id>/edit", methods=["GET", "POST"])
@login_required
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    form = OrderForm(obj=order)
    _populate_form_choices(form)
    
    # Populate phone book fields for editing
    form.consignor_concerned_person_id.data = order.consignor_concerned_person_id
    form.consignor_phone_number_id.data = order.consignor_phone_number_id
    form.consignee_concerned_person_id.data = order.consignee_concerned_person_id
    form.consignee_phone_number_id.data = order.consignee_phone_number_id
    form.agent_concerned_person_id.data = order.agent_concerned_person_id
    form.agent_phone_number_id.data = order.agent_phone_number_id

    if form.validate_on_submit():
        try:
            order.date = form.date.data
            order.firm = form.firm.data
            order.order_type = form.order_type.data
            order.from_station_id = form.from_station_id.data if form.from_station_id.data != 0 else None
            order.to_station_id = form.to_station_id.data if form.to_station_id.data != 0 else None
            order.consignor_id = form.consignor_id.data if form.consignor_id.data != 0 else None
            order.consignee_id = form.consignee_id.data if form.consignee_id.data != 0 else None
            order.goods_id = form.goods_id.data
            order.weight = form.weight.data
            order.rate = form.rate.data
            order.description = form.description.data
            order.consignor_phone = form.consignor_phone.data
            order.consignee_phone = form.consignee_phone.data
            order.booking_agent_id = form.booking_agent_id.data if form.booking_agent_id.data != 0 else None
            # New phone book fields
            order.consignor_concerned_person_id = request.form.get('consignor_concerned_person_id') if request.form.get('consignor_concerned_person_id') != '' else None
            order.consignor_phone_number_id = request.form.get('consignor_phone_number_id') if request.form.get('consignor_phone_number_id') != '' else None
            order.consignee_concerned_person_id = request.form.get('consignee_concerned_person_id') if request.form.get('consignee_concerned_person_id') != '' else None
            order.consignee_phone_number_id = request.form.get('consignee_phone_number_id') if request.form.get('consignee_phone_number_id') != '' else None
            order.agent_concerned_person_id = request.form.get('agent_concerned_person_id') if request.form.get('agent_concerned_person_id') != '' else None
            order.agent_phone_number_id = request.form.get('agent_phone_number_id') if request.form.get('agent_phone_number_id') != '' else None
            order.status = form.status.data
            db.session.add(order)
            
            # Update related builty records if they exist
            related_builty = Builty.query.filter_by(order_id=order.id).first()
            if related_builty:
                # Sync consignor/consignee data from order to builty
                if form.consignor_id.data and form.consignor_id.data != 0:
                    related_builty.consignor_id = form.consignor_id.data
                if form.consignee_id.data and form.consignee_id.data != 0:
                    related_builty.consignee_id = form.consignee_id.data
                if form.booking_agent_id.data and form.booking_agent_id.data != 0:
                    related_builty.booking_agent_id = form.booking_agent_id.data
                db.session.add(related_builty)
            
            db.session.add(TransactionLog(entity="Order", entity_id=order.id, action="UPDATE"))
            db.session.commit()
            flash("Order updated successfully", "success")
            
            # Handle AJAX requests differently
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Order updated successfully',
                    'redirect_url': url_for("orders.list_orders")
                })
            else:
                return redirect(url_for("orders.list_orders"))
                
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            if "Deadlock found" in error_msg:
                flash("Order update failed due to system load. Please try again.", "error")
            else:
                flash(f"Error updating order: {error_msg}", "error")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render_template("orders/form.html", form=form, mode="edit", order=order)
            else:
                return render_template("orders/form.html", form=form, mode="edit", order=order)
    return render_template("orders/form.html", form=form, mode="edit", order=order)


@bp.post("/<int:order_id>/status")
def status_action(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status")
    if new_status:
        order.status = new_status
        db.session.add(order)
        db.session.add(TransactionLog(entity="Order", entity_id=order.id, action=f"STATUS:{new_status}"))
        db.session.commit()
        flash("Status updated", "success")
    return redirect(url_for("orders.list_orders"))
