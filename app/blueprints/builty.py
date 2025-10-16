from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import date
from ..extensions import db
from ..models import Builty, Order, Vehicle, Driver, Owner, Station, Goods, TransactionLog, Consignor, Consignee, BookingAgent
from ..forms import BuiltyForm

bp = Blueprint("builty", __name__, url_prefix="/builty")


def _choices():
    return {
        "orders": [(o.id, f"Order #{o.id}") for o in Order.query.order_by(Order.id.desc()).all()],
        "vehicles": [(v.id, v.lorry_no) for v in Vehicle.query.order_by(Vehicle.lorry_no).all()],
        "drivers": [(d.id, d.name) for d in Driver.query.order_by(Driver.name).all()],
        "owners": [(o.id, o.name) for o in Owner.query.order_by(Owner.name).all()],
        "stations": [(s.id, s.name) for s in Station.query.order_by(Station.name).all()],
        "goods": [(g.id, g.description) for g in Goods.query.order_by(Goods.description).all()],
        "consignors": [(c.id, c.name) for c in Consignor.query.order_by(Consignor.name).all()],
        "consignees": [(c.id, c.name) for c in Consignee.query.order_by(Consignee.name).all()],
        "agents": [(a.id, a.name) for a in BookingAgent.query.order_by(BookingAgent.name).all()],
    }


@bp.route("/")
def list_builty():
    # Filter by status if provided
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('q', '')
    
    query = Builty.query
    
    # Apply status filter
    if status_filter != 'all':
        query = query.filter(Builty.status == status_filter)
    
    if search_query:
        search_term = f"%{search_query}%"
        # Use explicit joins to avoid ambiguous foreign key errors
        query = query.outerjoin(Order, Builty.order_id == Order.id)\
                     .outerjoin(Vehicle, Builty.vehicle_id == Vehicle.id)\
                     .outerjoin(Driver, Builty.driver_id == Driver.id)\
                     .outerjoin(Owner, Builty.owner_id == Owner.id)\
                     .outerjoin(Station, db.or_(
                         Builty.from_station_id == Station.id,
                         Builty.to_station_id == Station.id
                     )).filter(
            db.or_(
                Builty.id.like(search_term),
                Builty.firm.ilike(search_term),
                Builty.lr_no.ilike(search_term),
                Builty.invoice_no.ilike(search_term),
                Vehicle.lorry_no.ilike(search_term),
                Driver.name.ilike(search_term),
                Owner.name.ilike(search_term),
                Station.name.ilike(search_term)
            )
        )
    
    # Eagerly load relationships to avoid N+1 queries
    builty_list = query.options(
        db.joinedload(Builty.order),
        db.joinedload(Builty.consignor),
        db.joinedload(Builty.consignee),
        db.joinedload(Builty.from_station),
        db.joinedload(Builty.to_station),
        db.joinedload(Builty.vehicle),
        db.joinedload(Builty.driver),
        db.joinedload(Builty.owner),
        db.joinedload(Builty.goods),
        db.joinedload(Builty.booking_agent)
    ).order_by(Builty.id.desc()).limit(200).all()
    view_type = request.args.get('view', 'deck')
    return render_template("builty/list.html", builty_list=builty_list, search_query=search_query, status_filter=status_filter, view_type=view_type)


