from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional, Length
from .constants import INDIA_STATES_AND_UTS

# Helper function to handle coerce for optional integer fields
def coerce_int_or_none(value):
    """Convert value to int if valid, otherwise return None for empty/None values"""
    if value is None or value == '' or value == 0:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


class ConsignorForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    address = TextAreaField("Address", validators=[Optional(), Length(max=512)])
    gstin = StringField("GSTIN", validators=[Optional(), Length(max=32)])
    pan = StringField("PAN", validators=[Optional(), Length(max=16)])
    station_id = SelectField("Station", coerce=coerce_int_or_none, validators=[Optional()])
    pin_code_id = SelectField("Pin Code", coerce=coerce_int_or_none, validators=[Optional()])
    phone = StringField("Phone", validators=[Optional(), Length(max=32)])
    email = StringField("Email", validators=[Optional(), Length(max=128)])
    concerned_person_id = SelectField("Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    phone_number_id = SelectField("Phone Number", coerce=coerce_int_or_none, validators=[Optional()])


class ConsigneeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    address = TextAreaField("Address", validators=[Optional(), Length(max=512)])
    gstin = StringField("GSTIN", validators=[Optional(), Length(max=32)])
    pan = StringField("PAN", validators=[Optional(), Length(max=16)])
    station_id = SelectField("Station", coerce=coerce_int_or_none, validators=[Optional()])
    pin_code_id = SelectField("Pin Code", coerce=coerce_int_or_none, validators=[Optional()])
    phone = StringField("Phone", validators=[Optional(), Length(max=32)])
    email = StringField("Email", validators=[Optional(), Length(max=128)])
    concerned_person_id = SelectField("Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    phone_number_id = SelectField("Phone Number", coerce=coerce_int_or_none, validators=[Optional()])


class GoodsForm(FlaskForm):
    description = StringField("Description", validators=[DataRequired(), Length(max=255)])


class StationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    state = SelectField("State", choices=[(s, s) for s in INDIA_STATES_AND_UTS], validators=[Optional()])


class PinCodeForm(FlaskForm):
    code = StringField("Pin Code", validators=[DataRequired(), Length(max=10)])
    state = SelectField("State", choices=[(s, s) for s in INDIA_STATES_AND_UTS], validators=[Optional()])
    station_id = SelectField("Station", coerce=coerce_int_or_none, validators=[Optional()])


class BookingAgentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    phone = StringField("Phone", validators=[Optional(), Length(max=32)])
    gstin = StringField("GSTIN", validators=[Optional(), Length(max=32)])
    pan = StringField("PAN", validators=[Optional(), Length(max=16)])
    station_id = SelectField("Station", coerce=coerce_int_or_none, validators=[Optional()])
    city = StringField("City", validators=[Optional(), Length(max=128)])
    state = SelectField("State", choices=[(s, s) for s in INDIA_STATES_AND_UTS], validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Length(max=128)])
    concerned_person_id = SelectField("Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    phone_number_id = SelectField("Phone Number", coerce=coerce_int_or_none, validators=[Optional()])


class OwnerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    pan = StringField("PAN", validators=[Optional(), Length(max=16)])
    aadhar = StringField("Aadhaar", validators=[Optional(), Length(max=20)])
    address = TextAreaField("Address", validators=[Optional(), Length(max=512)])
    concerned_person_id = SelectField("Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    phone_number_id = SelectField("Phone Number", coerce=coerce_int_or_none, validators=[Optional()])


class DriverForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    address = TextAreaField("Address", validators=[Optional(), Length(max=512)])
    license_no = StringField("License No", validators=[DataRequired(), Length(max=64)])
    validity = DateField("Validity", validators=[Optional()])
    aadhar = StringField("Aadhaar", validators=[Optional(), Length(max=20)])
    concerned_person_id = SelectField("Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    phone_number_id = SelectField("Phone Number", coerce=coerce_int_or_none, validators=[Optional()])


class VehicleForm(FlaskForm):
    lorry_no = StringField("Lorry No", validators=[DataRequired(), Length(max=32)])
    capacity = FloatField("Capacity", validators=[Optional()])
    chassis_no = StringField("Chassis No", validators=[Optional(), Length(max=64)])
    engine_no = StringField("Engine No", validators=[Optional(), Length(max=64)])
    owner_id = SelectField("Owner", coerce=coerce_int_or_none, validators=[Optional()])
    driver_id = SelectField("Driver", coerce=coerce_int_or_none, validators=[Optional()])


class OrderForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    firm = SelectField("Firm", choices=[
        ("New Jalaram Transport Service", "New Jalaram Transport Service"),
        ("Jayshree Transport Company", "Jayshree Transport Company"),
        ("Jalaram Cargo", "Jalaram Cargo")
    ], validators=[DataRequired()])
    order_type = SelectField("Order Type", choices=[
        ("PARTY", "Party (Consignor/Consignee)"),
        ("AGENT", "Agent")
    ], validators=[DataRequired()])
    
    # Stations
    from_station_id = SelectField("From Station", coerce=coerce_int_or_none, validators=[Optional()])
    to_station_id = SelectField("To Station", coerce=coerce_int_or_none, validators=[Optional()])
    station_pin_code = StringField("Station Pin Code", validators=[Optional(), Length(max=10)])
    
    # Party fields
    consignor_id = SelectField("Consignor", coerce=coerce_int_or_none, validators=[Optional()])
    consignor_phone = StringField("Consignor Phone", validators=[Optional(), Length(max=32)])  # Legacy field
    consignee_id = SelectField("Consignee", coerce=coerce_int_or_none, validators=[Optional()])
    consignee_phone = StringField("Consignee Phone", validators=[Optional(), Length(max=32)])  # Legacy field
    
    # New phone book fields
    consignor_concerned_person_id = SelectField("Consignor Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    consignor_phone_number_id = SelectField("Consignor Phone Number", coerce=coerce_int_or_none, validators=[Optional()])
    consignee_concerned_person_id = SelectField("Consignee Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    consignee_phone_number_id = SelectField("Consignee Phone Number", coerce=coerce_int_or_none, validators=[Optional()])
    
    # Agent field
    booking_agent_id = SelectField("Booking Agent", coerce=coerce_int_or_none, validators=[Optional()])
    agent_concerned_person_id = SelectField("Agent Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    agent_phone_number_id = SelectField("Agent Phone Number", coerce=coerce_int_or_none, validators=[Optional()])
    
    # Goods
    goods_id = SelectField("Goods", coerce=coerce_int_or_none, validators=[DataRequired()])
    weight = FloatField("Weight", validators=[Optional()])
    rate = FloatField("Rate", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional(), Length(max=512)])
    status = SelectField("Status", choices=[("NEW","NEW"),("CONFIRMED","CONFIRMED"),("DISPATCHED","DISPATCHED"),("CLOSED","CLOSED")])


class BuiltyForm(FlaskForm):
    order_id = SelectField("Order", coerce=coerce_int_or_none, validators=[Optional()])
    vehicle_id = SelectField("Vehicle", coerce=coerce_int_or_none, validators=[Optional()])
    driver_id = SelectField("Driver", coerce=coerce_int_or_none, validators=[Optional()])
    owner_id = SelectField("Owner", coerce=coerce_int_or_none, validators=[Optional()])
    date = DateField("Date", validators=[Optional()])
    from_station_id = SelectField("From Station", coerce=coerce_int_or_none, validators=[Optional()])
    to_station_id = SelectField("To Station", coerce=coerce_int_or_none, validators=[Optional()])
    firm = SelectField("Firm", choices=[
        ("New Jalaram Transport Service", "New Jalaram Transport Service"),
        ("Jayshree Transport Company", "Jayshree Transport Company"),
        ("Jalaram Cargo", "Jalaram Cargo")
    ], validators=[Optional()])
    lr_no = StringField("LR No", validators=[Optional(), Length(max=64)])
    goods_id = SelectField("Goods", coerce=coerce_int_or_none, validators=[Optional()])
    actual_weight = FloatField("Actual Weight", validators=[Optional()])
    charged_weight = FloatField("Charged Weight", validators=[Optional()])
    rate = FloatField("Rate", validators=[Optional()])
    advance_amount = FloatField("Advance Amount", validators=[Optional()])
    invoice_no = StringField("Invoice No", validators=[Optional(), Length(max=64)])
    eway_bill_no = StringField("E-Way Bill No", validators=[Optional(), Length(max=64)])
    status = SelectField("Status", choices=[("IN_TRANSIT","IN_TRANSIT"),("DELIVERED","DELIVERED")])
    
    # Party fields (inherited from order but can be overridden)
    consignor_id = SelectField("Consignor", coerce=coerce_int_or_none, validators=[Optional()])
    consignor_concerned_person_id = SelectField("Consignor Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    consignor_phone_number_id = SelectField("Consignor Phone Number", coerce=coerce_int_or_none, validators=[Optional()])
    consignee_id = SelectField("Consignee", coerce=coerce_int_or_none, validators=[Optional()])
    consignee_concerned_person_id = SelectField("Consignee Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    consignee_phone_number_id = SelectField("Consignee Phone Number", coerce=coerce_int_or_none, validators=[Optional()])
    
    # Agent field (inherited from order but can be overridden)
    booking_agent_id = SelectField("Booking Agent", coerce=coerce_int_or_none, validators=[Optional()])
    agent_concerned_person_id = SelectField("Agent Concerned Person", coerce=coerce_int_or_none, validators=[Optional()])
    agent_phone_number_id = SelectField("Agent Phone Number", coerce=coerce_int_or_none, validators=[Optional()])