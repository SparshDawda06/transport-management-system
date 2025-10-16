from datetime import datetime
from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class PinCode(db.Model, TimestampMixin):
    __tablename__ = "pin_codes"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    state = db.Column(db.String(64), nullable=True)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="SET NULL"))
    station = db.relationship("Station", back_populates="pin_codes")


class Address(db.Model, TimestampMixin):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    line1 = db.Column(db.String(255))
    line2 = db.Column(db.String(255))
    city = db.Column(db.String(128))
    district = db.Column(db.String(128))
    state = db.Column(db.String(64))
    pin_code_id = db.Column(db.Integer, db.ForeignKey("pin_codes.id", ondelete="RESTRICT"))
    pin_code_text = db.Column(db.String(10))
    pin_code = db.relationship("PinCode")


class Consignor(db.Model, TimestampMixin):
    __tablename__ = "consignors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    address = db.Column(db.String(512))
    gstin = db.Column(db.String(32), unique=True)
    pan = db.Column(db.String(16), unique=False)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="SET NULL"))
    pin_code_id = db.Column(db.Integer, db.ForeignKey("pin_codes.id", ondelete="SET NULL"))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(128))
    holiday_info = db.Column(db.Text)
    station = db.relationship("Station")
    pin_code = db.relationship("PinCode")
    __table_args__ = (
        db.UniqueConstraint("name", "station_id", name="uq_consignor_name_station"),
    )


class Consignee(db.Model, TimestampMixin):
    __tablename__ = "consignees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    address = db.Column(db.String(512))
    gstin = db.Column(db.String(32), unique=True)
    pan = db.Column(db.String(16))
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="SET NULL"))
    pin_code_id = db.Column(db.Integer, db.ForeignKey("pin_codes.id", ondelete="SET NULL"))
    phone = db.Column(db.String(32))
    email = db.Column(db.String(128))
    holiday_info = db.Column(db.Text)
    station = db.relationship("Station")
    pin_code = db.relationship("PinCode")
    __table_args__ = (
        db.UniqueConstraint("name", "station_id", name="uq_consignee_name_station"),
    )


class BookingAgent(db.Model, TimestampMixin):
    __tablename__ = "booking_agents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    phone = db.Column(db.String(32))
    gstin = db.Column(db.String(32))
    pan = db.Column(db.String(16))
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="SET NULL"))
    city = db.Column(db.String(128))
    state = db.Column(db.String(64))
    email = db.Column(db.String(128))
    station = db.relationship("Station")


class Goods(db.Model, TimestampMixin):
    __tablename__ = "goods"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False, unique=True)


class Owner(db.Model, TimestampMixin):
    __tablename__ = "owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    phone = db.Column(db.String(32))
    pan = db.Column(db.String(16))
    aadhar = db.Column(db.String(20))
    address = db.Column(db.String(512))


class Driver(db.Model, TimestampMixin):
    __tablename__ = "drivers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    address = db.Column(db.String(512))
    license_no = db.Column(db.String(64), nullable=False, unique=True)
    validity = db.Column(db.Date)
    license_file = db.Column(db.String(255))
    rto = db.Column(db.String(64))
    aadhar = db.Column(db.String(20))
    phone = db.Column(db.String(32))


class Station(db.Model, TimestampMixin):
    __tablename__ = "stations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    state = db.Column(db.String(64))
    pin_codes = db.relationship("PinCode", back_populates="station")


class Vehicle(db.Model, TimestampMixin):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    lorry_no = db.Column(db.String(32), nullable=False, unique=True, index=True)
    capacity = db.Column(db.Float)
    chassis_no = db.Column(db.String(64))
    engine_no = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id", ondelete="RESTRICT"), nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True)
    rc_file = db.Column(db.String(255))
    insurance_file = db.Column(db.String(255))
    insurance_status = db.Column(db.String(64))

    owner = db.relationship("Owner")
    driver = db.relationship("Driver")


