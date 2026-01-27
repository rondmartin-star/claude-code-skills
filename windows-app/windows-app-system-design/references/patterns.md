# System Design Patterns Reference

Load this file when implementing integration services or multi-tenant architecture.

---

## Integration Services Pattern

When the application integrates with external hardware/services, create dedicated service classes.

### Service Structure

```python
# app/services/integration_services.py

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    UNKNOWN = "unknown"

@dataclass
class CommandResult:
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class VMixService:
    """HTTP API integration for vMix video switcher."""
    
    def __init__(self, host: str, port: int = 8088):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}/api"
    
    def test_connection(self) -> ConnectionStatus:
        """Test if vMix is reachable."""
        try:
            response = requests.get(f"{self.base_url}", timeout=5)
            return ConnectionStatus.CONNECTED if response.ok else ConnectionStatus.ERROR
        except requests.RequestException:
            return ConnectionStatus.DISCONNECTED
    
    def switch_camera(self, input_number: int) -> CommandResult:
        """Switch to specified camera input."""
        # Implementation
        pass

class QSysService:
    """TCP JSON-RPC integration for Q-Sys audio processor."""
    
    def __init__(self, host: str, port: int = 1710):
        self.host = host
        self.port = port
    
    def test_connection(self) -> ConnectionStatus:
        """Test if Q-Sys is reachable."""
        pass
    
    def recall_preset(self, preset_name: str) -> CommandResult:
        """Recall a Q-Sys preset."""
        pass

# Factory functions for dependency injection
def get_vmix_service(venue) -> Optional[VMixService]:
    """Create VMixService from venue configuration."""
    if venue.vmix_host:
        return VMixService(venue.vmix_host, venue.vmix_port or 8088)
    return None
```

### Testing Integration Endpoints

```python
# routes/settings.py

@router.get("/api/test-vmix")
async def test_vmix_connection(
    venue_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Test vMix connection for specified venue."""
    venue = db.query(Venue).get(venue_id) if venue_id else \
            db.query(Venue).filter(Venue.is_default == True).first()
    
    if not venue:
        return {"status": "error", "message": "No venue found"}
    
    service = get_vmix_service(venue)
    if not service:
        return {"status": "not_configured", "message": "vMix not configured"}
    
    status = service.test_connection()
    return {
        "status": status.value,
        "venue": venue.name,
        "host": venue.vmix_host
    }
```

### Equipment Discovery

```python
@router.get("/api/discover-equipment")
async def discover_equipment(
    subnet: str = "192.168.1",
    db: Session = Depends(get_db)
):
    """Scan network for vMix/Q-Sys devices."""
    found = []
    
    # Scan common ports
    for host in range(1, 255):
        ip = f"{subnet}.{host}"
        # Check vMix port 8088
        if check_port(ip, 8088):
            found.append({"ip": ip, "type": "vMix", "port": 8088})
        # Check Q-Sys port 1710
        if check_port(ip, 1710):
            found.append({"ip": ip, "type": "Q-Sys", "port": 1710})
    
    return {"devices": found}
```

---

## Multi-Tenant Database Design

If the system might have multiple venues/locations/organizations:

### Design Pattern: Tenant FK on All Relevant Tables

```python
class Venue(Base):
    """Tenant/organization entity."""
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    is_default = Column(Boolean, default=False)  # For single-tenant compat

class Service(Base):
    """Always belongs to a venue."""
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)
    # ... other fields
    
    venue = relationship("Venue", back_populates="services")

class Equipment(Base):
    """Equipment is venue-specific."""
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)
    # ...
```

### Query Pattern: Always Filter by Tenant

```python
# WRONG - Returns all services across all venues
services = db.query(Service).all()

# RIGHT - Filter by venue
services = db.query(Service).filter(Service.venue_id == venue_id).all()

# WRONG - Assumes single venue
venue = db.query(Venue).first()

# RIGHT - Get specific or default venue
venue = db.query(Venue).get(venue_id) if venue_id else \
        db.query(Venue).filter(Venue.is_default == True).first()
```

### API Pattern: Accept Tenant ID

```python
@router.get("/api/services")
async def list_services(
    venue_id: Optional[int] = None,  # Allow filtering
    db: Session = Depends(get_db)
):
    query = db.query(Service)
    if venue_id:
        query = query.filter(Service.venue_id == venue_id)
    return query.all()
```

---

## Seed Data Column Validation

Every column used in seed data MUST exist in the model definition.

```python
# WRONG - Using is_default but model doesn't have it
def init_db():
    venue = Venue(name="Main Campus", is_default=True)  # ERROR!

# models.py - Column missing!
class Venue(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    # is_default not defined!
```

**Prevention Pattern:**

```python
# 1. Define ALL columns in model FIRST
class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    is_default = Column(Boolean, default=False)  # ✓ Defined
    
# 2. THEN write seed data using those columns
def seed_database(db: Session):
    venue = Venue(name="Main Campus", is_default=True)  # ✓ Works
```

---

## Consistent Naming Conventions

Establish naming patterns early and apply consistently throughout.

Example: Liturgical Calendar Naming

```python
# INCONSISTENT - Different prepositions per season
"First Sunday in Advent"      # "in"
"First Sunday after Epiphany" # "after"
"First Sunday of Lent"        # "of"

# CONSISTENT - Same pattern everywhere
"First Sunday of Advent"
"First Sunday of Epiphany"
"First Sunday of Lent"
"First Sunday of Easter"
"First Sunday of Ordinary Time"
```

**Document the pattern:**

```markdown
## Naming Convention: [Feature Name]

Pattern: "[Ordinal] [Unit] of [Category]"

Examples:
- First Sunday of Advent
- Second Sunday of Christmas
- Third Sunday of Epiphany
```

---

*End of System Design Patterns Reference*