@bp.route("/new", methods=["GET", "POST"])
def create_builty():
    form = BuiltyForm()
    
    # Populate choices
    choices = _choices()
    form.order_id.choices = [(0, 'Select Order')] + choices['orders']
    form.vehicle_id.choices = [(0, 'Select Vehicle')] + choices['vehicles']
    form.driver_id.choices = [(0, 'Select Driver')] + choices['drivers']
    form.owner_id.choices = [(0, 'Select Owner')] + choices['owners']
    form.from_station_id.choices = [(0, 'Select Station')] + choices['stations']
    form.to_station_id.choices = [(0, 'Select Station')] + choices['stations']
    form.goods_id.choices = [(0, 'Select Goods')] + choices['goods']
    form.consignor_id.choices = [(0, 'Select Consignor')] + choices['consignors']
    form.consignee_id.choices = [(0, 'Select Consignee')] + choices['consignees']
    form.booking_agent_id.choices = [(0, 'Select Agent')] + choices['agents']
    
    # Debug: Check if all fields have choices
    import logging
    logger = logging.getLogger(__name__)
    for field_name, field in form._fields.items():
        if hasattr(field, 'choices') and field.choices is None:
            logger.warning(f"Field {field_name} has no choices")
    
    if not form.date.data:
        form.date.data = date.today()

    # Auto-populate from order if order_id is provided
    pre_order_id = request.args.get("order_id", type=int)
    order_data = None
    if pre_order_id:
        order = Order.query.get(pre_order_id)
        if order:
            form.order_id.data = pre_order_id
            # Pre-fill fields from order if not already submitted
            if request.method == 'GET':
                form.firm.data = order.firm
                if order.goods_id:
                    form.goods_id.data = order.goods_id
                if order.from_station_id:
                    form.from_station_id.data = order.from_station_id
                if order.to_station_id:
                    form.to_station_id.data = order.to_station_id
                if order.rate:
                    form.rate.data = order.rate
                # Auto-populate consignor/consignee/agent based on order type
                if order.order_type == 'PARTY':
                    if order.consignor_id:
                        form.consignor_id.data = order.consignor_id
                    if order.consignee_id:
                        form.consignee_id.data = order.consignee_id
                    # Note: Phone numbers will be loaded via JavaScript from the phone book system
                elif order.order_type == 'AGENT':
                    if order.booking_agent_id:
                        form.booking_agent_id.data = order.booking_agent_id
            # Pass order data to template for JavaScript
            order_data = {
                'id': order.id,
                'order_type': order.order_type,
                'goods_id': order.goods_id,
                'from_station_id': order.from_station_id,
                'to_station_id': order.to_station_id,
                'consignor_id': order.consignor_id,
                'consignee_id': order.consignee_id,
                'booking_agent_id': order.booking_agent_id,
                'weight': float(order.weight) if order.weight else None,
                'rate': float(order.rate) if order.rate else None
            }

    # Custom validation for required fields
    validation_errors = []
    
    # Check required fields that need valid IDs (not 0)
    required_fields = [
        ('order_id', 'Order'),
        ('vehicle_id', 'Vehicle'), 
        ('driver_id', 'Driver'),
        ('owner_id', 'Owner'),
        ('from_station_id', 'From Station'),
        ('to_station_id', 'To Station')
    ]
    
    for field_name, field_label in required_fields:
        if getattr(form, field_name).data == 0:
            validation_errors.append(f"{field_label} is required")
            getattr(form, field_name).errors.append(f"{field_label} is required")
    
    # Check date
    if not form.date.data:
        validation_errors.append("Date is required")
        form.date.errors.append("Date is required")
    
    if not validation_errors and form.validate_on_submit():
        try:
            b = Builty(
                order_id=form.order_id.data,
                vehicle_id=form.vehicle_id.data,
                driver_id=form.driver_id.data,
                owner_id=form.owner_id.data,
                date=form.date.data,
                from_station_id=form.from_station_id.data,
                to_station_id=form.to_station_id.data,
                firm=form.firm.data,
                lr_no=form.lr_no.data,
                status=form.status.data,
                invoice_no=form.invoice_no.data,
                eway_bill_no=form.eway_bill_no.data,
                goods_id=form.goods_id.data if form.goods_id.data != 0 else None,
                actual_weight=form.actual_weight.data,
                charged_weight=form.charged_weight.data,
                rate=form.rate.data,
                advance_amount=form.advance_amount.data,
                consignor_id=form.consignor_id.data if form.consignor_id.data != 0 else None,
                consignee_id=form.consignee_id.data if form.consignee_id.data != 0 else None,
                booking_agent_id=form.booking_agent_id.data if form.booking_agent_id.data != 0 else None,
                # Phone book fields
                consignor_concerned_person_id=request.form.get('consignor_concerned_person_id') if request.form.get('consignor_concerned_person_id') != '' else None,
                consignor_phone_number_id=request.form.get('consignor_phone_number_id') if request.form.get('consignor_phone_number_id') != '' else None,
                consignee_concerned_person_id=request.form.get('consignee_concerned_person_id') if request.form.get('consignee_concerned_person_id') != '' else None,
                consignee_phone_number_id=request.form.get('consignee_phone_number_id') if request.form.get('consignee_phone_number_id') != '' else None,
                agent_concerned_person_id=request.form.get('agent_concerned_person_id') if request.form.get('agent_concerned_person_id') != '' else None,
                agent_phone_number_id=request.form.get('agent_phone_number_id') if request.form.get('agent_phone_number_id') != '' else None,
            )
            db.session.add(b)
            db.session.flush()
            
            # Update referenced order with builty data and set status to DISPATCHED
            order = Order.query.get(form.order_id.data)
            if order:
                order.status = "DISPATCHED"
                # Sync consignor/consignee data from builty to order
                if form.consignor_id.data and form.consignor_id.data != 0:
                    order.consignor_id = form.consignor_id.data
                if form.consignee_id.data and form.consignee_id.data != 0:
                    order.consignee_id = form.consignee_id.data
                if form.booking_agent_id.data and form.booking_agent_id.data != 0:
                    order.booking_agent_id = form.booking_agent_id.data
                db.session.add(order)
            
            db.session.add(TransactionLog(entity="Builty", entity_id=b.id, action="CREATE"))
            db.session.commit()
            flash("Builty created", "success")
            
            # Handle AJAX requests differently
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Builty created successfully',
                    'redirect_url': url_for("builty.list_builty")
                })
            else:
                return redirect(url_for("builty.list_builty"))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating builty: {str(e)}", "error")
            # Log error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Builty creation error: {str(e)}")
            
            # Handle AJAX requests differently
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': f'Error creating builty: {str(e)}'
                }), 400
            else:
                return render_template("builty/form.html", form=form, mode="create", order_data=order_data)
    else:
        # Form validation failed
        if validation_errors:
            flash("Please correct the following errors:", "error")
            for error in validation_errors:
                flash(error, "error")
        else:
            flash("Please correct the errors below", "error")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", "error")
                
    return render_template("builty/form.html", form=form, mode="create", order_data=order_data)


