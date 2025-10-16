from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..extensions import db
from ..models import Station, PinCode, Goods, TransactionLog
from ..forms import StationForm, PinCodeForm, GoodsForm
from ..auth import login_required

bp = Blueprint("system", __name__, url_prefix="/system")


# Stations
@bp.route("/stations")
@login_required
def list_stations():
    items = Station.query.order_by(Station.name).all()
    return render_template("system/stations_list.html", items=items, entity_type="stations")


@bp.route("/stations/new", methods=["GET", "POST"])
@login_required
def create_station():
    form = StationForm()
    if form.validate_on_submit():
        s = Station(
            name=form.name.data,
            state=form.state.data,
        )
        db.session.add(s)
        db.session.flush()
        db.session.add(TransactionLog(entity="Station", entity_id=s.id, action="CREATE"))
        db.session.commit()
        flash("Station created", "success")
        return redirect(url_for("system.list_stations"))
    return render_template("system/station_form.html", form=form, mode="create")


@bp.route("/stations/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_station(item_id):
    s = Station.query.get_or_404(item_id)
    form = StationForm(obj=s)
    if form.validate_on_submit():
        form.populate_obj(s)
        db.session.add(s)
        db.session.add(TransactionLog(entity="Station", entity_id=s.id, action="UPDATE"))
        db.session.commit()
        flash("Station updated", "success")
        return redirect(url_for("system.list_stations"))
    return render_template("system/station_form.html", form=form, mode="edit", item=s)


# Pin Codes
@bp.route("/pincodes")
@login_required
def list_pincodes():
    items = PinCode.query.order_by(PinCode.code).all()
    return render_template("system/pincodes_list.html", items=items, entity_type="pincodes")


@bp.route("/pincodes/new", methods=["GET", "POST"])
@login_required
def create_pincode():
    form = PinCodeForm()
    stations = Station.query.order_by(Station.name).all()
    form.station_id.choices = [(0, 'Select Station')] + [(s.id, s.name) for s in stations]
    
    if form.validate_on_submit():
        p = PinCode(
            code=form.code.data,
            state=form.state.data,
            station_id=form.station_id.data,
        )
        db.session.add(p)
        db.session.flush()
        db.session.add(TransactionLog(entity="PinCode", entity_id=p.id, action="CREATE"))
        db.session.commit()
        flash("Pin Code created", "success")
        return redirect(url_for("system.list_pincodes"))
    return render_template("system/pincode_form.html", form=form, mode="create")


@bp.route("/pincodes/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_pincode(item_id):
    p = PinCode.query.get_or_404(item_id)
    form = PinCodeForm(obj=p)
    stations = Station.query.order_by(Station.name).all()
    form.station_id.choices = [(0, 'Select Station')] + [(s.id, s.name) for s in stations]
    
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.add(p)
        db.session.add(TransactionLog(entity="PinCode", entity_id=p.id, action="UPDATE"))
        db.session.commit()
        flash("Pin Code updated", "success")
        return redirect(url_for("system.list_pincodes"))
    return render_template("system/pincode_form.html", form=form, mode="edit", item=p)


# Goods
@bp.route("/goods")
@login_required
def list_goods():
    items = Goods.query.order_by(Goods.description).all()
    return render_template("system/goods_list.html", items=items, entity_type="goods")


@bp.route("/goods/new", methods=["GET", "POST"])
@login_required
def create_goods():
    form = GoodsForm()
    if form.validate_on_submit():
        g = Goods(
            description=form.description.data,
        )
        db.session.add(g)
        db.session.flush()
        db.session.add(TransactionLog(entity="Goods", entity_id=g.id, action="CREATE"))
        db.session.commit()
        flash("Goods created", "success")
        return redirect(url_for("system.list_goods"))
    return render_template("system/goods_form.html", form=form, mode="create")


@bp.route("/goods/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_goods(item_id):
    g = Goods.query.get_or_404(item_id)
    form = GoodsForm(obj=g)
    if form.validate_on_submit():
        form.populate_obj(g)
        db.session.add(g)
        db.session.add(TransactionLog(entity="Goods", entity_id=g.id, action="UPDATE"))
        db.session.commit()
        flash("Goods updated", "success")
        return redirect(url_for("system.list_goods"))
    return render_template("system/goods_form.html", form=form, mode="edit", item=g)
