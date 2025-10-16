from flask import Blueprint, request, jsonify, render_template_string
from ..extensions import db, csrf
from ..models import Consignor, Consignee, Goods, Station, PinCode, BookingAgent, Vehicle, Driver, Owner, Order
from ..constants import INDIA_STATES_AND_UTS, to_title

bp = Blueprint("api", __name__, url_prefix="/api")
csrf.exempt(bp)


def _apply_search(query, model, label_attr: str):
    q = request.args.get('q')
    if q:
        query = query.filter(getattr(model, label_attr).ilike(f"%{q}%"))
    return query


def _list(model, label_attr):
    query = model.query
    if model is Station:
        state = request.args.get('state')
        if state:
            query = query.filter(Station.state == state)
    query = _apply_search(query, model, label_attr)
    items = query.order_by(getattr(model, label_attr)).limit(100).all()
    return jsonify([{"id": i.id, "label": getattr(i, label_attr)} for i in items])


@bp.get("/consignors")
def list_consignors():
    query = Consignor.query
    q = request.args.get('q')
    if q:
        query = query.filter(Consignor.name.ilike(f"%{q}%"))
    items = query.order_by(Consignor.name).limit(100).all()
    return jsonify([{"id": i.id, "label": i.name, "station_id": i.station_id} for i in items])


@bp.get("/consignees")
def list_consignees():
    query = Consignee.query
    q = request.args.get('q')
    if q:
        query = query.filter(Consignee.name.ilike(f"%{q}%"))
    items = query.order_by(Consignee.name).limit(100).all()
    return jsonify([{"id": i.id, "label": i.name, "station_id": i.station_id} for i in items])


@bp.get("/goods")
def list_goods():
    return _list(Goods, "description")


@bp.get("/booking_agents")
def list_agents():
    query = BookingAgent.query
    q = request.args.get('q')
    if q:
        query = query.filter(BookingAgent.name.ilike(f"%{q}%"))
    items = query.order_by(BookingAgent.name).limit(100).all()
    return jsonify([{"id": i.id, "label": i.name, "station_id": i.station_id} for i in items])


@bp.get("/stations")
def list_stations():
    return _list(Station, "name")


@bp.get("/stations/<int:station_id>")
def get_station(station_id):
    station = Station.query.get_or_404(station_id)
    return jsonify({
        "id": station.id,
        "name": station.name,
        "state": station.state
    })


@bp.get("/pin_codes")
def list_pin_codes():
    query = PinCode.query
    station_id = request.args.get('station_id')
    if station_id:
        query = query.filter(PinCode.station_id == station_id)
    query = _apply_search(query, PinCode, "code")
    items = query.order_by(PinCode.code).limit(100).all()
    return jsonify([{"id": i.id, "label": f"{i.code} - {i.state or 'Unknown State'}"} for i in items])


@bp.get("/vehicles")
def list_vehicles():
    query = Vehicle.query
    q = request.args.get('q')
    owner_id = request.args.get('owner_id')
    if q:
        query = query.filter(Vehicle.lorry_no.ilike(f"%{q}%"))
    if owner_id:
        query = query.filter(Vehicle.owner_id == owner_id)
    items = query.order_by(Vehicle.lorry_no).limit(100).all()
    return jsonify([{"id": i.id, "label": i.lorry_no, "owner_id": i.owner_id, "driver_id": i.driver_id} for i in items])


@bp.get("/drivers")
def list_drivers():
    query = Driver.query
    q = request.args.get('q')
    vehicle_id = request.args.get('vehicle_id')
    if q:
        query = query.filter(Driver.name.ilike(f"%{q}%"))
    if vehicle_id:
        # Filter drivers by vehicle assignment
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle and vehicle.driver_id:
            query = query.filter(Driver.id == vehicle.driver_id)
    items = query.order_by(Driver.name).limit(100).all()
    return jsonify([{"id": i.id, "label": i.name} for i in items])


@bp.get("/owners")
def list_owners():
    return _list(Owner, "name")


@bp.get("/orders")
def list_orders():
    # label as Order #ID
    query = Order.query
    query = _apply_search(query, Order, "id")
    items = query.order_by(Order.id.desc()).limit(100).all()
    return jsonify([{"id": i.id, "label": f"Order #{i.id}"} for i in items])