@bp.route("/<int:builty_id>/view")
def view_builty(builty_id):
    builty = Builty.query.options(
        db.joinedload(Builty.order),
        db.joinedload(Builty.consignor),
        db.joinedload(Builty.consignee),
        db.joinedload(Builty.from_station),
        db.joinedload(Builty.to_station),
        db.joinedload(Builty.vehicle),
        db.joinedload(Builty.driver),
        db.joinedload(Builty.owner),
        db.joinedload(Builty.goods),
        db.joinedload(Builty.booking_agent)
    ).get_or_404(builty_id)
    return render_template("builty/detail.html", builty=builty)


@bp.route("/<int:builty_id>/edit", methods=["GET", "POST"])
def edit_builty(builty_id):
    builty = Builty.query.get_or_404(builty_id)
    form = BuiltyForm(obj=builty)
    
    # Populate choices
    choices = _choices()
    form.order_id.choices = [(0, 'Select Order')] + choices['orders']
    form.vehicle_id.choices = [(0, 'Select Vehicle')] + choices['vehicles']
    form.driver_id.choices = [(0, 'Select Driver')] + choices['drivers']
    form.owner_id.choices = [(0, 'Select Owner')] + choices['owners']
    form.from_station_id.choices = [(0, 'Select Station')] + choices['stations']
    form.to_station_id.choices = [(0, 'Select Station')] + choices['stations']
    form.goods_id.choices = [(0, 'Select Goods')] + choices['goods']
    form.consignor_id.choices = [(0, 'Select Consignor')] + choices['consignors']
    form.consignee_id.choices = [(0, 'Select Consignee')] + choices['consignees']
    form.booking_agent_id.choices = [(0, 'Select Agent')] + choices['agents']
    
    # Populate phone book fields for editing
    form.consignor_concerned_person_id.data = builty.consignor_concerned_person_id
    form.consignor_phone_number_id.data = builty.consignor_phone_number_id
    form.consignee_concerned_person_id.data = builty.consignee_concerned_person_id
    form.consignee_phone_number_id.data = builty.consignee_phone_number_id
    form.agent_concerned_person_id.data = builty.agent_concerned_person_id
    form.agent_phone_number_id.data = builty.agent_phone_number_id

    if form.validate_on_submit():
        try:
            # Update builty fields
            builty.vehicle_id = form.vehicle_id.data if form.vehicle_id.data != 0 else None
            builty.driver_id = form.driver_id.data if form.driver_id.data != 0 else None
            builty.owner_id = form.owner_id.data if form.owner_id.data != 0 else None
            builty.date = form.date.data
            builty.from_station_id = form.from_station_id.data if form.from_station_id.data != 0 else None
            builty.to_station_id = form.to_station_id.data if form.to_station_id.data != 0 else None
            builty.firm = form.firm.data
            builty.lr_no = form.lr_no.data
            builty.status = form.status.data
            builty.invoice_no = form.invoice_no.data
            builty.eway_bill_no = form.eway_bill_no.data
            builty.goods_id = form.goods_id.data if form.goods_id.data != 0 else None
            builty.actual_weight = form.actual_weight.data
            builty.charged_weight = form.charged_weight.data
            builty.rate = form.rate.data
            builty.advance_amount = form.advance_amount.data
            builty.consignor_id = form.consignor_id.data if form.consignor_id.data != 0 else None
            builty.consignee_id = form.consignee_id.data if form.consignee_id.data != 0 else None
            builty.booking_agent_id = form.booking_agent_id.data if form.booking_agent_id.data != 0 else None
            
            # Update phone book fields
            builty.consignor_concerned_person_id = request.form.get('consignor_concerned_person_id') if request.form.get('consignor_concerned_person_id') != '' else None
            builty.consignor_phone_number_id = request.form.get('consignor_phone_number_id') if request.form.get('consignor_phone_number_id') != '' else None
            builty.consignee_concerned_person_id = request.form.get('consignee_concerned_person_id') if request.form.get('consignee_concerned_person_id') != '' else None
            builty.consignee_phone_number_id = request.form.get('consignee_phone_number_id') if request.form.get('consignee_phone_number_id') != '' else None
            builty.agent_concerned_person_id = request.form.get('agent_concerned_person_id') if request.form.get('agent_concerned_person_id') != '' else None
            builty.agent_phone_number_id = request.form.get('agent_phone_number_id') if request.form.get('agent_phone_number_id') != '' else None
            
            db.session.add(builty)
            
            # Update referenced order with builty data changes
            order = Order.query.get(builty.order_id)
            if order:
                # Sync consignor/consignee data from builty to order
                if form.consignor_id.data and form.consignor_id.data != 0:
                    order.consignor_id = form.consignor_id.data
                if form.consignee_id.data and form.consignee_id.data != 0:
                    order.consignee_id = form.consignee_id.data
                if form.booking_agent_id.data and form.booking_agent_id.data != 0:
                    order.booking_agent_id = form.booking_agent_id.data
                db.session.add(order)
            
            db.session.add(TransactionLog(entity="Builty", entity_id=builty.id, action="UPDATE"))
            db.session.commit()
            flash("Builty updated", "success")
            
            # Handle AJAX requests differently
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Builty updated successfully',
                    'redirect_url': url_for("builty.list_builty")
                })
            else:
                return redirect(url_for("builty.list_builty"))
                
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating builty: {str(e)}", "error")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render_template("builty/form.html", form=form, mode="edit", builty=builty)
            else:
                return render_template("builty/form.html", form=form, mode="edit", builty=builty)
    
    return render_template("builty/form.html", form=form, mode="edit", builty=builty)


@bp.post("/from-order/<int:order_id>")
def create_from_order(order_id):
    return redirect(url_for("builty.create_builty") + f"?order_id={order_id}")
