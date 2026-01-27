# Requirements Templates Reference

Load this file when gathering requirements, writing user stories, or defining acceptance criteria.

---

## User Story Template

### Standard Format

```markdown
**User Story ID:** US-{Module}-{Number}
**Title:** {Brief descriptive title}
**Priority:** P0 (Must Have) | P1 (Should Have) | P2 (Nice to Have)
**Effort:** S (Small) | M (Medium) | L (Large) | XL (Extra Large)

**As a** {type of user},
**I want** {some goal or objective}
**so that** {some reason or benefit}.

**Acceptance Criteria:**
1. {Specific, testable criterion}
2. {Specific, testable criterion}
3. {Specific, testable criterion}

**Notes:**
- {Additional context}
- {Constraints}
- {Dependencies}

**Related Stories:** {Links to related stories}
**Tasks:** {Implementation tasks}
```

---

## User Story Examples by Domain

### Example 1: Property Management System

```markdown
**User Story ID:** US-BOOKING-001
**Title:** Reserve Property for Guest
**Priority:** P0 (Must Have)
**Effort:** M (Medium)

**As a** staff member,
**I want** to create a reservation for a guest selecting dates and property,
**so that** I can manage property availability and guest bookings.

**Acceptance Criteria:**
1. Given I am on the booking page,
   When I select a property, start date, end date, and guest,
   Then a new reservation is created in the database

2. Given a property is already booked for specific dates,
   When I try to create an overlapping reservation,
   Then the system prevents the booking and shows an error message

3. Given I successfully create a reservation,
   When I view the property calendar,
   Then the blocked dates are visible

4. Given I create a reservation,
   When the system calculates the total cost,
   Then it correctly applies nightly rates and any fees

**Notes:**
- Must check availability before creating reservation
- Support multi-night bookings
- Calculate total cost automatically
- Send confirmation email to guest

**Related Stories:**
- US-BOOKING-002 (Edit Reservation)
- US-PROPERTY-003 (View Calendar)

**Tasks:**
1. Create Reservation model with fields (property_id, guest_id, start_date, end_date, total_cost, status)
2. Implement availability check service
3. Build booking form UI
4. Add cost calculation logic
5. Create reservation confirmation email template
```

### Example 2: Inventory Management System

```markdown
**User Story ID:** US-INVENTORY-005
**Title:** Track Stock Levels with Low Stock Alerts
**Priority:** P0 (Must Have)
**Effort:** M (Medium)

**As a** warehouse manager,
**I want** to see current stock levels and receive alerts when inventory is low,
**so that** I can reorder items before running out of stock.

**Acceptance Criteria:**
1. Given I view an item's detail page,
   When the item's quantity is displayed,
   Then it shows the current available quantity and the reorder threshold

2. Given an item's quantity falls below the reorder threshold,
   When I view the inventory dashboard,
   Then the item appears in the "Low Stock" section with a warning indicator

3. Given I have low stock items,
   When I click "Generate Reorder Report",
   Then a PDF is generated listing all items below threshold with suggested reorder quantities

4. Given an item reaches zero quantity,
   When a customer tries to add it to cart,
   Then the system prevents the addition and shows "Out of Stock"

**Notes:**
- Reorder threshold configurable per item
- Alert should be visible on dashboard
- Email notifications optional (P1 feature)

**Related Stories:**
- US-INVENTORY-003 (Receive Stock)
- US-REPORTS-002 (Inventory Reports)

**Tasks:**
1. Add reorder_threshold field to Item model
2. Create low stock query/service
3. Build low stock dashboard widget
4. Implement PDF report generation
5. Add out-of-stock validation to cart logic
```

### Example 3: Project Management System