_form_templates = {
    "consignors": """
    <form>
      <label>Name</label><input name=\"name\" required />
      <label>State</label><select name=\"state\" required>
        <option value=\"\">Select State</option>
        <option value=\"Andhra Pradesh\">Andhra Pradesh</option>
        <option value=\"Arunachal Pradesh\">Arunachal Pradesh</option>
        <option value=\"Assam\">Assam</option>
        <option value=\"Bihar\">Bihar</option>
        <option value=\"Chhattisgarh\">Chhattisgarh</option>
        <option value=\"Goa\">Goa</option>
        <option value=\"Gujarat\">Gujarat</option>
        <option value=\"Haryana\">Haryana</option>
        <option value=\"Himachal Pradesh\">Himachal Pradesh</option>
        <option value=\"Jharkhand\">Jharkhand</option>
        <option value=\"Karnataka\">Karnataka</option>
        <option value=\"Kerala\">Kerala</option>
        <option value=\"Madhya Pradesh\">Madhya Pradesh</option>
        <option value=\"Maharashtra\">Maharashtra</option>
        <option value=\"Manipur\">Manipur</option>
        <option value=\"Meghalaya\">Meghalaya</option>
        <option value=\"Mizoram\">Mizoram</option>
        <option value=\"Nagaland\">Nagaland</option>
        <option value=\"Odisha\">Odisha</option>
        <option value=\"Punjab\">Punjab</option>
        <option value=\"Rajasthan\">Rajasthan</option>
        <option value=\"Sikkim\">Sikkim</option>
        <option value=\"Tamil Nadu\">Tamil Nadu</option>
        <option value=\"Telangana\">Telangana</option>
        <option value=\"Tripura\">Tripura</option>
        <option value=\"Uttar Pradesh\">Uttar Pradesh</option>
        <option value=\"Uttarakhand\">Uttarakhand</option>
        <option value=\"West Bengal\">West Bengal</option>
        <option value=\"Andaman and Nicobar Islands\">Andaman and Nicobar Islands</option>
        <option value=\"Chandigarh\">Chandigarh</option>
        <option value=\"Dadra and Nagar Haveli and Daman and Diu\">Dadra and Nagar Haveli and Daman and Diu</option>
        <option value=\"Delhi\">Delhi</option>
        <option value=\"Jammu and Kashmir\">Jammu and Kashmir</option>
        <option value=\"Ladakh\">Ladakh</option>
        <option value=\"Lakshadweep\">Lakshadweep</option>
        <option value=\"Puducherry\">Puducherry</option>
      </select>
      <label>Station</label><select name=\"station_pick\" data-populate-source=\"/api/stations\"></select>
      <label>Phone</label><input name=\"phone\" />
      <label>GSTIN</label><input name=\"gstin\" />
      <label>PAN</label><input name=\"pan\" />
      <label>Email</label><input name=\"email\" />
      <div style=\"display:flex;gap:8px;align-items:center;margin-top:8px;\">
        <button class=\"btn\" type=\"submit\">Save</button>
        <button class=\"btn secondary\" data-quick-add=\"stations\" type=\"button\">Add Station</button>
      </div>
    </form>
    """,
    "consignees": """
    <form>
      <label>Name</label><input name=\"name\" required />
      <label>State</label><select name=\"state\" required>
        <option value=\"\">Select State</option>
        <option value=\"Andhra Pradesh\">Andhra Pradesh</option>
        <option value=\"Arunachal Pradesh\">Arunachal Pradesh</option>
        <option value=\"Assam\">Assam</option>
        <option value=\"Bihar\">Bihar</option>
        <option value=\"Chhattisgarh\">Chhattisgarh</option>
        <option value=\"Goa\">Goa</option>
        <option value=\"Gujarat\">Gujarat</option>
        <option value=\"Haryana\">Haryana</option>
        <option value=\"Himachal Pradesh\">Himachal Pradesh</option>
        <option value=\"Jharkhand\">Jharkhand</option>
        <option value=\"Karnataka\">Karnataka</option>
        <option value=\"Kerala\">Kerala</option>
        <option value=\"Madhya Pradesh\">Madhya Pradesh</option>
        <option value=\"Maharashtra\">Maharashtra</option>
        <option value=\"Manipur\">Manipur</option>
        <option value=\"Meghalaya\">Meghalaya</option>
        <option value=\"Mizoram\">Mizoram</option>
        <option value=\"Nagaland\">Nagaland</option>
        <option value=\"Odisha\">Odisha</option>
        <option value=\"Punjab\">Punjab</option>
        <option value=\"Rajasthan\">Rajasthan</option>
        <option value=\"Sikkim\">Sikkim</option>
        <option value=\"Tamil Nadu\">Tamil Nadu</option>
        <option value=\"Telangana\">Telangana</option>
        <option value=\"Tripura\">Tripura</option>
        <option value=\"Uttar Pradesh\">Uttar Pradesh</option>
        <option value=\"Uttarakhand\">Uttarakhand</option>
        <option value=\"West Bengal\">West Bengal</option>
        <option value=\"Andaman and Nicobar Islands\">Andaman and Nicobar Islands</option>
        <option value=\"Chandigarh\">Chandigarh</option>
        <option value=\"Dadra and Nagar Haveli and Daman and Diu\">Dadra and Nagar Haveli and Daman and Diu</option>
        <option value=\"Delhi\">Delhi</option>
        <option value=\"Jammu and Kashmir\">Jammu and Kashmir</option>
        <option value=\"Ladakh\">Ladakh</option>
        <option value=\"Lakshadweep\">Lakshadweep</option>
        <option value=\"Puducherry\">Puducherry</option>
      </select>
      <label>Station</label><select name=\"station_pick\" data-populate-source=\"/api/stations\"></select>
      <label>Phone</label><input name=\"phone\" />
      <label>GSTIN</label><input name=\"gstin\" />
      <label>PAN</label><input name=\"pan\" />
      <label>Email</label><input name=\"email\" />
      <div style=\"display:flex;gap:8px;align-items:center;margin-top:8px;\">
        <button class=\"btn\" type=\"submit\">Save</button>
        <button class=\"btn secondary\" data-quick-add=\"stations\" type=\"button\">Add Station</button>
      </div>
    </form>
    """,
    "goods": """
    <form>
      <label>Description</label><input name=\"description\" required />
      <button class=\"btn\" type=\"submit\">Save</button>
    </form>
    """,
    "booking_agents": """
    <form>
      <label>Name</label><input name=\"name\" required />
      <label>Phone</label><input name=\"phone\" />
      <label>GSTIN</label><input name=\"gstin\" />
      <label>PAN</label><input name=\"pan\" />
      <label>Email</label><input name=\"email\" />
      <button class=\"btn\" type=\"submit\">Save</button>
    </form>
    """,
    "stations": """
    <form>
      <label>Name</label><input name=\"name\" required />
      <label>State</label><select name=\"state\" required>
        <option value=\"\">Select State</option>
        <option value=\"Andhra Pradesh\">Andhra Pradesh</option>
        <option value=\"Arunachal Pradesh\">Arunachal Pradesh</option>
        <option value=\"Assam\">Assam</option>
        <option value=\"Bihar\">Bihar</option>
        <option value=\"Chhattisgarh\">Chhattisgarh</option>
        <option value=\"Goa\">Goa</option>
        <option value=\"Gujarat\">Gujarat</option>
        <option value=\"Haryana\">Haryana</option>
        <option value=\"Himachal Pradesh\">Himachal Pradesh</option>
        <option value=\"Jharkhand\">Jharkhand</option>
        <option value=\"Karnataka\">Karnataka</option>
        <option value=\"Kerala\">Kerala</option>
        <option value=\"Madhya Pradesh\">Madhya Pradesh</option>
        <option value=\"Maharashtra\">Maharashtra</option>
        <option value=\"Manipur\">Manipur</option>
        <option value=\"Meghalaya\">Meghalaya</option>
        <option value=\"Mizoram\">Mizoram</option>
        <option value=\"Nagaland\">Nagaland</option>
        <option value=\"Odisha\">Odisha</option>
        <option value=\"Punjab\">Punjab</option>
        <option value=\"Rajasthan\">Rajasthan</option>
        <option value=\"Sikkim\">Sikkim</option>
        <option value=\"Tamil Nadu\">Tamil Nadu</option>
        <option value=\"Telangana\">Telangana</option>
        <option value=\"Tripura\">Tripura</option>
        <option value=\"Uttar Pradesh\">Uttar Pradesh</option>
        <option value=\"Uttarakhand\">Uttarakhand</option>
        <option value=\"West Bengal\">West Bengal</option>
        <option value=\"Andaman and Nicobar Islands\">Andaman and Nicobar Islands</option>
        <option value=\"Chandigarh\">Chandigarh</option>
        <option value=\"Dadra and Nagar Haveli and Daman and Diu\">Dadra and Nagar Haveli and Daman and Diu</option>
        <option value=\"Delhi\">Delhi</option>
        <option value=\"Jammu and Kashmir\">Jammu and Kashmir</option>
        <option value=\"Ladakh\">Ladakh</option>
        <option value=\"Lakshadweep\">Lakshadweep</option>
        <option value=\"Puducherry\">Puducherry</option>
      </select>
      <button class=\"btn\" type=\"submit\">Save</button>
    </form>
    """,
    "pin_codes": """
    <form>
      <label>Pin Code</label><input name=\"code\" required />
      <label>State</label><select name=\"state\" required>
        <option value=\"\">Select State</option>
        <option value=\"Andhra Pradesh\">Andhra Pradesh</option>
        <option value=\"Arunachal Pradesh\">Arunachal Pradesh</option>
        <option value=\"Assam\">Assam</option>
        <option value=\"Bihar\">Bihar</option>
        <option value=\"Chhattisgarh\">Chhattisgarh</option>
        <option value=\"Goa\">Goa</option>
        <option value=\"Gujarat\">Gujarat</option>
        <option value=\"Haryana\">Haryana</option>
        <option value=\"Himachal Pradesh\">Himachal Pradesh</option>
        <option value=\"Jharkhand\">Jharkhand</option>
        <option value=\"Karnataka\">Karnataka</option>
        <option value=\"Kerala\">Kerala</option>
        <option value=\"Madhya Pradesh\">Madhya Pradesh</option>
        <option value=\"Maharashtra\">Maharashtra</option>
        <option value=\"Manipur\">Manipur</option>
        <option value=\"Meghalaya\">Meghalaya</option>
        <option value=\"Mizoram\">Mizoram</option>
        <option value=\"Nagaland\">Nagaland</option>
        <option value=\"Odisha\">Odisha</option>
        <option value=\"Punjab\">Punjab</option>
        <option value=\"Rajasthan\">Rajasthan</option>
        <option value=\"Sikkim\">Sikkim</option>
        <option value=\"Tamil Nadu\">Tamil Nadu</option>
        <option value=\"Telangana\">Telangana</option>
        <option value=\"Tripura\">Tripura</option>
        <option value=\"Uttar Pradesh\">Uttar Pradesh</option>
        <option value=\"Uttarakhand\">Uttarakhand</option>
        <option value=\"West Bengal\">West Bengal</option>
        <option value=\"Andaman and Nicobar Islands\">Andaman and Nicobar Islands</option>
        <option value=\"Chandigarh\">Chandigarh</option>
        <option value=\"Dadra and Nagar Haveli and Daman and Diu\">Dadra and Nagar Haveli and Daman and Diu</option>
        <option value=\"Delhi\">Delhi</option>
        <option value=\"Jammu and Kashmir\">Jammu and Kashmir</option>
        <option value=\"Ladakh\">Ladakh</option>
        <option value=\"Lakshadweep\">Lakshadweep</option>
        <option value=\"Puducherry\">Puducherry</option>
      </select>
      <label>Station</label><select name=\"station_pick\" data-populate-source=\"/api/stations\"></select>
      <div style=\"display:flex;gap:8px;align-items:center;margin-top:8px;\">
        <button class=\"btn\" type=\"submit\">Save</button>
        <button class=\"btn secondary\" data-quick-add=\"stations\" type=\"button\">Add Station</button>
      </div>
    </form>
    """,
    "vehicles": """
    <form>
      <label>Lorry No</label><input name=\"lorry_no\" required />
      <label>Chassis No</label><input name=\"chassis_no\" />
      <label>Engine No</label><input name=\"engine_no\" />
      <button class=\"btn\" type=\"submit\">Save</button>
    </form>
    """,
    "drivers": """
    <form>
      <label>Name</label><input name=\"name\" required />
      <label>License No</label><input name=\"license_no\" required />
      <label>Phone</label><input name=\"phone\" />
      <button class=\"btn\" type=\"submit\">Save</button>
    </form>
    """,
    "owners": """
    <form>
      <label>Name</label><input name=\"name\" required />
      <label>Phone</label><input name=\"phone\" />
      <button class=\"btn\" type=\"submit\">Save</button>
    </form>
    """,
}


