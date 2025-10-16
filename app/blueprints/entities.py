from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..extensions import db
from ..models import Consignor, Consignee, BookingAgent, Station, PinCode, TransactionLog, PhoneBook
from ..forms import ConsignorForm, ConsigneeForm, BookingAgentForm
from ..auth import login_required

bp = Blueprint("entities", __name__, url_prefix="/entities")


def _get_choices():
    """Get common choices for forms"""
    stations = Station.query.order_by(Station.name).all()
    pin_codes = PinCode.query.order_by(PinCode.code).all()
    return {
        'stations': [(0, 'Select Station')] + [(s.id, s.name) for s in stations],
        'pin_codes': [(0, 'Select Pin Code')] + [(p.id, f"{p.code} - {p.state or 'Unknown'}") for p in pin_codes]
    }


# Consignors
@bp.route("/consignors")
@login_required
def list_consignors():
    items = Consignor.query.order_by(Consignor.name).all()
    return render_template("entities/consignors_list.html", items=items, entity_type="consignors")


@bp.route("/consignors/new", methods=["GET", "POST"])
@login_required
def create_consignor():
    form = ConsignorForm()
    choices = _get_choices()
    form.station_id.choices = choices['stations']
    form.pin_code_id.choices = choices['pin_codes']
    
    if form.validate_on_submit():
        c = Consignor(
            name=form.name.data,
            address=form.address.data,
            gstin=form.gstin.data,
            pan=form.pan.data,
            station_id=form.station_id.data,
            pin_code_id=form.pin_code_id.data,
            phone=form.phone.data,
            email=form.email.data,
        )
        db.session.add(c)
        db.session.flush()
        
        # Create phone book entry if phone number provided
        if form.phone.data and form.phone.data.strip():
            phone_entry = PhoneBook(
                entity_type='CONSIGNOR',
                entity_id=c.id,
                phone_number=form.phone.data.strip(),
                is_primary=True,
                label='Primary'
            )
            db.session.add(phone_entry)
        
        db.session.add(TransactionLog(entity="Consignor", entity_id=c.id, action="CREATE"))
        db.session.commit()
        flash("Consignor created", "success")
        return redirect(url_for("entities.list_consignors"))
    return render_template("entities/consignor_form.html", form=form, mode="create")


@bp.route("/consignors/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_consignor(item_id):
    c = Consignor.query.get_or_404(item_id)
    form = ConsignorForm(obj=c)
    choices = _get_choices()
    form.station_id.choices = choices['stations']
    form.pin_code_id.choices = choices['pin_codes']
    
    if form.validate_on_submit():
        c.name = form.name.data
        c.address = form.address.data
        c.gstin = form.gstin.data
        c.pan = form.pan.data
        c.station_id = form.station_id.data
        c.pin_code_id = form.pin_code_id.data
        c.phone = form.phone.data
        c.email = form.email.data
        db.session.add(c)
        db.session.add(TransactionLog(entity="Consignor", entity_id=c.id, action="UPDATE"))
        db.session.commit()
        flash("Consignor updated", "success")
        return redirect(url_for("entities.list_consignors"))
    return render_template("entities/consignor_form.html", form=form, mode="edit", item=c)


# Consignees
@bp.route("/consignees")
@login_required
def list_consignees():
    items = Consignee.query.order_by(Consignee.name).all()
    return render_template("entities/consignees_list.html", items=items, entity_type="consignees")


@bp.route("/consignees/new", methods=["GET", "POST"])
@login_required
def create_consignee():
    form = ConsigneeForm()
    choices = _get_choices()
    form.station_id.choices = choices['stations']
    form.pin_code_id.choices = choices['pin_codes']
    
    if form.validate_on_submit():
        c = Consignee(
            name=form.name.data,
            address=form.address.data,
            gstin=form.gstin.data,
            pan=form.pan.data,
            station_id=form.station_id.data,
            pin_code_id=form.pin_code_id.data,
            phone=form.phone.data,
            email=form.email.data,
        )
        db.session.add(c)
        db.session.flush()
        db.session.add(TransactionLog(entity="Consignee", entity_id=c.id, action="CREATE"))
        db.session.commit()
        flash("Consignee created", "success")
        return redirect(url_for("entities.list_consignees"))
    return render_template("entities/consignee_form.html", form=form, mode="create")


@bp.route("/consignees/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_consignee(item_id):
    c = Consignee.query.get_or_404(item_id)
    form = ConsigneeForm(obj=c)
    choices = _get_choices()
    form.station_id.choices = choices['stations']
    form.pin_code_id.choices = choices['pin_codes']
    
    if form.validate_on_submit():
        c.name = form.name.data
        c.address = form.address.data
        c.gstin = form.gstin.data
        c.pan = form.pan.data
        c.station_id = form.station_id.data
        c.pin_code_id = form.pin_code_id.data
        c.phone = form.phone.data
        c.email = form.email.data
        db.session.add(c)
        db.session.add(TransactionLog(entity="Consignee", entity_id=c.id, action="UPDATE"))
        db.session.commit()
        flash("Consignee updated", "success")
        return redirect(url_for("entities.list_consignees"))
    return render_template("entities/consignee_form.html", form=form, mode="edit", item=c)


# Agents
@bp.route("/agents")
@login_required
def list_agents():
    items = BookingAgent.query.order_by(BookingAgent.name).all()
    return render_template("entities/agents_list.html", items=items, entity_type="agents")


@bp.route("/agents/new", methods=["GET", "POST"])
@login_required
def create_agent():
    form = BookingAgentForm()
    if form.validate_on_submit():
        a = BookingAgent(
            name=form.name.data,
            phone=form.phone.data,
            gstin=form.gstin.data,
            pan=form.pan.data,
            city=form.city.data,
            state=form.state.data,
        )
        db.session.add(a)
        db.session.flush()
        db.session.add(TransactionLog(entity="BookingAgent", entity_id=a.id, action="CREATE"))
        db.session.commit()
        flash("Agent created", "success")
        return redirect(url_for("entities.list_agents"))
    return render_template("entities/agent_form.html", form=form, mode="create")


@bp.route("/agents/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_agent(item_id):
    a = BookingAgent.query.get_or_404(item_id)
    form = BookingAgentForm(obj=a)
    if form.validate_on_submit():
        form.populate_obj(a)
        db.session.add(a)
        db.session.add(TransactionLog(entity="BookingAgent", entity_id=a.id, action="UPDATE"))
        db.session.commit()
        flash("Agent updated", "success")
        return redirect(url_for("entities.list_agents"))
    return render_template("entities/agent_form.html", form=form, mode="edit", item=a)