class Order(db.Model, TimestampMixin):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    firm = db.Column(db.String(255), nullable=False, default="New Jalaram Transport Service")
    order_type = db.Column(db.String(32), default="PARTY")  # PARTY or AGENT
    
    # Station references
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="RESTRICT"), nullable=True)  # Deprecated, kept for compatibility
    from_station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="RESTRICT"), nullable=True)
    to_station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="RESTRICT"), nullable=True)
    station_pin_code = db.Column(db.String(10))
    
    # Party details (when order_type = PARTY)
    consignor_id = db.Column(db.Integer, db.ForeignKey("consignors.id", ondelete="RESTRICT"), nullable=True)
    consignee_id = db.Column(db.Integer, db.ForeignKey("consignees.id", ondelete="RESTRICT"), nullable=True)
    consignor_phone = db.Column(db.String(32))  # Legacy field
    consignee_phone = db.Column(db.String(32))  # Legacy field
    
    # New phone book fields
    consignor_concerned_person_id = db.Column(db.Integer, db.ForeignKey("concerned_persons.id", ondelete="SET NULL"), nullable=True)
    consignor_phone_number_id = db.Column(db.Integer, db.ForeignKey("phone_book.id", ondelete="SET NULL"), nullable=True)
    consignee_concerned_person_id = db.Column(db.Integer, db.ForeignKey("concerned_persons.id", ondelete="SET NULL"), nullable=True)
    consignee_phone_number_id = db.Column(db.Integer, db.ForeignKey("phone_book.id", ondelete="SET NULL"), nullable=True)
    
    # Agent details (when order_type = AGENT)
    booking_agent_id = db.Column(db.Integer, db.ForeignKey("booking_agents.id", ondelete="SET NULL"))
    agent_concerned_person_id = db.Column(db.Integer, db.ForeignKey("concerned_persons.id", ondelete="SET NULL"), nullable=True)
    agent_phone_number_id = db.Column(db.Integer, db.ForeignKey("phone_book.id", ondelete="SET NULL"), nullable=True)
    
    # Goods information
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id", ondelete="RESTRICT"), nullable=False)
    weight = db.Column(db.Float)
    rate = db.Column(db.Float)
    description = db.Column(db.String(512))
    order_by = db.Column(db.String(255))
    party = db.Column(db.String(255))
    status = db.Column(db.String(32), default="NEW", index=True)

    # Relationships
    station = db.relationship("Station", foreign_keys=[station_id])
    from_station = db.relationship("Station", foreign_keys=[from_station_id])
    to_station = db.relationship("Station", foreign_keys=[to_station_id])
    consignor = db.relationship("Consignor")
    consignee = db.relationship("Consignee")
    goods = db.relationship("Goods")
    booking_agent = db.relationship("BookingAgent")
    
    # Phone book relationships
    consignor_concerned_person = db.relationship("ConcernedPerson", foreign_keys=[consignor_concerned_person_id])
    consignor_phone_number = db.relationship("PhoneBook", foreign_keys=[consignor_phone_number_id])
    consignee_concerned_person = db.relationship("ConcernedPerson", foreign_keys=[consignee_concerned_person_id])
    consignee_phone_number = db.relationship("PhoneBook", foreign_keys=[consignee_phone_number_id])
    agent_concerned_person = db.relationship("ConcernedPerson", foreign_keys=[agent_concerned_person_id])
    agent_phone_number = db.relationship("PhoneBook", foreign_keys=[agent_phone_number_id])