@bp.get("/<entity>/new")
def inline_new(entity):
    html = _form_templates.get(entity)
    if not html:
        return ("Unsupported", 400)
    return render_template_string(html)


def _normalize_name(s: str) -> str:
    return to_title(s.strip()) if s else s


def _dedupe_by_name(model, name_field: str, name: str):
    # case-insensitive lookup
    return model.query.filter(db.func.lower(getattr(model, name_field)) == name.lower()).first()


@bp.post("/consignors")
def create_consignor():
    name = _normalize_name(request.form.get("name"))
    existing = _dedupe_by_name(Consignor, "name", name) if name else None
    if existing:
        return jsonify({"id": existing.id, "label": existing.name})
    
    # Get station info if station_pick is provided
    station_id = request.form.get("station_pick")
    station = Station.query.get(station_id) if station_id else None
    
    c = Consignor(
        name=name,
        station_id=station.id if station else None,
        phone=request.form.get("phone"), 
        gstin=request.form.get("gstin"), 
        pan=request.form.get("pan"), 
        email=request.form.get("email")
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id, "label": c.name})


@bp.post("/consignees")
def create_consignees():
    name = _normalize_name(request.form.get("name"))
    existing = _dedupe_by_name(Consignee, "name", name) if name else None
    if existing:
        return jsonify({"id": existing.id, "label": existing.name})
    
    # Get station info if station_pick is provided
    station_id = request.form.get("station_pick")
    station = Station.query.get(station_id) if station_id else None
    
    c = Consignee(
        name=name,
        station_id=station.id if station else None,
        phone=request.form.get("phone"), 
        gstin=request.form.get("gstin"), 
        pan=request.form.get("pan"), 
        email=request.form.get("email")
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"id": c.id, "label": c.name})