```markdown
**User Story ID:** US-TASK-012
**Title:** Assign Tasks with Dependencies
**Priority:** P1 (Should Have)
**Effort:** L (Large)

**As a** project manager,
**I want** to assign tasks to team members and define task dependencies,
**so that** I can ensure work is completed in the correct order.

**Acceptance Criteria:**
1. Given I am creating a task,
   When I assign it to a team member,
   Then they receive a notification and the task appears on their dashboard

2. Given I am editing a task,
   When I select "Add Dependency" and choose another task,
   Then the system links the tasks and prevents starting the dependent task until prerequisite is complete

3. Given a task has dependencies,
   When I try to mark it as "In Progress" before dependencies are done,
   Then the system shows a warning listing incomplete dependencies

4. Given I view the project timeline,
   When tasks have dependencies,
   Then dependency arrows are shown connecting the tasks visually

**Notes:**
- Support multiple dependencies per task
- Circular dependencies should be prevented
- Visual timeline (Gantt chart) optional for P1

**Related Stories:**
- US-TASK-001 (Create Task)
- US-PROJECT-005 (Project Timeline View)

**Tasks:**
1. Create TaskDependency model (task_id, depends_on_task_id)
2. Add circular dependency validation
3. Implement task assignment with notifications
4. Build dependency selection UI
5. Create timeline visualization component
```

### Example 4: E-Commerce Platform

```markdown
**User Story ID:** US-CHECKOUT-008
**Title:** Apply Discount Codes at Checkout
**Priority:** P1 (Should Have)
**Effort:** M (Medium)

**As a** customer,
**I want** to apply a discount code during checkout,
**so that** I can receive promotional discounts on my order.

**Acceptance Criteria:**
1. Given I am on the checkout page,
   When I enter a valid discount code and click "Apply",
   Then the order total is reduced by the discount amount

2. Given I enter an invalid or expired discount code,
   When I click "Apply",
   Then an error message displays: "Invalid discount code"

3. Given a discount code has usage limits,
   When I apply a code that has been used maximum times,
   Then the system rejects it with message: "This code has expired"

4. Given I have applied a discount code,
   When I view the order summary,
   Then the discount is shown as a separate line item with the code name

5. Given a discount is for specific products only,
   When my cart doesn't contain those products,
   Then the code is rejected with: "This code is not applicable to your cart"

**Notes:**
- Support percentage and fixed amount discounts
- Support minimum order value requirements
- One code per order (P0), multiple codes is P2

**Related Stories:**
- US-ADMIN-015 (Create Discount Codes)
- US-CART-003 (View Cart Summary)

**Tasks:**
1. Create DiscountCode model (code, type, amount, min_order, max_uses, expires_at)
2. Implement code validation service
3. Add discount application logic to checkout
4. Build discount code input UI
5. Create admin interface for managing codes
```

---

## Acceptance Criteria Patterns

### Given-When-Then Format

**Structure:**
```
Given {precondition/context}
When {action/trigger}
Then {expected outcome}
```

**Examples:**

```markdown
# UI Interaction
Given I am logged in as an admin
When I click the "Delete User" button
Then a confirmation dialog appears

# Data Validation
Given I submit a form with an invalid email
When the form is validated
Then an error message appears below the email field

# State Change
Given a task is marked as "Complete"
When I view the project progress
Then the completion percentage increases accordingly

# Authorization
Given I am a regular user (not admin)
When I try to access the admin dashboard URL
Then I am redirected to the home page with "Access Denied" message
```

### Boundary Conditions

```markdown
# Minimum Value
Given a product price is set to $0.01
When the product is added to cart
Then the price displays correctly

# Maximum Value
Given a user tries to upload a 100MB file
When the file exceeds the 10MB limit
Then an error message displays before upload

# Empty State
Given there are no bookings in the system
When I view the bookings page
Then a message displays: "No bookings found"

# Edge Case
Given today is February 29, 2024 (leap year)
When I create a yearly recurring event
Then it recurs correctly in non-leap years (moves to Feb 28)
```

### Error Handling

