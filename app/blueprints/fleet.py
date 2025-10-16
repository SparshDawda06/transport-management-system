from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..extensions import db
from ..models import Vehicle, Driver, Owner, TransactionLog
from ..forms import VehicleForm, DriverForm, OwnerForm
from ..auth import login_required

bp = Blueprint("fleet", __name__, url_prefix="/fleet")


def _get_fleet_choices():
    """Get choices for fleet forms"""
    owners = Owner.query.order_by(Owner.name).all()
    drivers = Driver.query.order_by(Driver.name).all()
    return {
        'owners': [(0, 'Select Owner')] + [(o.id, o.name) for o in owners],
        'drivers': [(0, 'Select Driver')] + [(d.id, d.name) for d in drivers]
    }


# Vehicles
@bp.route("/vehicles")
@login_required
def list_vehicles():
    items = Vehicle.query.order_by(Vehicle.lorry_no).all()
    return render_template("fleet/vehicles_list.html", items=items, entity_type="vehicles")


@bp.route("/vehicles/new", methods=["GET", "POST"])
@login_required
def create_vehicle():
    form = VehicleForm()
    choices = _get_fleet_choices()
    form.owner_id.choices = choices['owners']
    form.driver_id.choices = choices['drivers']
    
    if form.validate_on_submit():
        v = Vehicle(
            lorry_no=form.lorry_no.data,
            capacity=form.capacity.data,
            chassis_no=form.chassis_no.data,
            engine_no=form.engine_no.data,
            owner_id=form.owner_id.data,
            driver_id=form.driver_id.data,
        )
        db.session.add(v)
        db.session.flush()
        db.session.add(TransactionLog(entity="Vehicle", entity_id=v.id, action="CREATE"))
        db.session.commit()
        flash("Vehicle created", "success")
        return redirect(url_for("fleet.list_vehicles"))
    return render_template("fleet/vehicle_form.html", form=form, mode="create")


@bp.route("/vehicles/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_vehicle(item_id):
    v = Vehicle.query.get_or_404(item_id)
    form = VehicleForm(obj=v)
    choices = _get_fleet_choices()
    form.owner_id.choices = choices['owners']
    form.driver_id.choices = choices['drivers']
    
    if form.validate_on_submit():
        form.populate_obj(v)
        db.session.add(v)
        db.session.add(TransactionLog(entity="Vehicle", entity_id=v.id, action="UPDATE"))
        db.session.commit()
        flash("Vehicle updated", "success")
        return redirect(url_for("fleet.list_vehicles"))
    return render_template("fleet/vehicle_form.html", form=form, mode="edit", item=v)


# Drivers
@bp.route("/drivers")
@login_required
def list_drivers():
    items = Driver.query.order_by(Driver.name).all()
    return render_template("fleet/drivers_list.html", items=items, entity_type="drivers")


@bp.route("/drivers/new", methods=["GET", "POST"])
@login_required
def create_driver():
    form = DriverForm()
    if form.validate_on_submit():
        d = Driver(
            name=form.name.data,
            address=form.address.data,
            license_no=form.license_no.data,
            validity=form.validity.data,
            aadhar=form.aadhar.data,
        )
        db.session.add(d)
        db.session.flush()
        db.session.add(TransactionLog(entity="Driver", entity_id=d.id, action="CREATE"))
        db.session.commit()
        flash("Driver created", "success")
        return redirect(url_for("fleet.list_drivers"))
    return render_template("fleet/driver_form.html", form=form, mode="create")


@bp.route("/drivers/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_driver(item_id):
    d = Driver.query.get_or_404(item_id)
    form = DriverForm(obj=d)
    if form.validate_on_submit():
        form.populate_obj(d)
        db.session.add(d)
        db.session.add(TransactionLog(entity="Driver", entity_id=d.id, action="UPDATE"))
        db.session.commit()
        flash("Driver updated", "success")
        return redirect(url_for("fleet.list_drivers"))
    return render_template("fleet/driver_form.html", form=form, mode="edit", item=d)


# Owners
@bp.route("/owners")
@login_required
def list_owners():
    items = Owner.query.order_by(Owner.name).all()
    return render_template("fleet/owners_list.html", items=items, entity_type="owners")


@bp.route("/owners/new", methods=["GET", "POST"])
@login_required
def create_owner():
    form = OwnerForm()
    if form.validate_on_submit():
        o = Owner(
            name=form.name.data,
            pan=form.pan.data,
            aadhar=form.aadhar.data,
            address=form.address.data,
        )
        db.session.add(o)
        db.session.flush()
        db.session.add(TransactionLog(entity="Owner", entity_id=o.id, action="CREATE"))
        db.session.commit()
        flash("Owner created", "success")
        return redirect(url_for("fleet.list_owners"))
    return render_template("fleet/owner_form.html", form=form, mode="create")


@bp.route("/owners/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_owner(item_id):
    o = Owner.query.get_or_404(item_id)
    form = OwnerForm(obj=o)
    if form.validate_on_submit():
        form.populate_obj(o)
        db.session.add(o)
        db.session.add(TransactionLog(entity="Owner", entity_id=o.id, action="UPDATE"))
        db.session.commit()
        flash("Owner updated", "success")
        return redirect(url_for("fleet.list_owners"))
    return render_template("fleet/owner_form.html", form=form, mode="edit", item=o)