class Builty(db.Model, TimestampMixin):
    __tablename__ = "builty"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id", ondelete="RESTRICT"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id", ondelete="RESTRICT"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id", ondelete="RESTRICT"), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    firm = db.Column(db.String(255))
    lr_no = db.Column(db.String(64))
    from_station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="RESTRICT"), nullable=False)
    to_station_id = db.Column(db.Integer, db.ForeignKey("stations.id", ondelete="RESTRICT"), nullable=False)
    status = db.Column(db.String(32), default="IN_TRANSIT", index=True)
    invoice_no = db.Column(db.String(64))
    eway_bill_no = db.Column(db.String(64))
    lr_file = db.Column(db.String(255))
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id", ondelete="SET NULL"))
    actual_weight = db.Column(db.Float)
    charged_weight = db.Column(db.Float)
    rate = db.Column(db.Float)
    advance_amount = db.Column(db.Float)
    
    # Party fields (inherited from order but can be overridden)
    consignor_id = db.Column(db.Integer, db.ForeignKey("consignors.id", ondelete="SET NULL"), nullable=True)
    consignor_phone = db.Column(db.String(32))  # Legacy field
    consignee_id = db.Column(db.Integer, db.ForeignKey("consignees.id", ondelete="SET NULL"), nullable=True)
    consignee_phone = db.Column(db.String(32))  # Legacy field
    
    # Phone book fields
    consignor_concerned_person_id = db.Column(db.Integer, db.ForeignKey("concerned_persons.id", ondelete="SET NULL"), nullable=True)
    consignor_phone_number_id = db.Column(db.Integer, db.ForeignKey("phone_book.id", ondelete="SET NULL"), nullable=True)
    consignee_concerned_person_id = db.Column(db.Integer, db.ForeignKey("concerned_persons.id", ondelete="SET NULL"), nullable=True)
    consignee_phone_number_id = db.Column(db.Integer, db.ForeignKey("phone_book.id", ondelete="SET NULL"), nullable=True)
    agent_concerned_person_id = db.Column(db.Integer, db.ForeignKey("concerned_persons.id", ondelete="SET NULL"), nullable=True)
    agent_phone_number_id = db.Column(db.Integer, db.ForeignKey("phone_book.id", ondelete="SET NULL"), nullable=True)
    
    # Agent field (inherited from order but can be overridden)
    booking_agent_id = db.Column(db.Integer, db.ForeignKey("booking_agents.id", ondelete="SET NULL"), nullable=True)

    order = db.relationship("Order")
    vehicle = db.relationship("Vehicle")
    driver = db.relationship("Driver")
    owner = db.relationship("Owner")
    from_station = db.relationship("Station", foreign_keys=[from_station_id])
    to_station = db.relationship("Station", foreign_keys=[to_station_id])
    goods = db.relationship("Goods")
    consignor = db.relationship("Consignor")
    consignee = db.relationship("Consignee")
    booking_agent = db.relationship("BookingAgent")
    
    # Phone book relationships
    consignor_concerned_person = db.relationship("ConcernedPerson", foreign_keys=[consignor_concerned_person_id])
    consignor_phone_number = db.relationship("PhoneBook", foreign_keys=[consignor_phone_number_id])
    consignee_concerned_person = db.relationship("ConcernedPerson", foreign_keys=[consignee_concerned_person_id])
    consignee_phone_number = db.relationship("PhoneBook", foreign_keys=[consignee_phone_number_id])
    agent_concerned_person = db.relationship("ConcernedPerson", foreign_keys=[agent_concerned_person_id])
    agent_phone_number = db.relationship("PhoneBook", foreign_keys=[agent_phone_number_id])


class ConcernedPerson(db.Model, TimestampMixin):
    __tablename__ = "concerned_persons"
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(32), nullable=False, index=True)  # CONSIGNOR, CONSIGNEE, AGENT, DRIVER, OWNER
    entity_id = db.Column(db.Integer, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    designation = db.Column(db.String(128))  # e.g., "Manager", "CEO", "Operations Head"
    is_primary = db.Column(db.Boolean, default=False)  # Primary contact person
    
    __table_args__ = (
        db.Index("ix_concerned_entity", "entity_type", "entity_id"),
        db.UniqueConstraint("entity_type", "entity_id", "is_primary", name="uq_primary_concerned"),
    )


class PhoneBook(db.Model, TimestampMixin):
    __tablename__ = "phone_book"
    id = db.Column(db.Integer, primary_key=True)
    concerned_person_id = db.Column(db.Integer, db.ForeignKey("concerned_persons.id", ondelete="CASCADE"), nullable=False)
    phone_number = db.Column(db.String(32), nullable=False, unique=True)  # Prevent duplicate phone numbers
    is_primary = db.Column(db.Boolean, default=False)  # Only one primary per concerned person
    label = db.Column(db.String(64))  # e.g., "Mobile", "Office", "Home"
    
    # Relationship
    concerned_person = db.relationship("ConcernedPerson", backref="phone_numbers")
    
    __table_args__ = (
        db.UniqueConstraint("concerned_person_id", "is_primary", name="uq_primary_phone_per_person"),
    )


class TransactionLog(db.Model, TimestampMixin):
    __tablename__ = "transaction_logs"
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(64), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(64), nullable=False)
    note = db.Column(db.Text)
    at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.Index("ix_tx_entity", "entity", "entity_id"),
    )