```markdown
# Network Failure
Given the payment gateway is unreachable
When I submit payment
Then the system shows "Payment service temporarily unavailable" and saves cart state

# Invalid Input
Given I enter "abc" in a numeric quantity field
When I submit the form
Then validation prevents submission with message "Quantity must be a number"

# Permission Denied
Given I am not the owner of a document
When I try to delete it
Then a 403 error page displays

# Resource Not Found
Given a booking ID doesn't exist
When I navigate to /bookings/{invalid_id}
Then a 404 page displays with "Booking not found"
```

---

## Non-Functional Requirements

### Performance Requirements

```markdown
## NFR-PERF-001: Page Load Time
**Requirement:** All pages must load within 2 seconds on a standard broadband connection.

**Measurement:**
- Use Google Lighthouse performance score > 90
- Server response time (TTFB) < 500ms
- Total page load < 2000ms

**Acceptance Criteria:**
1. Homepage loads in < 1.5s (including images)
2. Database queries complete in < 100ms for 95th percentile
3. Search results display in < 1s for datasets up to 10,000 records

**Testing:**
- Run Lighthouse audits on all major pages
- Load test with 100 concurrent users
- Monitor response times in production
```

```markdown
## NFR-PERF-002: Database Performance
**Requirement:** Database queries must support 1,000 concurrent users without degradation.

**Measurement:**
- Average query time < 100ms
- 95th percentile query time < 500ms
- Connection pool never exhausted

**Acceptance Criteria:**
1. All queries have appropriate indexes
2. N+1 query problems eliminated (use eager loading)
3. Read replicas configured for reporting queries

**Testing:**
- Use SQLAlchemy query logging to identify slow queries
- Run load tests with 1,000 simulated users
- Monitor database performance metrics
```

### Security Requirements

```markdown
## NFR-SEC-001: Authentication
**Requirement:** All user authentication must use industry-standard OAuth 2.0.

**Acceptance Criteria:**
1. Google OAuth 2.0 integration complete
2. Microsoft OAuth 2.0 integration complete
3. State parameter validation prevents CSRF attacks
4. Session tokens use cryptographically secure random generation
5. Sessions expire after 7 days of inactivity

**Testing:**
- Attempt OAuth CSRF attacks (should fail)
- Verify state token validation
- Test session expiration
```

```markdown
## NFR-SEC-002: Data Protection
**Requirement:** All sensitive data must be encrypted at rest and in transit.

**Acceptance Criteria:**
1. HTTPS enforced for all connections (HTTP redirects to HTTPS)
2. Database passwords hashed with bcrypt (work factor 12)
3. API keys encrypted using Fernet symmetric encryption
4. Session cookies have Secure and HttpOnly flags
5. Content-Security-Policy headers configured

**Testing:**
- Scan SSL/TLS configuration (Qualys SSL Labs)
- Verify password hashes in database (no plain text)
- Inspect cookies in browser dev tools
- Check HTTP headers with curl
```

### Usability Requirements

```markdown
## NFR-USABILITY-001: Accessibility
**Requirement:** Application must meet WCAG 2.1 Level AA accessibility standards.

**Acceptance Criteria:**
1. All images have alt text
2. Color contrast ratios meet AA standards (4.5:1 for normal text)
3. All interactive elements keyboard accessible
4. Screen reader compatible (test with NVDA/JAWS)
5. Form errors clearly associated with fields

**Testing:**
- Run axe DevTools accessibility scan (0 violations)
- Keyboard-only navigation test
- Screen reader testing (NVDA)
```

```markdown
## NFR-USABILITY-002: Responsive Design
**Requirement:** Application must be fully functional on mobile, tablet, and desktop.

**Acceptance Criteria:**
1. All pages render correctly at 320px, 768px, 1024px, 1920px widths
2. Touch targets minimum 44x44px on mobile
3. Text readable without zooming
4. No horizontal scrolling on any device

**Testing:**
- Test on physical devices (iPhone, iPad, Android)
- Chrome DevTools responsive mode testing
- Lighthouse mobile audit score > 90
```

### Reliability Requirements