@bp.post("/goods")
def create_goods():
    desc = _normalize_name(request.form.get("description"))
    existing = Goods.query.filter(db.func.lower(Goods.description) == desc.lower()).first() if desc else None
    if existing:
        return jsonify({"id": existing.id, "label": existing.description})
    g = Goods(description=desc)
    db.session.add(g)
    db.session.commit()
    return jsonify({"id": g.id, "label": g.description})


@bp.post("/booking_agents")
def create_agents():
    name = _normalize_name(request.form.get("name"))
    existing = _dedupe_by_name(BookingAgent, "name", name) if name else None
    if existing:
        return jsonify({"id": existing.id, "label": existing.name})
    a = BookingAgent(name=name, phone=request.form.get("phone"), gstin=request.form.get("gstin"), pan=request.form.get("pan"), email=request.form.get("email"))
    db.session.add(a)
    db.session.commit()
    return jsonify({"id": a.id, "label": a.name})


@bp.post("/stations")
def create_stations():
    name = _normalize_name(request.form.get("name"))
    existing = _dedupe_by_name(Station, "name", name) if name else None
    if existing:
        return jsonify({"id": existing.id, "label": existing.name})
    s = Station(name=name, state=request.form.get("state"))
    db.session.add(s)
    db.session.commit()
    return jsonify({"id": s.id, "label": s.name})


