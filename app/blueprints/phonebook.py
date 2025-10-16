from flask import Blueprint, request, jsonify, render_template
from ..extensions import db, csrf
from ..models import PhoneBook, ConcernedPerson, Consignor, Consignee, BookingAgent, Driver, Owner
from ..auth import login_required

bp = Blueprint("phonebook", __name__, url_prefix="/phonebook")


@bp.route("/")
@login_required
def list_phonebook():
    """Phone book management interface"""
    entity_type = request.args.get('entity', '').upper()
    entity_id = request.args.get('id')
    return_url = request.args.get('return_url')
    search_query = request.args.get('search', '')
    search_type = request.args.get('search_type', 'all')
    
    return render_template("phonebook/list.html", 
                         entity_type=entity_type, 
                         entity_id=entity_id,
                         return_url=return_url,
                         search_query=search_query,
                         search_type=search_type)


@bp.route("/api/search")
@login_required
def search_phonebook():
    """Search phone numbers across all entities with enhanced search options"""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all').lower()
    
    if not query:
        return jsonify([])
    
    # Build search query based on type
    if search_type == 'phone':
        # Search by phone number
        phone_entries = PhoneBook.query.filter(
            PhoneBook.phone_number.contains(query)
        ).all()
    elif search_type == 'name':
        # Search by concerned person name
        phone_entries = PhoneBook.query.join(ConcernedPerson).filter(
            ConcernedPerson.name.contains(query)
        ).all()
    elif search_type == 'company':
        # Search by company name
        phone_entries = PhoneBook.query.join(ConcernedPerson).all()
        # Filter by company name
        filtered_entries = []
        for entry in phone_entries:
            entity = get_entity_by_type_and_id(entry.concerned_person.entity_type, entry.concerned_person.entity_id)
            if entity and query.lower() in entity.name.lower():
                filtered_entries.append(entry)
        phone_entries = filtered_entries
    else:
        # Search all fields
        phone_entries = PhoneBook.query.join(ConcernedPerson).filter(
            (PhoneBook.phone_number.contains(query)) |
            (ConcernedPerson.name.contains(query))
        ).all()
        
        # Also search by company names
        all_entries = PhoneBook.query.join(ConcernedPerson).all()
        for entry in all_entries:
            entity = get_entity_by_type_and_id(entry.concerned_person.entity_type, entry.concerned_person.entity_id)
            if entity and query.lower() in entity.name.lower() and entry not in phone_entries:
                phone_entries.append(entry)
    
    results = []
    for entry in phone_entries:
        # Get concerned person details
        concerned_person = entry.concerned_person
        entity = get_entity_by_type_and_id(concerned_person.entity_type, concerned_person.entity_id)
        
        results.append({
            'id': entry.id,
            'phone_number': entry.phone_number,
            'label': entry.label or 'Primary',
            'is_primary': entry.is_primary,
            'entity_type': concerned_person.entity_type,
            'entity_id': concerned_person.entity_id,
            'entity_name': entity.name if entity else "Unknown",
            'person_name': concerned_person.name,
            'person_designation': concerned_person.designation or '',
            'person_is_primary': concerned_person.is_primary,
            'display_name': f"{entity.name if entity else 'Unknown'} ({concerned_person.entity_type}) - {entry.phone_number}"
        })
    
    return jsonify(results)

def get_entity_by_type_and_id(entity_type, entity_id):
    """Helper function to get entity by type and ID"""
    if entity_type == 'CONSIGNOR':
        return Consignor.query.get(entity_id)
    elif entity_type == 'CONSIGNEE':
        return Consignee.query.get(entity_id)
    elif entity_type == 'AGENT':
        return BookingAgent.query.get(entity_id)
    elif entity_type == 'DRIVER':
        return Driver.query.get(entity_id)
    elif entity_type == 'OWNER':
        return Owner.query.get(entity_id)
    return None