```markdown
## NFR-RELIABILITY-001: Uptime
**Requirement:** System must maintain 99.5% uptime (excluding planned maintenance).

**Measurement:**
- Maximum 3.65 hours downtime per month
- Planned maintenance windows pre-announced 7 days in advance

**Acceptance Criteria:**
1. Health check endpoint responds within 1s
2. Automated alerting for service failures
3. Database backups run daily at 2 AM
4. Backup restoration tested monthly

**Monitoring:**
- UptimeRobot pinging every 5 minutes
- Email/SMS alerts on failures
- Monthly uptime reports
```

---

## Requirements Traceability Matrix

### Template

| Story ID | Title | Priority | Status | Design Doc | Implementation | Tests | Deployed |
|----------|-------|----------|--------|------------|----------------|-------|----------|
| US-XXX-001 | {Title} | P0 | Complete | ✓ | ✓ | ✓ | ✓ |

### Example: Property Management System

| Story ID | Title | Priority | Status | Design Doc | Implementation | Tests | Deployed |
|----------|-------|----------|--------|------------|----------------|-------|----------|
| US-BOOKING-001 | Reserve Property | P0 | Complete | DESIGN.md#bookings | app/routes/bookings.py:25 | tests/test_bookings.py:15 | v1.2.0 |
| US-BOOKING-002 | Edit Reservation | P0 | Complete | DESIGN.md#bookings | app/routes/bookings.py:67 | tests/test_bookings.py:45 | v1.2.0 |
| US-BOOKING-003 | Cancel Reservation | P0 | Complete | DESIGN.md#bookings | app/routes/bookings.py:102 | tests/test_bookings.py:78 | v1.2.0 |
| US-PROPERTY-001 | Add Property | P0 | Complete | DESIGN.md#properties | app/routes/properties.py:18 | tests/test_properties.py:12 | v1.1.0 |
| US-PROPERTY-002 | Edit Property | P0 | Complete | DESIGN.md#properties | app/routes/properties.py:89 | tests/test_properties.py:54 | v1.1.0 |
| US-PROPERTY-003 | View Calendar | P1 | In Progress | DESIGN.md#calendar | WIP | - | - |
| US-GUEST-001 | Add Guest | P0 | Complete | DESIGN.md#guests | app/routes/guests.py:12 | tests/test_guests.py:8 | v1.0.0 |
| US-REPORTS-001 | Booking Report | P1 | Planned | - | - | - | - |

**Traceability Benefits:**
- Verify all requirements are implemented
- Track progress across development lifecycle
- Identify gaps in testing or documentation
- Support compliance audits

---

## Requirements Prioritization Matrix

### MoSCoW Method

**Must Have (P0):**
- Critical for MVP launch
- System unusable without these
- Legal/compliance requirements

**Should Have (P1):**
- Important but not critical
- Workarounds exist
- Adds significant value

**Could Have (P2):**
- Nice to have
- Minimal impact if excluded
- Can be added post-launch

**Won't Have (This Release):**
- Out of scope
- Future consideration
- Explicitly deferred

### Effort vs Impact Matrix

```
High Impact, Low Effort → Do First (Quick Wins)
High Impact, High Effort → Plan Carefully (Major Projects)
Low Impact, Low Effort → Do Later (Fill-Ins)
Low Impact, High Effort → Avoid (Time Sinks)
```

### Example Prioritization

| Story ID | Title | Impact | Effort | Priority | Rationale |
|----------|-------|--------|--------|----------|-----------|
| US-BOOKING-001 | Reserve Property | High | Medium | P0 | Core business function |
| US-BOOKING-006 | Recurring Bookings | Medium | High | P2 | Nice feature, complex implementation |
| US-REPORTS-003 | Revenue Analytics | High | High | P1 | Valuable insights, can launch without |
| US-UI-005 | Dark Mode | Low | Low | P2 | Easy to add, low user demand |

---

*End of Requirements Templates Reference*