@bp.post("/pin_codes")
def create_pin_codes():
    code = request.form.get("code")
    existing = PinCode.query.filter(PinCode.code == code).first() if code else None
    if existing:
        return jsonify({"id": existing.id, "label": f"{existing.code} - {existing.state or 'Unknown State'}"})
    
    # Get station info if station_pick is provided
    station_id = request.form.get("station_pick")
    station = Station.query.get(station_id) if station_id else None
    
    p = PinCode(
        code=code,
        state=request.form.get("state"),
        station_id=station.id if station else None
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id, "label": f"{p.code} - {p.state or 'Unknown State'}"})


@bp.post("/vehicles")
def create_vehicle():
    lorry_no = request.form.get("lorry_no")
    existing = Vehicle.query.filter(db.func.lower(Vehicle.lorry_no) == (lorry_no or '').lower()).first() if lorry_no else None
    if existing:
        return jsonify({"id": existing.id, "label": existing.lorry_no})
    v = Vehicle(lorry_no=lorry_no, chassis_no=request.form.get("chassis_no"), engine_no=request.form.get("engine_no"))
    db.session.add(v)
    db.session.commit()
    return jsonify({"id": v.id, "label": v.lorry_no})


@bp.post("/drivers")
def create_driver():
    name = _normalize_name(request.form.get("name"))
    existing = _dedupe_by_name(Driver, "name", name) if name else None
    if existing:
        return jsonify({"id": existing.id, "label": existing.name})
    d = Driver(name=name, license_no=request.form.get("license_no"), phone=request.form.get("phone"))
    db.session.add(d)
    db.session.commit()
    return jsonify({"id": d.id, "label": d.name})


@bp.post("/owners")
def create_owner():
    name = _normalize_name(request.form.get("name"))
    existing = _dedupe_by_name(Owner, "name", name) if name else None
    if existing:
        return jsonify({"id": existing.id, "label": existing.name})
    o = Owner(name=name, phone=request.form.get("phone"))
    db.session.add(o)
    db.session.commit()
    return jsonify({"id": o.id, "label": o.name})