@bp.route("/api/entity/<entity_type>/<int:entity_id>")
def get_entity_phones(entity_type, entity_id):
    """Get all phone numbers for a specific entity"""
    # Get all concerned persons for this entity
    concerned_persons = ConcernedPerson.query.filter_by(
        entity_type=entity_type.upper(),
        entity_id=entity_id
    ).all()
    
    # Get all phone numbers for these concerned persons
    phone_ids = [cp.id for cp in concerned_persons]
    phones = PhoneBook.query.filter(
        PhoneBook.concerned_person_id.in_(phone_ids)
    ).order_by(PhoneBook.is_primary.desc(), PhoneBook.id).all()
    
    return jsonify([{
        'id': phone.id,
        'phone_number': phone.phone_number,
        'label': phone.label or 'Primary',
        'is_primary': phone.is_primary,
        'concerned_person_id': phone.concerned_person_id,
        'person_name': phone.concerned_person.name if phone.concerned_person else 'Unknown'
    } for phone in phones])


@bp.route("/api/phone", methods=["POST"])
@csrf.exempt
def add_phone():
    """Add a new phone number to a concerned person"""
    data = request.get_json()
    
    concerned_person_id = data.get('concerned_person_id')
    phone_number = data.get('phone_number', '').strip()
    label = data.get('label', '').strip()
    is_primary = data.get('is_primary', False)
    
    if not all([concerned_person_id, phone_number]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if phone number already exists
    existing = PhoneBook.query.filter_by(phone_number=phone_number).first()
    if existing:
        return jsonify({'error': 'Phone number already exists'}), 400
    
    # If this is being set as primary, unset other primary phones for this concerned person
    if is_primary:
        PhoneBook.query.filter_by(
            concerned_person_id=concerned_person_id,
            is_primary=True
        ).update({'is_primary': False})
    
    phone = PhoneBook(
        concerned_person_id=concerned_person_id,
        phone_number=phone_number,
        label=label,
        is_primary=is_primary
    )
    
    db.session.add(phone)
    db.session.commit()
    
    return jsonify({
        'id': phone.id,
        'phone_number': phone.phone_number,
        'label': phone.label,
        'is_primary': phone.is_primary
    })


@bp.route("/api/phone/<int:phone_id>", methods=["PUT"])
@csrf.exempt
def update_phone(phone_id):
    """Update a phone number"""
    phone = PhoneBook.query.get_or_404(phone_id)
    data = request.get_json()
    
    phone_number = data.get('phone_number', '').strip()
    label = data.get('label', '').strip()
    is_primary = data.get('is_primary', False)
    
    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400
    
    # Check if phone number already exists (excluding current record)
    existing = PhoneBook.query.filter(
        PhoneBook.phone_number == phone_number,
        PhoneBook.id != phone_id
    ).first()
    if existing:
        return jsonify({'error': 'Phone number already exists'}), 400
    
    # If this is being set as primary, unset other primary phones for this concerned person
    if is_primary:
        PhoneBook.query.filter_by(
            concerned_person_id=phone.concerned_person_id,
            is_primary=True
        ).update({'is_primary': False})
    
    phone.phone_number = phone_number
    phone.label = label
    phone.is_primary = is_primary
    
    db.session.commit()
    
    return jsonify({
        'id': phone.id,
        'phone_number': phone.phone_number,
        'label': phone.label,
        'is_primary': phone.is_primary
    })


@bp.route("/api/phone/<int:phone_id>", methods=["DELETE"])
@csrf.exempt
def delete_phone(phone_id):
    """Delete a phone number"""
    phone = PhoneBook.query.get_or_404(phone_id)
    db.session.delete(phone)
    db.session.commit()
    
    return jsonify({'message': 'Phone number deleted successfully'})


@bp.route("/api/phone/<int:phone_id>/set-primary", methods=["POST"])
@csrf.exempt
def set_primary_phone(phone_id):
    """Set a phone number as primary for its entity"""
    phone = PhoneBook.query.get_or_404(phone_id)
    
    # Unset other primary phones for this concerned person
    PhoneBook.query.filter_by(
        concerned_person_id=phone.concerned_person_id,
        is_primary=True
    ).update({'is_primary': False})
    
    # Set this phone as primary
    phone.is_primary = True
    db.session.commit()
    
    return jsonify({'message': 'Primary phone updated successfully'})


@bp.route("/entity/<entity_type>/<int:entity_id>")
def entity_phones(entity_type, entity_id):
    """Entity-specific phone management page"""
    # Get entity details
    entity = None
    entity_name = "Unknown"
    
    if entity_type.upper() == 'CONSIGNOR':
        entity = Consignor.query.get(entity_id)
    elif entity_type.upper() == 'CONSIGNEE':
        entity = Consignee.query.get(entity_id)
    elif entity_type.upper() == 'AGENT':
        entity = BookingAgent.query.get(entity_id)
    elif entity_type.upper() == 'DRIVER':
        entity = Driver.query.get(entity_id)
    elif entity_type.upper() == 'OWNER':
        entity = Owner.query.get(entity_id)
    
    if entity:
        entity_name = entity.name
    
    return render_template("phonebook/entity_phones.html",
                         entity_type=entity_type.upper(),
                         entity_id=entity_id,
                         entity_name=entity_name)


@bp.route("/api/concerned-persons/<entity_type>/<int:entity_id>")
@csrf.exempt
def get_concerned_persons(entity_type, entity_id):
    """Get concerned persons for an entity"""
    persons = ConcernedPerson.query.filter_by(
        entity_type=entity_type.upper(),
        entity_id=entity_id
    ).order_by(ConcernedPerson.is_primary.desc(), ConcernedPerson.name).all()
    
    return jsonify([{
        'id': person.id,
        'name': person.name,
        'designation': person.designation or '',
        'is_primary': person.is_primary
    } for person in persons])


@bp.route("/api/phone-numbers/<int:concerned_person_id>")
@csrf.exempt
def get_phone_numbers(concerned_person_id):
    """Get phone numbers for a concerned person"""
    phones = PhoneBook.query.filter_by(
        concerned_person_id=concerned_person_id
    ).order_by(PhoneBook.is_primary.desc(), PhoneBook.id).all()
    
    return jsonify([{
        'id': phone.id,
        'phone_number': phone.phone_number,
        'label': phone.label or 'Primary',
        'is_primary': phone.is_primary
    } for phone in phones])


@bp.route("/api/concerned-person", methods=["POST"])
@csrf.exempt
def add_concerned_person():
    """Add a new concerned person to an entity"""
    data = request.get_json()
    
    entity_type = data.get('entity_type', '').upper()
    entity_id = data.get('entity_id')
    name = data.get('name', '').strip()
    designation = data.get('designation', '').strip()
    is_primary = data.get('is_primary', False)
    
    if not all([entity_type, entity_id, name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # If this is being set as primary, unset other primary persons for this entity
    if is_primary:
        ConcernedPerson.query.filter_by(
            entity_type=entity_type,
            entity_id=entity_id,
            is_primary=True
        ).update({'is_primary': False})
    
    person = ConcernedPerson(
        entity_type=entity_type,
        entity_id=entity_id,
        name=name,
        designation=designation,
        is_primary=is_primary
    )
    
    db.session.add(person)
    db.session.commit()
    
    return jsonify({
        'id': person.id,
        'name': person.name,
        'designation': person.designation,
        'is_primary': person.is_primary
    })


@bp.route("/api/phone-new", methods=["POST"])
@csrf.exempt
def add_phone_new():
    """Add a new phone number to a concerned person"""
    data = request.get_json()
    
    concerned_person_id = data.get('concerned_person_id')
    phone_number = data.get('phone_number', '').strip()
    label = data.get('label', '').strip()
    is_primary = data.get('is_primary', False)
    
    if not all([concerned_person_id, phone_number]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if phone number already exists
    existing = PhoneBook.query.filter_by(phone_number=phone_number).first()
    if existing:
        return jsonify({'error': 'Phone number already exists'}), 400
    
    # If this is being set as primary, unset other primary phones for this concerned person
    if is_primary:
        PhoneBook.query.filter_by(
            concerned_person_id=concerned_person_id,
            is_primary=True
        ).update({'is_primary': False})
    
    phone = PhoneBook(
        concerned_person_id=concerned_person_id,
        phone_number=phone_number,
        label=label,
        is_primary=is_primary
    )
    
    db.session.add(phone)
    db.session.commit()
    
    return jsonify({
        'id': phone.id,
        'phone_number': phone.phone_number,
        'label': phone.label,
        'is_primary': phone.is_primary
    })
